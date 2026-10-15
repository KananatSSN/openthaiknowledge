"""Area of a circle from two intersecting perpendicular chords."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def perpendicular_chord_radius_squared(first: int, second: int, third: int) -> Fraction:
    """Chords meet at P, with distances a,b on one and c,d on the other."""
    if min(first, second, third) <= 0:
        raise ValueError("chord segments must be positive")
    fourth = Fraction(first * second, third)
    # Intersecting-chord theorem gives a*b=c*d. With P at the origin,
    # the center is ((b-a)/2,(d-c)/2), and r^2=OP^2+a*b.
    return (
        Fraction(first * second)
        + Fraction((second - first) ** 2, 4)
        + (fourth - third) ** 2 / 4
    )


@question_type(
    "math.perpendicular_chord_circle_area_olympiad",
    display_name={"th": "พื้นที่วงกลมจากคอร์ดตั้งฉากสองเส้น"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class PerpendicularChordCircleArea(WordProblem):
    def expr(self, rng: Random):
        first = 2 * rng.randint(1, 7)
        second = 2 * rng.randint(2, 8)
        product = first * second
        candidates = [c for c in range(2, 17, 2) if product % c == 0 and product // c <= 30]
        third = rng.choice(candidates)
        fourth = product // third
        answer = perpendicular_chord_radius_squared(first, second, third)
        midpoint_error = Fraction((second - first) ** 2 + (fourth - third) ** 2, 4)
        return MathDraw(
            rf"PA={first},\quad PB={second},\quad PC={third}",
            str(answer),
            prompt=("คอร์ด AB และ CD ของวงกลมตัดกันเป็นมุมฉากที่จุด P "
                    "โดยมีระยะ PA, PB, PC ตามที่กำหนด "
                    "ถ้าพื้นที่วงกลมเป็น kπ ตารางหน่วย จงหา k"),
            hint=r"PA\cdot PB=PC\cdot PD,\qquad r^2=PA\cdot PB+OP^2",
            distractors=[
                str(product),  # treat chord product as radius squared
                str(midpoint_error),  # omit point power
                str(answer + product),  # add point power twice
                str(Fraction((first + second) ** 2, 4)),  # assume first chord is a diameter
            ],
        )
