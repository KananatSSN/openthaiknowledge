"""Draw the pictures named by ``otk.sets._support.math_pictures_extra``.

Run::

    python -m otk.pictures.extra_pictures   # optional: pre-draws into the diagram cache
"""

from __future__ import annotations

from pathlib import Path

from matplotlib.patches import Circle, Polygon, Rectangle, Wedge

from otk.sets._support import math_pictures_extra as mx

from .counting_pictures import INK, _save
from .measure_pictures import _axes

SHADE = "#64b5f6"


def make_polygon(p: mx.PolygonPic) -> Path:
    fig, ax = _axes(2.4, 2.0, (-1.45, 1.45), (-1.1, 1.1), scale=1.0)
    ax.add_patch(Polygon(p.points, closed=True, fc="#e3f2fd", ec=INK, lw=1.8, joinstyle="round"))
    return _save(fig, p.asset_id)


def make_bars(b: mx.Bars) -> Path:
    bars = b.wholes + 1
    W, H, gap = 4.0, 0.55, 0.3
    fig, ax = _axes(W + 0.4, bars * (H + gap) + 0.1, (-0.2, W + 0.2),
                    (-bars * (H + gap) + gap - 0.15, 0.15), scale=0.9)
    for i in range(bars):
        y = -i * (H + gap) - H
        shaded = b.d if i < b.wholes else b.part
        for k in range(b.d):
            ax.add_patch(Rectangle((k * W / b.d, y), W / b.d, H,
                                   fc=SHADE if k < shaded else "white", ec=INK, lw=1.2))
    return _save(fig, b.asset_id)


def make_grid(g: mx.Grid) -> Path:
    squares = g.wholes + 1
    cell, gap = 0.22, 0.45
    size = 10 * cell
    fig, ax = _axes(squares * (size + gap), size + 0.2, (-0.1, squares * (size + gap) - gap + 0.1),
                    (-0.1, size + 0.1), scale=0.85)
    for s in range(squares):
        x0 = s * (size + gap)
        shaded = 100 if s < g.wholes else g.hundredths
        # Column by column, as the book shades tenths then hundredths.
        for k in range(100):
            col, row = divmod(k, 10)
            ax.add_patch(Rectangle((x0 + col * cell, size - (row + 1) * cell), cell, cell,
                                   fc=SHADE if k < shaded else "white", ec="#475569", lw=0.6))
        ax.add_patch(Rectangle((x0, 0), size, size, fc="none", ec=INK, lw=1.4))
    return _save(fig, g.asset_id)


_FILL = {"red": "#e53935", "blue": "#42a5f5", "green": "#66bb6a", "yellow": "#fdd835"}


def make_spinner(s: mx.Spinner) -> Path:
    fig, ax = _axes(3.0, 3.0, (-1.3, 1.3), (-1.3, 1.3), scale=0.9)
    n = len(s.sectors)
    for i, c in enumerate(s.sectors):
        a0 = 90 - 360 * (i + 1) / n
        ax.add_patch(Wedge((0, 0), 1.1, a0, a0 + 360 / n, fc=_FILL[c], ec=INK, lw=1.4))
    ax.add_patch(Circle((0, 0), 1.1, fc="none", ec=INK, lw=2.0))
    # The pointer, fixed above the wheel.
    ax.add_patch(Polygon([(-0.1, 1.28), (0.1, 1.28), (0, 1.0)], fc=INK, ec=INK))
    ax.add_patch(Circle((0, 0), 0.08, fc="white", ec=INK, lw=1.2))
    return _save(fig, s.asset_id)


def make_extra_pictures() -> list[Path]:
    out = [make_bars(b) for b in mx.BARS]
    out += [make_grid(g) for g in mx.GRIDS]
    out += [make_spinner(s) for s in mx.SPINNERS]
    return out


if __name__ == "__main__":
    paths = make_extra_pictures()
    print(f"wrote {len(paths)} pictures, {sum(p.stat().st_size for p in paths) // 1024} KB")
