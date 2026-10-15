"""Slope of a collinear triple in an acute orthocenter construction."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def orthocenter_collinearity_slope(parameter: Fraction) -> Fraction:
    """For the rationally parameterized triangle, slope(DST)."""
    if parameter <= 0:
        raise ValueError("positive parameter required")
    return (1 - 3 * parameter**2) / (4 * parameter)


@question_type(
    "math.orthocenter_circumcircle_collinearity_olympiad",
    display_name={"th": "เส้นตรงร่วมจากออร์โทเซนเตอร์และวงกลมล้อมรอบ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class OrthocenterCircumcircleCollinearity(WordProblem):
    def expr(self, rng: Random):
        parameter = rng.choice(
            (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(1), Fraction(3, 2), Fraction(2))
        )
        u = 1 / (1 + 3 * parameter**2)
        v = 3 * parameter / (1 + 3 * parameter**2)
        answer = orthocenter_collinearity_slope(parameter)
        return MathDraw(
            rf"A=({u},{v}),\quad B=(0,0),\quad C=(1,0)",
            str(answer),
            prompt=(
                "ให้ D เป็นเท้าฉากจาก A ไป BC และ H เป็นออร์โทเซนเตอร์ "
                "จุด S,T อยู่บนวงกลมล้อมรอบ ABC โดย ∠BSH=∠CTH=90° "
                "จงหาความชันของเส้นตรงที่ผ่าน D,S,T"
            ),
            hint="เขียนสมการวงกลมล้อมรอบกับวงกลมเส้นผ่านศูนย์กลาง BH และ CH",
            distractors=[
                str(-answer),  # reverse the line's slope sign
                str(answer / 3),  # use AH instead of HD
                str(4 * answer),  # omit the factor four in the denominator
                str(-u * answer),  # give the y-intercept rather than slope
            ],
        )
