"""
config.py — Konstanta global Vektra
=====================================
Resolusi, warna UI, FPS, layout, dan parameter editor.
"""

# ─── Display ──────────────────────────────────────────────
SCREEN_WIDTH  = 1200
SCREEN_HEIGHT = 800
FPS = 60
TITLE = "Vektra — Vector Graphics Editor"

# ─── Layout ───────────────────────────────────────────────
MENUBAR_HEIGHT    = 30
TOOLBAR_WIDTH     = 70
PROPERTIES_HEIGHT = 80
# Canvas area dihitung otomatis dari sisa ruang

# ─── Canvas ───────────────────────────────────────────────
CANVAS_BG     = (250, 250, 250)  # Modern off-white
CANVAS_GRID   = (210, 210, 210)  # Soft gray for dot grid
GRID_SIZE     = 20

# ─── Color Palette (RGB) ─────────────────────────────────
C_BG          = (24,  24,  27)   # Zinc-900 background
C_PANEL       = (39,  39,  42)   # Zinc-800 panels
C_PANEL_LIGHT = (63,  63,  70)   # Zinc-700 hover state
C_BORDER      = (82,  82,  91)   # Zinc-600 borders
C_TEXT        = (244, 244, 245)  # Zinc-50 main text
C_TEXT_DIM    = (161, 161, 170)  # Zinc-400 muted text
C_ACCENT      = (59, 130, 246)   # Blue-500 brand / selection
C_ACCENT_HOVER= (96, 165, 250)   # Blue-400 hover
C_DANGER      = (239, 68,  68)   # Red-500
C_SUCCESS     = (34, 197,  94)   # Green-500
C_WHITE       = (255, 255, 255)
C_BLACK       = (0,   0,   0)

# Selection / handles
HANDLE_SIZE       = 8
HANDLE_COLOR      = (80, 160, 255)
HANDLE_FILL       = (255, 255, 255)
ROTATION_HANDLE_OFFSET = 25
SELECTION_DASH    = 4

# ─── Default Object Properties ───────────────────────────
DEFAULT_STROKE_COLOR = (0,   0,   0)
DEFAULT_FILL_COLOR   = None             # None = no fill
DEFAULT_STROKE_WIDTH = 2
DEFAULT_STROKE_STYLE = "solid"          # solid | putus | titik
DEFAULT_FONT_SIZE    = 24

# ─── Tool Shortcut Keys ──────────────────────────────────
# (mapped di main.py via pygame key constants)
TOOL_SHORTCUTS = {
    "select":  "s",
    "pen":     "p",
    "bezier":  "b",
    "rect":    "r",
    "polygon": "g",
    "text":    "t",
    "eraser":  "e",
}
