# Vektra — Mini Vector Graphics Editor

> **Vektra** is a simple, lightweight vector graphics editor built from scratch using Python and Pygame. 
> Developed as a Final Project for the Computer Graphics & Multimedia course.

Vektra allows users to draw shapes using various tools, modify visual attributes (color, thickness, line style), and manipulate objects through 2D transformations (translation, rotation, scaling). 

The core feature of Vektra is its **Custom Graphics Engine**. Instead of relying on Pygame's built-in drawing functions, the entire rendering pipeline—from drawing lines and curves to filling areas—is implemented from scratch using fundamental computer graphics algorithms.

## ✨ Features

### Custom Graphics Engine
- **Line Drawing**: DDA and Bresenham algorithms for efficient line rendering, including dashed and dotted styles.
- **Bezier Curves**: Cubic Bezier curves implemented mathematically.
- **Area Filling**: Scanline polygon fill algorithm supporting complex polygons.
- **2D Transformations**: Matrix-based transformations using Homogeneous Coordinates for translating, scaling, and rotating shapes around pivot points.

### Editor & Tools
- **Select Tool**: Interactive bounding boxes with 8 control handles to move, scale, and rotate objects.
- **Pen Tool**: Freehand drawing with optimization for performance.
- **Bezier Tool**: Draw and edit curves using interactive anchor and control handles.
- **Shape Tool**: Draw rectangles and arbitrary polygons with auto-closing functionality and customizable fills.
- **Text Tool**: Real-time canvas text rendering.
- **Eraser Tool**: Instantly delete objects by clicking or dragging across them.

### User Interface & History
- **Command Pattern Undo/Redo**: Full history stack supporting `Ctrl+Z` and `Ctrl+Y`.
- **Properties Panel**: Live-updating panel to tweak stroke color, fill color, line width, and line style.
- **Dynamic Layout**: Resizable workspace, zoom/pan navigation, and a functional menubar (File, Edit, View).
- **Export**: Save/Load project states (`.vk` format) and export canvas to PNG.

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **GUI & Rendering**: Pygame 2.x
- **Matrix Math**: NumPy (for 2D transformations)
- **Serialization**: `pickle` (for saving/loading custom `.vk` project files)

## 🚀 Installation & Running

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dhani2612/Vektra-ProjekGrafkom.git
   cd Vektra-ProjekGrafkom
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install pygame numpy
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## 👥 Team Members

This project was developed collaboratively with roles divided across engine development, object systems, UI, and integration:
- **A1** - Graphics Engineer (`engine/drawing.py`, `engine/fill.py`)
- **A2** - Transform & Selection (`engine/transform.py`, `editor/selection.py`)
- **A3** - Object & Tool System (`editor/objects.py`, `tools/`)
- **A4** - UI & Properties (`ui/toolbar.py`, `ui/properties.py`, `ui/menubar.py`)
- **A5** - Canvas & Integration (`editor/canvas.py`, `editor/history.py`, `main.py`)

## 📚 References

- **DDA & Bresenham**: Hearn & Baker, *Computer Graphics with OpenGL*, Ch. 3
- **Bezier Cubic**: de Casteljau algorithm; parametric form B(t)
- **Scanline Fill**: Foley et al., *Computer Graphics: Principles and Practice*, Ch. 3
- **Transformations**: Homogeneous coordinates & affine transformation matrix
- **Undo/Redo**: Gamma et al., *Design Patterns: Elements of Reusable OO Software* (Command Pattern)
