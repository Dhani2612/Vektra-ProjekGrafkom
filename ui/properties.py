"""
ui/properties.py — Panel Properties (bawah)
=============================================
Stroke color, fill color, width, style.
"""

import pygame
import config


class PropertiesPanel:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Courier New", 13, bold=True)

        # Color swatches yang bisa dipilih
        self.stroke_colors = [
            (0, 0, 0), (255, 0, 0), (0, 150, 0), (0, 0, 255),
            (255, 140, 0), (128, 0, 128), (0, 180, 180), (100, 100, 100),
        ]
        self.fill_colors = [
            None,  # No fill
            (255, 200, 200), (200, 255, 200), (200, 200, 255),
            (255, 255, 200), (255, 220, 180), (230, 200, 255), (220, 220, 220),
        ]
        self.widths = [1, 2, 3, 4, 5, 6]
        self.styles = ["solid", "putus", "titik"]

    def handle_click(self, mx: int, my: int, app) -> bool:
        """Return True jika klik mengenai panel."""
        if not self.rect.collidepoint(mx, my):
            return False

        lx = mx - self.rect.x  # local x
        ly = my - self.rect.y

        # Stroke color swatches (y offset ~5, size 18, gap 2)
        sx_start = 60
        for i, c in enumerate(self.stroke_colors):
            rx = sx_start + i * 20
            if rx <= lx <= rx + 18 and 5 <= ly <= 23:
                app.current_stroke_color = c
                return True

        # Fill color swatches (y offset ~30)
        fx_start = 60
        for i, c in enumerate(self.fill_colors):
            rx = fx_start + i * 20
            if rx <= lx <= rx + 18 and 32 <= ly <= 50:
                app.current_fill_color = c
                return True

        # Width buttons
        wx_start = 300
        for i, w in enumerate(self.widths):
            rx = wx_start + i * 30
            if rx <= lx <= rx + 25 and 5 <= ly <= 25:
                app.current_stroke_width = w
                return True

        # Style buttons
        stx_start = 550
        for i, st in enumerate(self.styles):
            rx = stx_start + i * 60
            if rx <= lx <= rx + 55 and 5 <= ly <= 25:
                app.current_stroke_style = st
                return True

        return True

    def draw(self, surface: pygame.Surface, app):
        # Panel background
        pygame.draw.rect(surface, config.C_PANEL, self.rect)
        pygame.draw.line(surface, config.C_BORDER,
                         (self.rect.left, self.rect.top),
                         (self.rect.right, self.rect.top), 1)

        bx, by = self.rect.x, self.rect.y

        # ── Stroke Color ──
        lbl = self.font.render("Garis:", True, config.C_TEXT)
        surface.blit(lbl, (bx + 5, by + 6))

        for i, c in enumerate(self.stroke_colors):
            rx = bx + 60 + i * 20
            rect = pygame.Rect(rx, by + 5, 18, 18)
            pygame.draw.rect(surface, c, rect)
            if c == app.current_stroke_color:
                pygame.draw.rect(surface, config.C_ACCENT, rect, 2)
            else:
                pygame.draw.rect(surface, config.C_BORDER, rect, 1)

        # ── Fill Color ──
        lbl2 = self.font.render("Isi:", True, config.C_TEXT)
        surface.blit(lbl2, (bx + 5, by + 33))

        for i, c in enumerate(self.fill_colors):
            rx = bx + 60 + i * 20
            rect = pygame.Rect(rx, by + 32, 18, 18)
            if c is None:
                pygame.draw.rect(surface, config.C_PANEL_LIGHT, rect)
                # Draw X for no fill
                pygame.draw.line(surface, config.C_DANGER, rect.topleft, rect.bottomright, 1)
                pygame.draw.line(surface, config.C_DANGER, rect.topright, rect.bottomleft, 1)
            else:
                pygame.draw.rect(surface, c, rect)
            if c == app.current_fill_color:
                pygame.draw.rect(surface, config.C_ACCENT, rect, 2)
            else:
                pygame.draw.rect(surface, config.C_BORDER, rect, 1)

        # ── Width ──
        lbl3 = self.font.render("Tebal:", True, config.C_TEXT)
        surface.blit(lbl3, (bx + 245, by + 6))

        for i, w in enumerate(self.widths):
            rx = bx + 300 + i * 30
            rect = pygame.Rect(rx, by + 5, 25, 20)
            is_active = (w == app.current_stroke_width)
            bg = config.C_ACCENT if is_active else config.C_PANEL_LIGHT
            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, config.C_BORDER, rect, 1, border_radius=3)
            wlbl = self.font.render(str(w), True,
                                    config.C_WHITE if is_active else config.C_TEXT)
            surface.blit(wlbl, wlbl.get_rect(center=rect.center))

        # ── Style ──
        lbl4 = self.font.render("Gaya:", True, config.C_TEXT)
        surface.blit(lbl4, (bx + 500, by + 6))

        for i, st in enumerate(self.styles):
            rx = bx + 550 + i * 60
            rect = pygame.Rect(rx, by + 5, 55, 20)
            is_active = (st == app.current_stroke_style)
            bg = config.C_ACCENT if is_active else config.C_PANEL_LIGHT
            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, config.C_BORDER, rect, 1, border_radius=3)
            slbl = self.font.render(st.capitalize(), True,
                                    config.C_WHITE if is_active else config.C_TEXT)
            surface.blit(slbl, slbl.get_rect(center=rect.center))
