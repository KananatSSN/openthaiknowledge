"""ม.4–ม.6 math sets read off a drawing: Venn diagrams, sine graphs, box plots,
scatter plots and a shaded normal curve.

Same contract as :mod:`.math_diagrams`: each family is a finite tuple of specs,
``otk/pictures/math_diagrams.py`` draws one PNG per spec,
and a question computes its answer from the spec it shows. Labels are numbers,
ASCII letters and set symbols; alt text is the same for every item of a set, so
it cannot carry the reading.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple


def _neg(n: int) -> str:
    return f"n{-n}" if n < 0 else str(n)


# ══ Specs ════════════════════════════════════════════════════════════════════

class Venn2(NamedTuple):
    a_only: int
    both: int
    b_only: int
    neither: int

    @property
    def asset_id(self) -> str:
        return f"mvenn_{self.a_only}_{self.both}_{self.b_only}_{self.neither}"


def _venns() -> tuple[Venn2, ...]:
    rng = Random(20260925)           # fixed: part of the shipped content
    out = set()
    while len(out) < 18:
        out.add(Venn2(rng.randint(2, 20), rng.randint(1, 12), rng.randint(2, 20), rng.randint(0, 15)))
    return tuple(sorted(out))


VENNS = _venns()


class SineGraph(NamedTuple):
    fn: str        # "sin" | "cos"
    a: int         # amplitude (sign included)
    b: int         # angular frequency: period 360/b degrees

    @property
    def asset_id(self) -> str:
        return f"mtrig_{self.fn}_{_neg(self.a)}_{self.b}"


SINE_GRAPHS = tuple(SineGraph(fn, a, b) for fn in ("sin", "cos") for a, b in (
    (1, 1), (2, 1), (3, 2), (-2, 1), (1, 2), (4, 3), (2, 4), (-1, 2)))


class BoxPlot(NamedTuple):
    lo: int
    q1: int
    med: int
    q3: int
    hi: int

    @property
    def asset_id(self) -> str:
        return f"mbox_{self.lo}_{self.q1}_{self.med}_{self.q3}_{self.hi}"


def _boxes() -> tuple[BoxPlot, ...]:
    rng = Random(20260926)
    out = []
    while len(out) < 18:
        pts = sorted(rng.sample(range(10, 100, 2), 5))
        if len(set(b - a for a, b in zip(pts, pts[1:]))) > 1 and min(b - a for a, b in zip(pts, pts[1:])) >= 4:
            out.append(BoxPlot(*pts))
    return tuple(out)


BOX_PLOTS = _boxes()
BOX_ALT = "แผนภาพกล่องบนเส้นจำนวนที่มีขีดทุก 2 หน่วย กำกับทุก 10 หน่วย"


class Scatter(NamedTuple):
    trend: str      # "strong_pos" | "weak_pos" | "strong_neg" | "weak_neg" | "none"
    seed: int

    @property
    def asset_id(self) -> str:
        return f"mscatter_{self.trend}_{self.seed}"


SCATTERS = tuple(Scatter(t, s) for t in ("strong_pos", "weak_pos", "strong_neg", "weak_neg", "none")
                 for s in (1, 2, 3))


class NormalShade(NamedTuple):
    lo: int      # z, or -9 for −∞
    hi: int      # z, or 9 for +∞

    @property
    def asset_id(self) -> str:
        return f"mnormal_{_neg(self.lo)}_{_neg(self.hi)}"


# Area under the standard normal curve between the bounds, in percent, by the
# 68–95–99.7 rule.
NORMAL_AREAS = {(-1, 1): Fraction(68), (-2, 2): Fraction(95), (-3, 3): Fraction(997, 10),
                (0, 1): Fraction(34), (-1, 0): Fraction(34), (0, 2): Fraction(95, 2),
                (-2, 0): Fraction(95, 2), (1, 2): Fraction(27, 2), (-2, -1): Fraction(27, 2),
                (0, 9): Fraction(50), (-9, 0): Fraction(50), (1, 9): Fraction(16), (-9, -1): Fraction(16),
                (2, 9): Fraction(5, 2), (-9, -2): Fraction(5, 2), (-1, 2): Fraction(163, 2)}
NORMALS = tuple(NormalShade(lo, hi) for lo, hi in NORMAL_AREAS)

ALL_HI_DIAGRAMS = VENNS + SINE_GRAPHS + BOX_PLOTS + SCATTERS + NORMALS


# ══ Sets ═════════════════════════════════════════════════════════════════════


