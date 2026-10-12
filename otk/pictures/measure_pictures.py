"""Draw the instruments named by ``otk.sets._support.math_measure_pictures``.

Run::

    python -m otk.pictures.measure_pictures   # optional: pre-draws into the diagram cache

Only digits, ASCII units and the degree-free marks of each instrument are
drawn; the stem carries the Thai.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

from otk.sets._support import math_measure_pictures as mm

from .counting_pictures import DRAW, INK, _save


def _axes(w: float, h: float, xlim, ylim, scale: float = 1.0):
    fig = plt.figure(figsize=(w * scale, h * scale))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


# ── ruler ────────────────────────────────────────────────────────────────────

def make_ruler(r: mm.Ruler) -> Path:
    cm = 0.5
    fig, ax = _axes(8.3, 1.9, (-0.4, 15 * cm + 0.4), (-0.75, 0.6), scale=0.95)
    ax.add_patch(Rectangle((-0.15, -0.7), 15 * cm + 0.3, 0.62, fc="#fff3c4", ec=INK, lw=1.2))
    for mm_ in range(0, 151):
        x = mm_ * cm / 10
        tall = 0.26 if mm_ % 10 == 0 else 0.16 if mm_ % 5 == 0 else 0.09
        ax.plot([x, x], [-0.08, -0.08 - tall], color=INK, lw=0.9 if mm_ % 10 == 0 else 0.5)
        if mm_ % 10 == 0:
            ax.text(x, -0.5, str(mm_ // 10), ha="center", va="center", fontsize=9, color=INK)
    # A pencil from start to start + length, just above the ruler.
    x0, x1 = r.start * cm, (r.start + r.length) * cm
    tip = min(0.35, (x1 - x0) * 0.3)
    y0, y1 = 0.02, 0.32
    ax.add_patch(Rectangle((x0, y0), x1 - x0 - tip, y1 - y0, fc="#fdd835", ec=INK, lw=1.1))
    ax.add_patch(Rectangle((x0, y0), 0.12, y1 - y0, fc="#ef9a9a", ec=INK, lw=1.1))
    ax.add_patch(Polygon([(x1 - tip, y0), (x1 - tip, y1), (x1, (y0 + y1) / 2)],
                         fc="#ffe0b2", ec=INK, lw=1.1))
    ax.plot([x0, x0], [y0, -0.08], color="#c0392b", lw=0.8, ls=":")
    ax.plot([x1, x1], [(y0 + y1) / 2, -0.08], color="#c0392b", lw=0.8, ls=":")
    return _save(fig, r.asset_id)


# ── pictograph ───────────────────────────────────────────────────────────────

def make_pictograph(p: mm.Pictograph) -> Path:
    rows = len(p.rows)
    width = 1.4 + 9
    fig, ax = _axes(width * 0.5, (rows + 0.4) * 0.5 * 1.1,
                    (-0.9, width - 0.9), (-(rows - 0.5) * 1.1 - 0.3, 0.8), scale=1.0)
    for i, (kind, n) in enumerate(p.rows):
        y = -i * 1.1
        DRAW[kind](ax, 0, y)                          # the row's label is its own icon
        ax.plot([0.7, 0.7], [y - 0.5, y + 0.5], color=INK, lw=1.2)
        for j in range(n):
            DRAW[kind](ax, 1.4 + j, y)
        if i < rows - 1:
            ax.plot([-0.6, 10.6], [y - 0.55, y - 0.55], color="#cbd5e1", lw=0.8)
    # The key (1 icon = n) is stated in the stem, where it can be in Thai.
    return _save(fig, p.asset_id)


# ── dial scale ───────────────────────────────────────────────────────────────

def make_scale(s: mm.Scale) -> Path:
    fig, ax = _axes(3.2, 3.4, (-1.45, 1.45), (-1.7, 1.35), scale=0.9)
    ax.add_patch(Rectangle((-1.1, -1.65), 2.2, 0.5, fc="#90a4ae", ec=INK, lw=1.2))
    ax.add_patch(Circle((0, 0), 1.25, fc="#eceff1", ec=INK, lw=2.0))
    ax.add_patch(Circle((0, 0), 1.12, fc="white", ec=INK, lw=0.8))
    # 0 at the top, the full dial is one turn for ``top`` kilograms.
    ticks = s.top * 10
    for k in range(ticks):
        a = math.radians(90 - 360 * k / ticks)
        long = k % 10 == 0
        mid = k % 5 == 0
        r0 = 0.86 if long else 0.95 if mid else 1.0
        ax.plot([r0 * math.cos(a), 1.1 * math.cos(a)], [r0 * math.sin(a), 1.1 * math.sin(a)],
                color=INK, lw=1.4 if long else 0.7)
        if long:
            ax.text(0.7 * math.cos(a), 0.7 * math.sin(a), str(k // 10), ha="center", va="center",
                    fontsize=12, fontweight="bold", color=INK)
    ax.text(0, -0.42, "kg", ha="center", va="center", fontsize=10, color=INK)
    value = s.kg + s.khit / 10
    a = math.radians(90 - 360 * value / s.top)
    ax.plot([0, 1.02 * math.cos(a)], [0, 1.02 * math.sin(a)], color="#c0392b", lw=2.2)
    ax.add_patch(Circle((0, 0), 0.06, fc="#c0392b", ec=INK, lw=0.8))
    return _save(fig, s.asset_id)


# ── measuring jug ────────────────────────────────────────────────────────────

def make_jug(j: mm.Jug) -> Path:
    H, W = 3.0, 1.3
    fig, ax = _axes(2.6, 3.7, (-0.5, W + 1.3), (-0.2, H + 0.5), scale=0.9)
    level = H * j.level / j.top
    ax.add_patch(Rectangle((0, 0), W, level, fc="#90caf9", ec="none"))
    ax.plot([0, 0, W, W], [H + 0.3, 0, 0, H + 0.3], color=INK, lw=2.0)
    ax.plot([W, W + 0.35, W + 0.35, W], [H * 0.85, H * 0.8, H * 0.35, H * 0.3], color=INK, lw=2.0)
    labelled = j.top // 5 if j.top != 500 else 100
    for v in range(j.step, j.top + 1, j.step):
        y = H * v / j.top
        major = v % labelled == 0
        ax.plot([0, 0.32 if major else 0.18], [y, y], color=INK, lw=1.2 if major else 0.8)
        if major:
            ax.text(0.4, y, str(v), ha="left", va="center", fontsize=9, color=INK)
    ax.text(W / 2, H + 0.4, "mL", ha="center", va="center", fontsize=10, color=INK)
    return _save(fig, j.asset_id)


# ── unit cubes ───────────────────────────────────────────────────────────────

_DX, _DY = 0.5, 0.3        # oblique depth offset per cube


def _cube(ax, x, y, z):
    ox, oy = x + z * _DX, y + z * _DY
    front = [(ox, oy), (ox + 1, oy), (ox + 1, oy + 1), (ox, oy + 1)]
    top = [(ox, oy + 1), (ox + 1, oy + 1), (ox + 1 + _DX, oy + 1 + _DY), (ox + _DX, oy + 1 + _DY)]
    side = [(ox + 1, oy), (ox + 1 + _DX, oy + _DY), (ox + 1 + _DX, oy + 1 + _DY), (ox + 1, oy + 1)]
    ax.add_patch(Polygon(side, fc="#90caf9", ec=INK, lw=0.9))
    ax.add_patch(Polygon(top, fc="#e3f2fd", ec=INK, lw=0.9))
    ax.add_patch(Polygon(front, fc="#bbdefb", ec=INK, lw=0.9))


def make_cubes(c: mm.Cubes) -> Path:
    W = c.w + c.d * _DX + 0.4
    H = c.h + c.d * _DY + 0.4
    fig, ax = _axes(W, H, (-0.2, W - 0.2), (-0.2, H - 0.2), scale=0.55)
    # Back to front, bottom to top, so nearer cubes cover farther ones.
    for z in range(c.d - 1, -1, -1):
        for y in range(c.h):
            for x in range(c.w):
                _cube(ax, x, y, z)
    return _save(fig, c.asset_id)


def make_measure_pictures() -> list[Path]:
    out = [make_ruler(r) for r in mm.RULERS]
    out += [make_pictograph(p) for p in mm.PICTOGRAPHS_P1 + mm.PICTOGRAPHS_P2]
    out += [make_scale(s) for s in mm.SCALES]
    out += [make_jug(j) for j in mm.JUGS]
    out += [make_cubes(c) for c in mm.CUBES]
    return out


if __name__ == "__main__":
    paths = make_measure_pictures()
    print(f"wrote {len(paths)} measurement pictures, "
          f"{sum(p.stat().st_size for p in paths) // 1024} KB")
