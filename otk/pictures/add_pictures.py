"""Draw the pictures named by ``otk.sets._support.math_pictures_add``.

Drawn on demand by ``otk.pictures.registry``; every label is a number,
ASCII or a single letter.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch

from otk.sets._support import math_pictures_add as ma
from otk.sets.math.m6.relative_extrema import _LETTERS

from .math_diagrams import ACCENT, GRID, INK, SHADE, SOFT, _plane, _save

BLUE = "#1d4ed8"


def _curve(ax, f, x0, x1, lim=6.5, colour=ACCENT, steps=600):
    """Plot f on [x0, x1], broken wherever it leaves the window."""
    xs, ys = [], []
    for i in range(steps + 1):
        x = x0 + (x1 - x0) * i / steps
        y = f(x)
        if abs(y) <= lim:
            xs.append(x)
            ys.append(y)
        elif xs:
            ax.plot(xs, ys, color=colour, lw=2.0)
            xs, ys = [], []
    if xs:
        ax.plot(xs, ys, color=colour, lw=2.0)


def _dot(ax, x, y, filled=True, colour=ACCENT):
    ax.plot(x, y, "o", ms=6, color=colour, mfc=colour if filled else "white", mew=1.6, zorder=5)


# ── quadratic inequality ─────────────────────────────────────────────────────

def make_quad_ineq(s: ma.QuadIneq) -> Path:
    fig, ax = _plane()
    depth = ((s.r2 - s.r1) / 2) ** 2
    scale = min(1.0, 5.0 / depth)
    _curve(ax, lambda x: s.a * scale * (x - s.r1) * (x - s.r2), -6.5, 6.5)
    for r in (s.r1, s.r2):
        _dot(ax, r, 0)
    fig.tight_layout()
    return _save(fig, s.asset_id)


# ── |x| graph ────────────────────────────────────────────────────────────────

def make_abs(s: ma.AbsGraph) -> Path:
    fig, ax = _plane()
    _curve(ax, lambda x: s.a * abs(x - s.h) + s.k, -6.5, 6.5, steps=1300)
    _dot(ax, s.h, s.k)
    fig.tight_layout()
    return _save(fig, s.asset_id)


# ── circle ───────────────────────────────────────────────────────────────────

def make_circle(s: ma.CircleGrid) -> Path:
    fig, ax = _plane()
    ax.add_patch(Circle((s.h, s.k), s.r, fill=False, ec=ACCENT, lw=2.0))
    _dot(ax, s.h, s.k)
    fig.tight_layout()
    return _save(fig, s.asset_id)


# ── exponential / log ────────────────────────────────────────────────────────

def make_exp_log(s: ma.ExpLogGraph) -> Path:
    fig, ax = _plane()
    b = float(s.base)
    if s.kind == "exp":
        _curve(ax, lambda x: b ** x + s.k, -6.5, 6.5)
        ax.axhline(s.k, color=INK, lw=1.0, ls="--")
        pts = [(x, b ** x + s.k) for x in range(-6, 7)]
    else:
        _curve(ax, lambda x: math.log(x, b) + s.k, 0.004, 6.5, steps=2000)
        ax.axvline(0, color=INK, lw=1.0, ls="--")
        pts = [(x, math.log(x, b) + s.k) for x in (0.25, 1 / 3, 0.5, 1, 2, 3, 4)]
    for x, y in pts:                        # mark the points that sit on a grid height
        if abs(y) <= 6 and abs(y - round(y)) < 1e-9:
            _dot(ax, x, round(y))
    fig.tight_layout()
    return _save(fig, s.asset_id)


# ── vectors ──────────────────────────────────────────────────────────────────

def _vec(ax, x, y, label, colour):
    ax.add_patch(FancyArrowPatch((0, 0), (x, y), arrowstyle="-|>", mutation_scale=14,
                                 color=colour, lw=2.2, zorder=4))
    ax.text(x * 1.08 + (0.35 if x >= 0 else -0.35), y * 1.08 + (0.3 if y >= 0 else -0.3), label,
            fontsize=12, fontweight="bold", color=colour, ha="center", va="center", style="italic")


def make_vectors(s: ma.VectorGrid) -> Path:
    fig, ax = _plane()
    _vec(ax, s.ux, s.uy, "u", ACCENT)
    _vec(ax, s.vx, s.vy, "v", BLUE)
    fig.tight_layout()
    return _save(fig, s.asset_id)


# ── unit circle ──────────────────────────────────────────────────────────────

def make_unit(s: ma.UnitPoint) -> Path:
    fig, ax = plt.subplots(figsize=(3.2, 3.2))
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.annotate("", (1.4, 0), (-1.4, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1))
    ax.annotate("", (0, 1.4), (0, -1.4), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1))
    ax.text(1.38, -0.12, "x", fontsize=10, color=INK)
    ax.text(0.06, 1.36, "y", fontsize=10, color=INK)
    ax.add_patch(Circle((0, 0), 1, fill=False, ec=INK, lw=1.4))
    for x, y, lab in ((1, 0, "1"), (-1, 0, "-1"), (0, 1, "1"), (0, -1, "-1")):
        ax.text(x + (0.08 if x > 0 else -0.14 if x < 0 else 0.05), y + (0.07 if y > 0 else -0.14 if y < 0 else -0.12),
                lab, fontsize=8, color=INK)
    t = math.radians(s.deg)
    px, py = math.cos(t), math.sin(t)
    ax.plot([0, px], [0, py], color=ACCENT, lw=1.8)
    _dot(ax, px, py)
    ax.text(px * 1.16, py * 1.16, "P", fontsize=11, fontweight="bold", color=ACCENT, ha="center", va="center")
    ax.text(-0.1, -0.12, "O", fontsize=9, color=INK)
    # θ from the positive x-axis, unlabelled beyond its name.
    ax.add_patch(Arc((0, 0), 0.34, 0.34, theta1=0, theta2=s.deg, color=BLUE, lw=1.3))
    mid = math.radians(s.deg / 2)
    ax.text(0.27 * math.cos(mid), 0.27 * math.sin(mid), r"$\theta$", fontsize=11, color=BLUE,
            ha="center", va="center")
    # The reference angle, between OP and the nearer side of the x-axis, in degrees.
    side = 0 if s.deg < 90 or s.deg > 270 else 180
    a1, a2 = sorted((side if not (side == 0 and s.deg > 270) else 360, s.deg))
    ax.add_patch(Arc((0, 0), 0.9, 0.9, theta1=a1, theta2=a2, color=ACCENT, lw=1.3))
    mid = math.radians((a1 + a2) / 2)
    ax.text(0.66 * math.cos(mid), 0.66 * math.sin(mid), f"{s.ref}°", fontsize=10, color=ACCENT,
            ha="center", va="center")
    fig.tight_layout()
    return _save(fig, s.asset_id)


# ── cosine-rule triangle ─────────────────────────────────────────────────────

def make_cos_triangle(s: ma.CosTriangle) -> Path:
    cos_a = float(s.cos_a)
    sin_a = math.sqrt(max(0.0, 1 - cos_a * cos_a))
    A, B, C = (0.0, 0.0), (float(s.c), 0.0), (s.b * cos_a, s.b * sin_a)
    xs, ys = [A[0], B[0], C[0]], [A[1], B[1], C[1]]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    k = 3.4 / max(w, h * 1.3)
    fig, ax = plt.subplots(figsize=(3.8, max(1.9, h * k + 1.1)))
    ax.set_aspect("equal")
    ax.axis("off")
    pad = max(w, h) * 0.16
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)
    ax.fill(xs, ys, color=SOFT, zorder=1)
    ax.plot(xs + [A[0]], ys + [A[1]], color=INK, lw=1.8, zorder=2)
    cx, cy = sum(xs) / 3, sum(ys) / 3
    for (x, y), name in ((A, "A"), (B, "B"), (C, "C")):
        dx, dy = x - cx, y - cy
        n = math.hypot(dx, dy) or 1
        ax.text(x + dx / n * pad * 0.45, y + dy / n * pad * 0.45, name, fontsize=11, fontweight="bold",
                color=INK, ha="center", va="center")

    def side(p, q, label):
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        dx, dy = mx - cx, my - cy
        n = math.hypot(dx, dy) or 1
        ax.text(mx + dx / n * pad * 0.5, my + dy / n * pad * 0.5, label, fontsize=11, color=INK,
                ha="center", va="center", style="italic" if label == "x" else "normal")

    side(B, C, "x" if s.hide else str(s.a))
    side(A, C, str(s.b))
    side(A, B, str(s.c))
    angle = math.degrees(math.atan2(C[1], C[0]))
    r = min(s.b, s.c) * 0.28
    ax.add_patch(Arc(A, 2 * r, 2 * r, theta1=0, theta2=angle, color=ACCENT, lw=1.5, zorder=3))
    mid = math.radians(angle / 2)
    label = f"{round(math.degrees(math.acos(cos_a)))}°" if s.hide else r"$\theta$"
    ax.text(r * 1.55 * math.cos(mid), r * 1.55 * math.sin(mid), label, fontsize=10, color=ACCENT,
            ha="center", va="center")
    return _save(fig, s.asset_id)


# ── limits ───────────────────────────────────────────────────────────────────

def make_limit(s: ma.LimitGraph) -> Path:
    fig, ax = _plane()
    _curve(ax, lambda x: s.left + s.ml * (x - s.c), -6.5, s.c - 1e-6, colour=BLUE)
    _curve(ax, lambda x: s.right + s.mr * (x - s.c), s.c + 1e-6, 6.5, colour=BLUE)
    _dot(ax, s.c, s.left, filled=s.at == s.left, colour=BLUE)
    if s.right != s.left:
        _dot(ax, s.c, s.right, filled=s.at == s.right, colour=BLUE)
    if s.at not in (s.left, s.right):
        _dot(ax, s.c, s.at, colour=BLUE)
    ax.plot([s.c, s.c], [0, max(s.left, s.right, s.at)] if max(s.left, s.right, s.at) > 0
            else [0, min(s.left, s.right, s.at)], color=INK, lw=0.8, ls=":")
    fig.tight_layout()
    return _save(fig, s.asset_id)


# ── where f' changes sign ────────────────────────────────────────────────────

def make_deriv(c: ma.DerivCurve) -> Path:
    def f(x):
        return c.s * (x ** 3 / 3 - (c.p + c.q) / 2 * x ** 2 + c.p * c.q * x)

    x0, x1 = min(c.xs) - 0.9, max(c.xs) + 0.9
    xs = [x0 + (x1 - x0) * i / 400 for i in range(401)]
    ys = [f(x) for x in xs]
    lo, hi = min(ys), max(ys)
    fig, ax = plt.subplots(figsize=(3.8, 2.8))
    ax.plot(xs, ys, color=ACCENT, lw=2.0)
    ax.set_xlim(x0, x1)
    ax.set_ylim(lo - (hi - lo) * 0.12, hi + (hi - lo) * 0.16)
    ax.set_xticks(range(math.ceil(x0), math.floor(x1) + 1))
    ax.set_yticks([])
    ax.grid(True, axis="x", color=GRID, lw=0.6)
    ax.tick_params(labelsize=7, colors=INK, length=0)
    for sd in ("top", "right", "left"):
        ax.spines[sd].set_visible(False)
    ax.spines["bottom"].set_color(INK)
    for letter, x in zip(_LETTERS, c.xs):
        y = f(x)
        _dot(ax, x, y)
        ax.text(x, y + (hi - lo) * 0.08, letter, fontsize=11, fontweight="bold", color=INK,
                ha="center", va="bottom")
    ax.text(x1, ax.get_ylim()[0], "x", fontsize=9, color=INK, ha="right", va="bottom")
    fig.tight_layout()
    return _save(fig, c.asset_id)


# ── area between curves ──────────────────────────────────────────────────────

def make_area(r: ma.AreaRegion) -> Path:
    n = r.n
    top, bottom = {
        "cap": (lambda x: n - x * x, lambda x: 0.0),
        "line": (lambda x: n * x, lambda x: x * x),
        "level": (lambda x: float(n), lambda x: x * x),
        "lens": (lambda x: 2 * n - x * x, lambda x: x * x),
    }[r.kind]
    lo, hi = r.bounds
    span = hi - lo
    x0, x1 = lo - max(1.0, span * 0.35), hi + max(1.0, span * 0.35)
    xs = [x0 + (x1 - x0) * i / 400 for i in range(401)]
    ymax = max(max(top(x) for x in (lo, hi, (lo + hi) / 2)), r.box / span) * 1.25
    ymin = -ymax * 0.18
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    inner = [lo + span * i / 200 for i in range(201)]
    ax.fill_between(inner, [bottom(x) for x in inner], [top(x) for x in inner], color=SHADE, alpha=0.35, lw=0)
    for g in (top, bottom):
        pts = [(x, g(x)) for x in xs if ymin <= g(x) <= ymax]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=ACCENT, lw=1.8)
    ax.set_xlim(x0, x1)
    ax.set_ylim(ymin, ymax)
    ax.grid(True, color=GRID, lw=0.6)
    ax.tick_params(labelsize=7, colors=INK, length=0)
    for sd in ("top", "right"):
        ax.spines[sd].set_visible(False)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    fig.tight_layout()
    return _save(fig, r.asset_id)
