"""Σ 2a(2a − s)/(b + c) ≥ s with s the semiperimeter; equality for equilateral."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 8",))


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def weighted_sum(a, b, c):
    s = (a + b + c) / 2
    return sum(2 * x * (2 * x - s) / (y + z) for x, y, z in ((a, b, c), (b, a, c), (c, a, b)))


def weighted_minimum(perimeter: int) -> Fraction:
    """With x = a/s ∈ (0, 1) each term is s·g(x), g(x) = 2x(2x − 1)/(2 − x).
    The tangent line at x = 2/3 gives g(x) ≥ 1/3 + (11/4)(x − 2/3) on (0, 1),
    and the x's sum to 2, so the total is at least s, with equality for the
    equilateral triangle."""
    return Fraction(perimeter, 2)


@question_type(
    "math.triangle_weighted_sum_minimum_olympiad",
    display_name={"th": "ค่าต่ำสุดของผลบวกถ่วงน้ำหนักด้านของรูปสามเหลี่ยม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class TriangleWeightedSumMinimum(WordProblem):
    def expr(self, rng: Random):
        perimeter = rng.randint(6, 90)
        answer = weighted_minimum(perimeter)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(perimeter), Fraction(perimeter, 3), Fraction(perimeter, 4), Fraction(3 * perimeter, 4), Fraction(perimeter, 2) + 1]) if v != answer]
        return MathDraw(
            rf"a+b+c={perimeter},\quad s=\frac{{a+b+c}}{{2}},\quad T=\frac{{2a(2a-s)}}{{b+c}}+\frac{{2b(2b-s)}}{{a+c}}+\frac{{2c(2c-s)}}{{a+b}}",
            frac_tex(answer),
            prompt="a, b, c เป็นความยาวด้านของรูปสามเหลี่ยมที่มีเส้นรอบรูปต่อไปนี้ จงหาค่าต่ำสุดของ T",
            hint="เขียน b + c = 2s − a แล้วเทียบแต่ละพจน์กับเส้นสัมผัสที่จุด a = b = c",
            distractors=wrong,
        )
