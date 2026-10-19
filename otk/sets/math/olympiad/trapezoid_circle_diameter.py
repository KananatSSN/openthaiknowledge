"""DF is a diameter: DE ∥ BC and EF ⊥ BC, so DF = 2R of triangle BCF."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 2",)
)


def diameter(x: int, y: int, z: int) -> Fraction:
    """BCED is an isosceles trapezoid (DE ∥ BC); EF ⊥ BC makes ∠DEF = 90°,
    so DF = 2R = xyz/(2Δ) for triangle BCF with BC = x, CF = y, BF = z."""
    sixteen_area_sq = 2 * (x * x * y * y + y * y * z * z + z * z * x * x) - x**4 - y**4 - z**4
    four_area = isqrt(sixteen_area_sq)
    if four_area * four_area != sixteen_area_sq:
        raise ValueError("not a Heronian triangle")
    return Fraction(2 * x * y * z, four_area)


HERONIAN = tuple(
    (x, y, z)
    for x in range(3, 40) for y in range(3, 40) for z in range(3, 40)
    if y != z and x < y + z and y < x + z and z < x + y
    and isqrt(2 * (x * x * y * y + y * y * z * z + z * z * x * x) - x**4 - y**4 - z**4) ** 2
    == 2 * (x * x * y * y + y * y * z * z + z * z * x * x) - x**4 - y**4 - z**4
)


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


@question_type(
    "math.trapezoid_circle_diameter_olympiad",
    display_name={"th": "DF เป็นเส้นผ่านศูนย์กลางในรูปสามเหลี่ยมหน้าจั่วกับวงกลม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class TrapezoidCircleDiameter(WordProblem):
    def expr(self, rng: Random):
        x, y, z = rng.choice(HERONIAN)
        answer = diameter(x, y, z)
        wrong = [frac_tex(v) for v in dict.fromkeys([
            answer / 2,  # the radius
            Fraction(y * z, x),
            Fraction(y + z, 2),
            Fraction(x),
            answer + Fraction(1, 2),
        ]) if v != answer]
        return MathDraw(
            rf"BC={x},\quad CF={y},\quad BF={z}",
            frac_tex(answer),
            prompt=(
                "รูปสามเหลี่ยม ABC มี AB = AC วงกลมผ่าน B, C ตัด AB, AC ที่ D, E "
                "และ F เป็นจุดบนวงกลมนี้ที่ทำให้ EF ⊥ BC จงหา DF"
            ),
            hint="BCED เป็นรูปสี่เหลี่ยมคางหมูหน้าจั่ว DE ∥ BC จึง ∠DEF = 90° และ DF เป็นเส้นผ่านศูนย์กลาง",
            distractors=wrong,
        )
