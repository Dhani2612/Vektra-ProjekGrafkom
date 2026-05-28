"""
engine/fill.py — Scanline Polygon Fill
========================================
Mengisi interior polygon arbitrer (convex & concave).

Referensi:
  Foley et al., Computer Graphics: Principles and Practice, Ch. 3
"""

import pygame
from engine.drawing import draw_pixel


def fill_polygon(surface: pygame.Surface, color: tuple, vertices: list) -> None:
    """
    Scanline polygon fill algorithm.

    Algoritma:
      1. Tentukan y_min, y_max dari seluruh vertex.
      2. Untuk setiap scanline y dari y_min hingga y_max:
         a. Cari semua interseksi scanline dengan edges polygon.
         b. Urutkan interseksi berdasarkan x.
         c. Fill pixel antara pasangan interseksi (0-1, 2-3, dst.).
      3. Handle: horizontal edges diabaikan, vertex sharing via < y2.

    Digunakan: fill shape tool (rectangle, polygon), preview warna fill.
    """
    if len(vertices) < 3:
        return

    y_min = int(min(v[1] for v in vertices))
    y_max = int(max(v[1] for v in vertices))
    n = len(vertices)
    w, h = surface.get_size()

    for y in range(max(0, y_min), min(h, y_max + 1)):
        intersections = []

        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]

            if y1 > y2:
                y1, y2 = y2, y1
                x1, x2 = x2, x1

            if y1 <= y < y2:
                if y2 != y1:
                    x_int = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    intersections.append(x_int)

        intersections.sort()

        for i in range(0, len(intersections) - 1, 2):
            xs = max(0, int(round(intersections[i])))
            xe = min(w - 1, int(round(intersections[i + 1])))
            for x in range(xs, xe + 1):
                surface.set_at((x, y), color)
