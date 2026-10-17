"""x with both ax − 1 and bx − 1 perfect squares; never all of 2, 5, 13."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันที่สอง ข้อ 1",)
)

PAIRS = ((2, 5), (2, 13), (5, 13))


def _square(v: int) -> bool:
    return v >= 0 and isqrt(v) ** 2 == v


def square_pair_count(a: int, b: int, limit: int) -> int:
    """Walk the squares s² = ax − 1 and test bx − 1. For all three of 2, 5, 13:
    2x − 1 odd square gives x ≡ 1 (mod 4), so 5x − 1 = 4u² and 13x − 1 = 4v²,
    and 2x = (v − u)(v + u) would be divisible by 4 though x is odd."""
    count = 0
    s = 0
    while (s * s + 1) <= a * limit:
        if (s * s + 1) % a == 0:
            x = (s * s + 1) // a
            if 1 <= x <= limit and _square(b * x - 1):
                count += 1
        s += 1
    return count


@question_type(
    "math.shifted_square_pairs_olympiad",
    display_name={"th": "จำนวน x ที่ ax − 1 และ bx − 1 เป็นกำลังสองสมบูรณ์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวนเชิงพีชคณิต",
)
class ShiftedSquarePairs(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.choice(PAIRS)
        limit = rng.choice([10**3, 10**4, 10**5, 10**6])
        answer = square_pair_count(a, b, limit)
        wrong = [v for v in dict.fromkeys([answer + 1, max(answer - 1, 0), answer + 2, 2 * answer, 0 if answer else 3]) if v != answer]
        return MathDraw(
            rf"{a}x-1,\ \ {b}x-1,\quad 1\le x\le {limit}",
            str(answer),
            prompt="มีจำนวนเต็ม x ในช่วงต่อไปนี้กี่จำนวนที่ทำให้ทั้งสองนิพจน์เป็นกำลังสองสมบูรณ์",
            hint="ไล่กำลังสอง s² = ax − 1 แทนการไล่ x และใช้มอดุโล 4 ตัดกรณี",
            distractors=[str(v) for v in wrong],
        )
