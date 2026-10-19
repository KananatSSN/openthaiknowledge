"""Circles in the 60° angle at A: each next circle has a third of the radius."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 3",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def second_radius(k: int) -> Fraction:
    """AB = k√3, BC = 3k gives ∠A = 60°. The circle tangent to AB at B and to
    AC has radius AB·tan 30° = k; for circles in an angle of half-width 30°,
    consecutive radii have ratio (1 − sin 30°)/(1 + sin 30°) = 1/3."""
    return Fraction(k, 3)


@question_type(
    "math.angle_chain_circle_radius_olympiad",
    display_name={"th": "รัศมีวงกลมที่สัมผัสกันในมุม 60°"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมสัมผัสกัน",
)
class AngleChainCircleRadius(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(1, 12)
        answer = second_radius(k)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(k), Fraction(3 * k), Fraction(k, 2), Fraction(k, 9), Fraction(2 * k, 3)]) if v != answer]
        ab = "" if k == 1 else str(k)
        return MathDraw(
            rf"\angle B=90^\circ,\quad AB={ab}\sqrt{{3}},\quad BC={3 * k}",
            frac_tex(answer),
            prompt="วงกลมวงแรกสัมผัส AB ที่ B และสัมผัส AC วงกลมวงที่สองอยู่ใกล้ A สัมผัสวงแรก และสัมผัส AB, AC จงหารัศมีของวงที่สอง",
            hint="หามุม A ก่อน วงกลมทั้งสองมีจุดศูนย์กลางบนเส้นแบ่งครึ่งมุม A อัตราส่วนรัศมีคือ (1 − sin(A/2))/(1 + sin(A/2))",
            distractors=wrong,
        )
