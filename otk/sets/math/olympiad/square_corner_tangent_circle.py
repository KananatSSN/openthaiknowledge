"""Square area from a circle tangent to two sides and passing its center."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def square_area_from_corner_circle_scale(scale: Fraction) -> Fraction:
    """The circle radius is scale*(sqrt(2)-1), with the circle inside the square."""
    if scale <= 0:
        raise ValueError("expected positive scale")
    # Circle center is (r,r), square center is (s/2,s/2).
    # Since r<s/2, sqrt(2)*(s/2-r)=r, so s=scale*sqrt(2).
    return 2 * scale**2


@question_type(
    "math.square_center_corner_tangent_circle_olympiad",
    display_name={"th": "พื้นที่สี่เหลี่ยมจัตุรัสจากวงกลมสัมผัสสองด้านและผ่านจุดศูนย์กลาง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class SquareCenterCornerTangentCircle(WordProblem):
    def expr(self, rng: Random):
        scale = Fraction(rng.randint(2, 10), rng.randint(1, 3))
        answer = square_area_from_corner_circle_scale(scale)
        return MathDraw(
            rf"r=\frac{{{scale.numerator}}}{{{scale.denominator}}}(\sqrt{{2}}-1)",
            str(answer),
            prompt=("วงกลมอยู่ภายในสี่เหลี่ยมจัตุรัสและสัมผัสด้านที่ประกอบเป็นมุมหนึ่ง "
                    "วงกลมผ่านจุดศูนย์กลางของสี่เหลี่ยม ถ้ารัศมีเป็น r ตามที่กำหนด "
                    "พื้นที่สี่เหลี่ยมจัตุรัสเท่าใด"),
            hint=r"\sqrt{2}(s/2-r)=r",
            distractors=[
                str(scale**2),  # omit the square diagonal factor
                str(4 * scale**2),  # replace sqrt(2) side factor by 2
                str(2 * scale),  # forget to square the side scale
                str(8 * scale**2),  # use the full diagonal as a side
            ],
        )
