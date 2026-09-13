"""
ui/menubar.py — Menu Bar atas
===============================
File | Edit | View
"""

import pygame
import config


MENUS = {
    "Berkas": ["Baru", "Buka Proyek", "Simpan Proyek", "Ekspor PNG"],
    "Edit": ["Batal (Ctrl+Z)", "Ulangi (Ctrl+Y)"],
    "Tampilan": ["Tampilkan Grid", "Tampilkan Toolbar"],
}

MENU_ITEM_HEIGHT = 32
MENU_ITEM_WIDTH  = 160


class MenuBar:
    def __init__(self, width: int):
        self.rect = pygame.Rect(0, 0, width, config.MENUBAR_HEIGHT)
        self.font = pygame.font.SysFont("Segoe UI", 13, bold=True)
        self.font_item = pygame.font.SysFont("Segoe UI", 12)
        self.open_menu = None   # "File" / "Edit" / "View" / None
        self.hovered_item = -1

    def handle_click(self, mx: int, my: int, app) -> bool:
        """Return True jika klik mengenai menubar atau dropdown."""
        # Cek dropdown items dulu (jika open)
        if self.open_menu:
            items = MENUS[self.open_menu]
            ddx = self._get_menu_x(self.open_menu)
            ddy = self.rect.bottom

            for i, item in enumerate(items):
                item_rect = pygame.Rect(ddx, ddy + i * MENU_ITEM_HEIGHT,
                                        MENU_ITEM_WIDTH, MENU_ITEM_HEIGHT)
                if item_rect.collidepoint(mx, my):
                    self._execute(item, app)
                    self.open_menu = None
                    return True

            # Klik di luar dropdown → tutup
            if not self.rect.collidepoint(mx, my):
                self.open_menu = None
                return False

        # Cek menu bar labels
        if not self.rect.collidepoint(mx, my):
            return False

        x_offset = 10
        for menu_name in MENUS:
            tw = self.font.size(menu_name)[0] + 20
            if x_offset <= mx <= x_offset + tw and 0 <= my <= self.rect.bottom:
                if self.open_menu == menu_name:
                    self.open_menu = None
                else:
                    self.open_menu = menu_name
                return True
            x_offset += tw

        self.open_menu = None
        return True

    def handle_hover(self, mx: int, my: int):
        self.hovered_item = -1
        if self.open_menu:
            items = MENUS[self.open_menu]
            ddx = self._get_menu_x(self.open_menu)
            ddy = self.rect.bottom
            for i, item in enumerate(items):
                item_rect = pygame.Rect(ddx, ddy + i * MENU_ITEM_HEIGHT,
                                        MENU_ITEM_WIDTH, MENU_ITEM_HEIGHT)
                if item_rect.collidepoint(mx, my):
                    self.hovered_item = i

    def draw(self, surface: pygame.Surface):
        # Bar background
        pygame.draw.rect(surface, config.C_PANEL, self.rect)
        pygame.draw.line(surface, config.C_BORDER,
                         (0, self.rect.bottom - 1),
                         (self.rect.width, self.rect.bottom - 1), 1)

        # Menu labels
        x_offset = 10
        for menu_name in MENUS:
            tw = self.font.size(menu_name)[0] + 20
            is_open = (self.open_menu == menu_name)

            if is_open:
                pygame.draw.rect(surface, config.C_PANEL_LIGHT,
                                 (x_offset - 5, 2, tw, self.rect.height - 4),
                                 border_radius=3)

            color = config.C_ACCENT if is_open else config.C_TEXT
            lbl = self.font.render(menu_name, True, color)
            surface.blit(lbl, (x_offset, 7))
            x_offset += tw

        # Dropdown
        if self.open_menu:
            items = MENUS[self.open_menu]
            ddx = self._get_menu_x(self.open_menu)
            ddy = self.rect.bottom
            dd_height = len(items) * MENU_ITEM_HEIGHT

            # Shadow + background
            pygame.draw.rect(surface, (15, 15, 18),
                             (ddx + 3, ddy + 3, MENU_ITEM_WIDTH, dd_height), border_radius=6)
            pygame.draw.rect(surface, config.C_PANEL,
                             (ddx, ddy, MENU_ITEM_WIDTH, dd_height), border_radius=6)
            pygame.draw.rect(surface, config.C_BORDER,
                             (ddx, ddy, MENU_ITEM_WIDTH, dd_height), 1, border_radius=6)

            for i, item in enumerate(items):
                iy = ddy + i * MENU_ITEM_HEIGHT
                if i == self.hovered_item:
                    pygame.draw.rect(surface, config.C_ACCENT,
                                     (ddx + 4, iy + 2, MENU_ITEM_WIDTH - 8, MENU_ITEM_HEIGHT - 4), border_radius=4)
                    color = config.C_WHITE
                else:
                    color = config.C_TEXT

                ilbl = self.font_item.render(item, True, color)
                surface.blit(ilbl, (ddx + 10, iy + 5))

    def _get_menu_x(self, menu_name):
        x = 5
        for name in MENUS:
            if name == menu_name:
                return x
            x += self.font.size(name)[0] + 20
        return x

    def _execute(self, item_label: str, app):
        if item_label == "Baru":
            app.new_project()
        elif item_label == "Buka Proyek":
            app.load_project()
        elif item_label == "Simpan Proyek":
            app.save_project()
        elif item_label == "Ekspor PNG":
            app.export_png()
        elif item_label.startswith("Batal"):
            app.history.undo()
        elif item_label.startswith("Ulangi"):
            app.history.redo()
        elif item_label == "Tampilkan Grid":
            app.canvas.show_grid = not app.canvas.show_grid
        elif item_label == "Tampilkan Toolbar":
            app.toggle_toolbar()
