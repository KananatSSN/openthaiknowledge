"""The science diagrams, drawn on demand like the math ones.

Nothing here is committed: ``otk.pictures.registry`` registers each
spec tuple with its drawing function below, and a PNG is drawn into
``_output.output_dir()`` the first time it is asked for. Running this module
draws every registered diagram there::

    python -m otk.pictures.generate

Marker coordinates in the anatomy types are aligned with the skeleton drawing; the
wave PNGs are rendered from ``WAVE_SPECS`` so the drawn graph matches exactly the
amplitude / wavelength / cycle count the type asks about, and the ไฟฟ้า circuit
schematics from ``CIRCUIT_SPECS`` so the resistor values printed in the picture
are the ones ``elec.circuit_*`` computes its answers from. The เคมี ม.2
chromatograms come from ``CHROMA_SPECS`` the same way — the millimetre scale
drawn beside the strip is what makes ``chem.rf_value`` readable off the picture —
and the separation set-ups from ``APPARATUS_SPECS``.
"""

from __future__ import annotations

import io
import math as _math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.patches import Arc, Circle, Ellipse, FancyBboxPatch, Polygon

from ._output import save_image

BONE = "#ece7d9"
EDGE = "#4a4a4a"


def _save(fig, asset_id: str, dpi: int, **kw) -> Path:
    buf = io.BytesIO()
    fig.savefig(buf, dpi=dpi, facecolor="white", format="png", **kw)
    plt.close(fig)
    buf.seek(0)
    return save_image(Image.open(buf), asset_id)


def _bone(ax, x0, y0, x1, y1, lw=9):
    ax.plot([x0, x1], [y0, y1], color=EDGE, lw=lw + 2, solid_capstyle="round", zorder=1)
    ax.plot([x0, x1], [y0, y1], color=BONE, lw=lw, solid_capstyle="round", zorder=2)


def make_skeleton(_spec=None) -> Path:
    # Marker coordinates are normalized against the complete bitmap. A portrait
    # canvas plus equal data aspect adds vertical letterboxing and shifts the
    # overlaid marker away from the named bone, so the bitmap must remain square.
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(1, 0)              # top-left origin, matching normalized markers
    ax.set_aspect("equal")
    ax.axis("off")

    # Skull + jaw
    ax.add_patch(Circle((0.5, 0.08), 0.055, facecolor=BONE, edgecolor=EDGE,
                        lw=1.5, zorder=3))
    ax.add_patch(FancyBboxPatch((0.468, 0.11), 0.064, 0.028,
                                boxstyle="round,pad=0.004", facecolor=BONE,
                                edgecolor=EDGE, lw=1, zorder=3))

    # Clavicle / shoulders
    _bone(ax, 0.30, 0.22, 0.5, 0.20)
    _bone(ax, 0.70, 0.22, 0.5, 0.20)

    # Spine (stacked vertebrae)
    for yy in [x / 100 for x in range(16, 53, 4)]:
        ax.add_patch(FancyBboxPatch((0.484, yy - 0.008), 0.032, 0.016,
                                    boxstyle="round,pad=0.003", facecolor=BONE,
                                    edgecolor=EDGE, lw=0.8, zorder=4))

    # Ribcage
    for r in (0.06, 0.09, 0.12, 0.15):
        ax.add_patch(Arc((0.5, 0.34), r * 2, r * 2.4, theta1=20, theta2=160,
                         edgecolor=EDGE, lw=1.6, zorder=2))

    # Arms
    _bone(ax, 0.30, 0.22, 0.24, 0.40)
    _bone(ax, 0.24, 0.40, 0.22, 0.56)
    _bone(ax, 0.70, 0.22, 0.76, 0.40)
    _bone(ax, 0.76, 0.40, 0.78, 0.56)

    # Pelvis
    ax.add_patch(Arc((0.5, 0.54), 0.24, 0.14, theta1=200, theta2=340,
                     edgecolor=EDGE, lw=3, zorder=2))

    # Femurs + knees + tibiae + feet
    _bone(ax, 0.45, 0.55, 0.44, 0.72)
    _bone(ax, 0.55, 0.55, 0.56, 0.72)
    ax.add_patch(Circle((0.44, 0.72), 0.02, facecolor=BONE, edgecolor=EDGE, lw=1, zorder=3))
    ax.add_patch(Circle((0.56, 0.72), 0.02, facecolor=BONE, edgecolor=EDGE, lw=1, zorder=3))
    _bone(ax, 0.44, 0.73, 0.43, 0.92)
    _bone(ax, 0.56, 0.73, 0.57, 0.92)
    _bone(ax, 0.43, 0.92, 0.37, 0.95, lw=7)
    _bone(ax, 0.57, 0.92, 0.63, 0.95, lw=7)

    return _save(fig, "skeleton", dpi=100)


WAVE_LINE = "#1350c4"
WAVE_AXIS = "#555555"
WAVE_GRID = "#d5dae2"


def make_wave(spec) -> Path:
    """A sine graph on a numbered grid: y = amp·sin(2π x / wavelength) over
    ``cycles`` full waves. Axes are numbered so ความยาวคลื่น (x) and แอมพลิจูด (y)
    read straight off, and the whole waves are countable. Labels are ASCII so no
    Thai font is needed to render the asset."""
    amp, wavelength, cycles = spec.amp, spec.wavelength, spec.cycles
    span = wavelength * cycles
    xs = [i * span / 400 for i in range(401)]
    ys = [amp * _math.sin(2 * _math.pi * x / wavelength) for x in xs]

    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.axhline(0, color=WAVE_AXIS, lw=1.1, zorder=2)
    ax.plot(xs, ys, color=WAVE_LINE, lw=2.4, zorder=3)
    ax.set_xlim(0, span)
    ax.set_ylim(-(amp + 1), amp + 1)
    ax.set_xticks(range(0, span + 1))
    ax.set_yticks(range(-(amp + 1), amp + 2))
    ax.grid(True, color=WAVE_GRID, lw=0.8, zorder=1)
    ax.set_xlabel("x (m)", fontsize=10)
    ax.set_ylabel("y (cm)", fontsize=10)
    ax.tick_params(labelsize=9, colors=WAVE_AXIS)
    for spine in ax.spines.values():
        spine.set_color(WAVE_AXIS)
    fig.tight_layout()

    return _save(fig, spec.asset_id, dpi=92)


# ── ไฟฟ้า circuit schematics ─────────────────────────────────────────────────

WIRE = "#333333"
BOX = "#ffffff"

# The loop the current runs around, in axes coordinates.
LEFT, RIGHT, TOP, BOT = 0.10, 0.90, 0.80, 0.20


def _wire(ax, xs, ys):
    ax.plot(xs, ys, color=WIRE, lw=1.8, solid_capstyle="round", zorder=2)


def _battery(ax, x, y, label):
    """The cell on the left edge: a long plate (+), a short plate (-), a label."""
    _wire(ax, [x, x], [BOT, y - 0.05])          # leave a gap for the plates
    _wire(ax, [x, x], [y + 0.05, TOP])
    _wire(ax, [x - 0.055, x + 0.055], [y + 0.05, y + 0.05])     # long plate
    _wire(ax, [x - 0.026, x + 0.026], [y - 0.05, y - 0.05])     # short plate
    ax.text(x + 0.075, y, label, fontsize=10, ha="left", va="center", color=WIRE)


def _box(ax, cx, cy, w, h):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="square,pad=0", facecolor=BOX,
                                edgecolor=WIRE, lw=1.8, zorder=3))


def _resistor_h(ax, cx, cy, label):
    """A resistor lying on a horizontal rail; its label sits above it."""
    _box(ax, cx, cy, 0.15, 0.06)
    ax.text(cx, cy + 0.075, label, fontsize=9.5, ha="center", va="bottom",
            color=WIRE, zorder=4)


def _resistor_v(ax, cx, cy, label):
    """A resistor on a vertical branch; its label sits below it.

    The branch wire runs on down through where the label goes, so the label
    carries a white background to mask it — the usual schematic convention.
    """
    _box(ax, cx, cy, 0.06, 0.17)
    ax.text(cx, cy - 0.115, label, fontsize=9.5, ha="center", va="top",
            color=WIRE, zorder=4,
            bbox=dict(facecolor=BOX, edgecolor="none", pad=1.5))


def _spread(x0, x1, n):
    """``n`` branch positions ending at ``x1`` — one branch means just the edge."""
    if n == 1:
        return [x1]
    return [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]


def make_circuit(spec) -> Path:
    """One schematic: a cell driving resistors in series, parallel, or a mix.

    Series resistors lie along the top rail; parallel ones hang as vertical
    branches between the two rails, so a ``mixed`` circuit reads left to right as
    "R1, then the branches" — exactly the R1 + (R2∥R3) that ``CircuitSpec.total``
    computes. Labels are ASCII plus Ω, so no Thai font is needed to render.
    """
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _wire(ax, [LEFT, RIGHT], [TOP, TOP])            # top rail
    _wire(ax, [LEFT, RIGHT], [BOT, BOT])            # bottom rail
    _wire(ax, [RIGHT, RIGHT], [BOT, TOP])           # right edge
    _battery(ax, LEFT, 0.5, f"{spec.volts} V")      # left edge, broken by the cell

    if spec.kind == "series":
        n = len(spec.resistors)
        x0, x1 = LEFT + 0.14, RIGHT
        for i, r in enumerate(spec.resistors):
            _resistor_h(ax, x0 + (x1 - x0) * (i + 0.5) / n, TOP, f"R{i + 1} = {r} Ω")
    else:
        branch = spec.resistors
        if spec.kind == "mixed":                    # R1 first, in series with the rest
            branch = spec.resistors[1:]
            _resistor_h(ax, LEFT + 0.20, TOP, f"R1 = {spec.resistors[0]} Ω")
        first = 0.50 if spec.kind == "mixed" else 0.38
        for k, (x, r) in enumerate(zip(_spread(first, RIGHT, len(branch)), branch)):
            if x < RIGHT:                           # the last branch *is* the right edge
                _wire(ax, [x, x], [BOT, TOP])
            n = k + 2 if spec.kind == "mixed" else k + 1
            _resistor_v(ax, x, 0.5, f"R{n} = {r} Ω")

    return _save(fig, spec.asset_id, dpi=92)


# ── ป.6 สัญลักษณ์ไฟฟ้า และวงจรไฟฟ้าอย่างง่าย ──────────────────────────────────

# At ป.6 the symbols *are* the content — there is no resistance to print and no
# value to read off — so these carry no text at all. That also settles the Thai
# font question for good: nothing is written, so nothing can fail to render.

P6_LEFT, P6_RIGHT, P6_TOP, P6_BOT = 0.12, 0.88, 0.78, 0.22
P6_SIZE, CARD_SIZE = (5.0, 3.0), (2.6, 1.5)
# Plate sizes for a cell drawn lying on its side across a card.
PLATES = dict(long_half=0.26, short_half=0.13, gap=0.035)
BULB_R, CARD_BULB_R = 0.050, 0.115


def _cell(ax, x, y, horizontal=False, long_half=0.058, short_half=0.028,
          gap=0.030):
    """One เซลล์ไฟฟ้า: a long plate and a short one, the standard IPST symbol.

    The plate sizes are given rather than fixed because the two canvases have
    different shapes: the same numbers that read well down a circuit's left edge
    shrink to a few pixels when the symbol is turned on its side on a wide card.
    """
    if horizontal:
        ax.plot([x - gap, x - gap], [y - long_half, y + long_half],
                color=WIRE, lw=2.2, zorder=3)
        ax.plot([x + gap, x + gap], [y - short_half, y + short_half],
                color=WIRE, lw=3.4, zorder=3)
    else:
        ax.plot([x - long_half, x + long_half], [y + gap, y + gap],
                color=WIRE, lw=2.2, zorder=3)
        ax.plot([x - short_half, x + short_half], [y - gap, y - gap],
                color=WIRE, lw=3.4, zorder=3)


def _bulb(ax, cx, cy, aspect, r=BULB_R):
    """หลอดไฟ: a circle with a cross through it.

    The axes span 0–1 both ways on a figure that is wider than it is tall, so a
    circle of equal data radius draws as a flat ellipse. ``aspect`` is the
    figure's width/height and stretches the vertical radius back out — the
    symbol has to read as a circle, since that is the shape the student is being
    asked to recognise.
    """
    ry = r * aspect
    ax.add_patch(Ellipse((cx, cy), r * 2, ry * 2, facecolor=BOX,
                         edgecolor=WIRE, lw=1.8, zorder=3))
    dx, dy = r * 0.707, ry * 0.707
    ax.plot([cx - dx, cx + dx], [cy - dy, cy + dy], color=WIRE, lw=1.5, zorder=4)
    ax.plot([cx - dx, cx + dx], [cy + dy, cy - dy], color=WIRE, lw=1.5, zorder=4)


def _switch(ax, cx, cy, closed: bool, aspect, half=0.075, rise=0.085, dot=0.012):
    """สวิตช์: two contacts and a lever, resting on them or tilted off one.

    The lever is hinged on the left contact and lifts off the right one, which
    is the difference the student is asked to read. ``rise`` and ``dot`` are
    given per canvas for the same reason the cell's plates are.
    """
    for x in (cx - half, cx + half):
        ax.add_patch(Ellipse((x, cy), dot * 2, dot * 2 * aspect,
                             facecolor=WIRE, edgecolor=WIRE, zorder=4))
    end_y = cy if closed else cy + rise
    ax.plot([cx - half, cx + half], [cy, end_y], color=WIRE, lw=2.2,
            solid_capstyle="round", zorder=3)


def make_p6_symbol_card(card) -> Path:
    """One symbol alone, centred on a small card, with stub wires either side."""
    fig, ax = plt.subplots(figsize=CARD_SIZE)
    aspect = CARD_SIZE[0] / CARD_SIZE[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    if card.code == "wire":
        # A plain conductor has no symbol of its own — it is the right-angled
        # line every other symbol sits on, so that is what the card shows.
        _wire(ax, [0.12, 0.62, 0.62], [0.32, 0.32, 0.74])
    elif card.code == "bulb":
        _wire(ax, [0.12, 0.5 - CARD_BULB_R], [0.5, 0.5])
        _wire(ax, [0.5 + CARD_BULB_R, 0.88], [0.5, 0.5])
        _bulb(ax, 0.5, 0.5, aspect, r=CARD_BULB_R)
    elif card.code == "cell":
        _wire(ax, [0.12, 0.44], [0.5, 0.5])
        _wire(ax, [0.56, 0.88], [0.5, 0.5])
        _cell(ax, 0.5, 0.5, horizontal=True, **PLATES)
    elif card.code == "battery":
        # Three plate pairs butted together — the convention that distinguishes
        # a แบตเตอรี่ from the single pair on the ``cell`` card.
        _wire(ax, [0.12, 0.34], [0.5, 0.5])
        _wire(ax, [0.66, 0.88], [0.5, 0.5])
        for x in (0.38, 0.50, 0.62):
            _cell(ax, x, 0.5, horizontal=True, **PLATES)
    else:                                            # switch_open | switch_closed
        _wire(ax, [0.12, 0.5 - 0.15], [0.42, 0.42])
        _wire(ax, [0.5 + 0.15, 0.88], [0.42, 0.42])
        _switch(ax, 0.5, 0.42, card.code == "switch_closed", aspect,
                half=0.16, rise=0.30, dot=0.026)

    return _save(fig, card.asset_id, dpi=100)


def make_p6_circuit(spec) -> Path:
    """A simple circuit in symbols: cells left, switch below, bulbs above.

    Series bulbs sit along the top rail; parallel ones hang as branches between
    the rails, the same convention ``make_circuit`` uses one level up. ``gap``
    breaks the right edge short of the top corner, so วงจรไม่ครบวงจร is visible
    rather than asserted.
    """
    fig, ax = plt.subplots(figsize=P6_SIZE)
    aspect = P6_SIZE[0] / P6_SIZE[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _wire(ax, [P6_LEFT, P6_RIGHT], [P6_BOT, P6_BOT])      # bottom rail
    _wire(ax, [P6_RIGHT, P6_RIGHT], [P6_BOT, P6_TOP])     # right edge
    _wire(ax, [P6_LEFT, P6_RIGHT], [P6_TOP, P6_TOP])      # top rail
    # The switch sits on the bottom rail left of every parallel branch, so a
    # branch never lands on top of it.
    _switch(ax, P6_LEFT + 0.14, P6_BOT, spec.switch == "closed", aspect)

    # Left edge, broken by the cells stacked in series. ``gap`` leaves out the
    # run from the top cell up to the top rail altogether, so the corner is
    # visibly unconnected rather than nearly so. A break there cuts the loop
    # whatever the bulbs do, which a break in the right edge would not for
    # parallel branches.
    ys = _spread(P6_BOT + 0.16, P6_TOP - 0.16, spec.cells) if spec.cells > 1 \
        else [(P6_BOT + P6_TOP) / 2]
    _wire(ax, [P6_LEFT, P6_LEFT], [P6_BOT, ys[0] - 0.05])
    if not spec.gap:
        _wire(ax, [P6_LEFT, P6_LEFT], [ys[-1] + 0.05, P6_TOP])
    for y, nxt in zip(ys, ys[1:]):
        _wire(ax, [P6_LEFT, P6_LEFT], [y + 0.05, nxt - 0.05])
    for y in ys:
        _cell(ax, P6_LEFT, y)

    if spec.wiring == "series" or spec.bulbs == 1:
        n = spec.bulbs
        x0, x1 = P6_LEFT + 0.14, P6_RIGHT - 0.04
        for i in range(n):
            _bulb(ax, x0 + (x1 - x0) * (i + 0.5) / n, P6_TOP, aspect)
    else:
        for x in _spread(P6_LEFT + 0.30, P6_RIGHT - 0.14, spec.bulbs):
            _wire(ax, [x, x], [P6_BOT, P6_TOP])
            _bulb(ax, x, (P6_BOT + P6_TOP) / 2, aspect)

    return _save(fig, spec.asset_id, dpi=96)


# ── ม.1 ความร้อน และ ลมฟ้าอากาศ ──────────────────────────────────────────────

# Every label below is a number, an ASCII unit, or the letters H/L that a
# pressure chart uses worldwide — the bundled font has no Thai, and these
# drawings are the ones a student reads values off, so nothing may fail to
# render. See otk/sets/_support/ms1_diagrams.py.

CURVE = "#c0392b"
AXIS = "#555555"
GRID = "#d5dae2"
MERCURY = "#c0392b"
GLASS = "#3b4a5a"
FLAME = "#e8871a"
METAL = "#9aa4ad"
WATER_BLUE = "#7fb8e0"
HOT = "#c0392b"
COLD = "#2f6fb5"


def make_heating_curve(spec) -> Path:
    """Temperature against time for a steadily heated substance.

    The flat stretch is drawn, not asserted: a student reads the plateau's
    temperature and its start and end minutes straight off the grid, which is
    the whole point of ``ว 2.3 ม.1/1``'s "แปลความหมายข้อมูล".
    """
    xs = [0, spec.warm_to, spec.plateau_end, spec.total]
    ys = [spec.start, spec.plateau, spec.plateau, spec.end]

    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.plot(xs, ys, color=CURVE, lw=2.4, marker="o", ms=4, zorder=3)
    ax.set_xlim(0, spec.total)
    ax.set_ylim(min(ys) - 10, max(ys) + 10)
    ax.set_xticks(range(0, spec.total + 1, 2))
    ax.grid(True, color=GRID, lw=0.8, zorder=1)
    ax.set_xlabel("time (min)", fontsize=10)
    ax.set_ylabel("temperature (C)", fontsize=10)
    ax.tick_params(labelsize=9, colors=AXIS)
    for spine in ax.spines.values():
        spine.set_color(AXIS)
    fig.tight_layout()

    return _save(fig, spec.asset_id, dpi=94)


def make_thermometer(spec) -> Path:
    """A liquid-in-glass thermometer with its column standing at one reading."""
    fig, ax = plt.subplots(figsize=(2.2, 4.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(spec.lo - (spec.hi - spec.lo) * 0.10, spec.hi)
    ax.axis("off")

    x = 0.42
    half = 0.085
    # Tube, then the coloured column inside it, then the bulb.
    ax.add_patch(FancyBboxPatch((x - half, spec.lo), half * 2, spec.hi - spec.lo,
                                boxstyle="square,pad=0", facecolor="white",
                                edgecolor=GLASS, lw=1.6, zorder=2))
    ax.add_patch(FancyBboxPatch((x - half * 0.55, spec.lo),
                                half * 1.1, spec.reading - spec.lo,
                                boxstyle="square,pad=0", facecolor=MERCURY,
                                edgecolor="none", zorder=3))
    ax.add_patch(Ellipse((x, spec.lo - (spec.hi - spec.lo) * 0.045),
                         half * 2.4, (spec.hi - spec.lo) * 0.075,
                         facecolor=MERCURY, edgecolor=GLASS, lw=1.6, zorder=4))

    for value in range(spec.lo, spec.hi + 1, spec.step):
        major = (value - spec.lo) % spec.label_every == 0
        ax.plot([x + half, x + half + (0.10 if major else 0.05)], [value] * 2,
                color=GLASS, lw=1.1 if major else 0.7, zorder=5)
        if major:
            ax.text(x + half + 0.14, value, str(value), fontsize=9,
                    ha="left", va="center", color=GLASS)
    ax.text(0.04, spec.hi, "C", fontsize=10, ha="left", va="top", color=GLASS)

    return _save(fig, spec.asset_id, dpi=100, bbox_inches="tight")


def make_atmosphere_profile(_spec=None) -> Path:
    """Temperature against altitude, with the four layers separated and numbered.

    Altitude is logarithmic: the thermosphere runs to 500 km and would otherwise
    squash the troposphere — the layer the question is usually about — into a
    line two pixels tall.
    """
    from otk.sets._support.ms1_diagrams import ATMOSPHERE, ATMOSPHERE_ASSET

    # The thermosphere reaches about 1000 C. Drawn to scale it would flatten the
    # other three layers, whose whole range is -90 to 15, into one vertical line,
    # so the x-axis stops at 150 and that segment leaves the plot with an
    # arrowhead — "keeps rising", which is all ม.1 asks of it.
    x_max = 150
    fig, ax = plt.subplots(figsize=(4.4, 4.2))
    for index, layer in enumerate(ATMOSPHERE):
        base = max(layer.base_km, 1)        # 0 km has no place on a log axis
        ax.plot([layer.base_c, layer.top_c], [base, layer.top_km],
                color=CURVE, lw=2.4, zorder=3, clip_on=True)
        if layer.top_km < 500:
            ax.axhline(layer.top_km, color=AXIS, lw=0.9, ls="--", zorder=2)
        mid = (base * layer.top_km) ** 0.5
        ax.text(1.02, mid, str(index + 1), transform=ax.get_yaxis_transform(),
                fontsize=12, ha="left", va="center", color=AXIS, zorder=5)
        if layer.top_c > x_max:
            frac = (x_max - layer.base_c) / (layer.top_c - layer.base_c)
            y_edge = base + (layer.top_km - base) * frac
            ax.annotate("", xy=(x_max, y_edge * 1.35), xytext=(x_max * 0.72, y_edge),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.22,head_length=0.4",
                                        color=CURVE, lw=2.4), zorder=4)

    ax.set_yscale("log")
    ax.set_ylim(1, 500)
    ax.set_xlim(-120, x_max)
    ax.set_yticks([1, 10, 50, 80, 500])
    ax.set_yticklabels(["0", "10", "50", "80", "500"])
    ax.set_xticks([-100, -50, 0, 50, 100])
    ax.grid(True, color=GRID, lw=0.8, zorder=1)
    ax.set_xlabel("temperature (C)", fontsize=10)
    ax.set_ylabel("height (km)", fontsize=10)
    ax.tick_params(labelsize=9, colors=AXIS)
    for spine in ax.spines.values():
        spine.set_color(AXIS)
    fig.tight_layout()

    return _save(fig, ATMOSPHERE_ASSET, dpi=96)


def make_weather_chart(spec) -> Path:
    """A pressure chart: an H and an L, each ringed by labelled isobars."""
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0.02, 0.04), 0.96, 0.92, facecolor="white",
                               edgecolor=AXIS, lw=1.2, zorder=1))

    centres = {"left": 0.27, "right": 0.73}
    for letter, side, colour, sign in (("H", spec.high_side, HOT, -1),
                                       ("L", spec.low_side, COLD, +1)):
        cx = centres[side]
        base = spec.high_hpa if letter == "H" else spec.low_hpa
        for ring in (1, 2, 3):
            ax.add_patch(Ellipse((cx, 0.5), 0.14 * ring, 0.22 * ring,
                                 facecolor="none", edgecolor=colour, lw=1.2,
                                 zorder=2))
            ax.text(cx, 0.5 + 0.11 * ring, str(base + sign * 4 * ring),
                    fontsize=8, ha="center", va="center", color=colour,
                    zorder=4, bbox=dict(facecolor="white", edgecolor="none",
                                        pad=1.0))
        ax.text(cx, 0.5, letter, fontsize=22, ha="center", va="center",
                color=colour, fontweight="bold", zorder=5)
        # The centre's own value, masked over the innermost isobar it sits on —
        # the schematic convention _resistor_v uses for the same collision.
        ax.text(cx, 0.5 - 0.115, str(base), fontsize=9, ha="center", va="center",
                color=colour, zorder=6,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
    ax.text(0.5, 0.965, "hPa", fontsize=9, ha="center", va="top", color=AXIS)

    return _save(fig, spec.asset_id, dpi=96)


def _arrow(ax, x0, y0, x1, y1, colour=HOT, lw=2.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>,head_width=0.18,head_length=0.36",
                                color=colour, lw=lw), zorder=5)


def _flame(ax, cx, cy, w=0.10, h=0.11):
    ax.add_patch(Ellipse((cx, cy), w, h, facecolor=FLAME, edgecolor="none",
                         zorder=3))
    ax.add_patch(Ellipse((cx, cy - h * 0.14), w * 0.5, h * 0.55,
                         facecolor="#f6c453", edgecolor="none", zorder=4))


def make_heat_scene(spec) -> Path:
    """One of the three modes, drawn so the picture alone settles which it is.

    What the heat crosses is what separates them, so each scene draws that: a
    solid whose arrows run *through* it, a fluid whose arrows *circulate*, or a
    gap with nothing in it at all.
    """
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    if spec.scene == "bar":
        ax.add_patch(plt.Rectangle((0.16, 0.44), 0.68, 0.12, facecolor=METAL,
                                   edgecolor=GLASS, lw=1.4, zorder=2))
        _flame(ax, 0.19, 0.39, w=0.14, h=0.17)
        for x in (0.30, 0.46, 0.62):
            _arrow(ax, x, 0.50, x + 0.11, 0.50)
    elif spec.scene == "spoon":
        ax.add_patch(plt.Rectangle((0.30, 0.16), 0.40, 0.46,
                                   facecolor=WATER_BLUE, edgecolor=GLASS,
                                   lw=1.6, zorder=2))
        ax.add_patch(plt.Rectangle((0.46, 0.22), 0.05, 0.64, facecolor=METAL,
                                   edgecolor=GLASS, lw=1.2, zorder=3))
        for y in (0.34, 0.52, 0.68):
            _arrow(ax, 0.485, y, 0.485, y + 0.12)
    elif spec.scene == "pot":
        ax.add_patch(plt.Rectangle((0.24, 0.26), 0.52, 0.44,
                                   facecolor=WATER_BLUE, edgecolor=GLASS,
                                   lw=1.8, zorder=2))
        _flame(ax, 0.50, 0.22, w=0.18, h=0.18)
        # Symmetric circulation: up over the flame, out along the surface, down
        # both walls, back in along the base. Drawing only one side made the pot
        # look half empty and the loop look like a stray arrow.
        _arrow(ax, 0.50, 0.33, 0.50, 0.60)
        for wall, inward in ((0.70, -1), (0.30, +1)):
            _arrow(ax, 0.50, 0.63, wall, 0.63)
            _arrow(ax, wall, 0.61, wall, 0.35)
            _arrow(ax, wall, 0.32, wall + inward * 0.16, 0.32)
    elif spec.scene == "room":
        ax.add_patch(plt.Rectangle((0.12, 0.14), 0.76, 0.72, facecolor="white",
                                   edgecolor=GLASS, lw=1.8, zorder=2))
        ax.add_patch(plt.Rectangle((0.17, 0.18), 0.10, 0.16, facecolor=HOT,
                                   edgecolor=GLASS, lw=1.2, zorder=3))
        _arrow(ax, 0.22, 0.36, 0.22, 0.72)
        _arrow(ax, 0.24, 0.76, 0.72, 0.76)
        _arrow(ax, 0.76, 0.72, 0.76, 0.30, colour=COLD)
        _arrow(ax, 0.72, 0.24, 0.32, 0.24, colour=COLD)
    elif spec.scene == "fire":
        _flame(ax, 0.24, 0.42, w=0.20, h=0.30)
        # A person: head and body, standing clear of the fire.
        ax.add_patch(Ellipse((0.80, 0.66), 0.075, 0.12, facecolor=METAL,
                             edgecolor=GLASS, lw=1.2, zorder=3))
        ax.add_patch(plt.Rectangle((0.775, 0.24), 0.05, 0.36, facecolor=METAL,
                                   edgecolor=GLASS, lw=1.2, zorder=3))
        for y in (0.34, 0.46, 0.58):
            _arrow(ax, 0.36, y, 0.72, y)
    elif spec.scene == "pan":
        ax.add_patch(plt.Rectangle((0.16, 0.40), 0.38, 0.09, facecolor=METAL,
                                   edgecolor=GLASS, lw=1.6, zorder=2))
        ax.add_patch(plt.Rectangle((0.54, 0.415), 0.36, 0.06, facecolor=METAL,
                                   edgecolor=GLASS, lw=1.2, zorder=2))
        _flame(ax, 0.35, 0.33, w=0.18, h=0.14)
        for x in (0.57, 0.73):
            _arrow(ax, x, 0.445, x + 0.12, 0.445)
    elif spec.scene == "tank":
        ax.add_patch(plt.Rectangle((0.18, 0.14), 0.64, 0.64,
                                   facecolor=WATER_BLUE, edgecolor=GLASS,
                                   lw=1.8, zorder=2))
        ax.add_patch(plt.Rectangle((0.21, 0.17), 0.13, 0.06, facecolor=HOT,
                                   edgecolor=GLASS, lw=1.2, zorder=3))
        _arrow(ax, 0.275, 0.26, 0.275, 0.68)
        _arrow(ax, 0.30, 0.72, 0.72, 0.72)
        _arrow(ax, 0.76, 0.68, 0.76, 0.28, colour=COLD)
        _arrow(ax, 0.72, 0.21, 0.40, 0.21, colour=COLD)
    elif spec.scene == "lamp":
        ax.add_patch(plt.Rectangle((0.40, 0.84), 0.20, 0.07, facecolor=METAL,
                                   edgecolor=GLASS, lw=1.4, zorder=3))
        ax.add_patch(Ellipse((0.50, 0.80), 0.10, 0.07, facecolor=FLAME,
                             edgecolor="none", zorder=4))
        ax.add_patch(plt.Rectangle((0.22, 0.08), 0.56, 0.08, facecolor="#8d6e4f",
                                   edgecolor=GLASS, lw=1.2, zorder=3))
        for x0, x1 in ((0.44, 0.32), (0.50, 0.50), (0.56, 0.68)):
            _arrow(ax, x0, 0.72, x1, 0.22)
    else:                                       # sun
        ax.add_patch(Ellipse((0.20, 0.74), 0.20, 0.26, facecolor=FLAME,
                             edgecolor="none", zorder=3))
        ax.add_patch(plt.Rectangle((0.06, 0.06), 0.88, 0.13,
                                   facecolor="#8d6e4f", edgecolor=GLASS,
                                   lw=1.2, zorder=3))
        for x0, y0, x1, y1 in ((0.30, 0.62, 0.48, 0.24),
                               (0.36, 0.68, 0.66, 0.24),
                               (0.40, 0.76, 0.84, 0.28)):
            _arrow(ax, x0, y0, x1, y1)

    return _save(fig, spec.asset_id, dpi=96)


BAR = "#4a7fb5"


def make_experiment_chart(spec) -> Path:
    """Four measured values as numbered bars — the graph a skills set reads.

    The groups carry numbers, not names: the drawing has no Thai glyphs, and a
    numbered bar lets one picture serve several different experiments, with the
    stem saying what the numbers stand for.
    """
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.bar([1, 2, 3, 4], spec.values, color=BAR, edgecolor=AXIS, lw=1.0,
           width=0.62, zorder=3)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_ylim(0, spec.y_max)
    ax.set_xlabel("group", fontsize=10)
    ax.set_ylabel(spec.axis, fontsize=10)
    ax.grid(True, axis="y", color=GRID, lw=0.8, zorder=1)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=9, colors=AXIS)
    for spine in ax.spines.values():
        spine.set_color(AXIS)
    fig.tight_layout()

    return _save(fig, spec.asset_id, dpi=94)


# ── เคมี ม.2: โครมาโทแกรม ─────────────────────────────────────────────────────

GLASS = "#3b4a5a"
LIQUID = "#bcd8f0"
PAPER = "#fbfaf6"
# Spots are lettered as well as coloured, so a worksheet printed in black and
# white still identifies them. The palette only helps them stand apart in colour.
SPOT_COLOURS = ["#d62728", "#1f4fd6", "#2ca02c", "#e6a800"]

# The strip, in axes coordinates. The baseline and the solvent front bracket the
# distance scale, so a spot's y is a straight interpolation of its millimetres.
#
# The figure is deliberately narrow and the content fills it edge to edge. The
# PDF renderer caps a diagram at a tenth of the page height and derives the
# width from the aspect ratio, so empty margins in the asset are paid for twice:
# they shrink the strip *and* the millimetre scale, which has to stay legible or
# chem.rf_value cannot be answered from the picture at all. The front/start
# labels sit above and below rather than to the right for the same reason.
STRIP_X0, STRIP_X1 = 0.34, 0.74
BASE_Y, FRONT_Y = 0.16, 0.84
SCALE_X = 0.26


def make_chromatogram(spec) -> Path:
    """A paper chromatogram with a millimetre scale beside it.

    One lane: a single spot was placed on the baseline and its components have
    run to different heights. The scale is what makes ``chem.rf_value``
    answerable — every distance in ``CHROMA_SPECS`` is a multiple of 5 mm, and
    the grid is drawn at 5 mm, so the values are read off rather than guessed.
    """
    fig, ax = plt.subplots(figsize=(2.9, 3.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def y_of(mm: float) -> float:
        return BASE_Y + (FRONT_Y - BASE_Y) * mm / spec.solvent

    cx = (STRIP_X0 + STRIP_X1) / 2

    # The paper strip
    ax.add_patch(FancyBboxPatch((STRIP_X0, 0.10), STRIP_X1 - STRIP_X0, 0.78,
                                boxstyle="square,pad=0", facecolor=PAPER,
                                edgecolor=GLASS, lw=1.4, zorder=2))

    # The millimetre scale: minor ticks every 5 mm, labels every 10 (or 20 for a
    # 100 mm front, which would otherwise carry ten crowded labels).
    label_step = 10 if spec.solvent <= 60 else 20
    ax.plot([SCALE_X, SCALE_X], [y_of(0), y_of(spec.solvent)],
            color=GLASS, lw=1.2, zorder=3)
    for mm in range(0, spec.solvent + 1, 5):
        major = mm % label_step == 0
        ax.plot([SCALE_X - (0.035 if major else 0.018), SCALE_X],
                [y_of(mm)] * 2, color=GLASS, lw=1.0 if major else 0.7, zorder=3)
        if major:
            ax.text(SCALE_X - 0.05, y_of(mm), str(mm), fontsize=9,
                    ha="right", va="center", color=GLASS)
    # "mm" goes in the corner, clear of the front label centred over the strip
    ax.text(0.03, 0.90, "mm", fontsize=9, ha="left", va="bottom", color=GLASS)

    # Baseline and solvent front, dashed right across so the scale lines up.
    # The captions sit outside the strip, above and below it.
    for y, label, cap_y, va in ((y_of(0), "start line", 0.08, "top"),
                                (y_of(spec.solvent), "solvent front", 0.90, "bottom")):
        ax.plot([SCALE_X, STRIP_X1 + 0.03], [y, y], color=GLASS, lw=0.9,
                ls="--", dashes=(4, 3), zorder=4)
        ax.text(cx, cap_y, label, fontsize=8.5, ha="center", va=va, color=GLASS)

    # The separated components, lettered A upward
    for i, mm in enumerate(spec.spots):
        ax.add_patch(Ellipse((cx, y_of(mm)), 0.30, 0.055,
                             facecolor=SPOT_COLOURS[i % len(SPOT_COLOURS)],
                             edgecolor="none", alpha=0.85, zorder=5))
        ax.text(cx, y_of(mm), chr(ord("A") + i), fontsize=10, ha="center",
                va="center", color="white", fontweight="bold", zorder=6)

    return _save(fig, spec.asset_id, dpi=92)


# ── เคมี ม.2: ชุดอุปกรณ์แยกสาร ────────────────────────────────────────────────

FLAME = "#f0a030"
PAPER_FILL = "#efe7d4"

# Layering is the same in all four drawings: liquid goes down first, the
# glassware outline is stroked over it unfilled, so a fill never paints out the
# line that gives the vessel its shape.
Z_FILL, Z_GLASS, Z_TOP = 2, 4, 6


def _segment(cx, cy, r, y_cut, steps=48):
    """Points of the part of a circle below ``y_cut`` — liquid in a round vessel.

    A ``Wedge`` would join the arc back to the centre and leave a pie-slice
    notch poking up out of the liquid; the flat chord is what a surface is.
    """
    k = max(-1.0, min(1.0, (y_cut - cy) / r))
    a = _math.asin(k)
    lo, hi = _math.pi - a, 2 * _math.pi + a
    return [(cx + r * _math.cos(lo + (hi - lo) * i / steps),
             cy + r * _math.sin(lo + (hi - lo) * i / steps))
            for i in range(steps + 1)]


def _arc_pts(cx, cy, r, deg0, deg1, steps=48):
    return [(cx + r * _math.cos(_math.radians(d)), cy + r * _math.sin(_math.radians(d)))
            for d in [deg0 + (deg1 - deg0) * i / steps for i in range(steps + 1)]]


def _rot(pts, cx, cy, deg):
    c, s = _math.cos(_math.radians(deg)), _math.sin(_math.radians(deg))
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c)
            for x, y in pts]


def _outline(ax, pts, closed=True, lw=1.5):
    ax.add_patch(Polygon(pts, closed=closed, facecolor="none", edgecolor=GLASS,
                         lw=lw, zorder=Z_GLASS))


def _fill(ax, pts, colour=LIQUID):
    ax.add_patch(Polygon(pts, closed=True, facecolor=colour, edgecolor="none",
                         zorder=Z_FILL))


def _burner(ax, x, y):
    """A spirit lamp with its flame, sitting with its base on ``y``."""
    ax.add_patch(Polygon([(x - 0.05, y), (x + 0.05, y),
                          (x + 0.032, y + 0.055), (x - 0.032, y + 0.055)],
                         facecolor="#d9d2c4", edgecolor=GLASS, lw=1.2,
                         zorder=Z_GLASS))
    ax.add_patch(Polygon([(x - 0.022, y + 0.055), (x + 0.022, y + 0.055),
                          (x, y + 0.155)],
                         facecolor=FLAME, edgecolor="none", zorder=Z_TOP))


def _stand(ax, x0, x1, y, foot):
    """The tripod rail a vessel is heated on, with two legs down to ``foot``."""
    ax.plot([x0, x1], [y, y], color=GLASS, lw=2.0, zorder=Z_GLASS)
    for x in (x0 + 0.03, x1 - 0.03):
        ax.plot([x, x], [y, foot], color=GLASS, lw=1.6, zorder=Z_GLASS)


def _beaker(ax, cx, y, w=0.20, h=0.16, fill=0.45):
    """A plain beaker, part filled."""
    if fill:
        _fill(ax, [(cx - w / 2, y), (cx + w / 2, y),
                   (cx + w / 2, y + h * fill), (cx - w / 2, y + h * fill)])
    _outline(ax, [(cx - w / 2, y + h), (cx - w / 2, y), (cx + w / 2, y),
                  (cx + w / 2, y + h)], closed=False, lw=1.4)


def _vapour(ax, x, y):
    """Two little curls of rising vapour."""
    for dx in (-0.045, 0.045):
        xs = [x + dx + 0.014 * _math.sin(i * 0.8) for i in range(10)]
        ys = [y + 0.013 * i for i in range(10)]
        ax.plot(xs, ys, color="#8fa4b8", lw=1.1, zorder=Z_TOP)


def _apparatus_fig():
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def _draw_distillation(ax):
    """Boiling flask over a burner → water-jacketed condenser → receiver."""
    fx, fy, fr = 0.16, 0.34, 0.115
    _burner(ax, fx, 0.05)
    _fill(ax, _segment(fx, fy, fr, fy - 0.02))
    _outline(ax, _arc_pts(fx, fy, fr, 0, 360), closed=True)
    ax.plot([fx, fx], [fy + fr, 0.80], color=GLASS, lw=1.5, zorder=Z_GLASS)
    ax.plot([fx, 0.30], [0.80, 0.80], color=GLASS, lw=1.5, zorder=Z_GLASS)

    # The condenser, as a slab of glass around the sloping inner tube
    sx, sy, ex, ey = 0.30, 0.80, 0.74, 0.52
    dx, dy = ex - sx, ey - sy
    n = _math.hypot(dx, dy)
    px, py = -dy / n * 0.05, dx / n * 0.05            # perpendicular, half-thick
    ax.add_patch(Polygon([(sx + px, sy + py), (ex + px, ey + py),
                          (ex - px, ey - py), (sx - px, sy - py)],
                         facecolor="#e7f1fa", edgecolor=GLASS, lw=1.4,
                         zorder=Z_GLASS))
    ax.plot([sx, ex], [sy, ey], color=GLASS, lw=1.1, zorder=Z_TOP)
    for t in (0.22, 0.78):                           # cooling water in / out
        bx, by = sx + dx * t + px, sy + dy * t + py
        ax.plot([bx, bx + px], [by, by + py], color=GLASS, lw=1.5, zorder=Z_GLASS)

    ax.plot([ex, 0.82, 0.82], [ey, ey - 0.04, 0.36], color=GLASS, lw=1.5,
            zorder=Z_GLASS)                          # delivery tube
    ax.plot([0.82, 0.82], [0.36, 0.30], color=LIQUID, lw=2.4, zorder=Z_TOP)
    _beaker(ax, 0.82, 0.12, fill=0.35)


def _draw_funnel(ax):
    """Separatory funnel: two layers, a stopcock, a receiver under the tap."""
    body = [(0.50, 0.46), (0.55, 0.53), (0.62, 0.63), (0.66, 0.74),
            (0.655, 0.82), (0.62, 0.88), (0.38, 0.88), (0.345, 0.82),
            (0.34, 0.74), (0.38, 0.63), (0.45, 0.53)]
    _fill(ax, [(0.50, 0.47), (0.55, 0.54), (0.62, 0.64), (0.633, 0.68),
               (0.367, 0.68), (0.38, 0.64), (0.45, 0.54)], "#cfe3f5")
    _fill(ax, [(0.367, 0.68), (0.633, 0.68), (0.66, 0.74), (0.655, 0.82),
               (0.345, 0.82), (0.34, 0.74)], "#f6e2b8")
    _outline(ax, body)
    ax.plot([0.367, 0.633], [0.68, 0.68], color=GLASS, lw=1.0, zorder=Z_TOP)
    ax.plot([0.42, 0.42, 0.58, 0.58], [0.88, 0.93, 0.93, 0.88],   # stopper
            color=GLASS, lw=1.4, zorder=Z_GLASS)

    ax.plot([0.50, 0.50], [0.46, 0.32], color=GLASS, lw=1.5, zorder=Z_GLASS)
    ax.add_patch(Circle((0.50, 0.39), 0.027, facecolor="#d9d2c4",
                        edgecolor=GLASS, lw=1.3, zorder=Z_TOP))          # stopcock
    ax.plot([0.452, 0.548], [0.39, 0.39], color=GLASS, lw=1.6, zorder=Z_TOP)
    _beaker(ax, 0.50, 0.10, fill=0.35)


def _draw_filtration(ax):
    """A filter-paper cone in a funnel on a beaker, liquid poured in from a jug."""
    # The jug, tipped over the funnel's mouth. Drawn empty: a level surface
    # inside a rotated vessel is a clipping problem, and a beaker mid-pour reads
    # perfectly well from its tilt and the stream leaving its lip.
    # Sitting the jug above the funnel rather than beside it is what makes the
    # pour read as a pour: a stream that falls further than it travels sideways.
    jug = _rot([(0.20, 0.82), (0.36, 0.82), (0.36, 0.95), (0.20, 0.95)],
               0.28, 0.885, -35)
    _outline(ax, jug, lw=1.4)
    lip = min(jug, key=lambda p: p[1])               # whichever corner tipped lowest
    ax.plot([lip[0], 0.48], [lip[1], 0.63], color=LIQUID, lw=2.4, zorder=Z_TOP)

    cone = [(0.32, 0.66), (0.68, 0.66), (0.50, 0.40)]
    paper = [(0.355, 0.635), (0.645, 0.635), (0.50, 0.435)]
    _fill(ax, paper, PAPER_FILL)
    _outline(ax, cone)
    _outline(ax, paper, lw=1.0)
    ax.plot([0.50, 0.50], [0.635, 0.435], color="#c9bfa4", lw=1.0,
            zorder=Z_TOP)                            # the fold in the paper
    ax.plot([0.50, 0.50], [0.40, 0.28], color=GLASS, lw=1.5, zorder=Z_GLASS)
    ax.plot([0.50, 0.50], [0.28, 0.24], color=LIQUID, lw=2.2, zorder=Z_TOP)
    _beaker(ax, 0.50, 0.06, fill=0.45)


def _draw_evaporation(ax):
    """Shallow dish on a tripod over a burner, vapour leaving the surface."""
    cx, cy, r = 0.50, 0.62, 0.20
    rim = cy + r * _math.sin(_math.radians(200))
    _burner(ax, cx, 0.18)                            # flame just under the dish
    _stand(ax, 0.24, 0.76, rim, 0.12)
    _fill(ax, _segment(cx, cy, r - 0.016, rim - 0.02))
    _outline(ax, _arc_pts(cx, cy, r, 200, 340), closed=False)
    ax.plot([cx - r * 0.94, cx + r * 0.94], [rim, rim], color=GLASS, lw=1.2,
            zorder=Z_GLASS)                          # the rim, seen edge-on
    _vapour(ax, cx, rim + 0.02)


_APPARATUS_DRAW = {
    "distillation": _draw_distillation,
    "funnel": _draw_funnel,
    "filtration": _draw_filtration,
    "evaporation": _draw_evaporation,
}


def make_apparatus(spec) -> Path:
    """One separation set-up. No text at all is drawn on these — the whole point
    of ``chem.apparatus_id`` is to recognise the glassware, and a label would
    both answer the question and need a Thai font."""
    fig, ax = _apparatus_fig()
    _APPARATUS_DRAW[spec.code](ax)
    return _save(fig, spec.asset_id, dpi=92)


# ── ว 2.2: แผนภาพแสดงแรง (free-body diagrams) ────────────────────────────────

# Named apart from the schematic ``BOX`` above: these two live in one module and
# a shared name would repaint every resistor and bulb in the ไฟฟ้า schematics.
FBD_BOX = "#f2d7a8"
WATER = "#cfe6f7"
GROUND = "#8d8d8d"
ARROW = "#c0392b"

# Where each direction's arrow starts on the box, and which way it travels.
_EDGE = {"up": (0.0, 0.5, 0.0, 1.0), "down": (0.0, -0.5, 0.0, -1.0),
         "left": (-0.5, 0.0, -1.0, 0.0), "right": (0.5, 0.0, 1.0, 0.0)}


def _force_arrow(ax, cx, cy, half, arrow, scale, rank=0):
    """One labelled force arrow leaving the box edge, length ∝ its newtons.

    ``rank`` staggers arrows that share a direction — two forces both pointing
    right would otherwise be drawn on top of each other with their labels
    overlapping, which is unreadable and was the first thing this renderer got
    wrong. Horizontal arrows stagger vertically and vice versa.
    """
    ex, ey, dx, dy = _EDGE[arrow.direction]
    shift = 0.07 * rank
    sx, sy = (0.0, shift) if dx else (shift, 0.0)
    x0, y0 = cx + ex * half * 2 + sx, cy + ey * half + sy
    length = arrow.newtons * scale
    x1, y1 = x0 + dx * length, y0 + dy * length
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>,head_width=0.16,head_length=0.32",
                                color=ARROW, lw=2.2))
    ox, oy = (0.035, 0.0) if dx == 0 else (0.0, 0.045)
    ax.text(x1 + dx * 0.02 + ox, y1 + dy * 0.02 + oy,
            f"{arrow.symbol} = {arrow.newtons} N", color=ARROW, fontsize=11,
            ha="left" if dx >= 0 else "right", va="center", zorder=5)


def make_force_diagram(spec) -> Path:
    """One free-body diagram: the scene, the box, and every arrow to scale.

    Arrow length is proportional to the force, so the picture answers the
    question on sight — a resultant to the right really is drawn longer to the
    right. Labels are ASCII symbols plus "N"; the bundled font has no Thai.
    """
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    cx, cy, half = 0.5, 0.5, 0.068
    biggest = max(a.newtons for a in spec.arrows)
    scale = 0.30 / biggest                    # longest arrow ≈ a third of the frame

    if spec.scene == "water":
        ax.add_patch(plt.Rectangle((0.06, 0.12), 0.88, 0.76, facecolor=WATER,
                                   edgecolor="#5a8fb5", lw=1.4, zorder=0))
        ax.plot([0.06, 0.94], [0.88, 0.88], color="#5a8fb5", lw=2, zorder=1)
    elif spec.scene in ("floor", "table"):
        ground = cy - half - 0.005
        ax.plot([0.10, 0.90], [ground, ground], color=GROUND, lw=3, zorder=1)
        for x in [0.10 + 0.08 * i for i in range(11)]:
            ax.plot([x, x - 0.035], [ground, ground - 0.035], color=GROUND,
                    lw=1.2, zorder=1)

    ax.add_patch(plt.Rectangle((cx - half * 2, cy - half), half * 4, half * 2,
                               facecolor=FBD_BOX, edgecolor="#8a6d3b", lw=1.6, zorder=3))
    seen: dict[str, int] = {}
    for arrow in spec.arrows:
        rank = seen.get(arrow.direction, 0)
        seen[arrow.direction] = rank + 1
        _force_arrow(ax, cx, cy, half, arrow, scale, rank)

    return _save(fig, spec.asset_id, dpi=92, bbox_inches="tight")



# ── วิทยาการคำนวณ ป.1-ป.3: โปรแกรมบล็อกบนตาราง ───────────────────────────────

START_FILL = "#2f6fb5"
STAR_FILL = "#f2b705"
BLOCK_FILL = "#e8f0fa"
REPEAT_FILL = "#fdf0d5"
COIN_FILL = "#f5c542"


def _block_arrow(ax, x, y, move, length=0.56):
    """A drawn arrow, not a glyph, so no font is needed for it."""
    dx, dy = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}[move]
    ax.annotate("", xy=(x + dx * length / 2, y + dy * length / 2),
                xytext=(x - dx * length / 2, y - dy * length / 2),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=EDGE, mutation_scale=12))


def make_block_program(spec) -> Path:
    """A 5 x 5 grid with the start (S), an optional star, and numbered arrow blocks.

    Labels are A-E and 1-5 only, and the arrows are drawn shapes, so the picture
    needs no Thai font. Columns run left to right and rows bottom to top, as
    the stems say.
    """
    has_program = bool(spec.blocks)
    if has_program:
        fig, (grid, panel) = plt.subplots(
            1, 2, figsize=(5.6, 3.1), gridspec_kw={"width_ratios": [1.0, 0.75]})
    else:
        fig, grid = plt.subplots(figsize=(3.3, 3.1))
    size = 5
    for i in range(size + 1):
        grid.plot([0, size], [i, i], color=AXIS, lw=0.9)
        grid.plot([i, i], [0, size], color=AXIS, lw=0.9)
    for i, letter in enumerate("ABCDE"):
        grid.text(i + 0.5, -0.32, letter, ha="center", va="center", fontsize=10, color=AXIS)
    for j in range(size):
        grid.text(-0.32, j + 0.5, str(j + 1), ha="center", va="center", fontsize=10, color=AXIS)
    sx, sy = spec.start
    grid.add_patch(Circle((sx + 0.5, sy + 0.5), 0.33, color=START_FILL))
    grid.text(sx + 0.5, sy + 0.5, "S", ha="center", va="center", fontsize=11,
              color="white", fontweight="bold")
    if spec.target is not None:
        tx, ty = spec.target
        grid.plot(tx + 0.5, ty + 0.5, marker="*", markersize=22, color=STAR_FILL,
                  markeredgecolor=EDGE, markeredgewidth=0.8)
    for cx, cy in spec.coins:
        grid.add_patch(Circle((cx + 0.5, cy + 0.5), 0.2, fc=COIN_FILL, ec=EDGE, lw=1.0))
    grid.set_xlim(-0.6, size + 0.1)
    grid.set_ylim(-0.6, size + 0.1)
    grid.set_aspect("equal")
    grid.axis("off")

    if has_program:
        n = len(spec.blocks)
        rows = max(n, 4)
        width = max([1] + [len(b) - 2 for b in spec.blocks if b.startswith("x")])
        right = 1.0 if width == 1 else 0.55 + 0.62 * width
        for i, block in enumerate(spec.blocks):
            y = rows - i - 0.5
            panel.text(0.06, y, str(i + 1), ha="center", va="center", fontsize=10, color=AXIS)
            if block.startswith("x"):
                # A repeat block: its count as "x3", then its moves in one row.
                inner = block[2:]
                panel.add_patch(FancyBboxPatch((0.18, y - 0.4), right - 0.26, 0.8,
                                               boxstyle="round,pad=0.02", fc=REPEAT_FILL, ec=EDGE, lw=1.2))
                panel.text(0.42, y, f"x{block[1]}", ha="center", va="center", fontsize=12,
                           color=EDGE, fontweight="bold")
                for j, move in enumerate(inner):
                    _block_arrow(panel, 0.9 + 0.6 * j, y, move, length=0.46)
            else:
                panel.add_patch(FancyBboxPatch((0.18, y - 0.38), 0.74, 0.76,
                                               boxstyle="round,pad=0.02", fc=BLOCK_FILL, ec=EDGE, lw=1.0))
                _block_arrow(panel, 0.55, y, block)
        panel.set_xlim(0, right)
        panel.set_ylim(rows - n - 0.1, rows + 0.1)
        panel.set_aspect("equal")
        panel.axis("off")
    fig.tight_layout()
    return _save(fig, spec.asset_id, dpi=92)


FLOW_BOX_FILL = "#e8f0fa"
FLOW_TEST_FILL = "#fdf0d5"
FLOW_END_FILL = "#dcefdc"
FLOW_HOLE_FILL = "#fde2e2"
FLOW_W, FLOW_H = 2.0, 0.56          # statement box
FLOW_DW, FLOW_DH = 2.4, 0.9         # decision diamond
FLOW_GAP = 1.0                      # centre to centre down the column


def _flow_node(ax, x, y, shape, label):
    """One flowchart shape centred on (x, y), with its ASCII label."""
    w, h = FLOW_W, FLOW_H
    if shape == "end":
        ax.add_patch(FancyBboxPatch((x - w / 2 + 0.25, y - h / 2 + 0.02), w - 0.5, h - 0.04,
                                    boxstyle="round,pad=0,rounding_size=0.26",
                                    fc=FLOW_END_FILL, ec=EDGE, lw=1.1))
    elif shape == "io":
        skew = 0.16
        ax.add_patch(Polygon([(x - w / 2 + skew, y + h / 2), (x + w / 2 + skew, y + h / 2),
                              (x + w / 2 - skew, y - h / 2), (x - w / 2 - skew, y - h / 2)],
                             closed=True, fc=FLOW_BOX_FILL, ec=EDGE, lw=1.1))
    elif shape == "test":
        dw, dh = FLOW_DW / 2, FLOW_DH / 2
        ax.add_patch(Polygon([(x, y + dh), (x + dw, y), (x, y - dh), (x - dw, y)],
                             closed=True, fc=FLOW_TEST_FILL, ec=EDGE, lw=1.1))
    else:
        fill = FLOW_HOLE_FILL if label == "?" else FLOW_BOX_FILL
        ax.add_patch(Polygon([(x - w / 2, y + h / 2), (x + w / 2, y + h / 2),
                              (x + w / 2, y - h / 2), (x - w / 2, y - h / 2)],
                             closed=True, fc=fill, ec=EDGE, lw=1.1))
    ax.text(x, y, label, ha="center", va="center", fontsize=10.5, family="monospace",
            color=EDGE, fontweight="bold" if label == "?" else "normal")


def _flow_half(shape):
    return FLOW_DH / 2 if shape == "test" else FLOW_H / 2


def _flow_line(ax, pts, head=True):
    """A connector through ``pts``, with an arrowhead on its last segment."""
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=EDGE, lw=1.1)
    if head:
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1.1, mutation_scale=11))


def _flow_column(ax, x, y, nodes):
    """Stack nodes down from y, joining each to the next; returns the centres."""
    centres = []
    for i, (shape, label) in enumerate(nodes):
        if i:
            prev_shape = nodes[i - 1][0]
            _flow_line(ax, [(x, centres[-1] - _flow_half(prev_shape)), (x, y + _flow_half(shape))])
        _flow_node(ax, x, y, shape, label)
        centres.append(y)
        y -= FLOW_GAP
    return centres


def make_flowchart(spec) -> Path:
    """A flowchart in the standard shapes: Start/End, Input/Output, statements, a test.

    Every label is ASCII, so the picture needs no Thai font. A decision's two
    sides meet before the output; a loop's Yes path runs down and returns up the
    left to re-enter above the test, and its No exit leads right to the output.
    """
    top = [("end", "Start"), ("io", "Input x")] + [("box", spec.shown(i)) for i in range(len(spec.setup))]
    tail = [("io", f"Output {spec.out}"), ("end", "End")]
    fig, ax = plt.subplots()
    if not spec.test:
        centres = _flow_column(ax, 0, 0, top + tail)
        x_lo, x_hi, y_lo = -1.4, 1.4, centres[-1]
    else:
        centres = _flow_column(ax, 0, 0, top)
        y_t = centres[-1] - FLOW_GAP - 0.2
        entry = y_t + FLOW_DH / 2 + 0.25
        _flow_line(ax, [(0, centres[-1] - FLOW_H / 2), (0, y_t + FLOW_DH / 2)])
        _flow_node(ax, 0, y_t, "test", spec.test)
        if spec.loop:
            body = [("box", s) for s in spec.yes]
            y_b = y_t - FLOW_GAP - 0.2
            _flow_line(ax, [(0, y_t - FLOW_DH / 2), (0, y_b + FLOW_H / 2)])
            ax.text(0.15, y_t - FLOW_DH / 2 - 0.12, "Yes", ha="left", va="center", fontsize=9, color=EDGE)
            body_centres = _flow_column(ax, 0, y_b, body)
            low = body_centres[-1] - FLOW_H / 2 - 0.3
            _flow_line(ax, [(0, body_centres[-1] - FLOW_H / 2), (0, low), (-1.7, low),
                            (-1.7, entry), (-0.04, entry)])
            out_x = 2.6
            ax.text(FLOW_DW / 2 + 0.2, y_t + 0.14, "No", ha="left", va="bottom", fontsize=9, color=EDGE)
            _flow_line(ax, [(FLOW_DW / 2, y_t), (out_x, y_t), (out_x, y_t - FLOW_GAP - 0.2 + FLOW_H / 2)])
            ends = _flow_column(ax, out_x, y_t - FLOW_GAP - 0.2, tail)
            x_lo, x_hi, y_lo = -2.0, out_x + 1.25, min(low, ends[-1])
        else:
            side = 1.5
            y_s = y_t - FLOW_GAP - 0.2
            for sign, word, steps in ((-1, "Yes", spec.yes), (1, "No", spec.no)):
                sx = sign * side
                _flow_line(ax, [(sign * FLOW_DW / 2, y_t), (sx, y_t), (sx, y_s + FLOW_H / 2)])
                ax.text(sign * (FLOW_DW / 2 + 0.05), y_t + 0.12, word, ha="right" if sign < 0 else "left",
                        va="bottom", fontsize=9, color=EDGE)
                _flow_node(ax, sx, y_s, "box", steps[0])
                y_m = y_s - FLOW_H / 2 - 0.3
                _flow_line(ax, [(sx, y_s - FLOW_H / 2), (sx, y_m), (0, y_m)], head=False)
            y_o = y_m - 0.2 - FLOW_H / 2 - 0.3
            _flow_line(ax, [(0, y_m), (0, y_o + FLOW_H / 2)])
            ends = _flow_column(ax, 0, y_o, tail)
            x_lo, x_hi, y_lo = -side - 1.1, side + 1.1, ends[-1]
    y_lo -= FLOW_H / 2 + 0.1
    y_hi = FLOW_H / 2 + 0.1
    ax.set_xlim(x_lo - 0.1, x_hi + 0.1)
    ax.set_ylim(y_lo, y_hi)
    ax.set_aspect("equal")
    ax.axis("off")
    scale = 0.62
    fig.set_size_inches((x_hi - x_lo + 0.2) * scale, (y_hi - y_lo) * scale)
    fig.subplots_adjust(0, 0, 1, 1)
    return _save(fig, spec.asset_id, dpi=100)


def main() -> None:
    """Draw every registered diagram — science and math — into the output dir."""
    from ..diagrams import diagram_path, registry
    for asset_id in registry():
        print("wrote", diagram_path(asset_id))


if __name__ == "__main__":
    main()


PLACE_FILL = "#2f6fb5"
BOARD_FILL = "#3d6b4f"


def make_grid_map(spec) -> Path:
    """Lettered places on a grid: a community map with a north arrow, or a
    classroom plan whose top edge is the board.

    Labels are A-H and N only, so the picture needs no Thai font. The stems
    name what each letter stands for.
    """
    size = spec.size
    fig, ax = plt.subplots(figsize=(3.6, 3.4))
    for i in range(size + 1):
        ax.plot([0, size], [i, i], color=AXIS, lw=0.8)
        ax.plot([i, i], [0, size], color=AXIS, lw=0.8)
    for letter, (x, y) in zip("ABCDEFGH", spec.places):
        ax.add_patch(Circle((x + 0.5, y + 0.5), 0.34, color=PLACE_FILL))
        ax.text(x + 0.5, y + 0.5, letter, ha="center", va="center", fontsize=12,
                color="white", fontweight="bold")
    if spec.board:
        ax.add_patch(FancyBboxPatch((size * 0.2, size + 0.18), size * 0.6, 0.32,
                                    boxstyle="round,pad=0.02", fc=BOARD_FILL, ec=EDGE, lw=1.0))
        right = size + 0.1
    else:
        # North arrow beside the grid, pointing up.
        cx = size + 0.55
        ax.add_patch(Polygon([(cx, size - 0.2), (cx - 0.22, size - 0.85), (cx + 0.22, size - 0.85)],
                             closed=True, fc=EDGE, ec=EDGE))
        ax.plot([cx, cx], [size - 0.85, size - 1.5], color=EDGE, lw=2)
        ax.text(cx, size + 0.12, "N", ha="center", va="center", fontsize=13,
                color=EDGE, fontweight="bold")
        right = size + 1.0
    ax.set_xlim(-0.1, right)
    ax.set_ylim(-0.1, size + 0.6)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    return _save(fig, spec.asset_id, dpi=92)
