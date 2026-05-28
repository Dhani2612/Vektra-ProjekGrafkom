"""
tools/base_tool.py — Kelas dasar untuk semua tool
"""


class BaseTool:
    """Interface dasar tool. Semua tool wajib override method ini."""

    name = "base"

    def __init__(self, app):
        self.app = app   # referensi ke main App

    def on_mouse_down(self, pos, button):
        """Dipanggil saat mouse button ditekan. pos = canvas coords."""
        pass

    def on_mouse_drag(self, pos, rel):
        """Dipanggil saat mouse di-drag. pos = canvas coords."""
        pass

    def on_mouse_up(self, pos, button):
        """Dipanggil saat mouse button dilepas."""
        pass

    def on_key_down(self, event):
        """Dipanggil saat keyboard key ditekan."""
        pass

    def render_preview(self, surface):
        """Gambar preview (sebelum objek di-commit) ke canvas surface."""
        pass
