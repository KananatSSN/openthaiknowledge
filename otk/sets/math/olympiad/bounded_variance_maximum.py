"""Max Σ(xᵢ − m)² over [0, 1]ᴺ: half the values at 0 and half at 1."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 6",)
)


def variance_sum_maximum(n: int) -> Fraction:
    """Σ(xᵢ − m)² = Σxᵢ² − (Σxᵢ)²/N is convex in each xᵢ, so the maximum is
    at a vertex: k ones give k(N − k)/N, largest at k = ⌊N/2⌋."""
    k = n // 2
    return Fraction(k * (n - k), n)


def _tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


@question_type(
    "math.bounded_variance_maximum_olympiad",
    display_name={"th": "ค่ามากสุดของผลบวกกำลังสองของส่วนเบี่ยงเบนในช่วง [0, 1]"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class BoundedVarianceMaximum(WordProblem):
    def expr(self, rng: Random):
        n = 2 * rng.randint(1, 1500) + 1  # odd, like the source's 2011
        answer = variance_sum_maximum(n)
        k = n // 2
        wrong = [_tex(v) for v in dict.fromkeys([
            Fraction((k - 1) * (n - k + 1), n),  # one value too few at 1
            Fraction(k * k, n),  # put exactly half, k, on each side
            Fraction((k + 1) ** 2, n),
            Fraction(k * (k + 2), n),
            Fraction((k - 1) * (k + 1), n),
        ]) if v != answer and v > 0]
        return MathDraw(
            rf"N={n},\quad \sum_{{i=1}}^{{N}}(x_i-m)^2,\quad m=\frac{{x_1+\cdots+x_N}}{{N}}",
            _tex(answer),
            prompt="สำหรับ 0 ≤ x₁, …, x_N ≤ 1 ใด ๆ จงหาค่ามากที่สุดของผลบวกต่อไปนี้",
            hint="ผลบวกเท่ากับ Σxᵢ² − (Σxᵢ)²/N ซึ่งเป็นฟังก์ชันนูนในแต่ละ xᵢ ค่ามากสุดจึงเกิดที่ xᵢ เป็น 0 หรือ 1",
            distractors=wrong,
        )
