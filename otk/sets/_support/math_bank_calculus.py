"""Calculus sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found four units, exercised by กสพท and A-level questions in
``openthaiknowledge-bank/rathcenter/15 แคลคูลัส``, that no problem set practised. The
existing sets hand over the function and ask for its derivative, extremum,
tangent or area; the exams run the other way:

=====================================  ==========================================  ========================
unit                                   set                                         topic
=====================================  ==========================================  ========================
calculus.parabola-area                 math.parabola_area_m6                       พื้นที่
calculus.cubic-critical-points         math.cubic_critical_points_m6               ค่าสูงสุด-ต่ำสุดสัมพัทธ์
calculus.tangent-conditions            math.tangent_conditions_m6                  เส้นสัมผัส
derivative.inverse-product             math.derivative_inverse_product_m6          อนุพันธ์
=====================================  ==========================================  ========================

Every function is a polynomial (or k/(x + d)) with rational coefficients, so
all arithmetic is exact. ``test_math_bank_calculus.py`` re-derives each answer
with SymPy (integrals, derivatives, inverse functions, sign charts) and pins
the source exams' answers.
"""

from __future__ import annotations

from fractions import Fraction

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.kit.math_problems import frac_tex

M6 = {"th": "ม.6"}


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Named mistakes first; duplicates and the answer itself dropped; three kept."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _num_q(stem: list, right, named: list, topic: str) -> GeneratedQuestion:
    right = Fraction(right)
    pool = [*named, right + 1, right - 1, right * 2, -right, right + 2]
    return _tex_q(stem, frac_tex(right), [frac_tex(Fraction(w)) for w in pool if w is not None], topic)


def poly_tex(coefs: list[Fraction], var: str = "x") -> str:
    """Highest power first: [1, 0, -3, 2] → x^{3} - 3x + 2."""
    deg = len(coefs) - 1
    out = ""
    for i, c in enumerate(coefs):
        c = Fraction(c)
        if c == 0:
            continue
        p = deg - i
        mag = abs(c)
        body = ("" if mag == 1 and p else frac_tex(mag)) + (var if p else "") + (f"^{{{p}}}" if p > 1 else "")
        if not out:
            out = ("-" if c < 0 else "") + body
        else:
            out += f" {'-' if c < 0 else '+'} {body}"
    return out or "0"


# ── Parabolas from enclosed areas ────────────────────────────────────────────

def parabola_area(c: Fraction, a: Fraction) -> Fraction:
    """Area between y = c − ax² (a, c > 0) and the x-axis, times 1: (4/3)·c·r with r = √(c/a) (must be rational)."""
    r2 = c / a
    r = _rational_sqrt(r2)
    return Fraction(4, 3) * c * r


def _rational_sqrt(q: Fraction) -> Fraction:
    from math import isqrt
    n, d = isqrt(q.numerator), isqrt(q.denominator)
    if n * n != q.numerator or d * d != q.denominator:
        raise ValueError(q)
    return Fraction(n, d)


def a_from_area(c: Fraction, area: Fraction) -> Fraction:
    """a for y = ax² − c (vertex (0, −c)) enclosing the given area with the x-axis: r = 3A/(4c), a = c/r²."""
    r = 3 * area / (4 * c)
    return c / (r * r)


def k_from_area(area: Fraction) -> Fraction:
    """k for y = k − x² enclosing the given area: (4/3)k^(3/2) = A, so k³ = (3A/4)² (a whole cube here)."""
    cube = (3 * Fraction(area) / 4) ** 2
    root = Fraction(round(float(cube) ** (1 / 3)))
    if root ** 3 != cube:
        raise ValueError(area)
    return root


# ── Cubics from their critical points ────────────────────────────────────────


def peval(coefs: list[Fraction], x) -> Fraction:
    v = Fraction(0)
    for cf in coefs:
        v = v * x + cf
    return v


# ── Tangents fixed by a slope or a line ──────────────────────────────────────


# ── Inverse-function derivatives and the product rule backwards ─────────────


