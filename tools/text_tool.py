"""
tools/text_tool.py — Insert & Edit Teks
=========================================
Klik kanvas → cursor teks → ketik → Esc/klik lain → commit.
"""

import pygame
import config
from tools.base_tool import BaseTool
from editor.objects import TextObj
from editor.history import AddObjectCommand


class TextTool(BaseTool):
    name = "text"

    def __init__(self, app):
        super().__init__(app)
        self.text_pos = None
        self.text_buffer = ""
        self.active = False
        self._font = pygame.font.SysFont("Arial", config.DEFAULT_FONT_SIZE)
        self._cursor_blink = 0

    def on_mouse_down(self, pos, button):
        if button != 1:
            return

        if self.active:
            # Commit text sekarang
            self._commit()
        # Mulai typing baru
        self.text_pos = pos
        self.text_buffer = ""
        self.active = True

    def on_key_down(self, event):
        if not self.active:
            return

        if event.key == pygame.K_ESCAPE:
            if self.text_buffer:
                self._commit()
            else:
                self.active = False
                self.text_pos = None
        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self._commit()
        elif event.key == pygame.K_BACKSPACE:
            self.text_buffer = self.text_buffer[:-1]
        else:
            # Gunakan unicode dari event untuk input karakter
            if hasattr(event, 'unicode') and event.unicode:
                # Filter karakter kontrol tidak terlihat jika perlu, tapi pygame sudah handle cukup baik
                if event.unicode.isprintable():
                    self.text_buffer += event.unicode

    def render_preview(self, surface):
        if not self.active or not self.text_pos:
            return

        self._cursor_blink = (self._cursor_blink + 1) % 60

        x, y = int(self.text_pos[0]), int(self.text_pos[1])

        if self.text_buffer:
            text_surf = self._font.render(self.text_buffer, True,
                                          self.app.current_stroke_color)
            surface.blit(text_surf, (x, y))
            # Cursor
            if self._cursor_blink < 30:
                tw = self._font.size(self.text_buffer)[0]
                th = self._font.get_height()
                pygame.draw.line(surface, config.C_ACCENT,
                                 (x + tw + 1, y), (x + tw + 1, y + th), 2)
        else:
            # Cursor saja
            if self._cursor_blink < 30:
                th = self._font.get_height()
                pygame.draw.line(surface, config.C_ACCENT,
                                 (x, y), (x, y + th), 2)

    def _commit(self):
        if self.text_buffer and self.text_pos:
            text_obj = TextObj(self.text_pos[0], self.text_pos[1],
                               self.text_buffer, config.DEFAULT_FONT_SIZE)
            text_obj.stroke_color = self.app.current_stroke_color

            cmd = AddObjectCommand(self.app.canvas.objects, text_obj)
            self.app.history.do(cmd)

        self.active = False
        self.text_pos = None
        self.text_buffer = ""
