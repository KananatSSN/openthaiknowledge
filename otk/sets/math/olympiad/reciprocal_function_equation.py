"""Evaluate the unique positive solution of a nested functional equation."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def reciprocal_function_value(constant: int, argument: int) -> Fraction:
    """The equation forces f(x)=sqrt(constant)/x."""
    root = isqrt(constant)
    if constant <= 0 or root * root != constant or argument <= 0:
        raise ValueError("positive square constant and argument required")
    return Fraction(root, argument)


@question_type(
    "math.reciprocal_function_equation_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันแบบส่วนกลับ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class ReciprocalFunctionEquation(WordProblem):
    def expr(self, rng: Random):
        argument = rng.randint(2, 8)
        factor = rng.choice(tuple(k for k in range(2, 9) if k != argument))
        root = argument * factor
        constant = root * root
        answer = reciprocal_function_value(constant, argument)
        return MathDraw(
            rf"c={constant},\quad t={argument}",
            str(answer),
            prompt=(
                "ฟังก์ชัน f จากจำนวนจริงบวกไปยังจำนวนจริงบวกสอดคล้องกับ "
                "x² f(xf(y)) f(x) f(y)=c สำหรับทุก x,y>0 จงหา f(t)"
            ),
            hint="กำหนด F(x)=xf(x) และปรับค่าคงตัว c ให้เป็น 1 ก่อน",
            distractors=[
                str(root * argument),  # multiply instead of divide by t
                str(Fraction(constant, argument)),  # use c instead of its square root
                str(Fraction(argument, root)),  # invert the reciprocal solution
                str(root + argument),  # add argument to the scale
            ],
        )
