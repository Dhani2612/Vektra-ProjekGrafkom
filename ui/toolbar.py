"""
ui/toolbar.py — Panel Tool di sisi kiri
=========================================
Ikon-ikon tool yang bisa diklik.
"""

import pygame
import config


# Definisi tool: (id, label pendek, shortcut key)
TOOL_DEFS = [
    ("select",  "Pilih", "S"),
    ("pen",     "Pena", "P"),
    ("bezier",  "Kurva", "B"),
    ("rect",    "Kotak", "R"),
    ("polygon", "Segi-N", "G"),
    ("text",    "Teks", "T"),
    ("eraser",  "Hapus", "E"),
]

BUTTON_SIZE = config.TOOLBAR_WIDTH - 8
BUTTON_PAD  = 4


class Toolbar:
    def __init__(self, x: int, y: int, height: int):
        self.rect = pygame.Rect(x, y, config.TOOLBAR_WIDTH, height)
        self.font = pygame.font.SysFont("Courier New", 11, bold=True)
        self.font_small = pygame.font.SysFont("Courier New", 9)
        self.active_tool = "select"
        self.hovered = None

    def handle_click(self, mx: int, my: int) -> str:
        """Return tool id jika tombol diklik, atau None."""
        if not self.rect.collidepoint(mx, my):
            return None

        for i, (tid, label, shortcut) in enumerate(TOOL_DEFS):
            btn_y = self.rect.y + BUTTON_PAD + i * (BUTTON_SIZE + BUTTON_PAD)
            btn_rect = pygame.Rect(self.rect.x + 4, btn_y, BUTTON_SIZE, BUTTON_SIZE)
            if btn_rect.collidepoint(mx, my):
                self.active_tool = tid
                return tid
        return None

    def handle_hover(self, mx: int, my: int):
        self.hovered = None
        if not self.rect.collidepoint(mx, my):
            return
        for i, (tid, label, shortcut) in enumerate(TOOL_DEFS):
            btn_y = self.rect.y + BUTTON_PAD + i * (BUTTON_SIZE + BUTTON_PAD)
            btn_rect = pygame.Rect(self.rect.x + 4, btn_y, BUTTON_SIZE, BUTTON_SIZE)
            if btn_rect.collidepoint(mx, my):
                self.hovered = tid

    def draw(self, surface: pygame.Surface):
        # Panel background
        pygame.draw.rect(surface, config.C_PANEL, self.rect)
        pygame.draw.line(surface, config.C_BORDER,
                         (self.rect.right - 1, self.rect.top),
                         (self.rect.right - 1, self.rect.bottom), 1)

        for i, (tid, label, shortcut) in enumerate(TOOL_DEFS):
            btn_y = self.rect.y + BUTTON_PAD + i * (BUTTON_SIZE + BUTTON_PAD)
            btn_rect = pygame.Rect(self.rect.x + 4, btn_y, BUTTON_SIZE, BUTTON_SIZE)

            # Background
            if tid == self.active_tool:
                color = config.C_ACCENT
            elif tid == self.hovered:
                color = config.C_PANEL_LIGHT
            else:
                color = config.C_PANEL

            pygame.draw.rect(surface, color, btn_rect, border_radius=4)
            pygame.draw.rect(surface, config.C_BORDER, btn_rect, 1, border_radius=4)

            # Label/Icon
            text_color = config.C_WHITE if tid == self.active_tool else config.C_TEXT
            self._draw_icon(surface, tid, btn_rect.centerx, btn_rect.centery - 4, text_color)

            # Shortcut hint
            hint_surf = self.font_small.render(shortcut, True, config.C_TEXT_DIM)
            hint_rect = hint_surf.get_rect(center=(btn_rect.centerx, btn_rect.centery + 14))
            surface.blit(hint_surf, hint_rect)

    def _draw_icon(self, surface: pygame.Surface, tid: str, cx: int, cy: int, color: tuple):
        import math
        if tid == "select":
            # Draw cursor arrow
            pts = [(cx - 4, cy - 8), (cx - 4, cy + 8), (cx + 1, cy + 3), (cx + 6, cy + 8), (cx + 8, cy + 6), (cx + 3, cy + 1), (cx + 8, cy - 1)]
            pygame.draw.polygon(surface, color, pts)
            pygame.draw.polygon(surface, config.C_BG, pts, 1)
        elif tid == "pen":
            # Draw squiggly line
            pts = [(cx - 8, cy + 4), (cx - 4, cy - 4), (cx, cy + 4), (cx + 4, cy - 4), (cx + 8, cy + 4)]
            pygame.draw.lines(surface, color, False, pts, 2)
        elif tid == "bezier":
            # Draw curve
            pts = [(cx - 8, cy + 6), (cx - 4, cy - 8), (cx + 4, cy - 8), (cx + 8, cy + 6)]
            pygame.draw.lines(surface, color, False, pts, 2)
            pygame.draw.circle(surface, color, pts[0], 2)
            pygame.draw.circle(surface, color, pts[3], 2)
        elif tid == "rect":
            pygame.draw.rect(surface, color, (cx - 8, cy - 6, 16, 12), 2, border_radius=2)
        elif tid == "polygon":
            # Pentagon
            r = 8
            pts = [(cx + r * math.sin(i * 2 * math.pi / 5), cy - r * math.cos(i * 2 * math.pi / 5)) for i in range(5)]
            pygame.draw.polygon(surface, color, pts, 2)
        elif tid == "text":
            font = pygame.font.SysFont("Courier New", 18, bold=True)
            ts = font.render("T", True, color)
            tr = ts.get_rect(center=(cx, cy))
            surface.blit(ts, tr)
        elif tid == "eraser":
            pts = [(cx - 6, cy + 2), (cx - 2, cy - 6), (cx + 6, cy - 2), (cx + 2, cy + 6)]
            pygame.draw.polygon(surface, color, pts, 2)
            pygame.draw.line(surface, color, (cx - 4, cy - 2), (cx + 4, cy + 2), 2)
