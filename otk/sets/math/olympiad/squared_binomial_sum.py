"""Σ (2n)!/((k!)²((n − k)!)²) = C(2n, n)·Σ C(n, k)² = C(2n, n)²."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 9",))


def factorial_sum(n: int) -> int:
    """(2n)!/(k!²(n − k)!²) = C(2n, n)·C(n, k)², and Σ C(n, k)² = C(2n, n)
    (source: general n)."""
    return comb(2 * n, n) ** 2


@question_type(
    "math.squared_binomial_sum_olympiad",
    display_name={"th": "ผลบวกของแฟกทอเรียลที่เป็นกำลังสองของสัมประสิทธิ์ทวินาม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การนับเชิงการจัด",
)
class SquaredBinomialSum(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(2, 14)
        answer = factorial_sum(n)
        wrong = [v for v in dict.fromkeys([comb(2 * n, n), comb(4 * n, 2 * n), 4**n * comb(2 * n, n), comb(2 * n, n) * 2**n, comb(2 * n, n) ** 2 // (n + 1)]) if v != answer]
        return MathDraw(
            rf"\sum_{{k=0}}^{{{n}}}\frac{{{2 * n}!}}{{(k!)^2\,(({n}-k)!)^2}}",
            str(answer),
            prompt="จงหาค่าของผลบวกต่อไปนี้",
            hint="เขียนแต่ละพจน์เป็น C(2n, n)·C(n, k)² แล้วใช้เอกลักษณ์ Σ C(n, k)² = C(2n, n)",
            distractors=[str(v) for v in wrong],
        )
