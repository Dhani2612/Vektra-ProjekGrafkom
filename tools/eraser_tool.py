
"""
tools/eraser_tool.py — Eraser Tool
====================================
Klik atau drag di atas objek untuk menghapusnya.
"""

from tools.base_tool import BaseTool
from editor.history import DeleteObjectCommand

class EraserTool(BaseTool):
    name = "eraser"

    def __init__(self, app):
        super().__init__(app)

    def on_mouse_down(self, pos, button):
        if button != 1:
            return
        self._erase_at(pos)

    def on_mouse_drag(self, pos, rel):
        self._erase_at(pos)

    def _erase_at(self, pos):
        mx, my = pos
        # Cari objek teratas yang terkena koordinat mouse
        obj = self.app.canvas.hit_test_objects(mx, my)
        if obj:
            # Hapus melalui command pattern agar bisa di-undo
            cmd = DeleteObjectCommand(self.app.canvas.objects, obj)
            self.app.history.do(cmd)
            
            # Jika objek yang dihapus sedang dipilih, batalkan seleksinya
            if self.app.selection.selected_object == obj:
                self.app.selection.deselect()