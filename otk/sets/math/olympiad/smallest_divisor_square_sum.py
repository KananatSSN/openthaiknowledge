"""Sum of squares of the four smallest divisors; N = d₁² + ⋯ + d₄² only for 130."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันที่สอง ข้อ 2",))


def small_divisors(n: int, count: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0][:count]


def divisor_square_sum(n: int) -> int:
    """For the source: an odd N gives an even sum of four odd squares, so N is
    even, d₂ = 2, and parity forces d₃ = p prime and d₄ = 2p, giving
    N = 5(1 + p²) and p = 5: N = 130."""
    return sum(d * d for d in small_divisors(n, 4))


CANDIDATES = tuple(n for n in range(12, 400) if len([d for d in range(1, n + 1) if n % d == 0]) >= 4)


@question_type(
    "math.smallest_divisor_square_sum_olympiad",
    display_name={"th": "ผลบวกกำลังสองของตัวหารสี่ตัวแรก"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ตัวประกอบของจำนวนเต็ม",
)
class SmallestDivisorSquareSum(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice(CANDIDATES)
        answer = divisor_square_sum(n)
        ds = small_divisors(n, 5)
        wrong = [v for v in dict.fromkeys([sum(ds[:4]), sum(d * d for d in ds[1:5]) if len(ds) == 5 else answer + 4, sum(d * d for d in ds[:3]), answer + 1, answer * 2]) if v != answer]
        return MathDraw(
            rf"N={n}",
            str(answer),
            prompt="ให้ d₁ < d₂ < d₃ < d₄ เป็นตัวหารบวกที่น้อยที่สุดสี่ตัวแรกของ N จงหา d₁² + d₂² + d₃² + d₄²",
            hint="ไล่ตัวหารจากน้อยไปมากเริ่มที่ 1",
            distractors=[str(v) for v in wrong],
        )
