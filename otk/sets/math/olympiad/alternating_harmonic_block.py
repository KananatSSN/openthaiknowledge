"""Σ 1/a_{2k−1} with aₙ = n(n + 1) telescopes to 1/(n + 1) + ⋯ + 1/(2n)."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันที่สอง ข้อ 3",))


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def odd_reciprocal_sum(n: int) -> Fraction:
    """1/((2k − 1)2k) = 1/(2k − 1) − 1/(2k), so the sum is the alternating
    harmonic sum 1 − 1/2 + ⋯ − 1/(2n) = Σ_{k=n+1}^{2n} 1/k ≥ 2n/(3n + 1) by
    the HM–AM inequality, which with AM–GM proves the source's inequality."""
    return sum((Fraction(1, k) for k in range(n + 1, 2 * n + 1)), Fraction(0))


@question_type(
    "math.alternating_harmonic_block_olympiad",
    display_name={"th": "ผลบวกส่วนกลับของ n(n + 1) ที่ตำแหน่งคี่"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อนุกรมสลับเครื่องหมาย",
)
class AlternatingHarmonicBlock(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(2, 8)
        answer = odd_reciprocal_sum(n)
        wrong = [frac_tex(v) for v in dict.fromkeys([
            sum((Fraction(1, k) for k in range(n, 2 * n)), Fraction(0)),
            sum((Fraction(1, k * (k + 1)) for k in range(1, n + 1)), Fraction(0)),
            Fraction(2 * n, 3 * n + 1),
            sum((Fraction(1, k) for k in range(n + 1, 2 * n + 2)), Fraction(0)),
            answer * 2,
        ]) if v != answer]
        return MathDraw(
            rf"a_k=k(k+1),\quad \frac{{1}}{{a_1}}+\frac{{1}}{{a_3}}+\cdots+\frac{{1}}{{a_{{{2 * n - 1}}}}}",
            frac_tex(answer),
            prompt="จงหาค่าของผลบวกต่อไปนี้",
            hint="แยกเศษส่วนย่อย 1/((2k − 1)2k) = 1/(2k − 1) − 1/(2k)",
            distractors=wrong,
        )
