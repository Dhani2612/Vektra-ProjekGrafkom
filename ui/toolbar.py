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

            # Label
            text_color = config.C_WHITE if tid == self.active_tool else config.C_TEXT
            text_surf = self.font.render(label, True, text_color)
            text_rect = text_surf.get_rect(center=(btn_rect.centerx, btn_rect.centery - 4))
            surface.blit(text_surf, text_rect)

            # Shortcut hint
            hint_surf = self.font_small.render(shortcut, True, config.C_TEXT_DIM)
            hint_rect = hint_surf.get_rect(center=(btn_rect.centerx, btn_rect.centery + 12))
            surface.blit(hint_surf, hint_rect)
