"""Probability of distinct labels from three overlapping boxes."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def distinct_box_probability(first: int, second: int, extra: int) -> Fraction:
    """First two label sets share only 1; third contains their union plus extras."""
    if first < 2 or second < 2 or extra < 0:
        raise ValueError("expected first, second >=2 and extra>=0")
    third = first + second + extra - 1
    # There are first*second-1 unequal pairs: only (1,1) collides.
    # Each unequal pair leaves third-2 labels in the final box.
    return Fraction((first * second - 1) * (third - 2), first * second * third)


@question_type(
    "math.overlapping_boxes_probability_olympiad",
    display_name={"th": "ความน่าจะเป็นที่หยิบป้ายจากกล่องซ้อนทับแล้วไม่ซ้ำกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ความน่าจะเป็น",
)
class OverlappingBoxesProbability(WordProblem):
    def expr(self, rng: Random):
        first = rng.randint(2, 5)
        second = rng.randint(2, 5)
        extra = rng.randint(1, 5)
        third = first + second + extra - 1
        total = first * second * third
        answer = distinct_box_probability(first, second, extra)
        return MathDraw(
            rf"A=\{{1,\ldots,{first}\}},\quad "
            rf"B=\{{1,{first + 1},\ldots,{first + second - 1}\}},\quad "
            rf"C=\{{1,\ldots,{third}\}}",
            str(answer),
            prompt=("กล่อง A, B, C มีป้ายหมายเลขตามเซตที่กำหนด "
                    "สุ่มหยิบป้ายกล่องละหนึ่งใบอย่างอิสระ "
                    "ความน่าจะเป็นที่หมายเลขทั้งสามไม่ซ้ำกันเท่าใด"),
            hint="คู่จาก A และ B ซ้ำกันได้เพียงคู่ (1,1)",
            distractors=[
                str(Fraction(third - 2, third)),  # assume first two always differ
                str(Fraction((first * second - 1) * (third - 1), total)),  # exclude only one prior label
                str(Fraction(first * second - 1, first * second)),  # ignore third-box collision
                str(Fraction((first * second - 1) * (third - 3), total)),  # exclude three labels from third box
            ],
        )
