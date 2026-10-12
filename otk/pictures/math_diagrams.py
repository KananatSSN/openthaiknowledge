"""Draw the math diagrams named by ``otk.sets._support.math_diagrams``.

One PNG per spec, drawn on demand by ``otk.pictures.registry`` into
``_output.output_dir()``; running this module draws them all there. Every
label is a number, an ASCII unit or a letter — the bundled matplotlib font has
no Thai. PNGs are quantised to a small palette: these are flat line drawings.
"""

from __future__ import annotations

import io
import math
from pathlib import Path
from random import Random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, Polygon, Rectangle, Wedge
from PIL import Image

from ._output import save_image
from otk.sets._support import math_diagrams as md
from otk.sets.math.p4.bar_chart import _LETTERS
from otk.sets._support import math_diagrams_geo as geo
from otk.sets._support import math_diagrams_hi as hi

_HERE = Path(__file__).parent

INK = "#1f2937"
SOFT = "#dbeafe"
SHADE = "#3b82f6"
GRID = "#d5dae2"
ACCENT = "#c0392b"


def _save(fig, asset_id: str, dpi: int = 100) -> Path:
    buf = io.BytesIO()
    fig.savefig(buf, dpi=dpi, facecolor="white", format="png")
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf).convert("RGB").quantize(colors=48, method=Image.Quantize.MEDIANCUT)
    return save_image(img, asset_id)


def _blank(w: float, h: float, xlim, ylim):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _poly(ax, pts, fill=SOFT, lw=1.8, ls="-", closed=True):
    ax.add_patch(Polygon(pts, closed=closed, facecolor=fill if closed else "none",
                         edgecolor=INK, lw=lw, ls=ls, joinstyle="round"))


def _line(ax, p, q, ls="-", lw=1.8, colour=INK):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=colour, lw=lw, ls=ls, solid_capstyle="round")


def _regular(n, r=1.0, cx=0.0, cy=0.0, start=90.0):
    return [(cx + r * math.cos(math.radians(start + 360 * i / n)),
             cy + r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)]


# ── รูปสองมิติ ────────────────────────────────────────────────────────────────

def make_shape_2d(s) -> Path:
    fig, ax = _blank(2.4, 2.0, (-1.3, 1.3), (-1.05, 1.05))
    if s.name == "triangle":
        _poly(ax, [(-1.0, -0.8), (1.0, -0.8), (0.1, 0.9)])
    elif s.name == "square":
        _poly(ax, [(-0.8, -0.8), (0.8, -0.8), (0.8, 0.8), (-0.8, 0.8)])
    elif s.name == "rectangle":
        _poly(ax, [(-1.2, -0.6), (1.2, -0.6), (1.2, 0.6), (-1.2, 0.6)])
    elif s.name == "circle":
        ax.add_patch(Circle((0, 0), 0.9, facecolor=SOFT, edgecolor=INK, lw=1.8))
    elif s.name == "ellipse":
        ax.add_patch(Ellipse((0, 0), 2.4, 1.3, facecolor=SOFT, edgecolor=INK, lw=1.8))
    elif s.name == "pentagon":
        _poly(ax, _regular(5, 0.95))
    else:
        _poly(ax, _regular(6, 0.95, start=0))
    return _save(fig, s.asset_id)


# ── รูปสามมิติ (oblique drawing, hidden edges dashed) ─────────────────────────

_DX, _DY = 0.55, 0.38


def _prism(ax, front, dx=_DX, dy=_DY):
    back = [(x + dx, y + dy) for x, y in front]
    hidden = min(range(len(front)), key=lambda i: front[i][0] + front[i][1] * 1.2)
    _poly(ax, back, fill="none", ls="-")
    # Re-draw the two back edges that meet the hidden corner as dashed.
    n = len(front)
    for j in ((hidden - 1) % n, hidden):
        a, b = back[j], back[(j + 1) % n]
        _line(ax, a, b, ls=(0, (3, 2)), lw=1.6, colour=INK)
        _line(ax, a, b, lw=2.4, colour="white")
        _line(ax, a, b, ls=(0, (3, 2)), lw=1.6)
    for i, (p, q) in enumerate(zip(front, back)):
        _line(ax, p, q, ls=(0, (3, 2)) if i == hidden else "-", lw=1.6)
    _poly(ax, front)


def make_solid(s) -> Path:
    fig, ax = _blank(2.6, 2.3, (-1.2, 1.9), (-1.2, 1.55))
    if s.name == "cube":
        _prism(ax, [(-0.8, -0.9), (0.4, -0.9), (0.4, 0.3), (-0.8, 0.3)])
    elif s.name == "cuboid":
        _prism(ax, [(-1.1, -0.9), (0.9, -0.9), (0.9, 0.2), (-1.1, 0.2)])
    elif s.name == "tri_prism":
        _prism(ax, [(-1.1, -0.9), (0.0, -0.9), (-0.55, 0.2)], dx=1.5, dy=0.45)
    elif s.name == "pent_prism":
        _prism(ax, _regular(5, 0.6, -0.55, -0.4), dx=1.35, dy=0.5)
    elif s.name in ("sq_pyramid", "tri_pyramid"):
        if s.name == "sq_pyramid":
            base = [(-1.0, -0.9), (0.6, -0.9), (1.1, -0.45), (-0.5, -0.45)]
            hidden = [(3, 0), (2, 3)]
        else:
            base = [(-1.0, -0.9), (0.8, -0.9), (0.35, -0.35)]
            hidden = [(1, 2), (2, 0)]
        apex = (sum(p[0] for p in base) / len(base), 1.2)
        n = len(base)
        for i in range(n):
            a, b = base[i], base[(i + 1) % n]
            dashed = (i, (i + 1) % n) in hidden or ((i + 1) % n, i) in hidden
            _line(ax, a, b, ls=(0, (3, 2)) if dashed else "-", lw=1.6)
        back_vertex = base[3] if s.name == "sq_pyramid" else base[2]
        for p in base:
            _line(ax, p, apex, ls=(0, (3, 2)) if p == back_vertex else "-", lw=1.6)
        front = [p for p in base if p != back_vertex]
        ax.add_patch(Polygon(front + [apex], closed=True, facecolor=SOFT, edgecolor="none", alpha=0.7))
    elif s.name == "cylinder":
        ax.add_patch(Rectangle((-0.8, -0.8), 1.6, 1.7, facecolor=SOFT, edgecolor="none"))
        ax.add_patch(Ellipse((0, -0.8), 1.6, 0.5, facecolor=SOFT, edgecolor="none"))
        ax.add_patch(Arc((0, -0.8), 1.6, 0.5, theta1=180, theta2=360, color=INK, lw=1.8))
        ax.add_patch(Arc((0, -0.8), 1.6, 0.5, theta1=0, theta2=180, color=INK, lw=1.4, ls=(0, (3, 2))))
        ax.add_patch(Ellipse((0, 0.9), 1.6, 0.5, facecolor=SOFT, edgecolor=INK, lw=1.8))
        _line(ax, (-0.8, -0.8), (-0.8, 0.9))
        _line(ax, (0.8, -0.8), (0.8, 0.9))
    elif s.name == "cone":
        ax.add_patch(Polygon([(-0.9, -0.8), (0.9, -0.8), (0, 1.3)], facecolor=SOFT, edgecolor="none"))
        ax.add_patch(Ellipse((0, -0.8), 1.8, 0.5, facecolor=SOFT, edgecolor="none"))
        ax.add_patch(Arc((0, -0.8), 1.8, 0.5, theta1=180, theta2=360, color=INK, lw=1.8))
        ax.add_patch(Arc((0, -0.8), 1.8, 0.5, theta1=0, theta2=180, color=INK, lw=1.4, ls=(0, (3, 2))))
        _line(ax, (-0.9, -0.8), (0, 1.3))
        _line(ax, (0.9, -0.8), (0, 1.3))
    else:  # sphere
        ax.add_patch(Circle((0.2, 0.1), 1.05, facecolor=SOFT, edgecolor=INK, lw=1.8))
        ax.add_patch(Arc((0.2, 0.1), 2.1, 0.55, theta1=180, theta2=360, color=INK, lw=1.4))
        ax.add_patch(Arc((0.2, 0.1), 2.1, 0.55, theta1=0, theta2=180, color=INK, lw=1.2, ls=(0, (3, 2))))
    return _save(fig, s.asset_id)


# ── รูปคลี่ ───────────────────────────────────────────────────────────────────

def _sq(ax, x, y, w, h):
    _poly(ax, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def make_net(n) -> Path:
    fig, ax = _blank(2.8, 2.8, (-0.2, 4.2), (-0.2, 4.2))
    if n.name == "cube":
        for x, y in ((1, 0), (1, 1), (1, 2), (1, 3), (0, 2), (2, 2)):
            _sq(ax, x, y, 1, 1)
    elif n.name == "cuboid":
        # Faces w × length, length × h, w × h laid out as a cross.
        w, length, h = 1.3, 0.8, 0.55
        x0 = 1.2
        ys = [0.1, 0.1 + h, 0.1 + h + length, 0.1 + 2 * h + length]
        for y, hh in zip(ys, (h, length, h, length)):
            _sq(ax, x0, y, w, hh)
        _sq(ax, x0 - h, ys[1], h, length)
        _sq(ax, x0 + w, ys[1], h, length)
    elif n.name == "tri_prism":
        for i in range(3):
            _sq(ax, 0.3 + 1.1 * i, 1.4, 1.1, 1.3)
        _poly(ax, [(1.4, 2.7), (2.5, 2.7), (1.95, 2.7 + 0.95)])
        _poly(ax, [(1.4, 1.4), (2.5, 1.4), (1.95, 1.4 - 0.95)])
    elif n.name == "sq_pyramid":
        _sq(ax, 1.3, 1.3, 1.4, 1.4)
        c = 1.2
        _poly(ax, [(1.3, 2.7), (2.7, 2.7), (2.0, 2.7 + c)])
        _poly(ax, [(1.3, 1.3), (2.7, 1.3), (2.0, 1.3 - c)])
        _poly(ax, [(1.3, 1.3), (1.3, 2.7), (1.3 - c, 2.0)])
        _poly(ax, [(2.7, 1.3), (2.7, 2.7), (2.7 + c, 2.0)])
    elif n.name == "cylinder":
        _sq(ax, 0.3, 1.45, 3.4, 1.1)
        ax.add_patch(Circle((2.0, 3.1), 0.55, facecolor=SOFT, edgecolor=INK, lw=1.8))
        ax.add_patch(Circle((2.0, 0.9), 0.55, facecolor=SOFT, edgecolor=INK, lw=1.8))
    else:  # cone
        ax.add_patch(Wedge((1.6, 3.6), 2.4, 245, 305, facecolor=SOFT, edgecolor=INK, lw=1.8))
        ax.add_patch(Circle((1.6, 0.55), 0.55, facecolor=SOFT, edgecolor=INK, lw=1.8))
    return _save(fig, n.asset_id)


# ── นาฬิกา ────────────────────────────────────────────────────────────────────

def make_clock(c) -> Path:
    fig, ax = _blank(2.2, 2.2, (-1.12, 1.12), (-1.12, 1.12))
    ax.add_patch(Circle((0, 0), 1.0, facecolor="white", edgecolor=INK, lw=2.2))
    for i in range(60):
        a = math.radians(90 - 6 * i)
        r0 = 0.86 if i % 5 == 0 else 0.92
        _line(ax, (r0 * math.cos(a), r0 * math.sin(a)), (0.97 * math.cos(a), 0.97 * math.sin(a)),
              lw=1.6 if i % 5 == 0 else 0.8)
    for n in range(1, 13):
        a = math.radians(90 - 30 * n)
        ax.text(0.72 * math.cos(a), 0.72 * math.sin(a), str(n), ha="center", va="center",
                fontsize=11, color=INK)
    hour = math.radians(90 - 30 * ((c.h % 12) + c.m / 60))
    minute = math.radians(90 - 6 * c.m)
    ax.plot([0, 0.46 * math.cos(hour)], [0, 0.46 * math.sin(hour)], color=INK, lw=4.2,
            solid_capstyle="round")
    ax.plot([0, 0.8 * math.cos(minute)], [0, 0.8 * math.sin(minute)], color=INK, lw=2.2,
            solid_capstyle="round")
    ax.add_patch(Circle((0, 0), 0.05, color=INK))
    return _save(fig, c.asset_id)


# ── มุม ──────────────────────────────────────────────────────────────────────

def make_protractor(a) -> Path:
    fig, ax = _blank(3.4, 2.0, (-1.3, 1.3), (-0.18, 1.3))
    ax.add_patch(Wedge((0, 0), 1.0, 0, 180, facecolor="#f3f4f6", edgecolor=INK, lw=1.2))
    for d in range(0, 181, 5):
        r = math.radians(d)
        r0 = 0.88 if d % 10 == 0 else 0.93
        _line(ax, (r0 * math.cos(r), r0 * math.sin(r)), (math.cos(r), math.sin(r)),
              lw=1.0 if d % 10 == 0 else 0.6)
        if d % 10 == 0:
            ax.text(1.1 * math.cos(r), 1.1 * math.sin(r), str(d), ha="center", va="center",
                    fontsize=6.5, color=INK, rotation=d - 90)
    _line(ax, (0, 0), (1.22, 0), lw=2.2, colour=ACCENT)
    r = math.radians(a.deg)
    _line(ax, (0, 0), (1.22 * math.cos(r), 1.22 * math.sin(r)), lw=2.2, colour=ACCENT)
    ax.add_patch(Arc((0, 0), 0.5, 0.5, theta1=0, theta2=a.deg, color=ACCENT, lw=1.6))
    ax.add_patch(Circle((0, 0), 0.025, color=INK))
    return _save(fig, a.asset_id)


def make_angle_kind(a) -> Path:
    fig, ax = _blank(2.6, 2.6, (-1.3, 1.3), (-1.3, 1.3))
    turn = (a.deg * 37) % 50 - 25          # not always sitting on the horizontal
    b = math.radians(turn)
    e = math.radians(turn + a.deg)
    _line(ax, (0, 0), (1.1 * math.cos(b), 1.1 * math.sin(b)), lw=2.2)
    _line(ax, (0, 0), (1.1 * math.cos(e), 1.1 * math.sin(e)), lw=2.2)
    if a.deg == 90:
        s = 0.2
        p1 = (s * math.cos(b), s * math.sin(b))
        p3 = (s * math.cos(e), s * math.sin(e))
        p2 = (p1[0] + p3[0], p1[1] + p3[1])
        ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=ACCENT, lw=1.6)
    else:
        ax.add_patch(Arc((0, 0), 0.6, 0.6, theta1=turn, theta2=turn + a.deg, color=ACCENT, lw=1.8))
    ax.add_patch(Circle((0, 0), 0.035, color=INK))
    return _save(fig, a.asset_id)


# ── เศษส่วนจากรูป ─────────────────────────────────────────────────────────────

def _shaded_parts(n: int, d: int) -> set[int]:
    order = list(range(d))
    Random(1000 * d + n).shuffle(order)     # a fixed, not always left-to-right, pattern
    return set(order[:n])


def make_fraction(f) -> Path:
    shaded = _shaded_parts(f.n, f.d)
    if f.shape == "bar":
        fig, ax = _blank(3.2, 0.9, (-0.05, 3.05), (-0.1, 0.8))
        w = 3.0 / f.d
        for i in range(f.d):
            ax.add_patch(Rectangle((i * w, 0), w, 0.7, facecolor=SHADE if i in shaded else "white",
                                   edgecolor=INK, lw=1.6))
    else:
        fig, ax = _blank(2.0, 2.0, (-1.08, 1.08), (-1.08, 1.08))
        for i in range(f.d):
            ax.add_patch(Wedge((0, 0), 1.0, 90 + 360 * i / f.d, 90 + 360 * (i + 1) / f.d,
                               facecolor=SHADE if i in shaded else "white", edgecolor=INK, lw=1.6))
    return _save(fig, f.asset_id)


# ── รูปที่มีความยาวกำกับ ──────────────────────────────────────────────────────

def _label(ax, x, y, s, **kw):
    ax.text(x, y, s, ha="center", va="center", fontsize=10, color=INK, **kw)


def _right_mark(ax, corner, u, v, s=0.12):
    p1 = (corner[0] + u[0] * s, corner[1] + u[1] * s)
    p3 = (corner[0] + v[0] * s, corner[1] + v[1] * s)
    p2 = (p1[0] + v[0] * s, p1[1] + v[1] * s)
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=INK, lw=1.0)


def _fit(w, h, box=2.4, least=0.38):
    """Scale real dimensions into the drawing box, never thinner than ``least``."""
    k = box / max(w, h)
    return max(w * k, least * box), max(h * k, least * box)


def make_figure(f) -> Path:
    u = f.unit
    fig, ax = _blank(3.2, 2.6, (-0.6, 3.1), (-0.55, 2.55))
    if f.kind in ("rect", "square"):
        w, length = (f.dims[0], f.dims[0]) if f.kind == "square" else f.dims
        W, H = _fit(length, w, 2.4)
        _poly(ax, [(0, 0), (W, 0), (W, H), (0, H)])
        for c, a, b in (((0, 0), (1, 0), (0, 1)), ((W, 0), (-1, 0), (0, 1)),
                        ((W, H), (-1, 0), (0, -1)), ((0, H), (1, 0), (0, -1))):
            _right_mark(ax, c, a, b)
        _label(ax, W / 2, -0.2, f"{length} {u}")
        if f.kind == "rect":
            _label(ax, -0.32, H / 2, f"{w} {u}", rotation=90)
    elif f.kind == "para":
        b, h, s = f.dims
        off = math.sqrt(max(s * s - h * h, 1))
        k = 2.2 / (b + off)
        B, Hh, origin = b * k, max(h * k, 0.9), off * k
        _poly(ax, [(0, 0), (B, 0), (B + origin, Hh), (origin, Hh)])
        _line(ax, (origin, Hh), (origin, 0), ls=(0, (3, 2)), lw=1.3)
        _right_mark(ax, (origin, 0), (1, 0), (0, 1), s=0.1)
        _label(ax, B / 2, -0.2, f"{b} {u}")
        _label(ax, origin + 0.3, Hh / 2, f"{h} {u}")
        _label(ax, B + origin / 2 + 0.35, Hh / 2, f"{s} {u}")
    elif f.kind == "trap":
        a, b, h = f.dims
        k = 2.5 / b
        A, B, Hh = a * k, b * k, max(h * k, 0.9)
        x0 = (B - A) / 2 + 0.1
        _poly(ax, [(0, 0), (B, 0), (x0 + A, Hh), (x0, Hh)])
        _line(ax, (x0, Hh), (x0, 0), ls=(0, (3, 2)), lw=1.3)
        _right_mark(ax, (x0, 0), (1, 0), (0, 1), s=0.1)
        _label(ax, B / 2, -0.2, f"{b} {u}")
        _label(ax, x0 + A / 2, Hh + 0.18, f"{a} {u}")
        _label(ax, x0 + 0.32, Hh / 2, f"{h} {u}")
    elif f.kind == "tri":
        b, h, at = f.dims
        B, Hh = _fit(b, h, 2.4)
        ax_ = B * at / 10
        _poly(ax, [(0, 0), (B, 0), (ax_, Hh)])
        if at:
            _line(ax, (ax_, Hh), (ax_, 0), ls=(0, (3, 2)), lw=1.3)
        _right_mark(ax, (ax_, 0), (1, 0), (0, 1), s=0.1)
        _label(ax, B / 2, -0.2, f"{b} {u}")
        _label(ax, ax_ + (0.32 if at else -0.32), Hh / 2, f"{h} {u}")
    elif f.kind == "lshape":
        w, h, cw, ch = f.dims
        k = 2.3 / max(w, h)
        W, H, CW, CH = w * k, h * k, cw * k, ch * k
        pts = [(0, 0), (W, 0), (W, H - CH), (W - CW, H - CH), (W - CW, H), (0, H)]
        _poly(ax, pts)
        _label(ax, W / 2, -0.2, f"{w} {u}")
        _label(ax, -0.32, H / 2, f"{h} {u}", rotation=90)
        _label(ax, (W - CW) / 2, H + 0.18, f"{w - cw} {u}")
        _label(ax, W + 0.34, (H - CH) / 2, f"{h - ch} {u}", rotation=90)
        # The notch's own sides are left for the learner to work out.
    else:  # rtri: legs a (vertical), b (horizontal), hypotenuse c
        a, b, c = f.dims
        B, A = _fit(b, a, 2.4)
        _poly(ax, [(0, 0), (B, 0), (0, A)])
        _right_mark(ax, (0, 0), (1, 0), (0, 1), s=0.14)
        show = {k: ("x" if k == f.unknown else str(v)) for k, v in (("a", a), ("b", b), ("c", c))}
        _label(ax, -0.3, A / 2, f"{show['a']} {u}" if show["a"] != "x" else "x", rotation=90)
        _label(ax, B / 2, -0.2, f"{show['b']} {u}" if show["b"] != "x" else "x")
        _label(ax, B / 2 + 0.3, A / 2 + 0.2, f"{show['c']} {u}" if show["c"] != "x" else "x",
               rotation=-math.degrees(math.atan2(A, B)))
    return _save(fig, f.asset_id)


# ── แผนภูมิแท่ง กราฟเส้น ─────────────────────────────────────────────────────

def _chart_axes(w=3.4, h=2.5):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.grid(True, axis="y", color=GRID, lw=0.8, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(labelsize=8, colors=INK)
    return fig, ax


def make_bar_chart(b) -> Path:
    fig, ax = _chart_axes()
    letters = list(_LETTERS[:len(b.values)])
    ax.bar(letters, b.values, color=SHADE, edgecolor=INK, lw=0.8, zorder=2, width=0.6)
    top = max(b.values) + b.scale
    ax.set_ylim(0, top)
    ax.set_yticks(range(0, top + 1, b.scale))
    fig.tight_layout()
    return _save(fig, b.asset_id)


def make_line_graph(g) -> Path:
    fig, ax = _chart_axes()
    xs = list(range(1, len(g.values) + 1))
    ax.plot(xs, g.values, color=ACCENT, lw=2.0, marker="o", ms=4, zorder=3)
    ax.grid(True, axis="x", color=GRID, lw=0.6, zorder=0)
    top = max(g.values) + g.step
    ax.set_ylim(0, top)
    ax.set_yticks(range(0, top + 1, g.step))
    ax.set_xticks(xs)
    ax.set_xlim(0.5, len(xs) + 0.5)
    fig.tight_layout()
    return _save(fig, g.asset_id)


# ── เส้นจำนวนและกราฟบนระนาบพิกัดฉาก ──────────────────────────────────────────

def make_number_line(s) -> Path:
    fig, ax = _blank(4.2, 0.9, (-10.8, 10.8), (-1.6, 1.4))
    ax.annotate("", xy=(10.7, 0), xytext=(-10.7, 0),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4))
    for x in range(-10, 11):
        ax.plot([x, x], [-0.25, 0.25], color=INK, lw=1.4 if x % 5 == 0 else 0.8)
        if x % 5 == 0:
            ax.text(x, -0.9, str(x), ha="center", va="center", fontsize=9, color=INK)
    ax.add_patch(Circle((s.p, 0), 0.28, color=ACCENT, zorder=3))
    ax.text(s.p, 0.85, "A", ha="center", va="center", fontsize=10, color=ACCENT, fontweight="bold")
    return _save(fig, s.asset_id)


def _plane():
    fig, ax = plt.subplots(figsize=(3.2, 3.2))
    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(-6.5, 6.5)
    ax.set_aspect("equal")
    ax.set_xticks(range(-6, 7))
    ax.set_yticks(range(-6, 7))
    ax.grid(True, color=GRID, lw=0.6)
    ax.tick_params(labelsize=6.5, colors=INK, length=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.text(6.4, 0.35, "x", fontsize=9, color=INK)
    ax.text(0.3, 6.2, "y", fontsize=9, color=INK)
    return fig, ax


def make_line_fn(fn) -> Path:
    fig, ax = _plane()
    xs = [x / 20 for x in range(-130, 131)]
    pts = [(x, fn.m * x + fn.c) for x in xs if -6.5 <= fn.m * x + fn.c <= 6.5]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=ACCENT, lw=2.0)
    for x in range(-6, 7):
        y = fn.m * x + fn.c
        if -6 <= y <= 6:
            ax.plot(x, y, "o", color=ACCENT, ms=2.5)
    fig.tight_layout()
    return _save(fig, fn.asset_id)


def make_parabola(p) -> Path:
    fig, ax = _plane()
    xs = [x / 40 for x in range(-260, 261)]
    pts = [(x, p.a * (x - p.h) ** 2 + p.k) for x in xs]
    pts = [q for q in pts if -6.5 <= q[1] <= 6.5]
    ax.plot([q[0] for q in pts], [q[1] for q in pts], color=ACCENT, lw=2.0)
    ax.plot(p.h, p.k, "o", color=ACCENT, ms=3.5)
    fig.tight_layout()
    return _save(fig, p.asset_id)


# ── ม.4–ม.6: Venn, sine, box, scatter, normal ────────────────────────────────

def make_venn(v) -> Path:
    fig, ax = _blank(3.4, 2.4, (-2.1, 2.1), (-1.45, 1.5))
    ax.add_patch(Rectangle((-2.0, -1.35), 4.0, 2.75, facecolor="white", edgecolor=INK, lw=1.6))
    ax.add_patch(Circle((-0.55, 0.0), 0.95, facecolor=SOFT, edgecolor=INK, lw=1.6, alpha=0.8))
    ax.add_patch(Circle((0.55, 0.0), 0.95, facecolor=SOFT, edgecolor=INK, lw=1.6, alpha=0.8))
    ax.add_patch(Circle((-0.55, 0.0), 0.95, facecolor="none", edgecolor=INK, lw=1.6))
    ax.add_patch(Circle((0.55, 0.0), 0.95, facecolor="none", edgecolor=INK, lw=1.6))
    ax.text(-1.85, 1.2, "U", fontsize=11, color=INK, ha="left", va="center")
    ax.text(-1.25, 0.95, "A", fontsize=11, color=INK, ha="center", va="center", fontweight="bold")
    ax.text(1.25, 0.95, "B", fontsize=11, color=INK, ha="center", va="center", fontweight="bold")
    for x, y, n in ((-0.95, 0.0, v.a_only), (0.0, 0.0, v.both), (0.95, 0.0, v.b_only), (1.6, -1.05, v.neither)):
        ax.text(x, y, str(n), fontsize=12, color=INK, ha="center", va="center")
    return _save(fig, v.asset_id)


def make_sine(g) -> Path:
    fig, ax = plt.subplots(figsize=(3.6, 2.4))
    xs = [d / 2 for d in range(0, 721)]
    f = math.sin if g.fn == "sin" else math.cos
    ax.plot(xs, [g.a * f(math.radians(g.b * x)) for x in xs], color=ACCENT, lw=2.0)
    top = max(abs(g.a), 1) + 1
    ax.set_xlim(0, 360)
    ax.set_ylim(-top, top)
    ax.set_xticks(range(0, 361, 45))
    ax.set_yticks(range(-top, top + 1))
    ax.grid(True, color=GRID, lw=0.6)
    ax.axhline(0, color=INK, lw=1.0)
    ax.tick_params(labelsize=7, colors=INK)
    ax.set_xlabel("x (degree)", fontsize=8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    return _save(fig, g.asset_id)


def make_box(b) -> Path:
    fig, ax = plt.subplots(figsize=(3.8, 1.6))
    y, h = 0.5, 0.36
    ax.plot([b.lo, b.q1], [y, y], color=INK, lw=1.6)
    ax.plot([b.q3, b.hi], [y, y], color=INK, lw=1.6)
    for x in (b.lo, b.hi):
        ax.plot([x, x], [y - h / 3, y + h / 3], color=INK, lw=1.6)
    ax.add_patch(Rectangle((b.q1, y - h / 2), b.q3 - b.q1, h, facecolor=SOFT, edgecolor=INK, lw=1.6,
                           zorder=3))
    ax.plot([b.med, b.med], [y - h / 2, y + h / 2], color=ACCENT, lw=2.2, zorder=4)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xticks(range(0, 111, 10))
    ax.set_xticks(range(0, 111, 2), minor=True)
    ax.grid(True, axis="x", which="both", color=GRID, lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=8, colors=INK)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    return _save(fig, b.asset_id)


def make_scatter(sc) -> Path:
    rng = Random(sum(map(ord, sc.trend)) * 31 + sc.seed)
    slope = {"strong_pos": 1, "weak_pos": 1, "strong_neg": -1, "weak_neg": -1, "none": 0}[sc.trend]
    noise = {"strong_pos": 0.6, "weak_pos": 2.6, "strong_neg": 0.6, "weak_neg": 2.6, "none": 3.0}[sc.trend]
    xs = [rng.uniform(1, 10) for _ in range(28)]
    ys = [5 + slope * (x - 5.5) * 0.9 + rng.gauss(0, noise) for x in xs]
    fig, ax = plt.subplots(figsize=(3.0, 2.6))
    ax.scatter(xs, ys, s=14, color=SHADE, edgecolor=INK, lw=0.4, zorder=3)
    ax.set_xlim(0, 11)
    ax.set_ylim(min(ys) - 1, max(ys) + 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("x", fontsize=9)
    ax.set_ylabel("y", fontsize=9, rotation=0)
    ax.grid(True, color=GRID, lw=0.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    return _save(fig, sc.asset_id)


def make_normal(n) -> Path:
    fig, ax = plt.subplots(figsize=(3.8, 2.0))
    xs = [x / 50 for x in range(-200, 201)]
    pdf = [math.exp(-x * x / 2) / math.sqrt(2 * math.pi) for x in xs]
    ax.plot(xs, pdf, color=INK, lw=1.8)
    lo = -4 if n.lo == -9 else n.lo
    hi = 4 if n.hi == 9 else n.hi
    sx = [x for x in xs if lo <= x <= hi]
    ax.fill_between(sx, [math.exp(-x * x / 2) / math.sqrt(2 * math.pi) for x in sx], color=SHADE, alpha=0.6)
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 0.45)
    ax.set_yticks([])
    ax.set_xticks(range(-3, 4))
    ax.set_xlabel("z", fontsize=9)
    ax.tick_params(labelsize=8, colors=INK)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    return _save(fig, n.asset_id)


# ── เรขาคณิตจากรูป (math_diagrams_geo) ──────────────────────────────────────────

def _letter(ax, x, y, s, size=10):
    ax.text(x, y, s, ha="center", va="center", fontsize=size, color=INK)


def _arrow(ax, frm, to):
    ax.annotate("", xy=to, xytext=frm,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8, mutation_scale=14))


def _dot(ax, p):
    ax.plot([p[0]], [p[1]], "o", color=INK, ms=5)


def _rot(p, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def make_line_ray(f) -> Path:
    fig, ax = _blank(3.2, 1.6, (-2.3, 2.3), (-1.0, 1.1))
    a, b = _rot((-1.0, 0.0), f.tilt), _rot((1.0, 0.0), f.tilt)
    far_a, far_b = _rot((-1.9, 0.0), f.tilt), _rot((1.9, 0.0), f.tilt)
    if f.kind == "segment":
        _line(ax, a, b)
    elif f.kind == "ray":
        _line(ax, a, b)
        _arrow(ax, b, far_b)
    elif f.kind == "ray_back":
        _line(ax, a, b)
        _arrow(ax, a, far_a)
    else:
        _line(ax, a, b)
        _arrow(ax, b, far_b)
        _arrow(ax, a, far_a)
    off = _rot((0.0, 0.32), f.tilt)
    for pt, name in ((a, f.names[0]), (b, f.names[1])):
        _dot(ax, pt)
        _letter(ax, pt[0] + off[0], pt[1] + off[1], name, 12)
    return _save(fig, f.asset_id)


def _angle_mark(ax, centre, t1, t2, label, r=0.3, lr=None):
    known = label.isdigit()
    colour = INK if known else ACCENT
    ax.add_patch(Arc(centre, 2 * r, 2 * r, theta1=t1, theta2=t2, color=colour, lw=1.4))
    mid = math.radians((t1 + t2) / 2)
    lr = lr or r + 0.28
    ax.text(centre[0] + lr * math.cos(mid), centre[1] + lr * math.sin(mid),
            f"{label}°" if known else label, fontsize=10, color=colour, ha="center", va="center",
            style="normal" if known else "italic")


def make_parallel(p) -> Path:
    fig, ax = _blank(3.6, 2.6, (-2.6, 2.6), (-1.85, 1.85))
    t = p.theta
    d = 0.9 / math.tan(math.radians(t))
    P, Q = (d, 0.9), (-d, -0.9)
    for y in (0.9, -0.9):
        _line(ax, (-2.5, y), (2.5, y))
        ax.text(-1.9, y, ">", fontsize=12, color=INK, ha="center", va="center")
    u = (math.cos(math.radians(t)), math.sin(math.radians(t)))
    _line(ax, (Q[0] - 0.85 * u[0], Q[1] - 0.85 * u[1]), (P[0] + 0.85 * u[0], P[1] + 0.85 * u[1]))
    spans = ((0, t), (t, 180), (180, 180 + t), (180 + t, 360))
    for pos, lab in p.marks:
        t1, t2 = spans[(pos - 1) % 4]
        _angle_mark(ax, P if pos <= 4 else Q, t1, t2, lab, r=0.26, lr=0.64 if t2 - t1 < 60 else 0.52)
    return _save(fig, p.asset_id)


def _tri_from_angles(a, b):
    c = 180 - a - b
    ac = math.sin(math.radians(b)) / math.sin(math.radians(c))
    return [(0.0, 0.0), (1.0, 0.0), (ac * math.cos(math.radians(a)), ac * math.sin(math.radians(a)))]


def _tri_from_sides(ab, bc, ca):
    ang = math.acos((ab * ab + ca * ca - bc * bc) / (2 * ab * ca))
    return [(0.0, 0.0), (float(ab), 0.0), (ca * math.cos(ang), ca * math.sin(ang))]


def _fit_pts(pts, box=2.6):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = box / max(max(xs) - min(xs), max(ys) - min(ys))
    return [((x - min(xs)) * k, (y - min(ys)) * k) for x, y in pts]


def _centroid(pts):
    return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)


def _outward(p, centre, dist):
    dx, dy = p[0] - centre[0], p[1] - centre[1]
    n = math.hypot(dx, dy) or 1
    return p[0] + dx / n * dist, p[1] + dy / n * dist


def _tag(ax, x, y, lab):
    """A measurement: a number in ink, an unknown in red italics."""
    known = lab[0].isdigit()
    ax.text(x, y, lab, fontsize=9, ha="center", va="center", color=INK if known else ACCENT,
            style="normal" if known else "italic")


def make_marked_triangle(t) -> Path:
    fig, ax = _blank(3.2, 2.6, (-0.5, 3.2), (-0.5, 2.9))
    pts = _fit_pts(_tri_from_sides(*t.sides) if t.sides else _tri_from_angles(*t.angles[:2]))
    _poly(ax, pts)
    g = _centroid(pts)
    for p, name in zip(pts, "ABC"):
        _letter(ax, *_outward(p, g, 0.25), name, 11)
    if t.sides:
        for (p, q), v in zip(((pts[0], pts[1]), (pts[1], pts[2]), (pts[2], pts[0])), t.sides):
            m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
            _tag(ax, *_outward(m, g, 0.26), f"{v} cm")
    else:
        labels = [f"{t.angles[0]}°", f"{t.angles[1]}°", f"{t.angles[2]}°" if t.shown == "abc" else "x"]
        for p, lab in zip(pts, labels):
            _tag(ax, *_outward(p, g, -0.45), lab)
    return _save(fig, t.asset_id)


_PIE_FILLS = (SOFT, "#fde68a", "#bbf7d0", "#fbcfe8")


def make_pie(p) -> Path:
    fig, ax = _blank(2.6, 2.6, (-1.15, 1.15), (-1.15, 1.15))
    start = 90.0
    for name, pct, fill in zip("ABCD", p.percents, _PIE_FILLS):
        sweep = 3.6 * pct
        ax.add_patch(Wedge((0, 0), 1.0, start - sweep, start, facecolor=fill, edgecolor=INK, lw=1.4))
        mid = math.radians(start - sweep / 2)
        ax.text(0.6 * math.cos(mid), 0.6 * math.sin(mid), f"{name}\n{pct}%", fontsize=9, color=INK,
                ha="center", va="center")
        start -= sweep
    return _save(fig, p.asset_id)


def make_transform(t) -> Path:
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(-6.5, 6.5)
    ax.set_aspect("equal")
    ticks = list(range(-6, 7))
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels([str(v) if v % 2 == 0 and v else "" for v in ticks])
    ax.set_yticklabels([str(v) if v % 2 == 0 and v else "" for v in ticks])
    ax.grid(True, color=GRID, lw=0.6)
    ax.axhline(0, color=INK, lw=1.0)
    ax.axvline(0, color=INK, lw=1.0)
    ax.tick_params(labelsize=7, colors=INK, length=0)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.text(6.2, 0.35, "X", fontsize=8, color=INK)
    ax.text(0.25, 6.1, "Y", fontsize=8, color=INK)
    img = t.image()
    _poly(ax, t.tri)
    ax.add_patch(Polygon(img, closed=True, facecolor="none", edgecolor=ACCENT, lw=1.8, ls="--"))
    for pts, names in ((t.tri, ("A", "B", "C")), (img, ("A'", "B'", "C'"))):
        g = _centroid(pts)
        for p, n in zip(pts, names):
            x, y = _outward(p, g, 0.6)
            ax.text(x, y, n, fontsize=8, color=INK, ha="center", va="center")
    fig.tight_layout()
    return _save(fig, t.asset_id)


def _mark_between(ax, v, p, q, label, r=0.22, lr=0.42):
    """Mark the angle at ``v`` between rays to ``p`` and ``q`` (the smaller side)."""
    a1 = math.degrees(math.atan2(p[1] - v[1], p[0] - v[0])) % 360
    a2 = math.degrees(math.atan2(q[1] - v[1], q[0] - v[0])) % 360
    if (a2 - a1) % 360 > 180:
        a1, a2 = a2, a1
    _angle_mark(ax, v, a1, a1 + (a2 - a1) % 360, label, r=r, lr=lr)


def make_circle_angle(c) -> Path:
    fig, ax = _blank(2.8, 2.8, (-1.4, 1.4), (-1.4, 1.4))
    ax.add_patch(Circle((0, 0), 1.0, facecolor="none", edgecolor=INK, lw=1.6))

    def on(deg):
        return (math.cos(math.radians(deg)), math.sin(math.radians(deg)))

    def name(p, s):
        _letter(ax, p[0] * 1.17, p[1] * 1.17, s, 10)

    origin = (0.0, 0.0)
    if c.kind in ("central", "inscribed"):
        cen = c.value if c.kind == "central" else 2 * c.value
        A, B, C = on(-90 - cen / 2), on(-90 + cen / 2), on(90)
        for p, q in ((origin, A), (origin, B), (C, A), (C, B)):
            _line(ax, p, q, lw=1.4)
        _dot(ax, origin)
        _letter(ax, 0.14, 0.12, "O", 10)
        for p, s in ((A, "A"), (B, "B"), (C, "C")):
            name(p, s)
        at_o, at_c = (str(c.value), "x") if c.kind == "central" else ("x", str(c.value))
        _mark_between(ax, origin, A, B, at_o, r=0.18, lr=0.36)
        _mark_between(ax, C, A, B, at_c, r=0.3, lr=0.52)
    elif c.kind == "semi":
        A, B, C = on(180), on(0), on(2 * c.value)
        for p, q in ((A, B), (A, C), (B, C)):
            _line(ax, p, q, lw=1.4)
        _dot(ax, origin)
        _letter(ax, 0.0, -0.14, "O", 10)
        for p, s in ((A, "A"), (B, "B"), (C, "C")):
            name(p, s)
        _mark_between(ax, A, B, C, str(c.value), r=0.3, lr=0.52)
        _mark_between(ax, B, A, C, "x", r=0.26, lr=0.48)
    else:
        v = c.value
        A, B, C, D = on(180), on(v + 20), on(0), on(20 - v)
        _poly(ax, [A, B, C, D], fill="none")
        for p, s in ((A, "A"), (B, "B"), (C, "C"), (D, "D")):
            name(p, s)
        _mark_between(ax, A, B, D, str(v), r=0.26, lr=0.48)
        _mark_between(ax, C, B, D, "x", r=0.22, lr=0.44)
    return _save(fig, c.asset_id)


def make_similar(s) -> Path:
    fig, ax = _blank(4.2, 2.4, (-0.3, 6.4), (-0.45, 3.35))
    big = [v * s.k for v in s.small]
    # Each triangle at its own scale, the small one never too cramped to label.
    su, bu = 1.7 / max(s.small), 3.0 / max(big)
    small_pts = [(x * su, y * su) for x, y in _tri_from_sides(*s.small)]
    shift = max(p[0] for p in small_pts) + 0.9
    big_pts = [(x * bu + shift, y * bu) for x, y in _tri_from_sides(*big)]
    small_lab = [str(v) for v in s.small]
    big_lab = [str(v) for v in big]
    (big_lab if s.unknown < 3 else small_lab)[s.unknown % 3] = "x"
    for pts, names, labels in ((small_pts, "ABC", small_lab), (big_pts, "DEF", big_lab)):
        _poly(ax, pts)
        g = _centroid(pts)
        for p, n in zip(pts, names):
            _letter(ax, *_outward(p, g, 0.22), n, 10)
        for (p, q), lab in zip(((pts[0], pts[1]), (pts[1], pts[2]), (pts[2], pts[0])), labels):
            m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
            _tag(ax, *_outward(m, g, 0.2), lab)
    return _save(fig, s.asset_id)


_SYM_SHAPES = {
    "square": [(-1, -1), (1, -1), (1, 1), (-1, 1)],
    "rectangle": [(-1.4, -0.8), (1.4, -0.8), (1.4, 0.8), (-1.4, 0.8)],
    "isosceles": [(-0.8, -1.0), (0.8, -1.0), (0.0, 1.2)],
    "scalene": [(-1.2, -0.9), (1.2, -0.9), (0.55, 1.0)],
    "rhombus": [(0, -1.2), (0.8, 0), (0, 1.2), (-0.8, 0)],
    "kite": [(0, -1.3), (0.8, 0.3), (0, 1.0), (-0.8, 0.3)],
    "parallelogram": [(-1.4, -0.8), (0.8, -0.8), (1.4, 0.8), (-0.8, 0.8)],
    "trapezoid": [(-1.3, -0.8), (1.3, -0.8), (0.7, 0.8), (-0.7, 0.8)],
    "arrow": [(-1.3, -0.35), (0.3, -0.35), (0.3, -0.9), (1.3, 0), (0.3, 0.9), (0.3, 0.35), (-1.3, 0.35)],
    "cross": [(-0.35, -1.1), (0.35, -1.1), (0.35, -0.35), (1.1, -0.35), (1.1, 0.35), (0.35, 0.35),
              (0.35, 1.1), (-0.35, 1.1), (-0.35, 0.35), (-1.1, 0.35), (-1.1, -0.35), (-0.35, -0.35)],
}


def make_symmetry(s) -> Path:
    fig, ax = _blank(2.4, 2.2, (-1.6, 1.6), (-1.45, 1.45))
    sides = {"equilateral": 3, "pentagon": 5, "hexagon": 6, "octagon": 8}
    pts = _regular(sides[s.name], 1.25) if s.name in sides else _SYM_SHAPES[s.name]
    if s.name == "equilateral":
        pts = [(x, y - 0.2) for x, y in pts]
    _poly(ax, pts)
    return _save(fig, s.asset_id)


def make_tangent(t) -> Path:
    fig, ax = _blank(3.4, 2.4, (-1.3, 3.3), (-1.55, 1.55))
    R = 1.0
    if t.kind in ("pt", "op"):
        r0, t0 = (t.a, math.isqrt(t.b ** 2 - t.a ** 2)) if t.kind == "pt" else (t.a, t.b)
        R = min(1.0, 2.9 * r0 / math.hypot(r0, t0))     # keep P on the canvas
    ax.add_patch(Circle((0, 0), R, facecolor="none", edgecolor=INK, lw=1.6))
    origin = (0.0, 0.0)
    _dot(ax, origin)
    _letter(ax, -0.14, -0.14, "O")
    if t.kind in ("pt", "op"):
        r, tl = (t.a, math.isqrt(t.b ** 2 - t.a ** 2)) if t.kind == "pt" else (t.a, t.b)
        d = math.hypot(r, tl) / r * R                 # OP in drawing units
        P = (d, 0.0)
        ang = math.acos(R / d)                        # ∠TOP
        T = (R * math.cos(ang), R * math.sin(ang))
        _line(ax, origin, T, lw=1.4)
        _line(ax, origin, P, lw=1.4)
        _line(ax, T, P)
        _dot(ax, P)
        _letter(ax, P[0] + 0.15, P[1] - 0.12, "P")
        _letter(ax, T[0] - 0.02, T[1] + 0.17, "T")
        u = ((origin[0] - T[0]) / R, (origin[1] - T[1]) / R)
        v = ((P[0] - T[0]) / math.hypot(P[0] - T[0], P[1] - T[1]), (P[1] - T[1]) / math.hypot(P[0] - T[0], P[1] - T[1]))
        _right_mark(ax, T, u, v, s=0.12)
        labels = {"OT": str(t.a), "OP": str(t.b) if t.kind == "pt" else "x",
                  "PT": "x" if t.kind == "pt" else str(t.b)}
        _tag(ax, T[0] / 2 - 0.15, T[1] / 2 + 0.05, labels["OT"])
        _tag(ax, d / 2, -0.17, labels["OP"])
        _tag(ax, (T[0] + P[0]) / 2 + 0.1, (T[1] + P[1]) / 2 + 0.13, labels["PT"])
    else:
        # Tangents from P touch at A (above) and B (below).
        apb = t.a if t.kind == "angle" else 50
        half = math.radians(90 - apb / 2)            # ∠AOP
        d = R / math.cos(half)
        P = (d, 0.0)
        A = (R * math.cos(half), R * math.sin(half))
        B = (A[0], -A[1])
        for q in (A, B):
            _line(ax, q, P)
        _dot(ax, P)
        _letter(ax, P[0] + 0.15, 0.0, "P")
        _letter(ax, A[0] - 0.05, A[1] + 0.17, "A")
        _letter(ax, B[0] - 0.05, B[1] - 0.17, "B")
        if t.kind == "two":
            _tag(ax, (A[0] + P[0]) / 2 + 0.12, (A[1] + P[1]) / 2 + 0.12, str(t.a))
            _tag(ax, (B[0] + P[0]) / 2 + 0.12, (B[1] + P[1]) / 2 - 0.12, "x")
        else:
            _line(ax, origin, A, lw=1.4)
            _line(ax, origin, B, lw=1.4)
            _mark_between(ax, P, A, B, str(t.a), r=0.35, lr=0.62)
            _mark_between(ax, origin, A, B, "x", r=0.2, lr=0.38)
    return _save(fig, t.asset_id)


def make_conic(g) -> Path:
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    L = 8
    ax.set_xlim(-L - 0.5, L + 0.5)
    ax.set_ylim(-L - 0.5, L + 0.5)
    ax.set_aspect("equal")
    ticks = list(range(-L, L + 1))
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels([str(v) if v % 2 == 0 and v else "" for v in ticks])
    ax.set_yticklabels([str(v) if v % 2 == 0 and v else "" for v in ticks])
    ax.grid(True, color=GRID, lw=0.5)
    ax.axhline(0, color=INK, lw=1.0)
    ax.axvline(0, color=INK, lw=1.0)
    ax.tick_params(labelsize=6, colors=INK, length=0)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ts = [i / 200 for i in range(-1200, 1201)]
    if g.kind == "par":
        p = g.a
        # y² = 4px through (p t², 2p t); swap for x² = 4py.
        xs = [p * t * t for t in ts]
        ys = [2 * p * t for t in ts]
        if g.vertical:
            xs, ys = ys, xs
        ax.plot(xs, ys, color=ACCENT, lw=2.0)
        # One labelled point on the curve pins p down: (p, 2|p|), or (2|p|, p).
        pt = (2 * abs(p), p) if g.vertical else (p, 2 * abs(p))
        ax.plot([pt[0]], [pt[1]], "o", color=INK, ms=4, zorder=5)
        ax.text(pt[0] + (0.4 if pt[0] >= 0 else -0.4), pt[1] + 0.6, f"({pt[0]}, {pt[1]})", fontsize=7,
                color=INK, ha="left" if pt[0] >= 0 else "right", va="bottom",
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5))
    elif g.kind == "ell":
        th = [2 * math.pi * i / 400 for i in range(401)]
        ax.plot([g.a * math.cos(t) for t in th], [g.b * math.sin(t) for t in th], color=ACCENT, lw=2.0)
    else:
        us = [i / 100 for i in range(-300, 301)]
        for sgn in (1, -1):
            xs = [sgn * g.a * math.cosh(u) for u in us]
            ys = [g.b * math.sinh(u) for u in us]
            if g.vertical:
                xs, ys = [g.b * math.sinh(u) for u in us], [sgn * g.a * math.cosh(u) for u in us]
            ax.plot(xs, ys, color=ACCENT, lw=2.0)
        # Asymptotes, dashed.
        k = g.b / g.a if not g.vertical else g.a / g.b
        for s in (1, -1):
            ax.plot([-L, L], [-s * k * L, s * k * L], color=INK, lw=0.8, ls="--")
    fig.tight_layout()
    return _save(fig, g.asset_id)


def make_right_triangle(r) -> Path:
    fig, ax = _blank(3.2, 2.6, (-0.5, 3.3), (-0.5, 2.7))
    k = 2.6 / max(r.adj, r.opp)
    A, C, B = (0.0, 0.0), (r.adj * k, 0.0), (r.adj * k, r.opp * k)
    _poly(ax, [A, C, B])
    _right_mark(ax, C, (-1, 0), (0, 1), s=0.14)
    _angle_mark(ax, A, 0, math.degrees(math.atan2(B[1], B[0])), "θ", r=0.35, lr=0.6)
    labels = {"o": (str(r.opp), (C[0] + 0.25, B[1] / 2)),
              "a": (str(r.adj), (C[0] / 2, -0.22)),
              "h": (str(r.hyp), (B[0] / 2 - 0.2, B[1] / 2 + 0.2))}
    for c in r.shown:
        lab, (x, y) = labels[c]
        _tag(ax, x, y, lab)
    return _save(fig, r.asset_id)


# ── all ──────────────────────────────────────────────────────────────────────

def make_math_diagrams() -> list[Path]:
    out = [make_shape_2d(s) for s in md.SHAPES_2D]
    out += [make_solid(s) for s in md.SOLIDS]
    out += [make_net(n) for n in md.NETS]
    out += [make_clock(c) for c in md.CLOCKS]
    out += [make_protractor(a) for a in md.PROTRACTOR_ANGLES]
    out += [make_angle_kind(a) for a in md.KIND_ANGLES]
    out += [make_fraction(f) for f in md.FRACTION_PICTURES]
    out += [make_figure(f) for f in (md.RECT_FIGURES + md.QUAD_FIGURES + md.TRIANGLE_FIGURES
                                     + md.L_FIGURES + md.RIGHT_TRIANGLE_FIGURES)]
    out += [make_bar_chart(b) for b in md.BAR_CHARTS]
    out += [make_line_graph(g) for g in md.LINE_GRAPHS]
    out += [make_number_line(s) for s in md.NUMBER_LINES]
    out += [make_line_fn(f) for f in md.LINE_FNS]
    out += [make_parabola(p) for p in md.PARABOLAS]
    out += [make_venn(v) for v in hi.VENNS]
    out += [make_sine(g) for g in hi.SINE_GRAPHS]
    out += [make_box(b) for b in hi.BOX_PLOTS]
    out += [make_scatter(sc) for sc in hi.SCATTERS]
    out += [make_normal(n) for n in hi.NORMALS]
    out += [make_line_ray(f) for f in geo.LINE_FIGURES]
    out += [make_parallel(p) for p in geo.PARALLEL_FIND + geo.PARALLEL_NAME + geo.PARALLEL_TWO]
    out += [make_marked_triangle(t) for t in geo.TRI_ANGLES + geo.TRI_SIDES]
    out += [make_pie(p) for p in geo.PIE_CHARTS]
    out += [make_transform(t) for t in geo.TRANSFORMS]
    out += [make_circle_angle(c) for c in geo.CIRCLE_ANGLES]
    out += [make_similar(s) for s in geo.SIMILAR_PAIRS]
    out += [make_symmetry(s) for s in geo.SYMMETRY_SHAPES]
    out += [make_tangent(t) for t in geo.TANGENTS]
    out += [make_conic(g) for g in geo.CONIC_GRAPHS]
    out += [make_right_triangle(r) for r in geo.RIGHT_TRIANGLES]
    return out


if __name__ == "__main__":
    paths = make_math_diagrams()
    print(f"wrote {len(paths)} math diagrams, {sum(p.stat().st_size for p in paths) // 1024} KB")
