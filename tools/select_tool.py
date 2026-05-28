"""
tools/select_tool.py — Select, Move, Rotate, Scale
====================================================
"""

import math
import numpy as np
import pygame
import config
from tools.base_tool import BaseTool
from engine.transform import translate, rotate_around, scale_around
from editor.history import TransformCommand


class SelectTool(BaseTool):
    name = "select"

    def __init__(self, app):
        super().__init__(app)
        self.drag_start = None
        self.drag_handle = None
        self.original_matrix = None

    def on_mouse_down(self, pos, button):
        if button != 1:
            return
        mx, my = pos
        sel = self.app.selection

        # Cek handle dulu (jika sudah ada selected object)
        handle = sel.get_handle_at(mx, my)
        if handle:
            self.drag_handle = handle
            self.drag_start = pos
            self.original_matrix = sel.selected_object.transform_matrix.copy()
            return

        # Hit test objek
        obj = self.app.canvas.hit_test_objects(mx, my)
        sel.select(obj)
        if obj:
            self.drag_handle = "move"
            self.drag_start = pos
            self.original_matrix = obj.transform_matrix.copy()
        else:
            self.drag_handle = None

    def on_mouse_drag(self, pos, rel):
        if not self.drag_handle or not self.app.selection.selected_object:
            return

        obj = self.app.selection.selected_object
        mx, my = pos
        sx, sy = self.drag_start

        if self.drag_handle == "move":
            # Translasi
            dx, dy = mx - sx, my - sy
            obj.transform_matrix = self.original_matrix @ translate(dx, dy)

        elif self.drag_handle == "rotate":
            # Rotasi di sekitar center bounding box
            bb = obj.get_bounding_box()
            cx = (bb[0] + bb[2]) / 2
            cy = (bb[1] + bb[3]) / 2
            angle_start = math.atan2(sy - cy, sx - cx)
            angle_now = math.atan2(my - cy, mx - cx)
            delta = angle_now - angle_start
            obj.transform_matrix = rotate_around(delta, cx, cy) @ self.original_matrix

        elif self.drag_handle in ("tl", "tr", "bl", "br"):
            # Scaling dari center
            bb = obj.get_bounding_box()
            cx = (bb[0] + bb[2]) / 2
            cy = (bb[1] + bb[3]) / 2
            
            # Hitung ratio scale
            dist_start = max(1, math.hypot(sx - cx, sy - cy))
            dist_now = max(1, math.hypot(mx - cx, my - cy))
            s = dist_now / dist_start
            obj.transform_matrix = scale_around(s, s, cx, cy) @ self.original_matrix

    def on_mouse_up(self, pos, button):
        if self.drag_handle and self.app.selection.selected_object and self.original_matrix is not None:
            obj = self.app.selection.selected_object
            new_matrix = obj.transform_matrix.copy()
            # Hanya simpan ke history jika matriks berubah
            if not np.array_equal(self.original_matrix, new_matrix):
                cmd = TransformCommand(obj, self.original_matrix, new_matrix)
                self.app.history.undo_stack.append(cmd)
                self.app.history.redo_stack.clear()

        self.drag_handle = None
        self.drag_start = None
        self.original_matrix = None

    def on_key_down(self, event):
        key = event.key
        if key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            obj = self.app.selection.selected_object
            if obj:
                from editor.history import DeleteObjectCommand
                cmd = DeleteObjectCommand(self.app.canvas.objects, obj)
                self.app.history.do(cmd)
                self.app.selection.deselect()
