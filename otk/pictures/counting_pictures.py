"""Draw the counting pictures named by ``otk.sets._support.math_pictures``.

Run::

    python -m otk.pictures.counting_pictures   # optional: pre-draws into the diagram cache

Each object is a few flat matplotlib patches in a unit cell centred on (0, 0),
so a scene is only a list of (object, x, y). Nothing Thai is drawn: the stem
names the objects. Like the other diagrams the PNGs are quantised, because
several hundred of them ship in the repository.
"""

from __future__ import annotations

import io
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle, Wedge
from PIL import Image

from ._output import save_image
from otk.sets._support import math_pictures as mp
from otk.sets._support import math_pictures_p2 as mp2

_HERE = Path(__file__).parent

INK = "#1f2937"
LINE = 1.2
_CELL = 1.0          # one object occupies a 1 x 1 cell; it is drawn within radius 0.42


def _save(fig, asset_id: str) -> Path:
    buf = io.BytesIO()
    fig.savefig(buf, dpi=100, facecolor="white", format="png")
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf).convert("RGB").quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    return save_image(img, asset_id)


def _canvas(cols: float, rows: float, scale: float = 0.62):
    fig = plt.figure(figsize=(cols * scale, rows * scale))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-(rows - 0.5), 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


# ── the objects ──────────────────────────────────────────────────────────────

def _apple(ax, x, y):
    ax.add_patch(Circle((x - 0.13, y - 0.04), 0.28, fc="#e53935", ec=INK, lw=LINE))
    ax.add_patch(Circle((x + 0.13, y - 0.04), 0.28, fc="#e53935", ec=INK, lw=LINE))
    ax.add_patch(Ellipse((x, y - 0.06), 0.46, 0.5, fc="#e53935", ec="none"))
    ax.plot([x, x + 0.04], [y + 0.18, y + 0.38], color="#6d4c41", lw=2.2, solid_capstyle="round")
    ax.add_patch(Ellipse((x + 0.17, y + 0.33), 0.22, 0.1, angle=25, fc="#43a047", ec=INK, lw=0.8))
    ax.add_patch(Ellipse((x - 0.14, y + 0.04), 0.08, 0.14, angle=-20, fc="#ffcdd2", ec="none"))


def _orange(ax, x, y):
    ax.add_patch(Circle((x, y - 0.03), 0.36, fc="#fb8c00", ec=INK, lw=LINE))
    for dx, dy in ((-0.12, 0.05), (0.1, -0.12), (0.14, 0.1), (-0.05, -0.18)):
        ax.add_patch(Circle((x + dx, y + dy), 0.018, fc="#ef6c00", ec="none"))
    ax.add_patch(Ellipse((x + 0.08, y + 0.34), 0.24, 0.1, angle=20, fc="#43a047", ec=INK, lw=0.8))


def _banana(ax, x, y):
    outer = [(x + 0.42 * math.cos(t), y + 0.2 + 0.55 * math.sin(t))
             for t in [math.radians(a) for a in range(200, 341, 10)]]
    inner = [(x + 0.32 * math.cos(t), y + 0.3 + 0.42 * math.sin(t))
             for t in [math.radians(a) for a in range(340, 199, -10)]]
    ax.add_patch(Polygon(outer + inner, closed=True, fc="#fdd835", ec=INK, lw=LINE))
    tip = outer[-1]
    ax.add_patch(Rectangle((tip[0] - 0.03, tip[1] - 0.01), 0.07, 0.07, fc="#6d4c41", ec="none"))


def _fish(ax, x, y):
    ax.add_patch(Polygon([(x + 0.18, y), (x + 0.42, y + 0.2), (x + 0.42, y - 0.2)],
                         fc="#29b6f6", ec=INK, lw=LINE))
    ax.add_patch(Ellipse((x - 0.06, y), 0.58, 0.36, fc="#29b6f6", ec=INK, lw=LINE))
    ax.add_patch(Circle((x - 0.22, y + 0.04), 0.04, fc=INK, ec="none"))
    ax.plot([x + 0.02, x + 0.02], [y - 0.1, y + 0.1], color="#0277bd", lw=1.0)


def _flower(ax, x, y):
    for k in range(5):
        a = math.radians(90 + 72 * k)
        ax.add_patch(Circle((x + 0.2 * math.cos(a), y + 0.2 * math.sin(a)), 0.16,
                            fc="#ec407a", ec=INK, lw=0.9))
    ax.add_patch(Circle((x, y), 0.13, fc="#ffee58", ec=INK, lw=0.9))


def _balloon(ax, x, y, fc="#7e57c2", shine="#d1c4e9"):
    ax.plot([x, x - 0.03, x + 0.03, x], [y - 0.18, y - 0.3, y - 0.38, y - 0.46],
            color=INK, lw=0.9)
    ax.add_patch(Polygon([(x - 0.05, y - 0.2), (x + 0.05, y - 0.2), (x, y - 0.14)],
                         fc=fc, ec=INK, lw=0.8))
    ax.add_patch(Ellipse((x, y + 0.1), 0.48, 0.58, fc=fc, ec=INK, lw=LINE))
    ax.add_patch(Ellipse((x - 0.1, y + 0.2), 0.08, 0.14, angle=-20, fc=shine, ec="none"))


def _star(ax, x, y):
    pts = []
    for k in range(10):
        r = 0.42 if k % 2 == 0 else 0.18
        a = math.radians(90 + 36 * k)
        pts.append((x + r * math.cos(a), y - 0.03 + r * math.sin(a)))
    ax.add_patch(Polygon(pts, closed=True, fc="#ffca28", ec=INK, lw=LINE))


def _ball(ax, x, y):
    # A beach ball: six coloured panels.
    for k, colour in enumerate(("#e53935", "white", "#1e88e5", "white", "#fdd835", "white")):
        ax.add_patch(Wedge((x, y), 0.36, 90 + 60 * k, 150 + 60 * k, fc=colour, ec=INK, lw=0.8))
    ax.add_patch(Circle((x, y), 0.36, fc="none", ec=INK, lw=LINE))
    ax.add_patch(Circle((x, y), 0.06, fc="white", ec=INK, lw=0.8))


DRAW = {
    "apple": _apple, "orange": _orange, "banana": _banana, "fish": _fish,
    "flower": _flower, "balloon": _balloon, "star": _star, "ball": _ball,
}


# ── extras drawn around the objects ──────────────────────────────────────────

def _cross(ax, x, y):
    ax.plot([x - 0.4, x + 0.4], [y - 0.4, y + 0.4], color=INK, lw=2.6)
    ax.plot([x - 0.4, x + 0.4], [y + 0.4, y - 0.4], color=INK, lw=2.6)


def _plus(ax, x, y):
    ax.plot([x - 0.22, x + 0.22], [y, y], color=INK, lw=3)
    ax.plot([x, x], [y - 0.22, y + 0.22], color=INK, lw=3)


def _box(ax, x0, y0, w, h, label: str = ""):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc="#d7b98e", ec=INK, lw=1.6))
    if label:
        ax.text(x0 + w / 2, y0 + h / 2, label, ha="center", va="center",
                fontsize=26, fontweight="bold", color=INK)


def _stick(ax, x, y, h=0.9, colour="#f2c14e"):
    ax.add_patch(Rectangle((x - 0.035, y - h / 2), 0.07, h, fc=colour, ec=INK, lw=0.6))


def _bundle(ax, x, y):
    for k in range(10):
        _stick(ax, x - 0.27 + 0.06 * k, y)
    ax.add_patch(Rectangle((x - 0.33, y - 0.06), 0.66, 0.12, fc="#c62828", ec=INK, lw=0.8))


# ── scenes ───────────────────────────────────────────────────────────────────

def make_scene(s: mp.Scene) -> Path:
    cols = max(x for _, x, _ in s.items) + 1
    rows = max(y for _, _, y in s.items) + 1
    fig, ax = _canvas(max(cols, 3), rows)
    for kind, x, y in s.items:
        DRAW[kind](ax, x, -y)
    return _save(fig, s.asset_id)


def make_crossed(s: mp.Crossed) -> Path:
    per_row = 5
    rows = (s.total + per_row - 1) // per_row
    fig, ax = _canvas(per_row, rows)
    for i in range(s.total):
        x, y = i % per_row, -(i // per_row)
        DRAW[s.kind](ax, x, y)
        if i >= s.total - s.gone:
            _cross(ax, x, y)
    return _save(fig, s.asset_id)


def make_joined(s: mp.Joined) -> Path:
    width = s.a + 1 + s.b
    fig, ax = _canvas(width, 1)
    for i in range(s.a):
        DRAW[s.kind](ax, i, 0)
    _plus(ax, s.a, 0)
    for i in range(s.b):
        DRAW[s.kind](ax, s.a + 1 + i, 0)
    return _save(fig, s.asset_id)


def make_hidden(s: mp.Hidden) -> Path:
    shown = s.total - s.inside
    fig, ax = _canvas(shown + 2.6, 1.3)
    _box(ax, -0.3, -0.58, 1.8, 1.1, "?")
    for i in range(shown):
        DRAW[s.kind](ax, 2.4 + i, -0.05)
    return _save(fig, s.asset_id)


def make_two_rows(s: mp.TwoRows) -> Path:
    width = max(s.top_n, s.bottom_n)
    fig, ax = _canvas(max(width, 3), 2.2)
    for i in range(s.top_n):
        DRAW[s.top](ax, i, 0)
    for i in range(s.bottom_n):
        DRAW[s.bottom](ax, i, -1.2)
    return _save(fig, s.asset_id)


def make_bundles(s: mp.Bundles) -> Path:
    width = s.tens * 0.85 + (s.ones * 0.2 + 0.5 if s.ones else 0)
    fig, ax = _canvas(max(width, 2.2), 1.2, scale=0.75)
    for k in range(s.tens):
        _bundle(ax, 0.1 + 0.85 * k, -0.1)
    x0 = 0.1 + 0.85 * s.tens + 0.15
    for k in range(s.ones):
        _stick(ax, x0 + 0.2 * k, -0.1)
    return _save(fig, s.asset_id)


# ── ป.2–ป.3 ──────────────────────────────────────────────────────────────────

def make_array(s: mp2.Array) -> Path:
    fig, ax = _canvas(s.cols, s.rows)
    for r in range(s.rows):
        for c in range(s.cols):
            DRAW[s.kind](ax, c, -r)
    return _save(fig, s.asset_id)


def _plate_layout(size: int) -> list[tuple[int, int]]:
    """(column, row) of each thing on a plate: 1–3 in a row, 4 as 2 × 2, 5 as 3 + 2."""
    per_row = {4: 2}.get(size, 3)
    return [(i % per_row, i // per_row) for i in range(size)]


def make_groups(s: mp2.Groups) -> Path:
    cells = _plate_layout(s.size)
    cols = max(c for c, _ in cells) + 1
    rows = max(r for _, r in cells) + 1
    pw, ph = cols * 0.9 + 0.3, rows * 0.9 + 0.3            # one plate
    per_line = min(s.groups, 3)
    lines = (s.groups + 2) // 3
    W, H = per_line * (pw + 0.3), lines * (ph + 0.3)
    fig = plt.figure(figsize=(W * 0.62, H * 0.62))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(-H, 0)
    ax.set_aspect("equal")
    ax.axis("off")
    for g in range(s.groups):
        x0 = 0.15 + (g % 3) * (pw + 0.3)
        y0 = -0.15 - (g // 3) * (ph + 0.3)
        ax.add_patch(FancyBboxPatch((x0, y0 - ph), pw, ph,
                                    boxstyle="round,pad=0,rounding_size=0.3",
                                    fc="#eceff1", ec=INK, lw=1.4))
        for c, r in cells:
            # A short last row is centred on the plate.
            short = cols - (s.size - r * cols) if r == rows - 1 and s.size % cols else 0
            DRAW[s.kind](ax, x0 + 0.6 + 0.9 * c + 0.45 * short, y0 - 0.6 - 0.9 * r)
    return _save(fig, s.asset_id)


_NOTE_COLOUR = {20: "#66bb6a", 50: "#42a5f5", 100: "#ef5350", 500: "#ab47bc"}


def _coin(ax, x, y, value):
    r = {1: 0.26, 2: 0.29, 5: 0.33, 10: 0.36}[value]
    if value == 10:
        ax.add_patch(Circle((x, y), r, fc="#e0b43c", ec=INK, lw=LINE))
        ax.add_patch(Circle((x, y), r * 0.72, fc="#cfd8dc", ec=INK, lw=0.8))
    else:
        ax.add_patch(Circle((x, y), r, fc="#e0b43c" if value == 2 else "#cfd8dc", ec=INK, lw=LINE))
    ax.text(x, y, str(value), ha="center", va="center", fontsize=11, fontweight="bold", color=INK)


def _note(ax, x, y, value):
    ax.add_patch(FancyBboxPatch((x - 0.78, y - 0.36), 1.56, 0.72,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                fc=_NOTE_COLOUR[value], ec=INK, lw=LINE))
    ax.add_patch(Circle((x + 0.42, y), 0.22, fc="white", ec=INK, lw=0.6, alpha=0.7))
    ax.text(x - 0.25, y, str(value), ha="center", va="center", fontsize=15,
            fontweight="bold", color="white")


def make_money(s: mp2.Money) -> Path:
    notes = [v for v, n in s.pieces for _ in range(n) if v in mp2.NOTES]
    coins = [v for v, n in s.pieces for _ in range(n) if v in mp2.COINS]
    rows = (1 if notes else 0) + (len(coins) + 5) // 6
    width = max(len(notes) * 1.8, min(len(coins), 6) * 0.85, 3)
    fig, ax = _canvas(width, rows, scale=0.7)
    ax.set_xlim(-0.5, width - 0.5)
    for i, v in enumerate(notes):
        _note(ax, 0.35 + 1.8 * i, 0, v)
    top = -1 if notes else 0
    for i, v in enumerate(coins):
        _coin(ax, 0.85 * (i % 6), top - (i // 6), v)
    return _save(fig, s.asset_id)


def make_blocks(s: mp2.Blocks) -> Path:
    u = 0.12                                  # one small cube
    flat, step = 10 * u, 10 * u + 0.18
    lines = 1 if s.hundreds <= 5 else 2
    flats_w = min(s.hundreds, 5) * step
    width = flats_w + s.tens * (u + 0.1) + (0.25 + ((s.ones + 1) // 2) * (u + 0.04) if s.ones else 0)
    height = lines * (flat + 0.18)
    fig = plt.figure(figsize=((width + 0.3) * 0.75, (height + 0.2) * 0.75))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-0.15, width + 0.15)
    ax.set_ylim(-height - 0.1, 0.1)
    ax.set_aspect("equal")
    ax.axis("off")
    for i in range(s.hundreds):
        x, y = (i % 5) * step, -(i // 5) * (flat + 0.18) - flat
        ax.add_patch(Rectangle((x, y), flat, flat, fc="#90caf9", ec=INK, lw=1.0))
        for k in range(1, 10):
            ax.plot([x + k * u, x + k * u], [y, y + flat], color="#1e88e5", lw=0.4)
            ax.plot([x, x + flat], [y + k * u, y + k * u], color="#1e88e5", lw=0.4)
    x = flats_w
    base = -height + 0.08
    for _ in range(s.tens):
        ax.add_patch(Rectangle((x, base), u, flat, fc="#a5d6a7", ec=INK, lw=0.9))
        for k in range(1, 10):
            ax.plot([x, x + u], [base + k * u, base + k * u], color="#2e7d32", lw=0.4)
        x += u + 0.1
    x += 0.15
    for k in range(s.ones):
        ax.add_patch(Rectangle((x + (k // 2) * (u + 0.04), base + (k % 2) * (u + 0.04)), u, u,
                               fc="#ffcc80", ec=INK, lw=0.8))
    return _save(fig, s.asset_id)


def make_shaded(s: mp2.Shaded) -> Path:
    per_row = 5
    rows = (s.n + per_row - 1) // per_row
    fig, ax = _canvas(per_row, rows)
    for i in range(s.n):
        red = i in set(mp._order(s.asset_id, list(range(s.n)))[:s.k])
        _balloon(ax, i % per_row, -(i // per_row),
                 fc="#e53935" if red else "#1e88e5", shine="#ffcdd2" if red else "#bbdefb")
    return _save(fig, s.asset_id)


def make_growing(g: mp2.Growing) -> Path:
    """Figures 1, 2 and 3 side by side, each labelled underneath."""
    cell = 0.42
    widths = [g.start + n - 1 for n in (1, 2, 3)]
    total_w = sum(w * cell for w in widths) + 0.9 * 2 + 0.4
    height = g.rows * cell + 0.55
    fig = plt.figure(figsize=(total_w * 0.9, height * 0.9))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, total_w)
    ax.set_ylim(-0.5, g.rows * cell + 0.05)
    ax.set_aspect("equal")
    ax.axis("off")
    x0 = 0.2
    for n, w in zip((1, 2, 3), widths):
        for c in range(w):
            newest = n > 1 and c == w - 1
            fc = "#ffb74d" if newest else "#64b5f6"
            for r in range(g.rows):
                x, y = x0 + c * cell, r * cell
                if g.style == "tile":
                    ax.add_patch(Rectangle((x, y), cell * 0.94, cell * 0.94, fc=fc, ec=INK, lw=1.0))
                else:
                    ax.add_patch(Circle((x + cell / 2, y + cell / 2), cell * 0.36, fc=fc, ec=INK, lw=1.0))
        ax.text(x0 + w * cell / 2, -0.28, str(n), ha="center", va="center",
                fontsize=12, fontweight="bold", color=INK)
        x0 += w * cell + 0.9
    return _save(fig, g.asset_id)


def make_counting_pictures() -> list[Path]:
    out = [make_scene(s) for s in mp.ALL_SCENES]
    out += [make_crossed(s) for s in mp.CROSSED]
    out += [make_joined(s) for s in mp.JOINED]
    out += [make_hidden(s) for s in mp.HIDDEN]
    out += [make_two_rows(s) for s in mp.TWO_ROWS]
    out += [make_bundles(s) for s in mp.BUNDLES]
    out += [make_array(s) for s in mp2.ARRAYS]
    out += [make_groups(s) for s in mp2.GROUPS]
    out += [make_money(s) for s in mp2.MONEY]
    out += [make_blocks(s) for s in mp2.BLOCKS]
    out += [make_shaded(s) for s in mp2.SHADED]
    out += [make_growing(g) for g in mp2.GROWING]
    return out


if __name__ == "__main__":
    paths = make_counting_pictures()
    print(f"wrote {len(paths)} counting pictures, "
          f"{sum(p.stat().st_size for p in paths) // 1024} KB")
