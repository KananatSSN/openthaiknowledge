"""Optimize a cyclic product under a sum of cube roots."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def cyclic_cube_product_maximum(scale: int) -> Fraction:
    """Maximum when the four cube roots sum to 4*scale."""
    if scale <= 0:
        raise ValueError("scale must be positive")
    return Fraction(4**14 * scale**24, 5**10)


@question_type(
    "math.cyclic_cube_product_maximum_olympiad",
    display_name={"th": "ค่าสูงสุดของผลคูณวนรอบภายใต้ผลบวกรากที่สาม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ค่าสูงสุด-ต่ำสุดสัมพัทธ์",
)
class CyclicCubeProductMaximum(WordProblem):
    def expr(self, rng: Random):
        scale = rng.randint(1, 3)
        answer = cyclic_cube_product_maximum(scale)
        pair_sum_at_maximum = Fraction(16 * scale**3, 5)
        wrong_stationary = Fraction(3, 4) ** 6 * Fraction(7, 2) ** 4 * scale**24
        return MathDraw(
            rf"\sqrt[3]a+\sqrt[3]b+\sqrt[3]c+\sqrt[3]d={4 * scale}",
            str(answer),
            prompt=(
                "เมื่อ a,b,c,d เป็นจำนวนจริงบวกและผลบวกรากที่สามเป็นค่าที่กำหนด "
                "จงหาค่าสูงสุดของ abcd(a+b)(b+c)(c+d)(d+a)"
            ),
            hint="ให้รากที่สามของตัวแปรที่อยู่ตรงข้ามกันเท่ากัน แล้วใช้ผลคูณของสองค่าที่เหลือ",
            distractors=[
                str(16 * scale**24),  # assume all four cube roots are equal
                str(pair_sum_at_maximum**4),  # omit abcd
                str(answer / pair_sum_at_maximum),  # omit one pair-sum factor
                str(wrong_stationary),  # use u=3/4 instead of 4/5
            ],
        )
