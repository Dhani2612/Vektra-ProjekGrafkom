"""
engine/drawing.py — Algoritma Drawing Primitif
================================================
Implementasi dari nol:
  • DDA Line Drawing
  • Bresenham Line Drawing (integer-only)
  • Dashed & Dotted Line (Bresenham-based)
  • Cubic Bezier Curve (parametric)
  • Control Handle Visualization
  • Bresenham Circle (midpoint)
  • Polygon Outline

Referensi:
  - Hearn & Baker, Computer Graphics with OpenGL, Ch. 3
  - Bresenham, J.E. (1965), Algorithm for computer control of a digital plotter
"""

from __future__ import annotations
import math
import pygame


# ════════════════════════════════════════════════════════════
#  PIXEL
# ════════════════════════════════════════════════════════════

def draw_pixel(surface: pygame.Surface, color: tuple, x: int, y: int) -> None:
    """Plot satu pixel pada surface, dengan boundary check."""
    w, h = surface.get_size()
    ix, iy = int(x), int(y)
    if 0 <= ix < w and 0 <= iy < h:
        surface.set_at((ix, iy), color)


def _draw_thick_pixel(surface: pygame.Surface, color: tuple,
                      x: int, y: int, thickness: int) -> None:
    """Plot area persegi thickness×thickness di sekitar (x, y)."""
    half = thickness // 2
    for dy in range(-half, half + 1):
        for dx in range(-half, half + 1):
            draw_pixel(surface, color, x + dx, y + dy)


# ════════════════════════════════════════════════════════════
#  DDA LINE DRAWING
# ════════════════════════════════════════════════════════════

def draw_line_dda(surface: pygame.Surface, color: tuple,
                  x0: float, y0: float, x1: float, y1: float,
                  thickness: int = 1) -> None:
    """
    Digital Differential Analyzer (DDA) line drawing algorithm.

    Algoritma:
      1. Hitung dx = x1 - x0, dy = y1 - y0
      2. steps = max(|dx|, |dy|)
      3. x_increment = dx / steps, y_increment = dy / steps
      4. Mulai dari (x0, y0), plot round(x), round(y) setiap step

    Menggunakan floating-point arithmetic.
    Digunakan: pen tool garis, grid kanvas, selection box.
    """
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        if thickness > 1:
            _draw_thick_pixel(surface, color, int(x0), int(y0), thickness)
        else:
            draw_pixel(surface, color, int(x0), int(y0))
        return

    x_inc = dx / steps
    y_inc = dy / steps
    x, y = float(x0), float(y0)

    for _ in range(int(steps) + 1):
        if thickness > 1:
            _draw_thick_pixel(surface, color, round(x), round(y), thickness)
        else:
            draw_pixel(surface, color, round(x), round(y))
        x += x_inc
        y += y_inc


# ════════════════════════════════════════════════════════════
#  BRESENHAM LINE DRAWING
# ════════════════════════════════════════════════════════════

def draw_line_bresenham(surface: pygame.Surface, color: tuple,
                        x0: int, y0: int, x1: int, y1: int,
                        thickness: int = 1) -> None:
    """
    Bresenham's line drawing algorithm (integer-only).

    Algoritma:
      1. dx = |x1-x0|, dy = |y1-y0|
      2. sx, sy = arah langkah (+1/-1)
      3. err = dx - dy (error term)
      4. Loop: plot pixel, update error
         - e2 = 2*err
         - Jika e2 > -dy: err -= dy, x += sx
         - Jika e2 < dx:  err += dx, y += sy

    Digunakan: render garis bantu, dashed line segments.
    """
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if thickness > 1:
            _draw_thick_pixel(surface, color, x0, y0, thickness)
        else:
            draw_pixel(surface, color, x0, y0)

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


# ════════════════════════════════════════════════════════════
#  DASHED & DOTTED LINE (Bresenham-based)
# ════════════════════════════════════════════════════════════

def _get_line_pixels(x0: int, y0: int, x1: int, y1: int) -> list:
    """Return list of (x, y) pixels sepanjang garis Bresenham tanpa menggambar."""
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    pixels = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        pixels.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return pixels


def draw_dashed_line(surface: pygame.Surface, color: tuple,
                     x0: float, y0: float, x1: float, y1: float,
                     dash: int = 8, gap: int = 4,
                     thickness: int = 1) -> None:
    """
    Garis putus-putus (dashed) menggunakan segmen Bresenham.

    Membagi pixel-pixel garis menjadi kelompok dash dan gap,
    lalu hanya menggambar kelompok dash.
    """
    pixels = _get_line_pixels(int(x0), int(y0), int(x1), int(y1))
    cycle = dash + gap
    for i, (px, py) in enumerate(pixels):
        if (i % cycle) < dash:
            if thickness > 1:
                _draw_thick_pixel(surface, color, px, py, thickness)
            else:
                draw_pixel(surface, color, px, py)


def draw_dotted_line(surface: pygame.Surface, color: tuple,
                     x0: float, y0: float, x1: float, y1: float,
                     dot_gap: int = 4, thickness: int = 1) -> None:
    """
    Garis titik-titik (dotted) — setiap dot_gap pixel, gambar 1 pixel.
    """
    pixels = _get_line_pixels(int(x0), int(y0), int(x1), int(y1))
    for i, (px, py) in enumerate(pixels):
        if i % dot_gap == 0:
            if thickness > 1:
                _draw_thick_pixel(surface, color, px, py, thickness)
            else:
                draw_pixel(surface, color, px, py)


def draw_styled_line(surface: pygame.Surface, color: tuple,
                     x0: float, y0: float, x1: float, y1: float,
                     style: str = "solid", thickness: int = 1) -> None:
    """Gambar garis dengan style: solid, putus, atau titik."""
    if style == "putus":
        draw_dashed_line(surface, color, x0, y0, x1, y1, thickness=thickness)
    elif style == "titik":
        draw_dotted_line(surface, color, x0, y0, x1, y1, thickness=thickness)
    else:
        draw_line_bresenham(surface, color, int(x0), int(y0), int(x1), int(y1), thickness)


# ════════════════════════════════════════════════════════════
#  CUBIC BEZIER CURVE
# ════════════════════════════════════════════════════════════

def _bezier_point(t: float, p0: tuple, p1: tuple, p2: tuple,
                  p3: tuple) -> tuple:
    """
    Titik pada cubic Bezier di parameter t.
    B(t) = (1-t)³·P0 + 3(1-t)²·t·P1 + 3(1-t)·t²·P2 + t³·P3
    """
    u = 1.0 - t
    u2, u3 = u * u, u * u * u
    t2, t3 = t * t, t * t * t
    x = u3 * p0[0] + 3 * u2 * t * p1[0] + 3 * u * t2 * p2[0] + t3 * p3[0]
    y = u3 * p0[1] + 3 * u2 * t * p1[1] + 3 * u * t2 * p2[1] + t3 * p3[1]
    return (x, y)


def draw_bezier_cubic(surface: pygame.Surface, color: tuple,
                      p0: tuple, p1: tuple, p2: tuple, p3: tuple,
                      steps: int = 100, thickness: int = 1) -> None:
    """
    Gambar cubic Bezier curve.

    B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃

    Evaluasi B(t) untuk t ∈ [0,1] lalu hubungkan segmen dengan Bresenham.
    Digunakan: bezier tool, render BezierCurveObj.
    """
    prev = p0
    for i in range(1, steps + 1):
        t = i / steps
        curr = _bezier_point(t, p0, p1, p2, p3)
        draw_line_bresenham(surface, color,
                            int(prev[0]), int(prev[1]),
                            int(curr[0]), int(curr[1]),
                            thickness)
        prev = curr


def get_bezier_points(p0: tuple, p1: tuple, p2: tuple, p3: tuple,
                      steps: int = 100) -> list:
    """Return daftar titik pada Bezier curve tanpa menggambar."""
    return [_bezier_point(i / steps, p0, p1, p2, p3) for i in range(steps + 1)]


def draw_control_handles(surface: pygame.Surface,
                         p0: tuple, p1: tuple, p2: tuple, p3: tuple) -> None:
    """
    Visualisasi control points & tangent lines saat Bezier dipilih.
    Menggambar garis tangent (dashed) dan lingkaran kecil di control points.
    """
    # Tangent lines
    draw_dashed_line(surface, (150, 150, 150),
                     p0[0], p0[1], p1[0], p1[1], dash=4, gap=3)
    draw_dashed_line(surface, (150, 150, 150),
                     p3[0], p3[1], p2[0], p2[1], dash=4, gap=3)

    # Control points
    for pt in (p0, p1, p2, p3):
        draw_circle_bresenham(surface, (80, 160, 255),
                              int(pt[0]), int(pt[1]), 4, filled=True)
        draw_circle_bresenham(surface, (255, 255, 255),
                              int(pt[0]), int(pt[1]), 4, filled=False)


# ════════════════════════════════════════════════════════════
#  BRESENHAM CIRCLE (Midpoint Circle Algorithm)
# ════════════════════════════════════════════════════════════

def draw_circle_bresenham(surface: pygame.Surface, color: tuple,
                          cx: int, cy: int, radius: int,
                          filled: bool = False) -> None:
    """
    Midpoint Circle Algorithm.

    Decision parameter p = 1 - radius.
    Plot 8 titik simetris setiap iterasi.
    Untuk filled: horizontal lines antara titik simetris.
    """
    cx, cy, radius = int(cx), int(cy), int(radius)
    if radius <= 0:
        draw_pixel(surface, color, cx, cy)
        return

    x, y = 0, radius
    p = 1 - radius

    def _plot(sx, sy):
        if filled:
            for xi in range(-sx, sx + 1):
                draw_pixel(surface, color, cx + xi, cy + sy)
                draw_pixel(surface, color, cx + xi, cy - sy)
            for xi in range(-sy, sy + 1):
                draw_pixel(surface, color, cx + xi, cy + sx)
                draw_pixel(surface, color, cx + xi, cy - sx)
        else:
            pts = [
                (cx + sx, cy + sy), (cx - sx, cy + sy),
                (cx + sx, cy - sy), (cx - sx, cy - sy),
                (cx + sy, cy + sx), (cx - sy, cy + sx),
                (cx + sy, cy - sx), (cx - sy, cy - sx),
            ]
            for px, py in pts:
                draw_pixel(surface, color, px, py)

    _plot(x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 3
        else:
            y -= 1
            p += 2 * (x - y) + 5
        _plot(x, y)


# ════════════════════════════════════════════════════════════
#  POLYGON OUTLINE
# ════════════════════════════════════════════════════════════

def draw_polygon_outline(surface: pygame.Surface, color: tuple,
                         vertices: list, thickness: int = 1,
                         style: str = "solid") -> None:
    """Gambar outline polygon (closed) menggunakan styled lines."""
    n = len(vertices)
    if n < 2:
        return
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        draw_styled_line(surface, color, x0, y0, x1, y1, style, thickness)
