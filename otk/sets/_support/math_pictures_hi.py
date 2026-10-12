"""Pictures for topics that had none: an area model for ×, a balance for
equations, fractions on a number line, a double bar chart, a dot plot and a
histogram.

Drawn by ``otk/pictures/hi_pictures.py``; labels are
digits and the letters A–E, and the stem says what the letters stand for.
"""

from __future__ import annotations

from fractions import Fraction
from typing import NamedTuple

# ── ป.3 area model ───────────────────────────────────────────────────────────

class AreaModel(NamedTuple):
    a: int               # two-digit factor, split into tens and ones
    b: int               # one-digit factor

    @property
    def asset_id(self) -> str:
        return f"pam_{self.a}_{self.b}"


AREA_MODELS = tuple(AreaModel(10 * t + o, b) for t in (1, 2, 3, 4) for o in range(1, 10, 2)
                    for b in (3, 4, 6, 7, 8) if (t + o + b) % 3 == 0)


# ── ม.1 balance ──────────────────────────────────────────────────────────────

class Balance(NamedTuple):
    """``a`` boxes and ``b`` weights on the left balance ``c`` boxes and ``d`` on the right."""
    a: int
    b: int
    c: int
    d: int

    @property
    def asset_id(self) -> str:
        return f"pbal_{self.a}_{self.b}_{self.c}_{self.d}"

    @property
    def x(self) -> int:
        return (self.d - self.b) // (self.a - self.c)


def _balances() -> tuple[Balance, ...]:
    out = []
    for a in (1, 2, 3, 4):
        for c in range(0, a):
            for x in (1, 2, 3, 4, 5):
                for b in (0, 1, 2, 3, 5):
                    d = (a - c) * x + b
                    if (d <= 12 and (a + b) <= 9 and (c + d) <= 14 and (a + c + x + b) % 2 == 0
                            and (b or c)):        # not already solved: x = d
                        out.append(Balance(a, b, c, d))
    return tuple(out)


BALANCES = _balances()


# ── ม.1 fractions on a number line ───────────────────────────────────────────

class FracLine(NamedTuple):
    d: int               # ticks per unit
    k: int               # the point is at k / d

    @property
    def asset_id(self) -> str:
        return f"pfl_{self.d}_{'n' if self.k < 0 else ''}{abs(self.k)}"

    @property
    def value(self) -> Fraction:
        return Fraction(self.k, self.d)


FRAC_LINES = tuple(FracLine(d, k) for d in (2, 3, 4, 5, 6) for k in range(-2 * d + 1, 2 * d)
                   if k % d and (k + d) % 2 == 0)


# ── ม.1 double bar chart ─────────────────────────────────────────────────────


class DoubleBars(NamedTuple):
    first: tuple[int, ...]           # the blue bar in each category
    second: tuple[int, ...]          # the orange bar

    @property
    def asset_id(self) -> str:
        return "pdb_" + "_".join(f"{a}-{b}" for a, b in zip(self.first, self.second))


def _double_bars() -> tuple[DoubleBars, ...]:
    out = []
    for i in range(40):
        n = 3 + i % 3
        first = tuple(5 * (1 + (i * 3 + j * 5) % 8) for j in range(n))
        second = tuple(5 * (1 + (i * 7 + j * 3 + 2) % 8) for j in range(n))
        out.append(DoubleBars(first, second))
    return tuple(dict.fromkeys(out))


DOUBLE_BARS = _double_bars()


# ── ม.2 dot plot ─────────────────────────────────────────────────────────────

class DotPlot(NamedTuple):
    start: int
    counts: tuple[int, ...]          # dots above start, start + 1, …

    @property
    def asset_id(self) -> str:
        return f"pdp_{self.start}_" + "".join(str(c) for c in self.counts)

    @property
    def data(self) -> list[int]:
        return [self.start + i for i, c in enumerate(self.counts) for _ in range(c)]


def _dot_plots() -> tuple[DotPlot, ...]:
    out = []
    for i in range(40):
        width = 6 + i % 3
        counts = [(i * 5 + j * 7) % 5 for j in range(width)]
        peak = (i * 3) % width
        counts[peak] = max(counts) + 1                 # one clear mode
        out.append(DotPlot(i % 4, tuple(counts)))
    return tuple(dict.fromkeys(out))


DOT_PLOTS = _dot_plots()


# ── ม.2 histogram ────────────────────────────────────────────────────────────

class Histogram(NamedTuple):
    low: int                          # first class starts here
    width: int
    freq: tuple[int, ...]

    @property
    def asset_id(self) -> str:
        return f"phg_{self.low}_{self.width}_" + "_".join(map(str, self.freq))

    def label(self, i: int) -> str:
        a = self.low + i * self.width
        return f"{a} – {a + self.width - 1}"


def _histograms() -> tuple[Histogram, ...]:
    out = []
    for i in range(36):
        low, width = ((20, 10), (30, 10), (140, 5), (40, 10))[i % 4]
        n = 5 + i % 2
        freq = [2 + (i * 5 + j * 3) % 9 for j in range(n)]
        peak = (i + 2) % n
        freq[peak] = max(freq) + 2
        out.append(Histogram(low, width, tuple(freq)))
    return tuple(dict.fromkeys(out))


HISTOGRAMS = _histograms()


ALL_PICTURE_IDS = tuple(s.asset_id for s in (*AREA_MODELS, *BALANCES, *FRAC_LINES, *DOUBLE_BARS,
                                             *DOT_PLOTS, *HISTOGRAMS))
