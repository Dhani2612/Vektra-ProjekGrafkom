"""
main.py — Entry Point Vektra Vector Graphics Editor
=====================================================
Event loop utama, integrasi engine + editor + tools + UI.
"""

import sys
import pygame

import config
from editor.canvas import Canvas
from editor.selection import SelectionManager
from editor.history import HistoryManager
from tools.select_tool import SelectTool
from tools.pen_tool import PenTool
from tools.bezier_tool import BezierTool
from tools.shape_tool import ShapeTool
from tools.text_tool import TextTool
from ui.toolbar import Toolbar
from ui.properties import PropertiesPanel
from ui.menubar import MenuBar
from tools.eraser_tool import EraserTool


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(config.TITLE)
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # ─── Layout ──────────────────────────────────
        canvas_x = config.TOOLBAR_WIDTH
        canvas_y = config.MENUBAR_HEIGHT
        canvas_w = config.SCREEN_WIDTH - config.TOOLBAR_WIDTH
        canvas_h = (config.SCREEN_HEIGHT - config.MENUBAR_HEIGHT
                    - config.PROPERTIES_HEIGHT)

        # ─── Core ────────────────────────────────────
        self.canvas = Canvas(canvas_x, canvas_y, canvas_w, canvas_h)
        self.selection = SelectionManager()
        self.history = HistoryManager()

        # ─── Current Properties ──────────────────────
        self.current_stroke_color = config.DEFAULT_STROKE_COLOR
        self.current_fill_color = config.DEFAULT_FILL_COLOR
        self.current_stroke_width = config.DEFAULT_STROKE_WIDTH
        self.current_stroke_style = config.DEFAULT_STROKE_STYLE

        # ─── UI ──────────────────────────────────────
        self.menubar = MenuBar(config.SCREEN_WIDTH)
        self.toolbar = Toolbar(0, config.MENUBAR_HEIGHT, canvas_h)
        self.properties = PropertiesPanel(
            0, config.SCREEN_HEIGHT - config.PROPERTIES_HEIGHT,
            config.SCREEN_WIDTH, config.PROPERTIES_HEIGHT)

        # ─── Tools ───────────────────────────────────
        self.tools = {
            "select":  SelectTool(self),
            "pen":     PenTool(self),
            "bezier":  BezierTool(self),
            "rect":    ShapeTool(self, mode="rect"),
            "polygon": ShapeTool(self, mode="polygon"),
            "text":    TextTool(self),
            "eraser":  EraserTool(self),
        }
        self.active_tool_name = "select"
        self.active_tool = self.tools["select"]
        self.show_toolbar = True

        # ─── Status bar font ─────────────────────────
        self.status_font = pygame.font.SysFont("Courier New", 12)

        # Mouse tracking
        self._mouse_down = False

    def set_tool(self, name: str):
        if name in self.tools:
            self.active_tool_name = name
            self.active_tool = self.tools[name]
            self.toolbar.active_tool = name

    def new_project(self):
        self.canvas.objects.clear()
        self.selection.deselect()
        self.history = HistoryManager()

    def save_project(self):
        import pickle
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.asksaveasfilename(defaultextension=".vk", filetypes=[("Vektra Project", "*.vk")])
        if filepath:
            with open(filepath, 'wb') as f:
                pickle.dump(self.canvas.objects, f)

    def load_project(self):
        import pickle
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(filetypes=[("Vektra Project", "*.vk")])
        if filepath:
            try:
                with open(filepath, 'rb') as f:
                    self.canvas.objects = pickle.load(f)
                    self.selection.deselect()
                    self.history.undo_stack.clear()
                    self.history.redo_stack.clear()
            except Exception as e:
                print(f"Gagal memuat proyek: {e}")

    def export_png(self):
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if filepath:
            self.canvas.export_png(filepath)

    def toggle_toolbar(self):
        self.show_toolbar = not self.show_toolbar
        self._update_layout()

    def _update_layout(self):
        self.menubar.rect.width = config.SCREEN_WIDTH
        
        toolbar_w = config.TOOLBAR_WIDTH if self.show_toolbar else 0
        canvas_h = config.SCREEN_HEIGHT - config.MENUBAR_HEIGHT - config.PROPERTIES_HEIGHT
        
        self.toolbar.rect.height = canvas_h
        
        self.properties.rect.y = config.SCREEN_HEIGHT - config.PROPERTIES_HEIGHT
        self.properties.rect.width = config.SCREEN_WIDTH
        
        self.canvas.rect.x = toolbar_w
        self.canvas.resize(config.SCREEN_WIDTH - toolbar_w, canvas_h)

    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            self._handle_events()
            self._draw()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.toolbar.handle_hover(*mouse_pos)
        self.menubar.handle_hover(*mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.VIDEORESIZE:
                config.SCREEN_WIDTH, config.SCREEN_HEIGHT = event.size
                self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                self._update_layout()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                self._mouse_down = True

                # 1) Menu bar
                if self.menubar.handle_click(mx, my, self):
                    continue

                # 2) Toolbar
                if self.show_toolbar:
                    tool_id = self.toolbar.handle_click(mx, my)
                    if tool_id:
                        self.set_tool(tool_id)
                        continue

                # 3) Properties panel
                if self.properties.handle_click(mx, my, self):
                    continue

                # 4) Canvas
                if self.canvas.is_inside(mx, my):
                    cx, cy = self.canvas.screen_to_canvas(mx, my)
                    self.active_tool.on_mouse_down((cx, cy), event.button)
                else:
                    # Klik di luar dropdown → tutup menu
                    self.menubar.open_menu = None

            elif event.type == pygame.MOUSEMOTION:
                if self._mouse_down and self.canvas.is_inside(*event.pos):
                    cx, cy = self.canvas.screen_to_canvas(*event.pos)
                    self.active_tool.on_mouse_drag((cx, cy), event.rel)

            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_down = False
                if self.canvas.is_inside(*event.pos):
                    cx, cy = self.canvas.screen_to_canvas(*event.pos)
                    self.active_tool.on_mouse_up((cx, cy), event.button)

            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()

                # Global shortcuts
                if mods & pygame.KMOD_CTRL:
                    if event.key == pygame.K_z:
                        self.history.undo()
                        continue
                    elif event.key == pygame.K_y:
                        self.history.redo()
                        continue

                # Tool shortcuts
                from tools.text_tool import TextTool
                is_text_typing = isinstance(self.active_tool, TextTool) and self.active_tool.active
                
                handled_shortcut = False
                if not is_text_typing and not (mods & pygame.KMOD_CTRL):
                    key_name = pygame.key.name(event.key).lower()
                    for tid, shortcut in config.TOOL_SHORTCUTS.items():
                        if key_name == shortcut:
                            self.set_tool(tid)
                            handled_shortcut = True
                            break
                            
                if not handled_shortcut:
                    # Forward ke tool aktif
                    self.active_tool.on_key_down(event)

    def _draw(self):
        self.screen.fill(config.C_BG)

        # Canvas (+ objek + selection + tool preview)
        self.canvas.render(self.screen, self.selection,
                           self.active_tool.render_preview)

        # UI panels
        if self.show_toolbar:
            self.toolbar.draw(self.screen)
        self.properties.draw(self.screen, self)
        # Menubar digambar terakhir agar dropdown menutupi toolbar
        self.menubar.draw(self.screen)

        # Status bar (di bawah properties)
        mouse_pos = pygame.mouse.get_pos()
        if self.canvas.is_inside(*mouse_pos):
            cx, cy = self.canvas.screen_to_canvas(*mouse_pos)
            status = (f"Tool: {self.active_tool_name.upper()}  |  "
                      f"Pos: ({int(cx)}, {int(cy)})  |  "
                      f"Objects: {len(self.canvas.objects)}  |  "
                      f"Undo: {len(self.history.undo_stack)}")
        else:
            status = f"Tool: {self.active_tool_name.upper()}  |  Objects: {len(self.canvas.objects)}"

        status_surf = self.status_font.render(status, True, config.C_TEXT_DIM)
        
        toolbar_w = config.TOOLBAR_WIDTH if self.show_toolbar else 0
        self.screen.blit(status_surf,
                         (toolbar_w + 10,
                          config.SCREEN_HEIGHT - 20))

        pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
