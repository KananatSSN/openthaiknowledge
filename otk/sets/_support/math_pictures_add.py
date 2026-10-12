"""Pictures for the สสวท. เพิ่มเติม track (ม.4–ม.6), which had almost none.

A graph read off a grid before the algebra that produces it: the solution set
of a quadratic inequality, |x| graphs, circles, exponential and log curves,
vectors, the unit circle, a cosine-rule triangle, one-sided limits, where f'
changes sign, and the area between two curves.

Drawn by ``otk/pictures/add_pictures.py``. Labels are
digits, ASCII and single letters; answers are computed from the same spec the
picture was drawn from.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from typing import NamedTuple

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.sets._support.math_diagrams import _neg


def _fr(f: Fraction) -> str:
    if f.denominator == 1:
        return str(f.numerator)
    sign = "-" if f < 0 else ""
    return rf"{sign}\frac{{{abs(f.numerator)}}}{{{f.denominator}}}"


def _sqrt(n: int) -> str:
    """√n in simplest form: 12 -> 2\\sqrt{3}, 16 -> 4."""
    out, rest = 1, n
    for p in range(2, isqrt(n) + 1):
        while rest % (p * p) == 0:
            out, rest = out * p, rest // (p * p)
    if rest == 1:
        return str(out)
    return (f"{out}" if out > 1 else "") + rf"\sqrt{{{rest}}}"


def _shift(v: int, var: str = "x") -> str:
    """x - 3 / x + 2 / x, for (x - h)."""
    if v == 0:
        return var
    return f"{var} - {v}" if v > 0 else f"{var} + {-v}"


def _plus(k: int) -> str:
    return "" if k == 0 else (f" + {k}" if k > 0 else f" - {-k}")


def _q(stem: list, correct: str, wrongs: list[str], topic: str, pad: list[str]) -> GeneratedQuestion:
    """Four tex choices: the named mistakes, then ``pad`` until there are three."""
    out = [w for w in dict.fromkeys(wrongs) if w != correct]
    for p in pad:
        if len(out) >= 3:
            break
        if p != correct and p not in out:
            out.append(p)
    return GeneratedQuestion(stem=stem, correct=[content_math(correct)],
                             distractors=fixed(*[[content_math(w)] for w in out[:3]]), topic=topic)


# ── ม.4 อสมการกำลังสอง: solution set from the graph ─────────────────────────────

class QuadIneq(NamedTuple):
    """y = a(x - r1)(x - r2), drawn; only the sign of a and the roots matter."""
    a: int
    r1: int
    r2: int

    @property
    def asset_id(self) -> str:
        return f"mqi_{_neg(self.a)}_{_neg(self.r1)}_{_neg(self.r2)}"


QUAD_INEQS = tuple(QuadIneq(a, r1, r2) for a in (1, -1)
                   for r1, r2 in ((-3, 1), (-2, 2), (-1, 3), (0, 4), (-4, 0), (-2, 1),
                                  (1, 4), (-3, 2), (-1, 2), (-5, -1), (2, 5)))


# ── ม.4 ค่าสัมบูรณ์: y = a|x - h| + k ────────────────────────────────────────────

class AbsGraph(NamedTuple):
    a: int
    h: int
    k: int

    @property
    def asset_id(self) -> str:
        return f"mabs_{_neg(self.a)}_{_neg(self.h)}_{_neg(self.k)}"


ABS_GRAPHS = tuple(AbsGraph(a, h, k) for a in (1, -1, 2, -2) for h in (-3, -1, 2, 3)
                   for k in (-3, -2, 1, 3) if (a > 0) == (k < 2) or abs(a) == 1)


# ── ม.4 สมการวงกลม: a circle on the grid ─────────────────────────────────────────

class CircleGrid(NamedTuple):
    h: int
    k: int
    r: int

    @property
    def asset_id(self) -> str:
        return f"mcirc_{_neg(self.h)}_{_neg(self.k)}_{self.r}"


CIRCLE_GRIDS = tuple(CircleGrid(h, k, r) for r in (2, 3, 4) for h in (-3, -2, -1, 1, 2, 3)
                     for k in (-3, -2, -1, 1, 2, 3)
                     if abs(h) + r <= 6 and abs(k) + r <= 6 and (h * 3 + k * 5 + r) % 4 != 0)


# ── ม.4 ลอการิทึม: which exponential or log curve ───────────────────────────────

_BASES = (Fraction(2), Fraction(3), Fraction(1, 2), Fraction(1, 3))


class ExpLogGraph(NamedTuple):
    kind: str            # "exp" or "log"
    base: Fraction
    k: int               # vertical shift

    @property
    def asset_id(self) -> str:
        return f"mexp_{self.kind}_{self.base.numerator}_{self.base.denominator}_{_neg(self.k)}"


EXP_LOG_GRAPHS = tuple(ExpLogGraph(kind, b, k) for kind in ("exp", "log") for b in _BASES
                       for k in (-2, 0, 1, 2))


# ── ม.5 เวกเตอร์: arrows on the grid ─────────────────────────────────────────────

class VectorGrid(NamedTuple):
    ux: int
    uy: int
    vx: int
    vy: int

    @property
    def asset_id(self) -> str:
        return "mvec_" + "_".join(_neg(n) for n in self)


def _vector_grids() -> tuple[VectorGrid, ...]:
    comps = [n for n in range(-4, 5) if n]
    out = []
    for ux in comps:
        for uy in comps:
            for vx in comps:
                for vy in comps:
                    if (ux * vy - uy * vx) and (ux * 7 + uy * 3 + vx * 5 + vy * 11) % 41 == 0:
                        out.append(VectorGrid(ux, uy, vx, vy))
    return tuple(out)


VECTOR_GRIDS = _vector_grids()


# ── ม.5 ฟังก์ชันตรีโกณมิติ: a point on the unit circle ──────────────────────────

UNIT_ANGLES = (30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330)


class UnitPoint(NamedTuple):
    deg: int

    @property
    def asset_id(self) -> str:
        return f"munit_{self.deg}"

    @property
    def ref(self) -> int:
        return min(self.deg % 180, 180 - self.deg % 180)


UNIT_POINTS = tuple(UnitPoint(d) for d in UNIT_ANGLES)


# ── ม.5 กฎของโคไซน์: a labelled triangle ─────────────────────────────────────────

class CosTriangle(NamedTuple):
    """Triangle with side a opposite angle A. ``hide`` draws side a as x and A in degrees;
    otherwise every side is labelled and A is marked θ."""
    a: int
    b: int
    c: int
    hide: bool

    @property
    def asset_id(self) -> str:
        return f"mcos_{self.a}_{self.b}_{self.c}_{int(self.hide)}"

    @property
    def cos_a(self) -> Fraction:
        return Fraction(self.b * self.b + self.c * self.c - self.a * self.a, 2 * self.b * self.c)


# 60° and 120° triangles with whole sides, and scalene triangles for cos θ.
_NICE = ((7, 3, 8), (7, 5, 8), (13, 7, 15), (13, 8, 15), (19, 5, 21), (19, 16, 21),
         (7, 3, 5), (13, 7, 8), (19, 5, 16), (14, 6, 10), (31, 11, 24))
_PLAIN = ((6, 4, 5), (8, 5, 7), (9, 7, 8), (5, 4, 6), (7, 5, 6), (10, 6, 9), (4, 5, 6),
          (6, 5, 8), (11, 7, 9), (3, 4, 6))
COS_TRIANGLES = (tuple(CosTriangle(*t, True) for t in _NICE)
                 + tuple(CosTriangle(*t, False) for t in _NICE + _PLAIN))


# ── ม.6 ลิมิต: one-sided limits read off a graph ────────────────────────────────

class LimitGraph(NamedTuple):
    """Line through (c, left) for x < c, line through (c, right) for x > c, f(c) = at."""
    c: int
    left: int
    right: int
    at: int
    ml: int
    mr: int

    @property
    def asset_id(self) -> str:
        return "mlim_" + "_".join(_neg(n) for n in self)


def _limit_graphs() -> tuple[LimitGraph, ...]:
    out = []
    for c in (-2, 1, 2, 3):
        for left, right, at in ((2, 2, 2), (3, 3, -1), (1, 4, 4), (4, 1, 1), (-1, 2, -1),
                                (2, -2, 0), (0, 0, 3), (3, -1, 3), (-2, 3, 1)):
            for ml, mr in ((1, -1), (-1, 1), (1, 1)):
                if (c + left * 3 + right + ml * 2 + mr) % 3 == 0:
                    out.append(LimitGraph(c, left, right, at, ml, mr))
    return tuple(out)


LIMIT_GRAPHS = _limit_graphs()


# ── ม.6 ค่าสูงสุด-ต่ำสุดสัมพัทธ์: where f' changes sign ─────────────────────────

class DerivCurve(NamedTuple):
    """A cubic with f'(x) = s(x - p)(x - q), and five lettered points at ``xs``."""
    s: int
    p: int
    q: int
    xs: tuple

    @property
    def asset_id(self) -> str:
        return f"mder_{_neg(self.s)}_{_neg(self.p)}_{_neg(self.q)}_" + "_".join(
            _neg(round(4 * x)) for x in self.xs)


def _deriv_curves() -> tuple[DerivCurve, ...]:
    out = []
    for s in (1, -1):
        for p, q in ((-2, 1), (-1, 2), (-3, 0), (0, 3), (-2, 2)):
            mid = (p + q) / 2
            # two outside and one between, or one outside and two between
            for xs in ((p - 1.5, p, mid, q, q + 1.5), (p - 1.5, p, p + 0.5, q - 0.5, q),
                       (p, p + 0.5, q, q + 0.75, q + 1.5)):
                out.append(DerivCurve(s, p, q, tuple(xs)))
    return tuple(out)


DERIV_CURVES = _deriv_curves()


# ── ม.6 พื้นที่ระหว่างเส้นโค้ง: the shaded region ──────────────────────────────

class AreaRegion(NamedTuple):
    """kind: cap (y = n - x² and the x-axis), line (y = x² and y = nx),
    level (y = x² and y = n), lens (y = x² and y = 2n - x²)."""
    kind: str
    n: int

    @property
    def asset_id(self) -> str:
        return f"marea_{self.kind}_{self.n}"

    @property
    def bounds(self) -> tuple[int, int]:
        if self.kind == "line":
            return 0, self.n
        r = isqrt(self.n)
        return -r, r

    @property
    def area(self) -> Fraction:
        lo, hi = self.bounds
        if self.kind == "line":
            return Fraction(self.n ** 3, 6)
        w = hi - lo
        return {"cap": Fraction(2, 3) * self.n * w, "level": Fraction(2, 3) * self.n * w,
                "lens": Fraction(4, 3) * self.n * w}[self.kind]

    @property
    def box(self) -> Fraction:
        """The rectangle around the region — subtracting from it is a common slip."""
        lo, hi = self.bounds
        height = {"cap": self.n, "line": self.n * self.n, "level": self.n, "lens": 2 * self.n}[self.kind]
        return Fraction((hi - lo) * height)

    def curves(self) -> tuple[str, str]:
        n = self.n
        return {"cap": (f"y = {n} - x^{{2}}", "y = 0"), "line": ("y = x^{2}", f"y = {n}x" if n > 1 else "y = x"),
                "level": ("y = x^{2}", f"y = {n}"), "lens": ("y = x^{2}", f"y = {2 * n} - x^{{2}}")}[self.kind]


AREA_REGIONS = (tuple(AreaRegion(k, n) for k in ("cap", "level", "lens") for n in (1, 4, 9))
                + tuple(AreaRegion("line", n) for n in (1, 2, 3, 4)))


ALL_ADD_PICTURES = (QUAD_INEQS + ABS_GRAPHS + CIRCLE_GRIDS + EXP_LOG_GRAPHS + VECTOR_GRIDS
                    + UNIT_POINTS + COS_TRIANGLES + LIMIT_GRAPHS + DERIV_CURVES + AREA_REGIONS)
