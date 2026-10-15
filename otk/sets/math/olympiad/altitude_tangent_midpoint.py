"""Find the midpoint cut by two circumcircle tangents."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 4",)
)


def altitude_tangent_midpoint_distance(left: int, right: int, height: int) -> Fraction:
    """DM for D=(0,0), A=(0,h), B=(-u,0), C=(v,0)."""
    if min(left, right, height) <= 0 or height * height <= left * right:
        raise ValueError("the triangle must be acute")
    return Fraction(height * left * right, height * height + left * right)


@question_type(
    "math.altitude_tangent_midpoint_olympiad",
    display_name={"th": "เส้นสัมผัสวงกลมกับจุดกึ่งกลางบนส่วนสูง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิตของวงกลม",
)
class AltitudeTangentMidpoint(WordProblem):
    def expr(self, rng: Random):
        while True:
            left, right, height = (rng.randint(2, 12) for _ in range(3))
            if height * height > left * right:
                break
        answer = altitude_tangent_midpoint_distance(left, right, height)
        return MathDraw(
            rf"BD={left},\quad DC={right},\quad AD={height}",
            str(answer),
            prompt=(
                "ในสามเหลี่ยมมุมแหลม ABC ให้ AD,BE,CF เป็นส่วนสูงและ P=AD∩EF "
                "เส้นสัมผัสวงกลมล้อมรอบ ADC ที่ D ตัด AB ที่ X "
                "เส้นสัมผัสวงกลมล้อมรอบ ADB ที่ D ตัด AC ที่ Y "
                "ถ้า M=XY∩AD จงหา DM"
            ),
            hint=(
                "วาง D=(0,0), A=(0,h), B=(-u,0), C=(v,0) "
                "แล้วหาส่วนสูงของ P กับจุดตัดของเส้นสัมผัสทั้งสอง"
            ),
            distractors=[
                str(2 * answer),  # return DP rather than DM
                str(Fraction(left * right, height * height + left * right)),  # omit h
                str(Fraction(height * left * right, height * height - left * right)),  # wrong sign
                str(Fraction(height * height, height * height + left * right)),  # use h² as numerator
                str(height - answer),  # measure AM rather than DM
                str(answer + 1),  # shift the midpoint height
            ],
        )
