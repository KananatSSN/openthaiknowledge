"""Σ x/(x − 1) over the roots of xⁿ + ax − b is n − P′(1)/P(1)."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 8",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def shifted_sum(n: int, a: int, b: int) -> Fraction:
    """x/(x − 1) = 1 + 1/(x − 1) and Σ 1/(1 − xₖ) = P′(1)/P(1), so the sum is
    n − (n + a)/(1 + a − b) (source: 84 − 91/2 = 77/2)."""
    return n - Fraction(n + a, 1 + a - b)


@question_type(
    "math.root_shift_reciprocal_sum_olympiad",
    display_name={"th": "ผลบวก x/(x − 1) บนรากของพหุนาม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รากของพหุนาม",
)
class RootShiftReciprocalSum(WordProblem):
    def expr(self, rng: Random):
        while True:
            n, a, b = rng.randint(3, 100), rng.randint(1, 12), rng.randint(1, 12)
            if 1 + a - b != 0:
                break
        answer = shifted_sum(n, a, b)
        wrong = [frac_tex(v) for v in dict.fromkeys([n + Fraction(n + a, 1 + a - b), Fraction(n + a, 1 + a - b), Fraction(n), n - Fraction(n, 1 + a - b), answer + 1]) if v != answer]
        return MathDraw(
            rf"x^{{{n}}}+{a}x-{b}=0,\quad \sum_{{k=1}}^{{{n}}}\frac{{x_k}}{{x_k-1}}",
            frac_tex(answer),
            prompt="x₁, …, xₙ เป็นรากทั้งหมดของสมการ จงหาค่าของผลบวก",
            hint="เขียน x/(x − 1) = 1 + 1/(x − 1) และใช้ Σ 1/(1 − xₖ) = P′(1)/P(1)",
            distractors=wrong,
        )
