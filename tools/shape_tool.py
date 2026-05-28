"""
tools/shape_tool.py — Rectangle & Polygon Tool
================================================
R = Rectangle (drag), G = Polygon (click-per-vertex, Enter to close).
"""

import math
import pygame
import config
from tools.base_tool import BaseTool
from editor.objects import RectangleObj, PolygonObj
from editor.history import AddObjectCommand
from engine.drawing import draw_line_bresenham, draw_polygon_outline
from engine.fill import fill_polygon


class ShapeTool(BaseTool):
    name = "shape"

    def __init__(self, app, mode="rect"):
        super().__init__(app)
        self.mode = mode      # "rect" atau "polygon"
        # Rect state
        self.rect_start = None
        self.rect_end = None
        # Polygon state
        self.poly_points = []
        self.current_pos = None

    def on_mouse_down(self, pos, button):
        if button != 1:
            return

        if self.mode == "rect":
            self.rect_start = pos
            self.rect_end = pos
        elif self.mode == "polygon":
            # Auto-commit jika klik dekat dengan titik pertama
            if len(self.poly_points) >= 3:
                first_pt = self.poly_points[0]
                dist = math.hypot(pos[0] - first_pt[0], pos[1] - first_pt[1])
                if dist <= 10.0:  # Threshold kedekatan (snap)
                    self._commit_polygon()
                    return
            self.poly_points.append(pos)
            self.current_pos = pos

    def on_mouse_drag(self, pos, rel):
        if self.mode == "rect" and self.rect_start:
            self.rect_end = pos
        elif self.mode == "polygon":
            self.current_pos = pos

    def on_mouse_up(self, pos, button):
        if self.mode == "rect" and self.rect_start:
            self.rect_end = pos
            self._commit_rect()

    def on_key_down(self, event):
        key = event.key
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            if self.mode == "polygon" and len(self.poly_points) >= 3:
                self._commit_polygon()
        elif key == pygame.K_ESCAPE:
            self.rect_start = None
            self.rect_end = None
            self.poly_points.clear()
            self.current_pos = None

    def render_preview(self, surface):
        if self.mode == "rect" and self.rect_start and self.rect_end:
            x0, y0 = self.rect_start
            x1, y1 = self.rect_end
            verts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            if self.app.current_fill_color:
                fill_polygon(surface, self.app.current_fill_color, verts)
            draw_polygon_outline(surface, config.C_ACCENT, verts,
                                 self.app.current_stroke_width)

        elif self.mode == "polygon" and self.poly_points:
            # Gambar garis antar titik yang sudah diklik
            for i in range(len(self.poly_points) - 1):
                p1, p2 = self.poly_points[i], self.poly_points[i + 1]
                draw_line_bresenham(surface, config.C_ACCENT,
                                    int(p1[0]), int(p1[1]),
                                    int(p2[0]), int(p2[1]),
                                    self.app.current_stroke_width)
            # Preview garis ke posisi mouse saat ini
            if self.current_pos and self.poly_points:
                last = self.poly_points[-1]
                draw_line_bresenham(surface, (150, 150, 200),
                                    int(last[0]), int(last[1]),
                                    int(self.current_pos[0]), int(self.current_pos[1]),
                                    1)
            # Titik-titik anchor
            from engine.drawing import draw_circle_bresenham
            for pt in self.poly_points:
                draw_circle_bresenham(surface, config.C_ACCENT,
                                      int(pt[0]), int(pt[1]), 3, filled=True)

    def _commit_rect(self):
        x0, y0 = self.rect_start
        x1, y1 = self.rect_end
        x, y = min(x0, x1), min(y0, y1)
        w, h = abs(x1 - x0), abs(y1 - y0)
        if w < 2 or h < 2:
            self.rect_start = None
            self.rect_end = None
            return

        rect = RectangleObj(x, y, w, h)
        rect.stroke_color = self.app.current_stroke_color
        rect.fill_color = self.app.current_fill_color
        rect.stroke_width = self.app.current_stroke_width
        rect.stroke_style = self.app.current_stroke_style

        cmd = AddObjectCommand(self.app.canvas.objects, rect)
        self.app.history.do(cmd)

        self.rect_start = None
        self.rect_end = None

    def _commit_polygon(self):
        poly = PolygonObj(list(self.poly_points))
        poly.stroke_color = self.app.current_stroke_color
        poly.fill_color = self.app.current_fill_color
        poly.stroke_width = self.app.current_stroke_width
        poly.stroke_style = self.app.current_stroke_style

        cmd = AddObjectCommand(self.app.canvas.objects, poly)
        self.app.history.do(cmd)

        self.poly_points.clear()
        self.current_pos = None
