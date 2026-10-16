"""Maximize the earlier square sum by minimizing a fixed-sum tail."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def tail_square_extremes(limit: int, picks: int, target: int) -> tuple[int, int]:
    """Minimum and maximum square sums for distinct labels totaling target."""
    if limit < 1 or picks < 1 or picks > limit or target < 0:
        raise ValueError("invalid label count, pick count, or target")
    states = {(0, 0): (0, 0)}
    for label in range(1, limit + 1):
        updated = states.copy()
        for (count, total), (minimum, maximum) in states.items():
            key = (count + 1, total + label)
            if count >= picks or key[1] > target:
                continue
            candidate = (minimum + label**2, maximum + label**2)
            if key in updated:
                old_min, old_max = updated[key]
                updated[key] = (min(old_min, candidate[0]), max(old_max, candidate[1]))
            else:
                updated[key] = candidate
        states = updated
    try:
        return states[picks, target]
    except KeyError as exc:
        raise ValueError("no distinct labels have this sum") from exc


def max_earlier_square_sum(limit: int, picks: int, target: int) -> int:
    minimum, _ = tail_square_extremes(limit, picks, target)
    return limit * (limit + 1) * (2 * limit + 1) // 6 - minimum


@question_type(
    "math.minimum_tail_squares_olympiad",
    display_name={"th": "ผลบวกกำลังสองส่วนต้นเมื่อส่วนท้ายมีค่าต่ำสุด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class MinimumTailSquares(WordProblem):
    def expr(self, rng: Random):
        limit = rng.randint(8, 13)
        picks = 3
        target = rng.randint(8, 3 * limit - 5)
        minimum, maximum = tail_square_extremes(limit, picks, target)
        total = limit * (limit + 1) * (2 * limit + 1) // 6
        answer = total - minimum
        quotient, remainder = divmod(target, picks)
        repeatable_minimum = (picks - remainder) * quotient**2 + remainder * (quotient + 1) ** 2
        return MathDraw(
            rf"N={limit},\quad S={target}",
            str(answer),
            prompt=("นำจำนวนเต็ม 1 ถึง N มาเรียงใหม่โดยไม่ใช้ซ้ำ "
                    "สามตำแหน่งท้ายมีผลบวกเท่ากับ S และมีผลบวกกำลังสองน้อยที่สุด "
                    "ผลบวกกำลังสองของจำนวนที่อยู่ก่อนสามตำแหน่งท้ายเป็นเท่าใด"),
            hint="ลดผลบวกกำลังสองของสามจำนวนท้ายภายใต้เงื่อนไขว่าต่างกัน",
            distractors=[
                str(total - maximum),  # maximize instead of minimize tail squares
                str(total - repeatable_minimum),  # allow repeated tail labels
                str(total - sum(i * i for i in range(1, picks + 1))),  # ignore target sum
                str(total - target**2 // picks),  # use Cauchy bound as if attainable
            ],
        )
