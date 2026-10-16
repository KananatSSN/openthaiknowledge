"""Classify a positive-real functional equation with a scale factor."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 7",)
)


def sum_of_solution_squares(scale: int) -> Fraction:
    """Sum f(t)^2 over f=0 and f=±1/scale, independent of t>0."""
    if scale < 1:
        raise ValueError("scale must be a positive integer")
    return Fraction(2, scale * scale)


@question_type(
    "math.multiplicative_additive_function_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันของผลคูณและผลบวก"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class MultiplicativeAdditiveFunction(WordProblem):
    def expr(self, rng: Random):
        scale = rng.randint(1, 9)
        point = rng.randint(2, 12)
        answer = sum_of_solution_squares(scale)
        return MathDraw(
            rf"f(xy)={scale * scale}f(x)f(y)f(x+y),\quad t={point}",
            str(answer),
            prompt=(
                "ให้ f วิ่งผ่านฟังก์ชันทุกตัวจากจำนวนจริงบวกไปจำนวนจริง "
                "ซึ่งเป็นไปตามสมการสำหรับทุก x,y>0 "
                "จงหาผลรวมของค่า f(t)² จากฟังก์ชันที่เป็นไปได้ทั้งหมด"
            ),
            hint=(
                "เริ่มจาก f(1) หากไม่เป็นศูนย์ ใช้คู่ x และ 1/x "
                "พิสูจน์ว่าฟังก์ชันไม่เป็นศูนย์เลย แล้วแทน x=1"
            ),
            distractors=[
                str(Fraction(1, scale * scale)),  # count only one nonzero solution
                str(Fraction(2, scale)),  # sum absolute values instead of squares
                str(Fraction(3, scale * scale)),  # include zero as a nonzero square
                str(Fraction(1, scale)),  # omit the second solution and squaring
                "0",  # retain only the zero function
                str(scale * scale),  # invert the coefficient
            ],
        )
