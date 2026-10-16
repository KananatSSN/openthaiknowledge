"""Proper colorings of a row with bounded color use."""

from __future__ import annotations

from functools import lru_cache
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def count_bounded_path_colorings(length: int, colors: int, cap: int) -> int:
    """Count labeled colorings of a path with no equal neighbors and usage<=cap."""
    if length < 1 or colors < 1 or cap < 1:
        raise ValueError("expected positive length, colors, and cap")

    @lru_cache(None)
    def extend(remaining: int, last: int, counts: tuple[int, ...]) -> int:
        if not remaining:
            return 1
        total = 0
        for color in range(colors):
            if color != last and counts[color] < cap:
                updated = list(counts)
                updated[color] += 1
                total += extend(remaining - 1, color, tuple(updated))
        return total

    return extend(length, -1, (0,) * colors)


@question_type(
    "math.bounded_path_colorings_olympiad",
    display_name={"th": "ระบายสีแถวโดยสีติดกันต่างกันและใช้สีได้จำกัด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class BoundedPathColorings(WordProblem):
    def expr(self, rng: Random):
        colors = rng.randint(3, 4)
        cap = rng.randint(2, 3)
        length = rng.randint(max(colors + 1, cap + 2), min(7, colors * cap))
        answer = count_bounded_path_colorings(length, colors, cap)
        no_cap = colors * (colors - 1) ** (length - 1)
        return MathDraw(
            rf"n={length},\quad c={colors},\quad r={cap}",
            str(answer),
            prompt=("ระบายสีช่องที่เรียงเป็นแถว n ช่องด้วยสีที่แยกกันได้ c สี "
                    "ช่องที่ติดกันต้องต่างสี และแต่ละสีใช้ได้ไม่เกิน r ช่อง "
                    "มีวิธีระบายสีทั้งหมดกี่วิธี"),
            hint="นับจากสีช่องก่อนหน้าและจำนวนครั้งที่ใช้แต่ละสี",
            distractors=[
                str(no_cap),  # ignore usage limit
                str(count_bounded_path_colorings(length, colors, cap + 1)),  # allow one extra use
                str(count_bounded_path_colorings(length - 1, colors, cap)),  # omit a slot
                str(answer // colors),  # treat colors as indistinguishable
                str(colors**length),  # ignore both restrictions
            ],
        )
