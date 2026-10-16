"""Recover a rectangular box's capacity from three water depths."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt, prod
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def capacity_from_water_depths(
    water_volume: int, depths: tuple[Fraction, Fraction, Fraction]
) -> Fraction:
    """Return box capacity when each depth is measured in a different orientation."""
    if water_volume <= 0 or len(depths) != 3 or any(depth <= 0 for depth in depths):
        raise ValueError("expected positive volume and three positive depths")
    capacity_squared = Fraction(water_volume**3, 1) / prod(depths)
    numerator_root = isqrt(capacity_squared.numerator)
    denominator_root = isqrt(capacity_squared.denominator)
    if numerator_root**2 != capacity_squared.numerator or denominator_root**2 != capacity_squared.denominator:
        raise ValueError("depths do not give a rational box capacity")
    return Fraction(numerator_root, denominator_root)


@question_type(
    "math.three_orientation_box_volume_olympiad",
    display_name={"th": "หาความจุกล่องจากระดับน้ำสามทิศทาง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ปริมาตร",
)
class ThreeOrientationBoxVolume(WordProblem):
    def expr(self, rng: Random):
        scale = rng.randint(2, 4)
        depths = tuple(rng.sample(range(2, 8), 3))
        water_volume = scale**2 * prod(depths)
        answer = capacity_from_water_depths(water_volume, depths)
        return MathDraw(
            rf"V={water_volume},\quad h_1={depths[0]},\quad h_2={depths[1]},\quad h_3={depths[2]}",
            str(answer),
            prompt=("ภาชนะทรงสี่เหลี่ยมมุมฉากมีน้ำปริมาตร V "
                    "เมื่อเปลี่ยนด้านที่วางเป็นฐานทั้งสามแบบโดยไม่หก "
                    "ระดับน้ำที่วัดตั้งฉากกับฐานเป็น h₁, h₂, h₃ ตามลำดับ "
                    "ภาชนะมีความจุทั้งหมดกี่ลูกบาศก์หน่วย"),
            hint=r"V=h_1A_1=h_2A_2=h_3A_3,\qquad C^2=A_1A_2A_3",
            distractors=[
                str(water_volume),  # confuse current water with full capacity
                str(answer * scale),  # apply fill correction twice
                str(prod(depths)),  # mistake water depths for side lengths
            ],
        )
