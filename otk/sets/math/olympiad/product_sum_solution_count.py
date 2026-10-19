"""(x₁ + … + x_p)(y₁ + … + y_q) = N: Σ over d | N of C(d − 1, p − 1)·C(N/d − 1, q − 1)."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 11",))


def solution_count(p: int, q: int, total: int) -> int:
    """Each factorisation N = d·e splits as compositions of d into p parts and
    of e into q parts (source: p = 3, q = 4, N = 91 → 3300 + 1320 = 4620)."""
    return sum(comb(d - 1, p - 1) * comb(total // d - 1, q - 1) for d in range(1, total + 1) if total % d == 0)


@question_type(
    "math.product_sum_solution_count_olympiad",
    display_name={"th": "จำนวนผลเฉลยของสมการผลคูณของผลบวก"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class ProductSumSolutionCount(WordProblem):
    def expr(self, rng: Random):
        p, q = rng.randint(2, 4), rng.randint(2, 5)
        total = rng.choice([n for n in range(30, 400) if sum(1 for d in range(1, n + 1) if n % d == 0) <= 6])
        answer = solution_count(p, q, total)
        wrong = [v for v in dict.fromkeys([solution_count(q, p, total), sum(comb(d + p - 1, p - 1) * comb(total // d + q - 1, q - 1) for d in range(1, total + 1) if total % d == 0), comb(total - 1, p + q - 1), max(comb(d - 1, p - 1) * comb(total // d - 1, q - 1) for d in range(1, total + 1) if total % d == 0), answer * 2]) if v != answer]
        xs = "+".join(f"x_{{{i}}}" for i in range(1, p + 1))
        ys = "+".join(f"y_{{{i}}}" for i in range(1, q + 1))
        return MathDraw(
            rf"({xs})({ys})={total}",
            str(answer),
            prompt="จงหาจำนวนผลเฉลยที่เป็นจำนวนเต็มบวกของสมการต่อไปนี้",
            hint="แยก N เป็นผลคูณ d·e แล้วนับวิธีเขียน d เป็นผลบวกของจำนวนเต็มบวก p จำนวน และ e เป็นผลบวก q จำนวน",
            distractors=[str(v) for v in wrong],
        )
