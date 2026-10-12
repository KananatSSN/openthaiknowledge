"""Draw the figures named by ``otk.sets._support.math_formats``.

Run::

    python -m otk.pictures.format_pictures   # optional: pre-draws into the diagram cache

A quadrilateral is identified the way the ป.5 book marks it: ticks on equal
sides, a square on right angles, arrowheads on parallel sides. The shape is
turned in two of its three pictures so it is not recognised by orientation.
"""

from __future__ import annotations

import math
from pathlib import Path

from matplotlib.patches import Arc, Circle, FancyBboxPatch

from otk.sets.math.p5 import types_of_quadrilaterals as mf
from otk.sets.math.m1 import prime_factorisation as mh
from otk.sets.math.m2.congruence import CONGRUENT_PAIRS, CongruentPair
from otk.sets.math.m3.trigonometric_ratios import SPECIAL_TRIANGLES, SpecialTriangle

from .math_diagrams import INK, SOFT, _blank, _poly, _right_mark, _save


def _unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def _ticks(ax, p, q, count, size=0.07):
    ux, uy = _unit(p, q)
    nx, ny = -uy, ux
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    for k in range(count):
        off = (k - (count - 1) / 2) * 0.06 - 0.1          # left of centre
        cx, cy = mx + ux * off, my + uy * off
        ax.plot([cx - nx * size, cx + nx * size], [cy - ny * size, cy + ny * size],
                color=INK, lw=1.4)


def _chevrons(ax, p, q, count, point_back: bool, size=0.07):
    ux, uy = _unit(p, q)
    nx, ny = -uy, ux
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    sx, sy = (-ux, -uy) if point_back else (ux, uy)
    for k in range(count):
        off = (k - (count - 1) / 2) * 0.08 + 0.14        # right of centre, clear of ticks
        tx, ty = mx + ux * off, my + uy * off
        bx, by = tx - sx * size, ty - sy * size
        ax.plot([bx + nx * size, tx, bx - nx * size], [by + ny * size, ty, by - ny * size],
                color=INK, lw=1.4)


def make_quad(p: mf.QuadPicture) -> Path:
    q = p.quad
    c, s = math.cos(math.radians(p.turn)), math.sin(math.radians(p.turn))
    pts = [(x * c - y * s, x * s + y * c) for x, y in q.pts]
    xs, ys = [x for x, _ in pts], [y for _, y in pts]
    pad = 0.3
    xlim = (min(xs) - pad, max(xs) + pad)
    ylim = (min(ys) - pad, max(ys) + pad)
    w, h = xlim[1] - xlim[0], ylim[1] - ylim[0]
    k = 2.6 / max(w, h)
    fig, ax = _blank(w * k, h * k, xlim, ylim)
    _poly(ax, pts, fill=SOFT)
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        if q.ticks[i]:
            _ticks(ax, a, b, q.ticks[i])
        if q.parallel[i]:
            # Sides 2 and 3 run back against 0 and 1, so their arrows turn round
            # to point the same way as their partner's.
            _chevrons(ax, a, b, q.parallel[i], point_back=i >= 2)
    for i in q.right:
        corner, nxt, prv = pts[i], pts[(i + 1) % 4], pts[(i - 1) % 4]
        _right_mark(ax, corner, _unit(corner, nxt), _unit(corner, prv), s=0.1)
    return _save(fig, p.asset_id)


# ── ม.1 factor trees ──────────────────────────────────────────────────────────

def make_factor_tree(t: mh.FactorTree) -> Path:
    tree = t.tree
    nodes = mh._nodes(tree)
    pos: dict[int, tuple[float, float]] = {}
    next_leaf = [0.0]

    def place(node, depth):
        if not node.children:
            x = next_leaf[0]
            next_leaf[0] += 1.0
        else:
            xs = [place(c, depth + 1) for c in node.children]
            x = sum(xs) / len(xs)
        pos[id(node)] = (x, -depth * 1.0)
        return x

    place(tree, 0)
    depth = -min(y for _, y in pos.values())
    width = next_leaf[0] - 1
    fig, ax = _blank((width + 1.2) * 0.75, (depth + 1.0) * 0.75,
                     (-0.6, width + 0.6), (-depth - 0.5, 0.5))

    def draw(node):
        x, y = pos[id(node)]
        for c in node.children:
            cx, cy = pos[id(c)]
            ax.plot([x, cx], [y - 0.2, cy + 0.2], color=INK, lw=1.2)
            draw(c)

    draw(tree)
    for i, node in enumerate(nodes):
        x, y = pos[id(node)]
        label = "?" if i == t.hidden and t.hidden else str(node.value)
        if node.children:
            ax.add_patch(FancyBboxPatch((x - 0.3, y - 0.19), 0.6, 0.38,
                                        boxstyle="round,pad=0,rounding_size=0.08",
                                        fc="white", ec=INK, lw=1.0))
        else:
            ax.add_patch(Circle((x, y), 0.24, fc="#fff3c4", ec=INK, lw=1.2))
        ax.text(x, y, label, ha="center", va="center", fontsize=12,
                fontweight="bold", color="#c0392b" if label == "?" else INK)
    return _save(fig, t.asset_id)


# ── ม.2 congruent triangles ──────────────────────────────────────────────────

_TRI = {"scalene": ((0.0, 0.0), (2.2, 0.0), (0.75, 1.3)),
        "right": ((0.0, 0.0), (2.0, 0.0), (0.0, 1.3))}
# (side ticks by side AB, BC, CA), (angle arcs at A, B, C), right angle at A
_CASE_MARKS = {
    "sss": ((1, 2, 3), (0, 0, 0), False),
    "sas": ((1, 0, 2), (1, 0, 0), False),
    "asa": ((1, 0, 0), (1, 2, 0), False),
    "aas": ((0, 1, 0), (1, 2, 0), False),
    "rhs": ((2, 1, 0), (0, 0, 0), True),
    "aaa": ((0, 0, 0), (1, 2, 3), False),
}


def _arcs(ax, v, p, q, count):
    a1 = math.degrees(math.atan2(p[1] - v[1], p[0] - v[0]))
    a2 = math.degrees(math.atan2(q[1] - v[1], q[0] - v[0]))
    lo, hi = sorted((a1, a2))
    if hi - lo > 180:
        lo, hi = hi, lo + 360
    for k in range(count):
        r = 0.22 + 0.07 * k
        ax.add_patch(Arc(v, 2 * r, 2 * r, theta1=lo, theta2=hi, color=INK, lw=1.2))


def _triangle(ax, pts, marks):
    ticks, arcs, right = marks
    _poly(ax, list(pts), fill=SOFT)
    for i in range(3):
        if ticks[i]:
            _ticks(ax, pts[i], pts[(i + 1) % 3], ticks[i])
        if arcs[i]:
            _arcs(ax, pts[i], pts[(i + 1) % 3], pts[(i - 1) % 3], arcs[i])
    if right:
        a, b, c = pts
        _right_mark(ax, a, _unit(a, b), _unit(a, c), s=0.14)


def make_congruent(p: CongruentPair) -> Path:
    marks = _CASE_MARKS[p.case]
    base = _TRI["right" if p.case == "rhs" else "scalene"]
    first = [(x, y) for x, y in base]
    scale = 0.7 if p.case == "aaa" else 1.0
    turn = (180.0, 200.0)[p.variant] if p.variant else 0.0
    second = []
    for x, y in base:
        x, y = x * scale, y * scale
        if p.variant == 0:
            x = -x                                   # a mirror image
        else:
            c, s = math.cos(math.radians(turn)), math.sin(math.radians(turn))
            x, y = x * c - y * s, x * s + y * c      # turned round
        second.append((x, y))
    sx0, sy0 = min(x for x, _ in second), min(y for _, y in second)
    second = [(x - sx0 + 3.0, y - sy0) for x, y in second]
    xs = [x for x, _ in first + second]
    ys = [y for _, y in first + second]
    xlim, ylim = (min(xs) - 0.3, max(xs) + 0.3), (min(ys) - 0.3, max(ys) + 0.3)
    fig, ax = _blank((xlim[1] - xlim[0]) * 0.85, (ylim[1] - ylim[0]) * 0.85, xlim, ylim)
    _triangle(ax, first, marks)
    _triangle(ax, second, marks)
    return _save(fig, p.asset_id)


# ── ม.3 special-angle right triangles ────────────────────────────────────────

def make_special_triangle(t: SpecialTriangle) -> Path:
    # θ at A, the right angle at C: AC is adjacent, CB opposite, AB the hypotenuse.
    L = 2.4 if t.angle <= 45 else 1.4
    h = L * math.tan(math.radians(t.angle))
    A, C, B = (0.0, 0.0), (L, 0.0), (L, h)
    xlim, ylim = (-0.45, L + 0.55), (-0.45, h + 0.3)
    fig, ax = _blank((xlim[1] - xlim[0]) * 0.9, (ylim[1] - ylim[0]) * 0.9, xlim, ylim)
    _poly(ax, [A, C, B], fill=SOFT)
    _right_mark(ax, C, (-1, 0), (0, 1), s=0.16)
    ax.add_patch(Arc(A, 0.7, 0.7, theta1=0, theta2=t.angle, color=INK, lw=1.2))
    mid = math.radians(t.angle / 2)
    ax.text(0.55 * math.cos(mid) + 0.08, 0.55 * math.sin(mid), f"{t.angle}°",
            ha="left", va="center", fontsize=11, color=INK)
    where = {"adj": ((L / 2, -0.22), "center"), "opp": ((L + 0.18, h / 2), "left"),
             "hyp": ((L / 2 - 0.2, h / 2 + 0.2), "right")}
    for side, label in ((t.given, str(t.value)), (t.asked, "x")):
        (x, y), ha = where[side]
        ax.text(x, y, label, ha=ha, va="center", fontsize=13, fontweight="bold",
                color="#c0392b" if label == "x" else INK)
    return _save(fig, t.asset_id)


def make_format_pictures() -> list[Path]:
    out = [make_quad(p) for p in mf.QUAD_PICTURES]
    out += [make_factor_tree(t) for t in mh.FACTOR_TREES]
    out += [make_congruent(p) for p in CONGRUENT_PAIRS]
    out += [make_special_triangle(t) for t in SPECIAL_TRIANGLES]
    return out


if __name__ == "__main__":
    paths = make_format_pictures()
    print(f"wrote {len(paths)} figures, {sum(p.stat().st_size for p in paths) // 1024} KB")
