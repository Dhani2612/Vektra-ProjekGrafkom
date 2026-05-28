# Vektra — Project Brief
> Proyek Akhir Grafika Komputer & Multimedia  
> Mini Vector Graphics Editor | Python + Pygame

---

## 1. Gambaran Proyek

**Vektra** adalah aplikasi editor grafis vektor sederhana — pikir Inkscape versi sangat ringan. Pengguna bisa menggambar bentuk menggunakan berbagai tool, mengubah atribut visual (warna, ketebalan, style garis), dan memanipulasi objek lewat transformasi 2D (geser, putar, scale).

Seluruh proses rendering — garis, kurva, hingga pengisian area — dibangun dari nol menggunakan algoritma grafika yang diimplementasikan sendiri, bukan sekadar memanggil fungsi bawaan Pygame.

---

## 2. Pemetaan Kriteria Wajib

| Kriteria | Implementasi di Vektra |
|---|---|
| Garis & Coretan | Pen tool (coretan bebas freehand), grid kanvas, garis bantu |
| Kurva (Bezier Cubic) | Bezier tool: klik anchor point → drag control handle |
| Fill Area (Scanline) | Semua shape tertutup (polygon, rectangle) bisa di-fill |
| Translasi | Move tool: drag objek ke posisi baru |
| Rotasi | Rotation handle di atas bounding box objek |
| Scaling | Corner handle bounding box untuk resize objek |
| Warna & Ketebalan | Panel properties: stroke color, fill color, line width |
| Style Garis | Solid, dashed, dotted — diterapkan saat render |
| Animasi | Selection highlight, transform handle hover effect, smooth drag |
| Interaksi Mouse | Klik untuk pilih, drag untuk gambar/geser, scroll untuk zoom |
| Interaksi Keyboard | Shortcut: Delete, Ctrl+Z, Ctrl+Y, S/P/B/T untuk ganti tool |
| Tombol / Menu | Toolbar kiri, properties panel kanan, menu bar atas |
| Layar & Jendela | Jendela aplikasi *resizable* (bisa dimaksimalkan ke *fullscreen*) dengan *layout* dinamis |
| Fitur Berkas | Menu untuk membuat kanvas baru, buka/simpan proyek (`.vk`), dan ekspor ke PNG |
| Teks | Text tool: klik kanvas → ketik teks → atur font size & warna |
| Gambar | Import gambar sebagai layer referensi (background) |

---

## 3. Tech Stack

```
Bahasa       : Python 3.11+
GUI & Render : Pygame 2.x
Matrix Math  : NumPy (transformasi 2D)
File I/O     : pickle (save/load project), pygame.image (export PNG)
Version Ctrl : Git + GitHub
```

> **Aturan rendering:** Semua garis dan kurva WAJIB melalui fungsi di `engine/drawing.py`. `pygame.draw.line()` hanya boleh untuk elemen UI (toolbar border, panel divider) — bukan untuk konten kanvas.

---

## 4. Arsitektur Proyek

```
vektra/
│
├── main.py                   # Entry point, event loop utama
├── config.py                 # Konstanta: resolusi, warna UI, FPS, font
│
├── engine/                   # Custom graphics engine — INTI PROYEK
│   ├── drawing.py            # DDA, Bresenham, Bezier cubic, rasterizer
│   ├── fill.py               # Scanline polygon fill
│   └── transform.py          # Matriks homogeneous 3×3, compose, apply
│
├── editor/                   # State & logika editor
│   ├── canvas.py             # Surface kanvas, render semua objek
│   ├── objects.py            # Kelas shape: Line, BezierCurve, Polygon, TextObj, ImageObj
│   ├── selection.py          # Hit-test, bounding box, transform handle
│   └── history.py            # Undo/redo stack (Command pattern)
│
├── tools/                    # Tool aktif yang menangani input mouse
│   ├── select_tool.py        # Pilih, move, rotate, scale objek
│   ├── pen_tool.py           # Gambar coretan bebas (FreehandObj)
│   ├── bezier_tool.py        # Gambar kurva Bezier cubic
│   ├── shape_tool.py         # Rectangle & polygon dengan fill
│   └── text_tool.py          # Insert & edit teks
│
├── ui/                       # Komponen antarmuka
│   ├── toolbar.py            # Panel tool kiri (ikon tool)
│   ├── properties.py         # Panel kanan: warna, ketebalan, style
│   ├── menubar.py            # Menu bar: Berkas, Edit, Tampilan
│   └── colorpicker.py        # Widget color picker sederhana (HSV/RGB)
│
└── assets/
    ├── icons/                # Ikon toolbar (PNG 24×24)
    └── fonts/                # File .ttf untuk text tool
```

---

## 5. Fitur Detail

### 5.1 Custom Graphics Engine

**DDA & Bresenham — `engine/drawing.py`**
```python
def draw_line_dda(surface, color, x0, y0, x1, y1, thickness=1):
    """Digunakan: pen tool, garis grid, selection box."""

def draw_line_bresenham(surface, color, x0, y0, x1, y1, thickness=1):
    """Lebih efisien dari DDA. Digunakan: garis bantu, render dashed line."""

def draw_dashed_line(surface, color, x0, y0, x1, y1, dash=8, gap=4):
    """Render garis putus-putus menggunakan Bresenham per segmen."""
```

**Bezier Cubic — `engine/drawing.py`**
```python
def draw_bezier_cubic(surface, color, p0, p1, p2, p3, steps=100, thickness=1):
    """
    B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
    Digunakan: bezier tool, render BezierCurve object.
    """

def draw_control_handles(surface, p0, p1, p2, p3):
    """Visualisasi control point & tangent line saat object dipilih."""
```

**Scanline Fill — `engine/fill.py`**
```python
def fill_polygon(surface, color, vertices):
    """
    Scanline fill untuk polygon arbitrer (convex & concave).
    Digunakan: fill shape tool, preview warna fill di properties panel.
    """
```

**Transformasi 2D — `engine/transform.py`**
```python
def translate(dx, dy) -> np.ndarray:      # Matriks 3×3
def rotate(angle_rad) -> np.ndarray:      # Rotasi di origin
def rotate_around(angle, cx, cy):         # Rotasi di titik pivot
def scale(sx, sy) -> np.ndarray:
def scale_around(sx, sy, cx, cy):         # Scale dari titik tengah objek
def apply(matrix, vertices) -> list:      # Transformasi batch titik

# Contoh komposisi:
# T = translate(cx, cy) @ rotate(angle) @ translate(-cx, -cy)
# new_verts = apply(T, old_verts)
```

---

### 5.2 Shape Objects — `editor/objects.py`

Semua objek mewarisi kelas `BaseObject`:

```
BaseObject
├── .vertices          # Titik-titik asli (pre-transform)
├── .transform_matrix  # Matriks akumulasi transformasi
├── .stroke_color
├── .fill_color        # None = tidak di-fill
├── .stroke_width
├── .stroke_style      # 'solid' | 'dashed' | 'dotted'
├── .render(surface)   # Panggil engine/drawing.py
└── .get_bounding_box()

Subclass:
├── FreehandObj        # Coretan garis bebas dengan titik yang saling terhubung
├── LineObj            # Satu segmen garis lurus
├── BezierCurveObj     # Kurva dengan 2 anchor + 2 control point
├── PolygonObj         # Polygon N sisi dengan fill opsional
├── RectangleObj       # Shorthand Polygon 4 sisi
├── TextObj            # Teks dengan font, size, warna
└── ImageObj           # Gambar referensi (import PNG/JPG)
```

---

### 5.3 Tool System — `tools/`

Setiap tool mengimplementasikan tiga method event:

```python
class BaseTool:
    def on_mouse_down(self, pos, button): ...
    def on_mouse_drag(self, pos, rel):    ...
    def on_mouse_up(self, pos, button):   ...
    def on_key_down(self, key):           ...
    def render_preview(self, surface):    ...  # Preview sebelum objek di-commit
```

**Select Tool (`S`)**
- Klik objek → tampilkan bounding box dengan 8 handle
- Drag dalam box → translasi
- Drag corner handle → scaling dari titik tengah
- Drag rotation handle (atas) → rotasi di titik pivot
- Klik kosong → deselect

**Pen Tool (`P`)**
- Klik + tahan + geser → menggambar coretan bebas secara kontinu (Freehand)
- Titik-titik baru ditangkap dengan memperhitungkan jarak minimal untuk menghemat memori
- Dilepas → menjadi objek `FreehandObj`

**Bezier Tool (`B`)**
- Klik → anchor point pertama
- Klik+drag → anchor point kedua + drag control handle
- Tampilkan tangent line & control point saat editing
- Enter → commit kurva ke kanvas

**Shape Tool (`R` untuk rect, `G` untuk polygon)**
- Rect: drag untuk gambar kotak
- Polygon: klik per vertex. Klik di dekat titik awal untuk menutup bidang (Auto-Close) & commit
- Fill langsung sesuai setting properties panel

**Text Tool (`T`)**
- Klik kanvas → muncul cursor teks
- Ketik → render teks real-time di kanvas
- Esc / klik lain → commit TextObj

---

### 5.4 Undo/Redo — `editor/history.py`

Implementasi **Command Pattern**: setiap aksi yang mengubah kanvas dibungkus sebagai Command object dengan method `execute()` dan `undo()`.

```python
class AddObjectCommand:      # Tambah objek
class DeleteObjectCommand:   # Hapus objek
class TransformCommand:      # Simpan state transform sebelum & sesudah
class ChangePropertyCommand: # Ubah warna, ketebalan, style
```

Stack undo/redo: `Ctrl+Z` dan `Ctrl+Y`.

---

### 5.5 Layout UI

```
┌─────────────────────────────────────────────────┐
│  Menu Bar: Berkas | Edit | Tampilan             │  ← menubar.py
├────┬────────────────────────────────────────────┤
│    │                                            │
│ T  │                                            │
│ O  │           KANVAS UTAMA                     │  ← canvas.py
│ O  │         (Fullscreen & Resizable)           │
│ L  │                                            │
│ B  │                                            │
│ A  │                                            │
│ R  │                                            │
│    │                                            │
├────┴────────────────────────────────────────────┤
│  Properties: [Garis ▼] [Isi ▼] [Tebal: 1..6]    │  ← properties.py
│              [Gaya: ○Solid ○Putus ○Titik]       │
└─────────────────────────────────────────────────┘
```

---

## 6. Pembagian Tugas

| Anggota | Peran | File Utama |
|---|---|---|
| **A1** | Graphics Engineer | `engine/drawing.py`, `engine/fill.py` |
| **A2** | Transform & Selection | `engine/transform.py`, `editor/selection.py` |
| **A3** | Object & Tool System | `editor/objects.py`, `tools/` (semua tool) |
| **A4** | UI & Properties | `ui/toolbar.py`, `ui/properties.py`, `ui/colorpicker.py`, `ui/menubar.py` |
| **A5** | Canvas & Integration | `editor/canvas.py`, `editor/history.py`, `main.py`, testing |

---

## 7. Timeline

| Minggu | Target | PIC |
|---|---|---|
| 1 | Setup repo, `config.py`, window dasar, toolbar placeholder | A5 |
| 2 | Interface contract antar modul, definisi `BaseObject` | Semua |
| 3 | DDA + Bresenham + test visual di sandbox | A1 |
| 4 | Bezier cubic + Scanline fill + test visual | A1 |
| 5 | Matriks transformasi 2D + apply ke vertices | A2 |
| 6 | `LineObj`, `PolygonObj`, `RectangleObj` + render ke kanvas | A3 |
| 7 | `BezierCurveObj` + Pen tool + Bezier tool | A3 |
| 8 | Select tool: move, rotate, scale via transform matrix | A2 |
| 9 | UI lengkap: toolbar, properties panel, color picker | A4 |
| 10 | Undo/redo, Text tool, import gambar, export PNG | A5 |
| 11 | Bug fixing, integrasi penuh, polish | Semua |
| 12 | Penulisan laporan | Semua |
| 13 | Gladi resik presentasi | Semua |
| 14–15 | **Presentasi** | Semua |

---

## 8. Standar Pengembangan

### Git Workflow
```bash
# Branch per fitur / per modul
git checkout -b feature/bezier-engine
git checkout -b feature/select-tool
git checkout -b feature/properties-panel

# Commit convention
feat: implementasi scanline fill untuk polygon concave
fix: perbaiki rotasi di titik pivot bukan di origin
refactor: pisahkan render preview dari commit object
```

### Sandbox Testing
Buat `debug_draw.py` sebagai file terpisah untuk testing visual setiap fungsi engine sebelum diintegrasikan:

```python
# debug_draw.py — jalankan terpisah untuk test engine
import pygame
from engine.drawing import draw_bezier_cubic, draw_line_bresenham
from engine.fill import fill_polygon

# Render hasil algoritma langsung di window kosong
```

### Konvensi Kode
- Semua fungsi di `engine/` wajib ada docstring + keterangan rumus/algoritma
- Gunakan type hints: `def draw_line_dda(surface: pygame.Surface, color: tuple, ...)`
- Hindari magic number — taruh di `config.py`

---

## 9. Instalasi & Menjalankan

```bash
git clone https://github.com/<Dhani2612>/vektra.git
cd vektra

pip install pygame numpy

python main.py
```

---

## 10. Referensi

| Topik | Referensi |
|---|---|
| DDA & Bresenham | Hearn & Baker, *Computer Graphics with OpenGL*, Ch. 3 |
| Bezier Cubic | de Casteljau algorithm; parametric form B(t) |
| Scanline Fill | Foley et al., *Computer Graphics: Principles and Practice*, Ch. 3 |
| Transformasi 2D | Homogeneous coordinates & affine transformation matrix |
| Command Pattern | Gamma et al., *Design Patterns: Elements of Reusable OO Software* |

---

*Dokumen ini adalah living document — update setiap ada perubahan desain atau pembagian tugas.*