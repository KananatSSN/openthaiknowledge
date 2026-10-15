"""Recover a contiguous group size from front/back row fractions."""

from __future__ import annotations

from fractions import Fraction
from math import lcm
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def possible_group_sizes(front: Fraction, back: Fraction, low: int, high: int) -> tuple[int, ...]:
    """Group sizes compatible with integral row, front, and back counts."""
    group_share = 1 - front - back
    if not 0 < front < 1 or not 0 < back < 1 or group_share <= 0 or not 1 <= low <= high:
        raise ValueError("invalid fractions or size interval")
    candidates = []
    for group in range(low, high + 1):
        total = Fraction(group, 1) / group_share
        if total.denominator == 1 and (total * front).denominator == 1 and (total * back).denominator == 1:
            candidates.append(group)
    return tuple(candidates)


@question_type(
    "math.contiguous_group_fraction_olympiad",
    display_name={"th": "ขนาดกลุ่มติดกันในแถวจากสัดส่วนคนหน้าและหลัง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อัตราส่วนและสัดส่วน",
)
class ContiguousGroupFraction(WordProblem):
    def expr(self, rng: Random):
        while True:
            front = Fraction(1, rng.randint(3, 8))
            back_denominator = rng.randint(5, 14)
            back = Fraction(rng.randint(1, back_denominator - 1), back_denominator)
            group_share = 1 - front - back
            if group_share <= 0:
                continue
            base_total = lcm(front.denominator, back.denominator)
            base_group = int(base_total * group_share)
            if 5 <= base_group <= 24 and base_total <= 100:
                break
        scale = rng.randint(2, 4)
        total = base_total * scale
        group = base_group * scale
        low = group - rng.randint(1, base_group - 1)
        high = group + rng.randint(1, base_group - 1)
        assert possible_group_sizes(front, back, low, high) == (group,)
        mistaken = [
            total,  # count whole row
            int(total * front),  # count people in front
            int(total * back),  # count people behind
            group + base_group,  # ignore the upper range bound
            group - base_group,  # ignore the lower range bound
        ]
        distractors = [str(value) for value in dict.fromkeys(mistaken) if value != group and value > 0]
        return MathDraw(
            rf"f=\frac{{{front.numerator}}}{{{front.denominator}}},\quad "
            rf"r=\frac{{{back.numerator}}}{{{back.denominator}}},\quad {low}\leq g\leq {high}",
            str(group),
            prompt=("คนกลุ่มหนึ่งยืนติดกันในแถวโดยไม่มีคนนอกกลุ่มแทรก "
                    "จำนวนคนที่อยู่หน้ากลุ่มเป็นสัดส่วน f ของทั้งแถว และจำนวนคนที่อยู่หลังกลุ่มเป็นสัดส่วน r "
                    "ของทั้งแถว ถ้าจำนวนคนในกลุ่ม g อยู่ในช่วงที่กำหนด กลุ่มนี้มีกี่คน"),
            hint="ส่วนของกลุ่มคือ 1-f-r แล้วใช้เงื่อนไขว่าจำนวนคนทุกส่วนต้องเป็นจำนวนเต็ม",
            distractors=distractors,
        )
