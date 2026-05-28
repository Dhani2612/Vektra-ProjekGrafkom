"""
editor/selection.py — Hit-test, Bounding Box, Transform Handles
================================================================
Mengelola state selection dan menggambar bounding box + handles.
"""

import math
import pygame
import config
from engine.drawing import draw_dashed_line, draw_circle_bresenham, draw_line_bresenham


class SelectionManager:
    """Mengelola objek terpilih dan menggambar handles."""

    def __init__(self):
        self.selected_object = None
        self.dragging = False
        self.drag_handle = None   # None, "move", "tl", "tr", "bl", "br", "rotate"
        self.drag_start = None
        self.original_matrix = None

    def select(self, obj):
        if self.selected_object:
            self.selected_object.selected = False
        self.selected_object = obj
        if obj:
            obj.selected = True

    def deselect(self):
        if self.selected_object:
            self.selected_object.selected = False
        self.selected_object = None

    def get_handle_at(self, mx, my) -> str:
        """Return nama handle di (mx, my), atau None."""
        if not self.selected_object:
            return None

        bb = self.selected_object.get_bounding_box()
        x0, y0, x1, y1 = bb
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        hs = config.HANDLE_SIZE

        handles = {
            "tl": (x0, y0), "tr": (x1, y0),
            "bl": (x0, y1), "br": (x1, y1),
        }
        # Rotation handle di atas tengah
        rot_y = y0 - config.ROTATION_HANDLE_OFFSET
        handles["rotate"] = (cx, rot_y)

        for name, (hx, hy) in handles.items():
            if abs(mx - hx) <= hs and abs(my - hy) <= hs:
                return name

        # Check inside bounding box for "move"
        if x0 <= mx <= x1 and y0 <= my <= y1:
            return "move"

        return None

    def draw_handles(self, surface: pygame.Surface):
        """Gambar bounding box dan handles di sekitar objek terpilih."""
        if not self.selected_object:
            return

        bb = self.selected_object.get_bounding_box()
        x0, y0, x1, y1 = [int(v) for v in bb]
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        hs = config.HANDLE_SIZE // 2

        # Dashed bounding box
        draw_dashed_line(surface, config.C_ACCENT, x0, y0, x1, y0, dash=4, gap=3)
        draw_dashed_line(surface, config.C_ACCENT, x1, y0, x1, y1, dash=4, gap=3)
        draw_dashed_line(surface, config.C_ACCENT, x1, y1, x0, y1, dash=4, gap=3)
        draw_dashed_line(surface, config.C_ACCENT, x0, y1, x0, y0, dash=4, gap=3)

        # Corner handles (kotak kecil)
        for hx, hy in [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]:
            pygame.draw.rect(surface, config.HANDLE_FILL,
                             (hx - hs, hy - hs, config.HANDLE_SIZE, config.HANDLE_SIZE))
            pygame.draw.rect(surface, config.HANDLE_COLOR,
                             (hx - hs, hy - hs, config.HANDLE_SIZE, config.HANDLE_SIZE), 1)

        # Rotation handle
        rot_y = y0 - config.ROTATION_HANDLE_OFFSET
        draw_dashed_line(surface, config.C_ACCENT, cx, y0, cx, rot_y, dash=3, gap=2)
        draw_circle_bresenham(surface, config.HANDLE_COLOR, cx, rot_y, 5, filled=True)
        draw_circle_bresenham(surface, config.HANDLE_FILL, cx, rot_y, 5, filled=False)
