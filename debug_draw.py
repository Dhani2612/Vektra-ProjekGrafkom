"""
debug_draw.py — Sandbox visual test untuk engine
==================================================
Jalankan terpisah: python debug_draw.py
"""

import sys
import math
import pygame
from engine.drawing import (
    draw_line_dda, draw_line_bresenham,
    draw_dashed_line, draw_dotted_line,
    draw_bezier_cubic, draw_control_handles,
    draw_circle_bresenham, draw_polygon_outline,
)
from engine.fill import fill_polygon
from engine.transform import translate, rotate, scale, compose, apply_transform


def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 650))
    pygame.display.set_caption("Vektra Engine — Debug Sandbox")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Courier New", 13, bold=True)
    time_t = 0.0

    base_poly = [(0, -30), (25, 15), (0, 5), (-25, 15)]

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        time_t += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 40))

        # ── 1. DDA Line ──
        draw_line_dda(screen, (0, 255, 120), 40, 50, 200, 120, thickness=2)
        screen.blit(font.render("DDA Line", True, (255, 255, 255)), (40, 30))

        # ── 2. Bresenham Line ──
        draw_line_bresenham(screen, (255, 160, 0), 250, 50, 410, 120, thickness=2)
        screen.blit(font.render("Bresenham Line", True, (255, 255, 255)), (250, 30))

        # ── 3. Dashed Line ──
        draw_dashed_line(screen, (255, 80, 80), 40, 170, 200, 220, dash=8, gap=4, thickness=2)
        screen.blit(font.render("Dashed", True, (255, 255, 255)), (40, 150))

        # ── 4. Dotted Line ──
        draw_dotted_line(screen, (80, 200, 255), 250, 170, 410, 220, dot_gap=5, thickness=2)
        screen.blit(font.render("Dotted", True, (255, 255, 255)), (250, 150))

        # ── 5. Bezier Curve ──
        p0, p1, p2, p3 = (40, 300), (150, 200), (300, 400), (410, 300)
        draw_bezier_cubic(screen, (200, 0, 255), p0, p1, p2, p3, steps=80, thickness=2)
        draw_control_handles(screen, p0, p1, p2, p3)
        screen.blit(font.render("Cubic Bezier + Handles", True, (255, 255, 255)), (40, 270))

        # ── 6. Circle ──
        draw_circle_bresenham(screen, (0, 200, 200), 550, 80, 40)
        draw_circle_bresenham(screen, (0, 200, 200), 660, 80, 40, filled=True)
        screen.blit(font.render("Circle (outline & filled)", True, (255, 255, 255)), (490, 30))

        # ── 7. Scanline Fill + Transform ──
        cx, cy = 580, 320
        angle = time_t * 0.8
        s = 1.0 + 0.3 * math.sin(time_t * 2)

        mat = compose(translate(cx, cy), rotate(angle), scale(s, s))
        tv = apply_transform(mat, base_poly)

        fill_polygon(screen, (200, 60, 60), tv)
        draw_polygon_outline(screen, (255, 220, 100), tv, thickness=2)
        screen.blit(font.render("Scanline Fill + Rotate + Scale", True, (255, 255, 255)), (470, 230))

        # ── 8. Styled Polygon ──
        poly2 = [(700, 400), (820, 370), (850, 480), (780, 530), (690, 500)]
        fill_polygon(screen, (60, 100, 180), poly2)
        draw_polygon_outline(screen, (180, 220, 255), poly2, thickness=2, style="dashed")
        screen.blit(font.render("Polygon + Dashed Outline", True, (255, 255, 255)), (670, 340))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
