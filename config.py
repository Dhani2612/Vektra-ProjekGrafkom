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
CANVAS_BG     = (245, 245, 245)
CANVAS_GRID   = (220, 220, 220)
GRID_SIZE     = 20

# ─── Color Palette (RGB) ─────────────────────────────────
C_BG          = (34,  34,  44)   # background umum
C_PANEL       = (44,  44,  58)   # panel toolbar / properties
C_PANEL_LIGHT = (58,  58,  76)   # hover panel
C_BORDER      = (70,  70,  95)   # border panel
C_TEXT        = (220, 220, 235)  # teks utama
C_TEXT_DIM    = (140, 140, 165)  # teks sekunder
C_ACCENT      = (80, 160, 255)   # warna aksen / selection
C_ACCENT_HOVER= (120, 190, 255)
C_DANGER      = (255, 80,  80)
C_SUCCESS     = (80, 220, 130)
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
}
