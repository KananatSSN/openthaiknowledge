"""Infer rational values from a tangential-quadrilateral identity."""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 3",)
)


def rational_function_value(unit_value: int, numerator: int, denominator: int) -> Fraction:
    """The quadrilateral condition implies additivity and rational homogeneity."""
    if unit_value == 0 or numerator < 1 or denominator < 1:
        raise ValueError("use a nonzero unit value and positive rational input")
    return Fraction(unit_value * numerator, denominator)


@question_type(
    "math.tangential_quadrilateral_additivity_olympiad",
    display_name={"th": "สมการฟังก์ชันจากรูปสี่เหลี่ยมมีวงกลมแนบใน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class TangentialQuadrilateralAdditivity(WordProblem):
    def expr(self, rng: Random):
        denominator = rng.randint(2, 8)
        numerator = rng.randint(2, 13)
        while gcd(numerator, denominator) != 1:
            numerator = rng.randint(2, 13)
        multiplier = rng.randint(2, 9)
        unit_value = denominator * multiplier
        answer = rational_function_value(unit_value, numerator, denominator)
        return MathDraw(
            rf"f(1)={unit_value},\quad x=\frac{{{numerator}}}{{{denominator}}}",
            str(answer),
            prompt=(
                "ให้ f เป็นฟังก์ชันจากจำนวนจริงบวกไปยังจำนวนจริง โดยทุกสี่เหลี่ยมที่มี"
                "วงกลมแนบในและมีด้าน a,b,c,d เป็นไปตาม "
                "f(a+b+c+d)=f(a)+f(b)+f(c)+f(d) "
                "จงหาค่า f(x)"
            ),
            hint=(
                "ใช้รูปสี่เหลี่ยมจัตุรัสและรูปว่าวที่มีด้าน a,b,b,a เพื่อพิสูจน์"
                "สมบัติค่ากึ่งกลาง แล้วอนุมาน f(x+y)=f(x)+f(y)"
            ),
            distractors=[
                str(unit_value * numerator),  # forget the denominator
                str(Fraction(unit_value, numerator * denominator)),  # invert numerator
                str(Fraction(unit_value * denominator, numerator)),  # invert the input
                str(unit_value + numerator),  # add rather than scale
                str(numerator + denominator * multiplier),  # use numerator as a whole increment
                str(answer + denominator),  # add denominator after scaling
            ],
        )
