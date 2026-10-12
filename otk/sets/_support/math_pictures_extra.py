"""More topics read off a picture: sides and corners of a drawn shape (ป.2),
change from money shown (ป.3), fraction bars (ป.4), hundred-square grids for
decimals (ป.4) and percentages (ป.5), and a coloured spinner (ม.3).

The shape and money questions reuse pictures that already ship; the rest are
drawn by ``otk/pictures/extra_pictures.py``.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random
from typing import NamedTuple


def _fr(n: int, d: int) -> str:
    return rf"\frac{{{n}}}{{{d}}}"


# ── ป.2 รูปเรขาคณิต ───────────────────────────────────────────────────────────


class PolygonPic(NamedTuple):
    """A convex polygon with 3–8 sides. Variant 0 is regular and upright,
    1 the same shape turned, 2 and 3 irregular, so a learner counts sides
    rather than recognising one familiar drawing."""
    sides: int
    variant: int

    @property
    def asset_id(self) -> str:
        return f"mpoly2_{self.sides}_{self.variant}"

    @property
    def points(self) -> list[tuple[float, float]]:
        n, step = self.sides, 360 / self.sides
        if self.variant < 2:
            start = 90 + (step / 2 if self.variant else 0)
            angles = [start + step * i for i in range(n)]
            stretch = 1.0
        else:
            # Corners on a stretched circle stay convex. Each gap between
            # corners is kept between 0.6 and 1.4 steps, so no corner is so
            # flat that it reads as part of a straight side.
            jitter = Random(n * 10 + self.variant)
            gaps = [step * jitter.uniform(0.6, 1.4) for _ in range(n)]
            gaps = [g * 360 / sum(gaps) for g in gaps]
            angles, a = [], jitter.uniform(0, 360)
            for g in gaps:
                angles.append(a)
                a += g
            stretch = 1.35 if self.variant == 2 else 0.8
        return [(round(math.cos(math.radians(t)) * stretch, 4), round(math.sin(math.radians(t)), 4))
                for t in angles]


POLYGON_PICS = tuple(PolygonPic(n, v) for n in range(3, 9) for v in range(4))


# ── ป.3 เงิน ─────────────────────────────────────────────────────────────────


# ── ป.4 เศษส่วน ──────────────────────────────────────────────────────────────

class Bars(NamedTuple):
    d: int               # parts per bar
    wholes: int          # fully shaded bars
    part: int            # shaded parts in the last bar

    @property
    def asset_id(self) -> str:
        return f"pfb_{self.d}_{self.wholes}_{self.part}"

    @property
    def value(self) -> Fraction:
        return self.wholes + Fraction(self.part, self.d)


BARS = tuple(Bars(d, w, p) for d in (2, 3, 4, 5, 6, 8) for w in (1, 2, 3)
             for p in range(1, d) if (d + w + p) % 2 == 0 or d <= 4)


# ── ป.4 ทศนิยม และ ป.5 ร้อยละ ────────────────────────────────────────────────

class Grid(NamedTuple):
    wholes: int          # fully shaded hundred-squares
    hundredths: int      # shaded small squares in the last one

    @property
    def asset_id(self) -> str:
        return f"pgr_{self.wholes}_{self.hundredths}"


GRIDS = tuple(dict.fromkeys(
    [Grid(0, h) for h in (3, 7, 9, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 64, 70, 75, 80, 88, 90, 99)]
    + [Grid(w, (i * 37) % 99 + 1) for i, w in enumerate([1] * 12 + [2] * 8)]))
GRID_ALT = "ภาพตารางร้อยช่อง บางช่องแรเงา"


# ── ม.3 ความน่าจะเป็น ────────────────────────────────────────────────────────

COLOURS = {"red": "สีแดง", "blue": "สีฟ้า", "green": "สีเขียว", "yellow": "สีเหลือง"}


class Spinner(NamedTuple):
    sectors: tuple[str, ...]           # colour of each equal sector, clockwise

    @property
    def asset_id(self) -> str:
        return "psp_" + "".join(c[0] for c in self.sectors)

    def count(self, colour: str) -> int:
        return self.sectors.count(colour)


def _spinners() -> tuple[Spinner, ...]:
    out = []
    names = list(COLOURS)
    for i in range(48):
        n = (4, 5, 6, 8, 10, 12)[i % 6]
        k = 2 + i % 3                                  # two to four colours
        used = [names[(i + j) % 4] for j in range(k)]
        sectors = [used[(j * (i % 5 + 1) + j // 3) % k] for j in range(n)]
        for c in used:                                 # every chosen colour appears
            if c not in sectors:
                sectors[-1 - used.index(c)] = c
        out.append(Spinner(tuple(sectors)))
    return tuple(dict.fromkeys(out))


SPINNERS = _spinners()


ALL_PICTURE_IDS = tuple(s.asset_id for s in (*POLYGON_PICS, *BARS, *GRIDS, *SPINNERS))
