"""
editor/canvas.py — Kanvas utama Vektra
========================================
Mengelola surface kanvas, render semua objek, grid.
"""

import pygame
import config
from engine.drawing import draw_line_dda


class Canvas:
    """Surface kanvas tempat semua objek dirender."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.objects = []       # list of BaseObject
        self.show_grid = True
        self.offset_x = 0.0    # untuk panning (masa depan)
        self.offset_y = 0.0

    def screen_to_canvas(self, sx: int, sy: int) -> tuple:
        """Konversi koordinat layar ke koordinat kanvas."""
        return (sx - self.rect.x - self.offset_x,
                sy - self.rect.y - self.offset_y)

    def canvas_to_screen(self, cx: float, cy: float) -> tuple:
        """Konversi koordinat kanvas ke layar."""
        return (cx + self.rect.x + self.offset_x,
                cy + self.rect.y + self.offset_y)

    def resize(self, width: int, height: int):
        """Ubah ukuran kanvas."""
        self.rect.width = width
        self.rect.height = height
        old_surface = self.surface
        self.surface = pygame.Surface((width, height))
        self.surface.blit(old_surface, (0, 0))

    def is_inside(self, sx: int, sy: int) -> bool:
        """Cek apakah titik layar berada di area kanvas."""
        return self.rect.collidepoint(sx, sy)

    def render(self, target_surface: pygame.Surface, selection_mgr=None, tool_preview_fn=None):
        """Render kanvas: background, grid, objek, selection, tool preview."""
        self.surface.fill(config.CANVAS_BG)

        # Grid
        if self.show_grid:
            self._draw_grid()

        # Render semua objek
        for obj in self.objects:
            obj.render(self.surface)

        # Selection handles
        if selection_mgr and selection_mgr.selected_object:
            selection_mgr.draw_handles(self.surface)

        # Tool preview (misalnya garis yang sedang digambar)
        if tool_preview_fn:
            tool_preview_fn(self.surface)

        # Blit kanvas ke target
        target_surface.blit(self.surface, (self.rect.x, self.rect.y))

    def _draw_grid(self):
        """Gambar grid menggunakan dot (titik) agar terlihat lebih modern."""
        w, h = self.surface.get_size()
        color = config.CANVAS_GRID

        # Gunakan grid titik yang halus, 2x2 px untuk setiap persimpangan
        for x in range(0, w, config.GRID_SIZE):
            for y in range(0, h, config.GRID_SIZE):
                self.surface.set_at((x, y), color)
                self.surface.set_at((x+1, y), color)
                self.surface.set_at((x, y+1), color)
                self.surface.set_at((x+1, y+1), color)

    def hit_test_objects(self, cx: float, cy: float):
        """Return objek yang terkena hit test (top-most first)."""
        for obj in reversed(self.objects):
            if obj.hit_test(cx, cy):
                return obj
        return None

    def export_png(self, filepath: str):
        """Export kanvas sebagai PNG."""
        pygame.image.save(self.surface, filepath)
