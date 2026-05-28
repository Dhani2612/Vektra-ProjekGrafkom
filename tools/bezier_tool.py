"""
tools/bezier_tool.py — Gambar kurva Bezier cubic
==================================================
Klik 1 = anchor pertama, klik 2 + drag = anchor kedua + control handle.
"""

import pygame
import config
from tools.base_tool import BaseTool
from editor.objects import BezierCurveObj
from editor.history import AddObjectCommand
from engine.drawing import draw_bezier_cubic, draw_control_handles, draw_circle_bresenham


class BezierTool(BaseTool):
    name = "bezier"

    def __init__(self, app):
        super().__init__(app)
        self.points = []       # list of (x,y) - accumulated anchor/control points
        self.current_pos = None
        self.dragging_cp = False  # sedang drag control point?

    def on_mouse_down(self, pos, button):
        if button != 1:
            return

        if len(self.points) == 0:
            # Anchor pertama
            self.points.append(pos)
        elif len(self.points) == 1:
            # Control point 1 (mulai drag)
            self.points.append(pos)
            self.dragging_cp = True
        elif len(self.points) == 2:
            # Anchor kedua
            self.points.append(pos)
            self.dragging_cp = True
        elif len(self.points) == 3:
            # Control point 2 → commit
            self.points.append(pos)
            self._commit()

    def on_mouse_drag(self, pos, rel):
        self.current_pos = pos
        if self.dragging_cp and len(self.points) >= 2:
            # Update posisi control point terakhir
            self.points[-1] = pos

    def on_mouse_up(self, pos, button):
        self.dragging_cp = False
        self.current_pos = pos
        
        # Auto-commit jika sudah 4 titik
        if len(self.points) >= 4:
            self._commit()

    def on_key_down(self, event):
        key = event.key
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            if len(self.points) >= 4:
                self._commit()
        elif key == pygame.K_ESCAPE:
            self.points.clear()
            self.current_pos = None

    def render_preview(self, surface):
        if not self.points:
            return

        # Gambar titik-titik yang sudah diklik
        for pt in self.points:
            draw_circle_bresenham(surface, config.C_ACCENT,
                                  int(pt[0]), int(pt[1]), 4, filled=True)

        # Preview kurva jika cukup titik
        if len(self.points) >= 4:
            draw_bezier_cubic(surface, config.C_ACCENT,
                              self.points[0], self.points[1],
                              self.points[2], self.points[3],
                              steps=80, thickness=self.app.current_stroke_width)
            draw_control_handles(surface,
                                 self.points[0], self.points[1],
                                 self.points[2], self.points[3])
        elif len(self.points) >= 2 and self.current_pos:
            # Partial preview
            from engine.drawing import draw_dashed_line
            draw_dashed_line(surface, (150, 150, 200),
                             self.points[0][0], self.points[0][1],
                             self.current_pos[0], self.current_pos[1],
                             dash=4, gap=3)

    def _commit(self):
        if len(self.points) < 4:
            return
        # points: [anchor0, ctrl0, anchor1, ctrl1]
        # Reorder ke: anchor0, ctrl0, ctrl1, anchor1
        p0 = self.points[0]
        p1 = self.points[1]
        p2 = self.points[3]
        p3 = self.points[2]

        bezier = BezierCurveObj(p0, p1, p2, p3)
        bezier.stroke_color = self.app.current_stroke_color
        bezier.stroke_width = self.app.current_stroke_width
        bezier.stroke_style = self.app.current_stroke_style

        cmd = AddObjectCommand(self.app.canvas.objects, bezier)
        self.app.history.do(cmd)

        self.points.clear()
        self.current_pos = None
