"""
tools/pen_tool.py — Gambar garis lurus (Bresenham)
====================================================
Klik pertama = titik awal, klik kedua = titik akhir.
Preview garis ditampilkan sebelum commit.
"""

import math
import pygame
import config
from tools.base_tool import BaseTool
from editor.objects import FreehandObj
from editor.history import AddObjectCommand
from engine.drawing import draw_line_bresenham


class PenTool(BaseTool):
    name = "pen"

    def __init__(self, app):
        super().__init__(app)
        self.points = []

    def on_mouse_down(self, pos, button):
        if button != 1:
            return
        self.points = [pos]

    def on_mouse_drag(self, pos, rel):
        if self.points:
            # Jarak minimal agar titik tidak terlalu rapat
            last_pos = self.points[-1]
            if math.hypot(pos[0] - last_pos[0], pos[1] - last_pos[1]) > 2:
                self.points.append(pos)

    def on_mouse_up(self, pos, button):
        if self.points and len(self.points) > 1:
            self._commit_line()
        self.points = []

    def on_key_down(self, event):
        if event.key == pygame.K_ESCAPE:
            self.points = []

    def render_preview(self, surface):
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                p1, p2 = self.points[i], self.points[i+1]
                draw_line_bresenham(surface, config.C_ACCENT,
                                    int(p1[0]), int(p1[1]),
                                    int(p2[0]), int(p2[1]),
                                    thickness=self.app.current_stroke_width)

    def _commit_line(self):
        line = FreehandObj(self.points)
        line.stroke_color = self.app.current_stroke_color
        line.stroke_width = self.app.current_stroke_width
        line.stroke_style = self.app.current_stroke_style

        cmd = AddObjectCommand(self.app.canvas.objects, line)
        self.app.history.do(cmd)

        self.points = []
