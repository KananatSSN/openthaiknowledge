"""ดิสคริมิแนนต์

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/1

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, poly_tex

PROVENANCE = Provenance("original")


@question_type("math.discriminant",
               display_name={"th": "ดิสคริมิแนนต์: จำนวนรากจริง"}, level={"th": "ม.4"},
               topic="ดิสคริมิแนนต์")
class Discriminant(MathType):
    def expr(self, rng: Random):
        b, c = rng.randint(-6, 6), rng.randint(-9, 9)
        if rng.random() < 0.25:
            b = rng.choice([-6, -4, -2, 2, 4, 6])
            c = b * b // 4
        disc = b * b - 4 * c
        if disc > 0:
            verdict = rf"D = {disc} > 0 \;\Rightarrow\; 2"
        elif disc == 0:
            verdict = r"D = 0 \;\Rightarrow\; 1"
        else:
            verdict = rf"D = {disc} < 0 \;\Rightarrow\; 0"
        tex = poly_tex((1, "x^{2}"), (b, "x"), (c, ""))
        return MathDraw(rf"{tex} = 0", verdict, hint=r"D = b^2 - 4ac",
                        prompt="สมการนี้มีรากจริงกี่ราก")


@question_type("math.discriminant_k", display_name={"th": "หาค่า k จากเงื่อนไขของราก"},
               level={"th": "ม.4"}, topic="ดิสคริมิแนนต์")
class DiscriminantK(MathType):
    """A repeated root means b² − 4ac = 0 — solved for the unknown coefficient."""

    def expr(self, rng: Random, a_hi: int = 4, half_b_hi: int = 9):
        a = rng.randint(1, a_hi)
        m = rng.randint(1, half_b_hi)
        b = 2 * a * m
        c = a * m * m                              # makes b² − 4ac = 0 exactly
        return MathDraw(
            poly_tex((a, "x^2"), (b, "x"), (0, "")) + " + k = 0", str(c),
            prompt="จงหาค่า k ที่ทำให้สมการมีรากซ้ำ",
            hint=r"b^2 - 4ac = 0",
            distractors=[str(-c), str(b * b), str(c * 2)])


@question_type("math.quadratic_complex",
               display_name={"th": "สมการกำลังสอง (รากเชิงซ้อน)"}, level={"th": "ม.4"},
               topic="ดิสคริมิแนนต์")
class QuadraticComplex(MathType):
    def expr(self, rng: Random):
        m = rng.randint(-3, 3)
        k = rng.randint(1, 3)
        tex = poly_tex((1, "x^{2}"), (-2 * m, "x"), (m * m + k * k, ""))
        ki = "i" if k == 1 else f"{k}i"
        answer = rf"x = \pm {ki}" if m == 0 else rf"x = {m} \pm {ki}"
        return MathDraw(rf"{tex} = 0", answer, hint=r"\sqrt{-1} = i",
                        prompt="จงแก้สมการ")

from fractions import Fraction  # noqa: E402
from math import isqrt  # noqa: E402

from otk.core.content import text as _text_block  # noqa: E402
from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m4 import M4 as LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


def _nz4(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk4(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk4(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk4(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt4(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk4(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk4(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))

# ── More discriminant (2026-11): its value, k for two real roots, k for none, which equation has rational
# roots, a tangent line to y = x², a parabola touching the x-axis, and a leading coefficient for a repeated
# root ──


@question_type("math.discriminant_value_m4", display_name={"th": "หาค่าดิสคริมิแนนต์"}, level=LEVEL, topic="ดิสคริมิแนนต์")
class DiscriminantValueM4(MathType):
    def expr(self, rng: Random):
        a, b, c = _nz4(rng, 1, 5), rng.randint(-9, 9), _nz4(rng, 1, 9)
        right = b * b - 4 * a * c
        # 4ac added; 2ac taken away; b not squared.
        return MathDraw(f"{poly_tex((a, 'x^{2}'), (b, 'x'), (c, ''))} = 0", str(right), prompt="จงหาค่าดิสคริมิแนนต์ (b² − 4ac)",
                        distractors=_nk4(b * b + 4 * a * c, b * b - 2 * a * c, b - 4 * a * c, right + 4, answer=right))


@question_type("math.k_two_real_roots_m4", display_name={"th": "ค่า k ที่ทำให้สมการมีรากจริงสองราก"}, level=LEVEL,
               topic="ดิสคริมิแนนต์")
class KTwoRealRootsM4(MathType):
    def expr(self, rng: Random):
        p = _nz4(rng, 1, 8)
        bound = p * p
        right = f"k < {bound}"
        # The inequality turned; equal only; the half-coefficient.
        wrongs = [f"k > {bound}", f"k = {bound}", f"k < {abs(p)}", f"k < {2 * bound}"]
        return MathDraw(f"x^{{2}} {'+' if p > 0 else '-'} {2 * abs(p)}x + k = 0", right,
                        prompt="สมการนี้มีรากเป็นจำนวนจริงสองรากที่ต่างกันเมื่อ k มีค่าเท่าใด",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.k_no_real_roots_m4", display_name={"th": "ค่า k ที่ทำให้สมการไม่มีรากจริง"}, level=LEVEL,
               topic="ดิสคริมิแนนต์")
class KNoRealRootsM4(MathType):
    def expr(self, rng: Random):
        p = _nz4(rng, 1, 8)
        a = rng.randint(1, 3)
        bound = Fraction(p * p, a)
        right = f"k > {frac_tex(bound)}"
        wrongs = [f"k < {frac_tex(bound)}", f"k > {frac_tex(4 * bound)}", f"k > {abs(p)}", f"k = {frac_tex(bound)}"]
        lead = "" if a == 1 else str(a)
        return MathDraw(f"{lead}x^{{2}} {'+' if p > 0 else '-'} {2 * abs(p)}x + k = 0", right,
                        prompt="สมการนี้ไม่มีรากที่เป็นจำนวนจริงเมื่อ k มีค่าเท่าใด", distractors=_tk4(*wrongs, answer=right))


@question_type("math.rational_roots_which_m4", display_name={"th": "สมการใดมีรากเป็นจำนวนตรรกยะ"}, level=LEVEL,
               topic="ดิสคริมิแนนต์")
class RationalRootsWhichM4(QuestionType):
    """Fixed choices: an equation from another draw could also have rational roots."""

    def build(self, rng: Random, **params):
        p, q = _nz4(rng, 1, 9), _nz4(rng, 1, 9)
        right = f"{poly_tex((1, 'x^{2}'), (-(p + q), 'x'), (p * q, ''))} = 0"
        wrongs = []
        for c in (p * q + 1, p * q - 1, p * q + 2, p * q - 2, p * q + 3):
            d = (p + q) ** 2 - 4 * c
            if d < 0 or isqrt(d) ** 2 != d:
                wrongs.append(f"{poly_tex((1, 'x^{2}'), (-(p + q), 'x'), (c, ''))} = 0")
        return _fixed_maths([_text_block("สมการใดมีรากเป็นจำนวนตรรกยะ")], right, _tk4(*wrongs, answer=right)[:3], self.topic)


@question_type("math.tangent_to_parabola_m4", display_name={"th": "เส้นตรงสัมผัสพาราโบลา y = x²"}, level=LEVEL,
               topic="ดิสคริมิแนนต์")
class TangentToParabolaM4(MathType):
    def expr(self, rng: Random):
        m = 2 * _nz4(rng, 1, 6)
        right = -(m * m) // 4
        # The square not quartered; the sign lost; half the slope.
        return MathDraw(f"y = {m}x + k", str(right), prompt="เส้นตรงนี้สัมผัสพาราโบลา y = x² ค่าของ k เท่ากับเท่าใด",
                        distractors=_nk4(-(m * m), m * m // 4, m // 2, right - 1, answer=right))


@question_type("math.touch_x_axis_m4", display_name={"th": "พาราโบลาสัมผัสแกน x"}, level=LEVEL, topic="ดิสคริมิแนนต์")
class TouchXAxisM4(MathType):
    def expr(self, rng: Random):
        h = _nz4(rng, 1, 9)
        right = h * h
        # Double h; h itself; the square negated.
        return MathDraw(f"y = x^{{2}} {'-' if h > 0 else '+'} {2 * abs(h)}x + c", str(right),
                        prompt="ถ้ากราฟนี้สัมผัสแกน x พอดี ค่าของ c เท่ากับเท่าใด",
                        distractors=_nk4(4 * h * h, abs(h), -right, 2 * right, answer=right))


@question_type("math.repeated_root_leading_m4", display_name={"th": "หาสัมประสิทธิ์นำที่ทำให้มีรากซ้ำ"}, level=LEVEL,
               topic="ดิสคริมิแนนต์")
class RepeatedRootLeadingM4(MathType):
    def expr(self, rng: Random):
        c = rng.randint(1, 6)
        k = rng.randint(1, 6)
        b = 2 * k * c
        # b² / 4c equals k·c² ... over c gives k·c; the plain ratio b/c.
        right = b * b // (4 * c)
        return MathDraw(f"ax^{{2}} + {b}x + {c} = 0", str(right), prompt="สมการนี้มีรากซ้ำ ค่าของ a เท่ากับเท่าใด",
                        distractors=_nk4(b * b // c, b // c if b % c == 0 else b, b * b, right + 1, answer=right, lo=1))
