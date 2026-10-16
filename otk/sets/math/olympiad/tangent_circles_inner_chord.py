"""Find the inner segment cut by two circles from a tangent construction."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2566, ข้อ 8",)
)


def inner_chord_length(a: int, u: int, v: int) -> Fraction:
    """PQ for A=(-a,0), B=(a,0), C=(u,v) in the tangent-circle construction."""
    if not (a > 0 and -a < u < a and v > 0 and u * u + v * v > a * a):
        raise ValueError("ABC must be acute with C above AB")
    radius_squared = u * u + v * v
    return Fraction(2 * a * (radius_squared - a * a), radius_squared + a * a)


@question_type(
    "math.tangent_circles_inner_chord_olympiad",
    display_name={"th": "ระยะตัดภายในจากวงกลมคู่และเส้นสัมผัส"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class TangentCirclesInnerChord(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(2, 8)
        u = rng.randint(1 - a, a - 1)
        v = rng.randint(a + 1, 2 * a + 3)
        length = inner_chord_length(a, u, v)
        radius_squared = u * u + v * v
        outer_chord = length + 2 * a
        return MathDraw(
            rf"A=(-{a},0),\quad B=({a},0),\quad C=({u},{v})",
            str(length),
            prompt=(
                "ในสามเหลี่ยม ABC ลากเส้นสัมผัสวงกลมล้อมรูปที่ A และ B "
                "ให้จุดตัดเป็น T และให้ D=CT∩AB วงกลม CAD ตัด TA อีกครั้งที่ E "
                "วงกลม CBD ตัด TB อีกครั้งที่ F เส้น EF ตัด AC ที่ P และ BC ที่ Q "
                "จงหาความยาว PQ"
            ),
            hint=(
                "ใช้พิกัดของจุดตัดเส้นสัมผัสหา D แล้วหาจุดตัดครั้งที่สองของ "
                "เส้น TA และ TB กับวงกลมทั้งสอง"
            ),
            distractors=[
                str(outer_chord),  # return EF instead of PQ
                str(Fraction(2 * a * radius_squared, radius_squared + a * a)),
                # omit the contribution from the short side of the line
                str(Fraction(2 * a * a * a, radius_squared + a * a)),
                # return the complement AB-PQ
                str(2 * a),  # return AB
                str(Fraction(2 * a * radius_squared, radius_squared - a * a)),
                # reverse the sign in the denominator
            ],
        )
