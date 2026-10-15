"""Recover a shifted sum of squares from two power sums."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def shifted_square_sum(count: int, first_sum: int, second_sum: int, shift: int = 1) -> int:
    """Expand sum((x_i-shift)^2) from sum(x_i) and sum(x_i^2)."""
    if count < 1:
        raise ValueError("at least one value is required")
    return second_sum - 2 * shift * first_sum + count * shift**2


@question_type(
    "math.shifted_square_sums_olympiad",
    display_name={"th": "ผลบวกกำลังสองหลังเลื่อนค่าทุกจำนวน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เอกลักษณ์พีชคณิต",
)
class ShiftedSquareSums(WordProblem):
    def expr(self, rng: Random):
        count = rng.randint(40, 180)
        values = [rng.randint(-1, 3) for _ in range(count)]
        first_sum = sum(values)
        while first_sum == 0:
            values = [rng.randint(-1, 3) for _ in range(count)]
            first_sum = sum(values)
        second_sum = sum(value * value for value in values)
        shift = rng.randint(1, 3)
        answer = shifted_square_sum(count, first_sum, second_sum, shift)
        return MathDraw(
            rf"n={count},\quad S={first_sum},\quad Q={second_sum},\quad c={shift}",
            str(answer),
            prompt=("จำนวนจริง x_1 ถึง x_n มีผลบวก S และผลบวกกำลังสอง Q "
                    "จงหาผลบวกกำลังสองของ (x_i-c) ทุกตัว"),
            hint="ขยาย (x_i-c)^2 แล้วรวมแต่ละพจน์",
            distractors=[
                str(second_sum - 2 * shift * first_sum),  # omit n*c^2
                str(second_sum + 2 * shift * first_sum + count * shift**2),  # wrong cross-term sign
                str(second_sum - shift * first_sum + count * shift**2),  # forget factor two
                str(second_sum - 2 * shift * first_sum + (count - 1) * shift**2),  # miscount values
            ],
        )
