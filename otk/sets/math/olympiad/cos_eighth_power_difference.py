"""cos⁸A − sin⁸A = cos 2A·(1 − sin²2A/2), with cos 2A ≥ 0 on [−π/4, π/4]."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 1",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def surd_tex(square: Fraction) -> str:
    """TeX for √square in the form (k/d)√m with m squarefree."""
    inside = square.numerator * square.denominator
    outside, f = 1, 2
    while f * f <= inside:
        while inside % (f * f) == 0:
            inside //= f * f
            outside *= f
        f += 1
    coef = Fraction(outside, square.denominator)
    if inside == 1:
        return frac_tex(coef)
    root = rf"\sqrt{{{inside}}}"
    top = ("" if coef.numerator == 1 else str(coef.numerator)) + root
    return top if coef.denominator == 1 else rf"\frac{{{top}}}{{{coef.denominator}}}"


def value_square(c: Fraction) -> Fraction:
    """cos²2A = (1 + c)/2 and sin²2A = (1 − c)/2 with c = cos 4A, so the value
    is √((1 + c)/2)·(3 + c)/4; returns its square (source: c = 1/3 → 5√6/18)."""
    return (1 + c) / 2 * ((3 + c) / 4) ** 2


@question_type(
    "math.cos_eighth_power_difference_olympiad",
    display_name={"th": "ค่า cos⁸A − sin⁸A จาก cos 4A"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ฟังก์ชันตรีโกณมิติ",
)
class CosEighthPowerDifference(WordProblem):
    def expr(self, rng: Random):
        q = rng.randint(2, 9)
        c = Fraction(rng.randint(-q + 1, q - 1), q)
        answer = value_square(c)
        wrong = [surd_tex(v) for v in dict.fromkeys([(1 + c) / 2, (1 + c) / 2 * ((3 - c) / 4) ** 2, ((3 + c) / 4) ** 2, (1 - c) / 2 * ((3 + c) / 4) ** 2, (1 + c) / 2 * ((1 + c) / 2) ** 2]) if v != answer and v > 0]
        return MathDraw(
            rf"\cos 4A={frac_tex(c)},\quad -\tfrac{{\pi}}{{4}}\le A\le\tfrac{{\pi}}{{4}}",
            surd_tex(answer),
            prompt="จงหาค่า cos⁸A − sin⁸A",
            hint="แยก cos⁸A − sin⁸A = (cos²A − sin²A)(cos⁴A + sin⁴A) = cos 2A·(1 − ½sin²2A) และ cos 2A ≥ 0 ในช่วงที่กำหนด",
            distractors=wrong,
        )
