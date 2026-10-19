"""f(xy − 1) + f(x)f(y) = 2xy − 1 has exactly the solutions x and −x²."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2557, ข้อ 2",)
)

SOLUTIONS = (lambda x: x, lambda x: -x * x)


def possible_values(n: int) -> tuple[int, int]:
    """f(n) for the two solutions: f(1) = 1 makes f additive and
    multiplicative (so f(x) = x); f(1) = −1 makes −f multiplicative with
    −f(x + 1) = −f(x) + 2x + 1 (so f(x) = −x²)."""
    return tuple(f(n) for f in SOLUTIONS)


@question_type(
    "math.two_solution_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันที่มีคำตอบสองฟังก์ชัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class TwoSolutionFunctional(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice([v for v in range(-12, 13) if v not in (-1, 0, 1)])
        first, second = possible_values(n)
        if rng.randrange(2):
            asked, answer = "ผลบวก", first + second
            candidates = [first, second, first - second, n + n * n, 2 * n]
        else:
            asked, answer = "ผลคูณ", first * second
            candidates = [first, second, n**3, first + second, -(n**2)]
        wrong = []
        for value in candidates + [answer + 1, answer - 1]:
            if value != answer and value not in wrong:
                wrong.append(value)
        return MathDraw(
            r"f(xy-1)+f(x)\,f(y)=2xy-1",
            str(answer),
            prompt=(
                "ฟังก์ชัน f : ℝ → ℝ สอดคล้องสมการต่อไปนี้ทุกจำนวนจริง x, y "
                f"จง{asked}ของค่าที่เป็นไปได้ทั้งหมดของ f({n})"
            ),
            hint="ให้ y = 0 ได้ f(0) = 0 และ f(−1) = −1 แล้ว x = y = 1 ได้ f(1) = ±1 แยกสองกรณี",
            distractors=[str(value) for value in wrong],
            variant=asked,
        )
