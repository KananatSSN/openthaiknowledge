"""(x₁ + x₂ + x₃)²(y₁ + y₂) = N: sum over squares s² | N of C(s − 1, 2)·(N/s² − 1)."""

from __future__ import annotations

from math import comb, isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 6",))


def solution_count(total: int) -> int:
    """For each s ≥ 3 with s² | N, there are C(s − 1, 2) ways for the x's and
    N/s² − 1 for the y's (source: N = 2548, s = 7, 14 → 765 + 936 = 1701)."""
    return sum(comb(s - 1, 2) * (total // (s * s) - 1) for s in range(3, isqrt(total) + 1) if total % (s * s) == 0)


CASES = tuple(n for n in range(200, 6000) if sum(1 for s in range(3, isqrt(n) + 1) if n % (s * s) == 0 and n // (s * s) >= 2) >= 2)


@question_type(
    "math.squared_sum_solution_count_olympiad",
    display_name={"th": "จำนวนผลเฉลยจำนวนเต็มบวกของสมการผลคูณกำลังสอง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class SquaredSumSolutionCount(WordProblem):
    def expr(self, rng: Random):
        total = rng.choice(CASES)
        answer = solution_count(total)
        squares = [s for s in range(3, isqrt(total) + 1) if total % (s * s) == 0]
        largest = comb(squares[-1] - 1, 2) * (total // squares[-1] ** 2 - 1)
        wrong = [v for v in dict.fromkeys([largest, sum(comb(s + 2, 2) * (total // (s * s) + 1) for s in squares), sum(comb(s - 1, 2) * (total // (s * s)) for s in squares), sum(total // (s * s) - 1 for s in squares), comb(squares[0] - 1, 2) * (total // squares[0] ** 2 - 1)]) if v != answer]
        return MathDraw(
            rf"(x_1+x_2+x_3)^2(y_1+y_2)={total}",
            str(answer),
            prompt="จงหาจำนวนผลเฉลยที่เป็นจำนวนเต็มบวกของสมการต่อไปนี้",
            hint="ให้ s = x₁ + x₂ + x₃ ≥ 3 ต้องมี s² หาร N แล้วนับวิธีแบ่ง s เป็นสามส่วนและ N/s² เป็นสองส่วน",
            distractors=[str(v) for v in wrong],
        )
