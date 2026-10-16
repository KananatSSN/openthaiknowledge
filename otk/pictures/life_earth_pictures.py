"""Biology and Earth-science diagrams: Earth's interior, food webs, plant and animal cells.

Drawn on demand like the other pictures; the specs are in
``otk.sets._support.life_earth_diagrams``. Only digits and Latin letters are
drawn, so nothing depends on a Thai font.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Wedge

from .generate import _save

INK = "#333333"
CRUST = "#9a8f7a"
MANTLE = "#c96a3b"
CORE = "#f2b134"
WALL_C = "#6b8e23"
CYTO = "#eef6e4"
ANIMAL_CYTO = "#fbeee6"
NUCLEUS_C = "#9b7fc4"
CHLORO = "#4caf50"
VACUOLE_C = "#cfe6f5"


def _label(ax, number: int, tip: tuple[float, float], at: tuple[float, float]) -> None:
    """A leader line from the part to its number in a white circle."""
    ax.plot([tip[0], at[0]], [tip[1], at[1]], color=INK, lw=1.0, zorder=8)
    ax.add_patch(Circle(tip, 0.008, color=INK, zorder=9))
    ax.text(at[0], at[1], str(number), fontsize=12, ha="center", va="center",
            color=INK, zorder=10, fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.25", facecolor="white", edgecolor=INK, lw=1.0))


def make_earth_section(spec) -> Path:
    """A half Earth cut open: crust (thickened to be seen), mantle and core, numbered."""
    fig, ax = plt.subplots(figsize=(5.0, 3.0))
    ax.set_xlim(-1.15, 1.75)
    ax.set_ylim(-0.08, 1.12)
    ax.set_aspect("equal")
    ax.axis("off")
    centre = (0.0, 0.0)
    ax.add_patch(Wedge(centre, 1.00, 0, 180, facecolor=CRUST, edgecolor=INK, lw=1.2))
    ax.add_patch(Wedge(centre, 0.93, 0, 180, facecolor=MANTLE, edgecolor=INK, lw=1.0))
    ax.add_patch(Wedge(centre, 0.50, 0, 180, facecolor=CORE, edgecolor=INK, lw=1.0))
    ax.plot([-1.0, 1.0], [0, 0], color=INK, lw=1.2)
    # Each layer's leader starts inside it and ends level with it, outermost
    # highest, so no two lines cross whatever numbers they carry.
    tips = ((math.cos(math.radians(62)) * 0.965, math.sin(math.radians(62)) * 0.965),
            (math.cos(math.radians(32)) * 0.72, math.sin(math.radians(32)) * 0.72),
            (0.20, 0.18))
    spots = ((1.40, 0.95), (1.40, 0.55), (1.40, 0.18))
    for layer_index, number in enumerate(spec.numbers):
        _label(ax, number, tips[layer_index], spots[layer_index])
    return _save(fig, spec.asset_id, dpi=96)


def make_food_web(spec) -> Path:
    """Organisms as lettered circles; arrows from what is eaten to what eats it."""
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.axis("off")
    radius = 0.055
    where = {o.letter: (o.x, o.y) for o in spec.organisms}
    for eater in spec.organisms:
        for food in eater.eats:
            x0, y0 = where[food]
            x1, y1 = where[eater.letter]
            length = math.hypot(x1 - x0, y1 - y0)
            ux, uy = (x1 - x0) / length, (y1 - y0) / length
            ax.annotate("", xy=(x1 - ux * radius * 1.15, y1 - uy * radius * 1.15),
                        xytext=(x0 + ux * radius * 1.15, y0 + uy * radius * 1.15),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.25,head_length=0.5",
                                        color=INK, lw=1.4), zorder=2)
    for organism in spec.organisms:
        colour = "#d8efcf" if not organism.eats else "#ffffff"
        ax.add_patch(Circle((organism.x, organism.y), radius, facecolor=colour,
                            edgecolor=INK, lw=1.4, zorder=3))
        ax.text(organism.x, organism.y, organism.letter, fontsize=15, ha="center",
                va="center", color=INK, fontweight="bold", zorder=4)
    return _save(fig, spec.asset_id, dpi=96)


def make_cell(spec) -> Path:
    """A plant cell (box with wall, chloroplasts, large vacuole) or a rounded animal cell."""
    from otk.sets._support.life_earth_diagrams import (
        CHLOROPLAST, CYTOPLASM, MEMBRANE, NUCLEUS, VACUOLE, WALL,
    )

    fig, ax = plt.subplots(figsize=(5.4, 3.5))
    ax.set_xlim(-0.25, 1.33)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    # (where the leader starts on the part, where its number sits). The nucleus
    # is labelled on the left and the rest on the right, top to bottom, so no
    # two leaders cross whichever numbers the spec gives them.
    if spec.kind == "plant":
        ax.add_patch(FancyBboxPatch((0.10, 0.10), 0.80, 0.80,
                                    boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor=WALL_C, edgecolor=INK, lw=1.4, zorder=1))
        ax.add_patch(FancyBboxPatch((0.135, 0.135), 0.73, 0.73,
                                    boxstyle="round,pad=0,rounding_size=0.03",
                                    facecolor=CYTO, edgecolor=INK, lw=1.0, zorder=2))
        ax.add_patch(FancyBboxPatch((0.30, 0.30), 0.42, 0.42,
                                    boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=VACUOLE_C, edgecolor=INK, lw=1.0, zorder=3))
        ax.add_patch(Circle((0.22, 0.74), 0.065, facecolor=NUCLEUS_C, edgecolor=INK, lw=1.0, zorder=4))
        for cx, cy, angle in ((0.20, 0.25, 30), (0.80, 0.22, -20), (0.79, 0.76, 15), (0.52, 0.80, 0)):
            ax.add_patch(Ellipse((cx, cy), 0.09, 0.045, angle=angle, facecolor=CHLORO,
                                 edgecolor=INK, lw=0.8, zorder=4))
        places = {WALL: ((0.65, 0.883), (1.20, 0.94)),
                  CHLOROPLAST: ((0.79, 0.76), (1.20, 0.76)),
                  MEMBRANE: ((0.865, 0.60), (1.20, 0.60)),
                  VACUOLE: ((0.66, 0.46), (1.20, 0.44)),
                  CYTOPLASM: ((0.80, 0.34), (1.20, 0.28)),
                  NUCLEUS: ((0.22, 0.74), (-0.12, 0.74))}
    else:
        ax.add_patch(Ellipse((0.50, 0.50), 0.80, 0.70, facecolor=ANIMAL_CYTO,
                             edgecolor=INK, lw=1.6, zorder=1))
        ax.add_patch(Circle((0.45, 0.52), 0.11, facecolor=NUCLEUS_C, edgecolor=INK, lw=1.0, zorder=3))
        places = {MEMBRANE: ((0.856, 0.659), (1.20, 0.78)),
                  CYTOPLASM: ((0.68, 0.36), (1.20, 0.30)),
                  NUCLEUS: ((0.45, 0.52), (-0.12, 0.52))}
    for i, part in enumerate(spec.labelled):
        tip, spot = places[part]
        _label(ax, i + 1, tip, spot)
    return _save(fig, spec.asset_id, dpi=96)


SOIL_FILLS = (("#5b4636", None), ("#7a5a3a", "."), ("#a9774a", None), ("#c2a27a", "o"), ("#8c8c8c", "x"))


def make_soil_profile(spec) -> Path:
    """Five horizons stacked from the surface down, each with its own fill and number."""
    fig, ax = plt.subplots(figsize=(4.2, 4.0))
    ax.set_xlim(0, 1.2)
    ax.set_ylim(0, 1.05)
    ax.axis("off")
    # (top, bottom) of each horizon; the thin litter layer on top, bedrock at the foot.
    bands = ((0.95, 0.88), (0.88, 0.68), (0.68, 0.46), (0.46, 0.22), (0.22, 0.04))
    for (top, bottom), (colour, hatch), number in zip(bands, SOIL_FILLS, spec.numbers):
        ax.add_patch(plt.Rectangle((0.08, bottom), 0.72, top - bottom, facecolor=colour,
                                   edgecolor=INK, lw=1.0, hatch=hatch, zorder=1))
        _label(ax, number, (0.70, (top + bottom) / 2), (1.02, (top + bottom) / 2))
    # Grass on the surface, so the top is unmistakably the top.
    for x in [0.10 + 0.05 * i for i in range(14)]:
        ax.plot([x, x - 0.012, x + 0.012], [0.95, 1.0, 0.95], color="#3f7f2f", lw=1.2, zorder=2)
    return _save(fig, spec.asset_id, dpi=96)


def _curved_arrow(ax, start, end, rad, number, at):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.6", color="#2a5d9f",
                                lw=2.0, connectionstyle=f"arc3,rad={rad}"), zorder=5)
    ax.text(at[0], at[1], str(number), fontsize=12, ha="center", va="center", color=INK,
            fontweight="bold", zorder=10,
            bbox=dict(boxstyle="circle,pad=0.25", facecolor="white", edgecolor=INK, lw=1.0))


def make_water_cycle(spec) -> Path:
    """Sea on the left, a hill on the right, a cloud between; numbered arrows for the four steps."""
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.set_xlim(0, 1.45)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 0.62, 0.18, facecolor="#7fb3e0", edgecolor=INK, lw=1.0))
    ax.add_patch(plt.Polygon([(0.55, 0.0), (1.10, 0.62), (1.45, 0.0)], facecolor="#8fbf6a",
                             edgecolor=INK, lw=1.0))
    ax.add_patch(plt.Rectangle((0.55, 0.0), 0.90, 0.04, facecolor="#8fbf6a", edgecolor="none"))
    ax.add_patch(Circle((0.12, 0.86), 0.07, facecolor="#f6c945", edgecolor=INK, lw=1.0))
    for cx, cy, r in ((0.62, 0.80, 0.08), (0.72, 0.84, 0.10), (0.83, 0.80, 0.08), (0.72, 0.76, 0.07)):
        ax.add_patch(Circle((cx, cy), r, facecolor="#e6e9ee", edgecolor=INK, lw=0.8))
    # Evaporation up from the sea, condensation into the cloud, rain onto the hill,
    # and run-off down the hill back to the sea; numbered in step order by the spec.
    arrows = (((0.30, 0.20), (0.40, 0.62), 0.0, (0.28, 0.42)),
              ((0.45, 0.66), (0.58, 0.80), -0.3, (0.44, 0.80)),
              ((0.98, 0.72), (1.05, 0.55), 0.0, (1.12, 0.70)),
              ((0.92, 0.36), (0.58, 0.14), 0.0, (0.80, 0.16)))
    for (start, end, rad, at), number in zip(arrows, spec.numbers):
        _curved_arrow(ax, start, end, rad, number, at)
    for x in (0.96, 1.01, 1.06):
        ax.plot([x, x - 0.02], [0.70, 0.62], color="#2a5d9f", lw=1.0)
    return _save(fig, spec.asset_id, dpi=96)


def make_flower(spec) -> Path:
    """A flower cut lengthways: sepals, petals, stamens either side, a pistil with ovules."""
    from otk.sets._support.life_earth_diagrams import FLOWER_PART_NAMES as P

    fig, ax = plt.subplots(figsize=(5.4, 4.2))
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(0, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.plot([0.5, 0.5], [0.0, 0.22], color="#3f7f2f", lw=5, zorder=1)
    # Receptacle and sepals.
    ax.add_patch(Ellipse((0.5, 0.25), 0.30, 0.10, facecolor="#7fae5a", edgecolor=INK, lw=1.0, zorder=2))
    for side in (-1, 1):
        ax.add_patch(plt.Polygon([(0.5 + side * 0.08, 0.26), (0.5 + side * 0.32, 0.30),
                                  (0.5 + side * 0.12, 0.34)], facecolor="#6fa04a", edgecolor=INK, lw=1.0, zorder=3))
        # Petals.
        ax.add_patch(Ellipse((0.5 + side * 0.30, 0.55), 0.16, 0.48, angle=-side * 25,
                             facecolor="#f4a6c1", edgecolor=INK, lw=1.0, zorder=2))
        # Stamens: filament and anther.
        ax.plot([0.5 + side * 0.10, 0.5 + side * 0.17], [0.30, 0.66], color=INK, lw=1.4, zorder=4)
        ax.add_patch(Ellipse((0.5 + side * 0.17, 0.69), 0.06, 0.09, facecolor="#f2c230",
                             edgecolor=INK, lw=1.0, zorder=5))
    # Pistil: ovary with ovules, style, stigma.
    ax.add_patch(Ellipse((0.5, 0.36), 0.16, 0.18, facecolor="#cfe8b0", edgecolor=INK, lw=1.0, zorder=4))
    for dy in (0.32, 0.38):
        ax.add_patch(Circle((0.5, dy), 0.018, facecolor="#ffffff", edgecolor=INK, lw=0.8, zorder=5))
    ax.plot([0.5, 0.5], [0.45, 0.74], color="#7a9a4a", lw=4, zorder=4)
    ax.add_patch(Ellipse((0.5, 0.77), 0.09, 0.05, facecolor="#9bc25a", edgecolor=INK, lw=1.0, zorder=5))
    # (leader start, number place); left column and right column, top to bottom.
    places = {
        P[4]: ((0.50, 0.78), (-0.35, 0.95)),   # stigma
        P[2]: ((0.33, 0.70), (-0.35, 0.78)),   # anther
        P[3]: ((0.36, 0.52), (-0.35, 0.58)),   # filament
        P[0]: ((0.24, 0.30), (-0.35, 0.30)),   # sepal
        P[1]: ((0.84, 0.62), (1.35, 0.85)),    # petal
        P[5]: ((0.50, 0.60), (1.35, 0.66)),    # style
        P[6]: ((0.56, 0.40), (1.35, 0.46)),    # ovary
        P[7]: ((0.50, 0.32), (1.35, 0.26)),    # ovule
    }
    for i, part in enumerate(spec.labelled):
        tip, spot = places[part]
        _label(ax, i + 1, tip, spot)
    return _save(fig, spec.asset_id, dpi=96)


def make_food_chain(spec) -> Path:
    """Four lettered circles at the corners of a square, joined by arrows in ``order``."""
    from otk.sets._support.life_earth_diagrams import CHAIN_PLACES

    fig, ax = plt.subplots(figsize=(3.6, 3.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    radius = 0.09
    for food, eater in zip(spec.order, spec.order[1:]):
        (x0, y0), (x1, y1) = CHAIN_PLACES[food], CHAIN_PLACES[eater]
        length = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / length, (y1 - y0) / length
        ax.annotate("", xy=(x1 - ux * radius * 1.1, y1 - uy * radius * 1.1),
                    xytext=(x0 + ux * radius * 1.1, y0 + uy * radius * 1.1),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.6",
                                    color=INK, lw=1.6))
    for letter, (x, y) in CHAIN_PLACES.items():
        ax.add_patch(Circle((x, y), radius, facecolor="white", edgecolor=INK, lw=1.4))
        ax.text(x, y, letter, fontsize=16, ha="center", va="center", color=INK, fontweight="bold")
    return _save(fig, spec.asset_id, dpi=96)


def _arrow_between(ax, a, b, shrink, colour=INK, lw=1.6, rad=0.0):
    (x0, y0), (x1, y1) = a, b
    length = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    ax.annotate("", xy=(x1 - ux * shrink, y1 - uy * shrink), xytext=(x0 + ux * shrink, y0 + uy * shrink),
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.6", color=colour, lw=lw,
                                connectionstyle=f"arc3,rad={rad}"), zorder=3)


def _number_badge(ax, number, at):
    ax.text(at[0], at[1], str(number), fontsize=11, ha="center", va="center", color=INK,
            fontweight="bold", zorder=10,
            bbox=dict(boxstyle="circle,pad=0.22", facecolor="#fff7d6", edgecolor=INK, lw=1.0))


def make_rock_cycle(spec) -> Path:
    """Five lettered stages on a ring, joined by the six numbered arrows of the cycle."""
    from otk.sets._support.life_earth_diagrams import ROCK_PLACES, ROCK_STAGES
    from otk.sets.earth_science.p6.rocks_and_the_rock_cycle import ROCK_CYCLE_ARROWS

    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(0, 1.02)
    ax.axis("off")
    for j, (start, end, _) in enumerate(ROCK_CYCLE_ARROWS):
        a = ROCK_PLACES[ROCK_STAGES.index(start)]
        b = ROCK_PLACES[ROCK_STAGES.index(end)]
        _arrow_between(ax, a, b, shrink=0.10)
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        # Push the number off the line, away from the ring's centre.
        dx, dy = mid[0] - 0.5, mid[1] - 0.5
        norm = math.hypot(dx, dy) or 1.0
        at = (mid[0] + dx / norm * 0.06, mid[1] + dy / norm * 0.06) if norm > 0.05 else (mid[0], mid[1] + 0.06)
        _number_badge(ax, spec.numbers[j], at)
    for i, (x, y) in enumerate(ROCK_PLACES):
        ax.add_patch(FancyBboxPatch((x - 0.07, y - 0.055), 0.14, 0.11,
                                    boxstyle="round,pad=0.01,rounding_size=0.03",
                                    facecolor="#f4efe6" if i else "#f7c39a", edgecolor=INK, lw=1.4, zorder=4))
        ax.text(x, y, spec.letters[i], fontsize=15, ha="center", va="center", color=INK,
                fontweight="bold", zorder=5)
    return _save(fig, spec.asset_id, dpi=96)


def make_plate(spec) -> Path:
    """Two plates at a boundary with arrows for their motion; mirrored pictures swap left and right."""
    from otk.sets._support.life_earth_diagrams import BOUNDARY_NAMES

    fig, ax = plt.subplots(figsize=(5.0, 3.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.62)
    ax.set_aspect("equal")
    ax.axis("off")
    kind = BOUNDARY_NAMES.index(spec.boundary)
    flip = (lambda x: 1 - x) if spec.mirrored else (lambda x: x)
    plate, mantle, magma = "#b9a27d", "#e7a76b", "#d9481c"

    def poly(points, colour):
        ax.add_patch(plt.Polygon([(flip(x), y) for x, y in points], facecolor=colour,
                                 edgecolor=INK, lw=1.2, zorder=2))

    def arrow(x0, x1, y, colour=INK):
        _arrow_between(ax, (flip(x0), y), (flip(x1), y), shrink=0.0, colour=colour, lw=2.4)

    if kind == 2:
        # Seen from above: a fault line across the middle, the two sides sliding past.
        poly([(0.05, 0.31), (0.95, 0.31), (0.95, 0.56), (0.05, 0.56)], plate)
        poly([(0.05, 0.06), (0.95, 0.06), (0.95, 0.31), (0.05, 0.31)], "#a8b98a")
        ax.plot([0.05, 0.95], [0.31, 0.31], color=INK, lw=2.4, ls="--", zorder=3)
        arrow(0.65, 0.35, 0.44)
        arrow(0.35, 0.65, 0.18)
        return _save(fig, spec.asset_id, dpi=96)
    poly([(0.0, 0.0), (1.0, 0.0), (1.0, 0.30), (0.0, 0.30)], mantle)
    if kind == 0:
        poly([(0.02, 0.30), (0.46, 0.30), (0.46, 0.42), (0.02, 0.42)], plate)
        poly([(0.54, 0.30), (0.98, 0.30), (0.98, 0.42), (0.54, 0.42)], plate)
        poly([(0.46, 0.30), (0.54, 0.30), (0.52, 0.40), (0.48, 0.40)], magma)
        _arrow_between(ax, (0.5, 0.06), (0.5, 0.28), shrink=0.0, colour=magma, lw=2.4)
        arrow(0.36, 0.14, 0.52)
        arrow(0.64, 0.86, 0.52)
    else:
        # The left plate dives under the right one, which is thicker and rises into mountains.
        poly([(0.02, 0.32), (0.50, 0.32), (0.62, 0.10), (0.56, 0.08), (0.46, 0.27), (0.02, 0.27)], "#8f9db0")
        poly([(0.50, 0.32), (0.98, 0.32), (0.98, 0.44), (0.72, 0.44), (0.64, 0.52), (0.58, 0.44), (0.52, 0.40)], plate)
        arrow(0.10, 0.34, 0.40)
        arrow(0.92, 0.76, 0.52)
    return _save(fig, spec.asset_id, dpi=96)


def make_heart(spec) -> Path:
    """Four chambers seen from the front, lungs above and the body below, with the loop's arrows."""
    fig, ax = plt.subplots(figsize=(4.4, 4.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.axis("off")
    blue, red = "#7da7d9", "#e07a6f"
    # Lungs on top, the body (a simple figure) below.
    for cx in (0.38, 0.62):
        ax.add_patch(Ellipse((cx, 0.92), 0.20, 0.16, facecolor="#f3b8c4", edgecolor=INK, lw=1.0))
    ax.add_patch(Circle((0.5, 0.17), 0.04, facecolor="#e8d3b9", edgecolor=INK, lw=1.0))
    ax.add_patch(FancyBboxPatch((0.43, 0.02), 0.14, 0.10, boxstyle="round,pad=0,rounding_size=0.02",
                                facecolor="#e8d3b9", edgecolor=INK, lw=1.0))
    # Chambers: picture-left is the body's right side.
    boxes = {0: (0.22, 0.56), 1: (0.22, 0.36), 2: (0.53, 0.56), 3: (0.53, 0.36)}
    for chamber, (x, y) in boxes.items():
        colour = blue if chamber < 2 else red
        ax.add_patch(FancyBboxPatch((x, y), 0.25, 0.18, boxstyle="round,pad=0,rounding_size=0.03",
                                    facecolor=colour, edgecolor=INK, lw=1.4, zorder=2))
        _number_badge(ax, spec.numbers[chamber], (x + 0.125, y + 0.09))
    # Right atrium to right ventricle, left atrium to left ventricle.
    _arrow_between(ax, (0.30, 0.56), (0.30, 0.54), shrink=0.0, lw=1.8)
    _arrow_between(ax, (0.61, 0.56), (0.61, 0.54), shrink=0.0, lw=1.8)
    # Right ventricle up to the lungs, lungs down into the left atrium.
    # It rises through the gap between the two sides, so it crosses no other route.
    ax.plot([0.47, 0.50, 0.50], [0.42, 0.42, 0.80], color=INK, lw=1.8, zorder=1)
    _arrow_between(ax, (0.50, 0.80), (0.44, 0.86), shrink=0.0, lw=1.8)
    _arrow_between(ax, (0.70, 0.86), (0.70, 0.74), shrink=0.0, lw=1.8)
    # Left ventricle down to the body, body back up into the right atrium.
    ax.plot([0.78, 0.88, 0.88], [0.45, 0.45, 0.12], color=INK, lw=1.8, zorder=1)
    _arrow_between(ax, (0.88, 0.12), (0.58, 0.07), shrink=0.0, lw=1.8)
    ax.plot([0.43, 0.06, 0.06], [0.07, 0.07, 0.65], color=INK, lw=1.8, zorder=1)
    _arrow_between(ax, (0.06, 0.65), (0.21, 0.65), shrink=0.0, lw=1.8)
    return _save(fig, spec.asset_id, dpi=96)


def make_digestive(spec) -> Path:
    """A simple digestive tract: mouth, gullet, stomach, liver, small and large intestine, numbered."""
    fig, ax = plt.subplots(figsize=(4.4, 4.6))
    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(0, 1.05)
    ax.axis("off")
    ax.add_patch(Ellipse((0.50, 0.95), 0.16, 0.07, facecolor="#e88f8f", edgecolor=INK, lw=1.2, zorder=3))
    ax.plot([0.50, 0.50], [0.92, 0.66], color="#c97a6a", lw=7, zorder=2)
    ax.add_patch(Ellipse((0.60, 0.60), 0.26, 0.15, angle=-25, facecolor="#e9a28f", edgecolor=INK, lw=1.2, zorder=3))
    ax.add_patch(plt.Polygon([(0.18, 0.70), (0.48, 0.70), (0.44, 0.58), (0.22, 0.52)],
                             facecolor="#9c5a3c", edgecolor=INK, lw=1.2, zorder=4))
    # Large intestine: a frame up the right, across, and down the left.
    ax.plot([0.30, 0.22, 0.22, 0.78, 0.78, 0.60], [0.10, 0.10, 0.46, 0.46, 0.12, 0.12],
            color="#c9a26b", lw=11, solid_capstyle="round", zorder=2)
    # Small intestine: a coil inside the frame.
    xs = [0.32 + 0.36 * (i / 60) for i in range(61)]
    ys = [0.29 + 0.08 * math.sin(i / 60 * 6 * math.pi) for i in range(61)]
    ax.plot(xs, ys, color="#e7b98a", lw=6, zorder=3)
    ax.plot(xs, ys, color=INK, lw=0.6, zorder=3)
    # (leader start, number place), in DIGESTIVE_NAMES order.
    places = (((0.50, 0.95), (-0.05, 0.95)),   # mouth
              ((0.50, 0.80), (1.05, 0.82)),    # gullet
              ((0.64, 0.60), (1.05, 0.62)),    # stomach
              ((0.44, 0.29), (-0.05, 0.25)),   # small intestine
              ((0.78, 0.30), (1.05, 0.30)),    # large intestine
              ((0.28, 0.62), (-0.05, 0.62)))   # liver
    for (tip, spot), number in zip(places, spec.numbers):
        _label(ax, number, tip, spot)
    return _save(fig, spec.asset_id, dpi=96)


def make_breathing(spec) -> Path:
    """Nose, windpipe branching into the lungs, and the dome of muscle under them, numbered."""
    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(0, 1.05)
    ax.axis("off")
    # Head outline with the nose, then the windpipe down the middle.
    ax.add_patch(Circle((0.50, 0.90), 0.11, facecolor="#f3dcc4", edgecolor=INK, lw=1.0))
    ax.add_patch(plt.Polygon([(0.60, 0.91), (0.67, 0.86), (0.60, 0.85)], facecolor="#e7c3a3",
                             edgecolor=INK, lw=1.0))
    ax.plot([0.50, 0.50], [0.79, 0.55], color="#d9a19a", lw=9, solid_capstyle="butt", zorder=2)
    for y in (0.75, 0.71, 0.67, 0.63, 0.59):
        ax.plot([0.47, 0.53], [y, y], color=INK, lw=0.8, zorder=3)
    for side in (-1, 1):
        ax.add_patch(Ellipse((0.50 + side * 0.22, 0.40), 0.30, 0.42, facecolor="#f3b8c4",
                             edgecolor=INK, lw=1.2, zorder=1))
        # Branches: bronchus then finer bronchioles.
        ax.plot([0.50, 0.50 + side * 0.12], [0.55, 0.47], color="#c98f88", lw=5, zorder=3)
        for dy, dx in ((0.0, 0.10), (-0.08, 0.08), (0.06, 0.07)):
            ax.plot([0.50 + side * 0.12, 0.50 + side * (0.12 + dx)], [0.47, 0.47 + dy - 0.04],
                    color="#c98f88", lw=2, zorder=3)
    # The diaphragm: a dome under both lungs.
    xs = [0.18 + 0.64 * i / 40 for i in range(41)]
    ys = [0.17 + 0.05 * math.sin(math.pi * i / 40) for i in range(41)]
    ax.plot(xs, ys, color="#a0522d", lw=5, zorder=2)
    # (leader start, number place) in BREATHING_PARTS order.
    places = (((0.64, 0.88), (1.05, 0.92)),   # nose
              ((0.50, 0.70), (-0.05, 0.72)),  # windpipe
              ((0.70, 0.45), (1.05, 0.52)),   # bronchioles
              ((0.24, 0.32), (-0.05, 0.32)),  # lung
              ((0.70, 0.20), (1.05, 0.15)))   # diaphragm
    for (tip, spot), number in zip(places, spec.numbers):
        _label(ax, number, tip, spot)
    return _save(fig, spec.asset_id, dpi=96)


def make_plant_organs(spec) -> Path:
    """A potted flowering plant: roots in the soil, stem, leaves and a flower, numbered."""
    fig, ax = plt.subplots(figsize=(4.2, 4.6))
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(0, 1.1)
    ax.axis("off")
    ax.add_patch(plt.Polygon([(0.25, 0.30), (0.75, 0.30), (0.68, 0.02), (0.32, 0.02)],
                             facecolor="#c98a5a", edgecolor=INK, lw=1.2, zorder=1))
    ax.add_patch(plt.Rectangle((0.27, 0.22), 0.46, 0.08, facecolor="#6b4f3a", edgecolor="none", zorder=2))
    for dx, end in ((-0.10, (0.36, 0.08)), (0.0, (0.50, 0.05)), (0.10, (0.62, 0.09)), (0.04, (0.56, 0.12))):
        ax.plot([0.50, 0.50 + dx * 0.5, end[0]], [0.28, 0.18, end[1]], color="#e9d8a6", lw=2, zorder=3)
    ax.plot([0.50, 0.50], [0.28, 0.86], color="#3f7f2f", lw=6, zorder=3)
    for y, side in ((0.48, -1), (0.62, 1), (0.74, -1)):
        ax.add_patch(Ellipse((0.50 + side * 0.13, y + 0.03), 0.22, 0.09, angle=side * 20,
                             facecolor="#5aa04a", edgecolor=INK, lw=1.0, zorder=4))
    for k in range(6):
        angle = k * math.pi / 3
        ax.add_patch(Ellipse((0.50 + 0.06 * math.cos(angle), 0.92 + 0.06 * math.sin(angle)),
                             0.08, 0.05, angle=math.degrees(angle), facecolor="#f2c230",
                             edgecolor=INK, lw=0.8, zorder=5))
    ax.add_patch(Circle((0.50, 0.92), 0.03, facecolor="#c0582c", edgecolor=INK, lw=0.8, zorder=6))
    # (leader start, number place) in PLANT_ORGANS order: root, stem, leaf, flower.
    places = (((0.42, 0.13), (-0.05, 0.13)), ((0.50, 0.55), (1.05, 0.50)),
              ((0.36, 0.52), (-0.05, 0.60)), ((0.55, 0.96), (1.05, 0.98)))
    for (tip, spot), number in zip(places, spec.numbers):
        _label(ax, number, tip, spot)
    return _save(fig, spec.asset_id, dpi=96)


LAYER_FILLS = (("#c9b28a", "."), ("#a8a8a8", "-"), ("#d8c39a", "o"), ("#b58a6a", "/"))


def make_rock_layers(spec) -> Path:
    """Four flat sedimentary layers lettered from the bottom up as ``letters`` says."""
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    ax.set_xlim(0, 1.2)
    ax.set_ylim(0, 0.9)
    ax.axis("off")
    for i, ((colour, hatch), letter) in enumerate(zip(LAYER_FILLS, spec.letters)):
        bottom = 0.05 + i * 0.19
        ax.add_patch(plt.Rectangle((0.08, bottom), 0.84, 0.19, facecolor=colour, edgecolor=INK,
                                   lw=1.0, hatch=hatch, zorder=1))
        ax.text(1.02, bottom + 0.095, letter, fontsize=15, ha="center", va="center", color=INK,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=INK, lw=1.0))
        ax.plot([0.92, 0.98], [bottom + 0.095, bottom + 0.095], color=INK, lw=1.0)
    # Ground surface with grass on top of the youngest layer.
    for x in [0.10 + 0.05 * i for i in range(17)]:
        ax.plot([x, x - 0.012, x + 0.012], [0.81, 0.85, 0.81], color="#3f7f2f", lw=1.2)
    return _save(fig, spec.asset_id, dpi=96)
