"""
editor/objects.py — Kelas Shape untuk Vektra
==============================================
BaseObject dan subclass: LineObj, BezierCurveObj, PolygonObj,
RectangleObj, TextObj, ImageObj.
"""

import math
import copy
import numpy as np
import pygame

import config
from engine.drawing import (
    draw_styled_line, draw_bezier_cubic, draw_control_handles,
    draw_polygon_outline, draw_line_bresenham, draw_line_dda
)
from engine.fill import fill_polygon
from engine.transform import apply_transform


class BaseObject:
    """Kelas dasar untuk semua objek di kanvas."""

    def __init__(self):
        self.vertices = []                        # titik asli (local space)
        self.transform_matrix = np.identity(3)    # matriks akumulasi
        self.stroke_color = config.DEFAULT_STROKE_COLOR
        self.fill_color = config.DEFAULT_FILL_COLOR
        self.stroke_width = config.DEFAULT_STROKE_WIDTH
        self.stroke_style = config.DEFAULT_STROKE_STYLE  # solid|dashed|dotted
        self.selected = False

    def get_transformed_vertices(self) -> list:
        """Return vertices setelah transformasi."""
        return apply_transform(self.transform_matrix, self.vertices)

    def get_bounding_box(self) -> tuple:
        """Return (min_x, min_y, max_x, max_y) dari transformed vertices."""
        tv = self.get_transformed_vertices()
        if not tv:
            return (0, 0, 0, 0)
        xs = [p[0] for p in tv]
        ys = [p[1] for p in tv]
        return (min(xs), min(ys), max(xs), max(ys))

    def hit_test(self, mx: float, my: float, threshold: float = 8.0) -> bool:
        """Cek apakah titik (mx, my) dekat dengan objek ini."""
        return False

    def render(self, surface: pygame.Surface):
        """Override di subclass."""
        pass

    def clone(self):
        """Deep copy objek."""
        return copy.deepcopy(self)


class LineObj(BaseObject):
    """Satu segmen garis lurus."""

    def __init__(self, x0, y0, x1, y1):
        super().__init__()
        self.vertices = [(x0, y0), (x1, y1)]

    def hit_test(self, mx, my, threshold=8.0):
        tv = self.get_transformed_vertices()
        if len(tv) < 2:
            return False
        return _point_near_segment(mx, my, tv[0], tv[1], threshold)

    def render(self, surface):
        tv = self.get_transformed_vertices()
        if len(tv) < 2:
            return
        draw_styled_line(surface, self.stroke_color,
                         tv[0][0], tv[0][1], tv[1][0], tv[1][1],
                         self.stroke_style, self.stroke_width)

class FreehandObj(BaseObject):
    """Garis bebas (corat-coret) dengan banyak titik."""
    def __init__(self, points):
        super().__init__()
        self.vertices = list(points)

    def hit_test(self, mx, my, threshold=8.0):
        tv = self.get_transformed_vertices()
        for i in range(len(tv) - 1):
            if _point_near_segment(mx, my, tv[i], tv[i + 1], threshold):
                return True
        return False

    def render(self, surface):
        tv = self.get_transformed_vertices()
        if len(tv) < 2:
            return
        # Render antar titik
        for i in range(len(tv) - 1):
            draw_styled_line(surface, self.stroke_color,
                             tv[i][0], tv[i][1], tv[i+1][0], tv[i+1][1],
                             self.stroke_style, self.stroke_width)


class BezierCurveObj(BaseObject):
    """Kurva cubic Bezier dengan 4 titik kontrol."""

    def __init__(self, p0, p1, p2, p3):
        super().__init__()
        self.vertices = [p0, p1, p2, p3]  # anchor0, ctrl0, ctrl1, anchor1

    def hit_test(self, mx, my, threshold=10.0):
        tv = self.get_transformed_vertices()
        if len(tv) < 4:
            return False
        from engine.drawing import get_bezier_points
        pts = get_bezier_points(tv[0], tv[1], tv[2], tv[3], steps=60)
        for i in range(len(pts) - 1):
            if _point_near_segment(mx, my, pts[i], pts[i + 1], threshold):
                return True
        return False

    def render(self, surface):
        tv = self.get_transformed_vertices()
        if len(tv) < 4:
            return
        draw_bezier_cubic(surface, self.stroke_color,
                          tv[0], tv[1], tv[2], tv[3],
                          steps=100, thickness=self.stroke_width)
        if self.selected:
            draw_control_handles(surface, tv[0], tv[1], tv[2], tv[3])


class PolygonObj(BaseObject):
    """Polygon N sisi, bisa di-fill."""

    def __init__(self, vertices: list):
        super().__init__()
        self.vertices = list(vertices)

    def hit_test(self, mx, my, threshold=8.0):
        tv = self.get_transformed_vertices()
        if len(tv) < 3:
            return False
        # Point-in-polygon (ray casting) atau proximity ke edge
        if self.fill_color and _point_in_polygon(mx, my, tv):
            return True
        for i in range(len(tv)):
            if _point_near_segment(mx, my, tv[i], tv[(i + 1) % len(tv)], threshold):
                return True
        return False

    def render(self, surface):
        tv = self.get_transformed_vertices()
        if len(tv) < 3:
            return
        if self.fill_color:
            fill_polygon(surface, self.fill_color, tv)
        draw_polygon_outline(surface, self.stroke_color, tv,
                             self.stroke_width, self.stroke_style)


class RectangleObj(PolygonObj):
    """Rectangle — shorthand polygon 4 sisi."""

    def __init__(self, x, y, w, h):
        verts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        super().__init__(verts)


class TextObj(BaseObject):
    """Teks yang dirender di kanvas."""

    def __init__(self, x, y, text, font_size=config.DEFAULT_FONT_SIZE):
        super().__init__()
        self.vertices = [(x, y)]
        self.text = text
        self.font_size = font_size
        self._font = None

    def _get_font(self):
        if self._font is None or self._font.get_height() != self.font_size:
            self._font = pygame.font.SysFont("Arial", self.font_size)
        return self._font

    def hit_test(self, mx, my, threshold=5.0):
        bb = self.get_bounding_box()
        return bb[0] - threshold <= mx <= bb[2] + threshold and \
               bb[1] - threshold <= my <= bb[3] + threshold

    def get_bounding_box(self):
        tv = self.get_transformed_vertices()
        if not tv:
            return (0, 0, 0, 0)
        font = self._get_font()
        tw, th = font.size(self.text if self.text else " ")
        x, y = tv[0]
        return (x, y, x + tw, y + th)

    def render(self, surface):
        tv = self.get_transformed_vertices()
        if not tv or not self.text:
            return
        font = self._get_font()
        color = self.stroke_color
        text_surf = font.render(self.text, True, color)
        surface.blit(text_surf, (int(tv[0][0]), int(tv[0][1])))


class ImageObj(BaseObject):
    """Gambar referensi (import PNG/JPG) sebagai layer background."""

    def __init__(self, x, y, image_path: str):
        super().__init__()
        self.image_path = image_path
        self._surface = pygame.image.load(image_path).convert_alpha()
        w, h = self._surface.get_size()
        self.vertices = [(x, y)]
        self.width = w
        self.height = h

    def hit_test(self, mx, my, threshold=5.0):
        bb = self.get_bounding_box()
        return bb[0] <= mx <= bb[2] and bb[1] <= my <= bb[3]

    def get_bounding_box(self):
        tv = self.get_transformed_vertices()
        x, y = tv[0]
        return (x, y, x + self.width, y + self.height)

    def render(self, surface):
        tv = self.get_transformed_vertices()
        surface.blit(self._surface, (int(tv[0][0]), int(tv[0][1])))


# ════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════

def _point_near_segment(px, py, a, b, threshold):
    """Cek apakah titik (px,py) berada dalam jarak threshold dari segmen a-b."""
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    len_sq = dx * dx + dy * dy
    if len_sq == 0:
        return math.hypot(px - ax, py - ay) < threshold

    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / len_sq))
    proj_x = ax + t * dx
    proj_y = ay + t * dy
    return math.hypot(px - proj_x, py - proj_y) < threshold


def _point_in_polygon(px, py, polygon):
    """Ray-casting algorithm untuk point-in-polygon test."""
    n = len(polygon)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside
