"""
engine/transform.py — Transformasi 2D via Matriks Homogeneous 3×3
==================================================================
Menggunakan NumPy untuk operasi matriks.
"""

import numpy as np


def translate(dx: float, dy: float) -> np.ndarray:
    """Matriks translasi 3×3."""
    return np.array([
        [1.0, 0.0, float(dx)],
        [0.0, 1.0, float(dy)],
        [0.0, 0.0, 1.0],
    ])


def rotate(angle_rad: float) -> np.ndarray:
    """Matriks rotasi 3×3 berpusat di origin."""
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [ c, -s, 0.0],
        [ s,  c, 0.0],
        [0.0, 0.0, 1.0],
    ])


def rotate_around(angle_rad: float, cx: float, cy: float) -> np.ndarray:
    """
    Rotasi di titik pivot (cx, cy).
    T(cx,cy) @ R(angle) @ T(-cx,-cy)
    """
    return translate(cx, cy) @ rotate(angle_rad) @ translate(-cx, -cy)


def scale(sx: float, sy: float) -> np.ndarray:
    """Matriks scaling 3×3."""
    return np.array([
        [float(sx), 0.0,       0.0],
        [0.0,       float(sy), 0.0],
        [0.0,       0.0,       1.0],
    ])


def scale_around(sx: float, sy: float, cx: float, cy: float) -> np.ndarray:
    """
    Scaling dari titik tengah (cx, cy).
    T(cx,cy) @ S(sx,sy) @ T(-cx,-cy)
    """
    return translate(cx, cy) @ scale(sx, sy) @ translate(-cx, -cy)


def compose(*matrices) -> np.ndarray:
    """Komposisi matriks (kiri ke kanan = aplikasi kanan ke kiri)."""
    if not matrices:
        return np.identity(3)
    result = matrices[0]
    for m in matrices[1:]:
        result = np.dot(result, m)
    return result


def apply_transform(matrix: np.ndarray, vertices: list) -> list:
    """
    Terapkan matriks 3×3 ke daftar vertex (x, y).
    Mengubah ke homogeneous coords, kalikan, ambil x/y.
    """
    result = []
    for x, y in vertices:
        v = np.array([x, y, 1.0])
        r = matrix @ v
        result.append((r[0], r[1]))
    return result
