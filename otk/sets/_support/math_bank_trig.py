"""Trigonometry sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found six units, exercised by A-level and กสพท questions in
``openthaiknowledge-bank/rathcenter/8 ตรีโกณมิติ``, that no problem set practised:

=====================================  ==========================================  ================================
unit                                   set                                         topic
=====================================  ==========================================  ================================
trig.right-triangle-relations          math.right_triangle_relations_m5            อัตราส่วนตรีโกณมิติ
trig.radian-arc                        math.trig_radian_arc_m5                     ฟังก์ชันตรีโกณมิติ
trig.identity-reduce                   math.trig_identity_reduce_m5                ฟังก์ชันตรีโกณมิติ
trig.inverse-compose,                  math.inverse_trig_sum_m5                    ตัวผกผันของฟังก์ชันตรีโกณมิติ
trig.arcsin-arccos-complement
trig.equation-count                    math.trig_equation_count_m5                 สมการตรีโกณมิติ
trig.obtuse-test                       math.triangle_side_type_m5                  กฎของโคไซน์
=====================================  ==========================================  ================================

Angles come from tables of multiples of π whose sines and cosines are exact,
and the inverse-trig items from Pythagorean triples, so every answer is an
exact rational or a rational multiple of one square root.
``test_math_bank_trig.py`` checks the identities and values with SymPy,
counts equation solutions numerically, and pins the source exams' answers.
"""

from __future__ import annotations

import math
from fractions import Fraction

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.kit.math_problems import frac_tex

M5 = {"th": "ม.5"}

#: Pythagorean (p, q, r): p² + q² = r².
TRIPLES = ((3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17), (7, 24, 25),
           (24, 7, 25))


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Named mistakes first; duplicates and the answer itself dropped; three kept."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _frac_q(stem: list, right: Fraction, named: list, topic: str) -> GeneratedQuestion:
    out: list[str] = []
    for w in [*named, right + 1, right * 2, right / 2, right - 1, right + 2, right - 2, right + Fraction(1, 2)]:
        t = frac_tex(Fraction(w))
        if t != frac_tex(right) and t not in out:
            out.append(t)
    return _tex_q(stem, frac_tex(right), out, topic)


def _int_q(stem: list, right: int, named: list[int], topic: str) -> GeneratedQuestion:
    pool = [*named, right + 1, right - 1, right + 2, right + 3, right * 2, right + 4]
    out = [str(w) for w in pool if w > 0 and w != right]
    return _tex_q(stem, str(right), out, topic)


def simplify_root(n: int) -> tuple[int, int]:
    """√n = k·√m with m square-free."""
    k = max(v for v in range(1, math.isqrt(n) + 1) if n % (v * v) == 0)
    return k, n // (k * k)


def surd_tex(c: Fraction, m: int) -> str:
    """c·√m with the root in the numerator: \\frac{3\\sqrt{3}}{4}."""
    c = Fraction(c)
    if m == 1 or c == 0:
        return frac_tex(c)
    sign = "-" if c < 0 else ""
    c = abs(c)
    num = ("" if c.numerator == 1 else str(c.numerator)) + rf"\sqrt{{{m}}}"
    return sign + (num if c.denominator == 1 else rf"\frac{{{num}}}{{{c.denominator}}}")


def pi_tex(t: Fraction) -> str:
    """t·π: \\frac{5\\pi}{6}, 2\\pi, -\\pi."""
    t = Fraction(t)
    if t == 0:
        return "0"
    sign = "-" if t < 0 else ""
    t = abs(t)
    num = ("" if t.numerator == 1 else str(t.numerator)) + r"\pi"
    return sign + (num if t.denominator == 1 else rf"\frac{{{num}}}{{{t.denominator}}}")


# ── Radians and arc length ───────────────────────────────────────────────────


# ── Identities: reducing expressions ─────────────────────────────────────────


# ── Inverse trig: sums of angles ─────────────────────────────────────────────


# ── Counting solutions in an interval ────────────────────────────────────────


# ── What kind of triangle the sides make ─────────────────────────────────────


# ── Right triangles: linking the two acute angles ────────────────────────────


# ── Reduction formulas (from the (rath) notes' answer-key digests) ─────────


# ── Product-to-sum and sum-to-product ───────────────────────────────────────


