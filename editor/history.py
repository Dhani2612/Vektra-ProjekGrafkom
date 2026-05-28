"""
editor/history.py — Undo/Redo (Command Pattern)
=================================================
Setiap aksi yang mengubah kanvas dibungkus sebagai Command.
"""

import copy


class Command:
    """Kelas dasar command."""
    def execute(self): pass
    def undo(self): pass


class AddObjectCommand(Command):
    def __init__(self, obj_list: list, obj):
        self.obj_list = obj_list
        self.obj = obj

    def execute(self):
        self.obj_list.append(self.obj)

    def undo(self):
        if self.obj in self.obj_list:
            self.obj_list.remove(self.obj)


class DeleteObjectCommand(Command):
    def __init__(self, obj_list: list, obj):
        self.obj_list = obj_list
        self.obj = obj
        self.index = -1

    def execute(self):
        if self.obj in self.obj_list:
            self.index = self.obj_list.index(self.obj)
            self.obj_list.remove(self.obj)

    def undo(self):
        if self.index >= 0:
            self.obj_list.insert(self.index, self.obj)


class TransformCommand(Command):
    def __init__(self, obj, old_matrix, new_matrix):
        self.obj = obj
        self.old_matrix = old_matrix.copy()
        self.new_matrix = new_matrix.copy()

    def execute(self):
        self.obj.transform_matrix = self.new_matrix.copy()

    def undo(self):
        self.obj.transform_matrix = self.old_matrix.copy()


class ChangePropertyCommand(Command):
    def __init__(self, obj, prop_name: str, old_value, new_value):
        self.obj = obj
        self.prop_name = prop_name
        self.old_value = old_value
        self.new_value = new_value

    def execute(self):
        setattr(self.obj, self.prop_name, self.new_value)

    def undo(self):
        setattr(self.obj, self.prop_name, self.old_value)


class HistoryManager:
    """Stack undo/redo."""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def do(self, command: Command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            cmd = self.undo_stack.pop()
            cmd.undo()
            self.redo_stack.append(cmd)

    def redo(self):
        if self.redo_stack:
            cmd = self.redo_stack.pop()
            cmd.execute()
            self.undo_stack.append(cmd)

    def can_undo(self):
        return len(self.undo_stack) > 0

    def can_redo(self):
        return len(self.redo_stack) > 0
