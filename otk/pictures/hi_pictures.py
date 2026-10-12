"""Draw the pictures named by ``otk.sets._support.math_pictures_hi``.

Run::

    python -m otk.pictures.hi_pictures   # optional: pre-draws into the diagram cache
"""

from __future__ import annotations

from pathlib import Path

from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

from otk.sets._support import math_pictures_hi as mh

from .counting_pictures import INK, _save
from .measure_pictures import _axes

BLUE, ORANGE = "#42a5f5", "#ffa726"


# ── area model ───────────────────────────────────────────────────────────────

def make_area_model(m: mh.AreaModel) -> Path:
    tens, ones = m.a // 10 * 10, m.a % 10
    u = 0.09                                     # one unit of length
    W1, W2, H = tens * u, max(ones * u, 0.45), m.b * u * 2.2
    fig, ax = _axes(W1 + W2 + 1.1, H + 0.9, (-0.6, W1 + W2 + 0.5), (-0.2, H + 0.7), scale=0.95)
    ax.add_patch(Rectangle((0, 0), W1, H, fc="#bbdefb", ec=INK, lw=1.5))
    ax.add_patch(Rectangle((W1, 0), W2, H, fc="#ffe0b2", ec=INK, lw=1.5))
    ax.text(W1 / 2, H + 0.3, str(tens), ha="center", va="center", fontsize=13, fontweight="bold", color=INK)
    ax.text(W1 + W2 / 2, H + 0.3, str(ones), ha="center", va="center", fontsize=13, fontweight="bold",
            color=INK)
    ax.text(-0.3, H / 2, str(m.b), ha="center", va="center", fontsize=13, fontweight="bold", color=INK)
    return _save(fig, m.asset_id)


# ── balance ──────────────────────────────────────────────────────────────────

def _pan_items(ax, cx, base, boxes, weights):
    """Boxes then weights, six to a row, standing on the pan at ``base``."""
    items = ["x"] * boxes + ["1"] * weights
    for r in range(0, len(items), 6):
        row = items[r:r + 6]
        width = sum(0.5 if it == "x" else 0.34 for it in row)
        x = cx - width / 2
        y = base + (r // 6) * 0.5
        for it in row:
            if it == "x":
                ax.add_patch(Rectangle((x + 0.03, y), 0.44, 0.44, fc="#ffcc80", ec=INK, lw=1.1))
                ax.text(x + 0.25, y + 0.22, "x", ha="center", va="center", fontsize=12,
                        fontweight="bold", color=INK, style="italic")
                x += 0.5
            else:
                ax.add_patch(Circle((x + 0.17, y + 0.15), 0.15, fc="#90a4ae", ec=INK, lw=1.0))
                x += 0.34


def make_balance(b: mh.Balance) -> Path:
    fig, ax = _axes(7.4, 3.0, (-3.7, 3.7), (-1.5, 1.5), scale=0.8)
    ax.add_patch(Polygon([(-0.4, -1.45), (0.4, -1.45), (0, -0.45)], fc="#78909c", ec=INK, lw=1.2))
    ax.plot([-2.6, 2.6], [-0.45, -0.45], color=INK, lw=3.5)   # level: the two sides balance
    for cx, boxes, weights in ((-2.0, b.a, b.b), (2.0, b.c, b.d)):
        ax.plot([cx, cx], [-0.45, -0.2], color=INK, lw=2)
        ax.add_patch(FancyBboxPatch((cx - 1.6, -0.22), 3.2, 0.12,
                                    boxstyle="round,pad=0,rounding_size=0.05",
                                    fc="#cfd8dc", ec=INK, lw=1.2))
        _pan_items(ax, cx, -0.08, boxes, weights)
    return _save(fig, b.asset_id)


# ── fraction number line ─────────────────────────────────────────────────────

def make_frac_line(f: mh.FracLine) -> Path:
    fig, ax = _axes(7.0, 1.5, (-2.35, 2.35), (-0.55, 0.55), scale=0.95)
    ax.annotate("", xy=(2.3, 0), xytext=(-2.3, 0),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.5, mutation_scale=12))
    for k in range(-2 * f.d, 2 * f.d + 1):
        x = k / f.d
        whole = k % f.d == 0
        ax.plot([x, x], [-0.12 if whole else -0.07, 0.12 if whole else 0.07], color=INK,
                lw=1.4 if whole else 0.9)
        if whole:
            ax.text(x, -0.3, str(k // f.d), ha="center", va="center", fontsize=12, color=INK)
    x = f.k / f.d
    ax.add_patch(Circle((x, 0), 0.06, fc="#c0392b", ec=INK, lw=0.8, zorder=5))
    ax.text(x, 0.3, "A", ha="center", va="center", fontsize=13, fontweight="bold", color="#c0392b")
    return _save(fig, f.asset_id)


# ── charts ───────────────────────────────────────────────────────────────────

def _value_axis(ax, top, step, x0, x1):
    for v in range(0, top + 1, step):
        ax.plot([x0, x1], [v, v], color="#e2e8f0", lw=0.7, zorder=0)
        ax.text(x0 - 0.15, v, str(v), ha="right", va="center", fontsize=9, color=INK)
    ax.plot([x0, x0], [0, top], color=INK, lw=1.2)
    ax.plot([x0, x1], [0, 0], color=INK, lw=1.2)


def make_double_bars(c: mh.DoubleBars) -> Path:
    import matplotlib.pyplot as plt
    n = len(c.first)
    top = max(max(c.first), max(c.second)) + 5
    fig = plt.figure(figsize=(1.0 + 1.1 * n, 2.8))
    ax = fig.add_axes([0.1, 0.12, 0.88, 0.84])
    ax.set_xlim(-0.8, n)
    ax.set_ylim(-4, top + 1)
    ax.axis("off")
    _value_axis(ax, top, 5 if top <= 30 else 10, -0.5, n - 0.1)
    for i, (a, b) in enumerate(zip(c.first, c.second)):
        ax.add_patch(Rectangle((i - 0.3, 0), 0.3, a, fc=BLUE, ec=INK, lw=0.9))
        ax.add_patch(Rectangle((i, 0), 0.3, b, fc=ORANGE, ec=INK, lw=0.9))
        ax.text(i, -2.2, "ABCDE"[i], ha="center", va="center", fontsize=11, fontweight="bold",
                color=INK)
    return _save(fig, c.asset_id)


def make_dot_plot(p: mh.DotPlot) -> Path:
    n = len(p.counts)
    tall = max(p.counts)
    fig, ax = _axes(n * 0.55 + 0.6, tall * 0.4 + 0.9, (-0.6, n - 0.4), (-0.7, tall * 0.62 + 0.3),
                    scale=0.95)
    ax.plot([-0.5, n - 0.5], [0, 0], color=INK, lw=1.4)
    for i, cnt in enumerate(p.counts):
        ax.plot([i, i], [-0.08, 0.08], color=INK, lw=1.2)
        ax.text(i, -0.4, str(p.start + i), ha="center", va="center", fontsize=11, color=INK)
        for j in range(cnt):
            ax.add_patch(Circle((i, 0.4 + j * 0.62), 0.22, fc=BLUE, ec=INK, lw=0.9))
    return _save(fig, p.asset_id)


def make_histogram(h: mh.Histogram) -> Path:
    import matplotlib.pyplot as plt
    n = len(h.freq)
    top = max(h.freq) + 2
    fig = plt.figure(figsize=(1.2 + 0.8 * n, 2.9))
    ax = fig.add_axes([0.1, 0.14, 0.88, 0.84])
    ax.set_xlim(-0.7, n + 0.3)
    ax.set_ylim(-top * 0.13, top + 0.5)
    ax.axis("off")
    _value_axis(ax, top, 2, -0.3, n + 0.1)
    for i, f in enumerate(h.freq):
        ax.add_patch(Rectangle((i, 0), 1, f, fc=BLUE, ec=INK, lw=1.0))
    # Class boundaries under the bar edges: 20, 30, …
    for i in range(n + 1):
        ax.text(i, -top * 0.07, str(h.low + i * h.width), ha="center", va="center",
                fontsize=9, color=INK)
    return _save(fig, h.asset_id)


def make_hi_pictures() -> list[Path]:
    out = [make_area_model(m) for m in mh.AREA_MODELS]
    out += [make_balance(b) for b in mh.BALANCES]
    out += [make_frac_line(f) for f in mh.FRAC_LINES]
    out += [make_double_bars(c) for c in mh.DOUBLE_BARS]
    out += [make_dot_plot(p) for p in mh.DOT_PLOTS]
    out += [make_histogram(h) for h in mh.HISTOGRAMS]
    return out


if __name__ == "__main__":
    paths = make_hi_pictures()
    print(f"wrote {len(paths)} pictures, {sum(p.stat().st_size for p in paths) // 1024} KB")
