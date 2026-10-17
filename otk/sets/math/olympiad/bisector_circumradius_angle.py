"""The bisector from A meets the circumcircle at D; ∠ADO = |B − C|/2."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 1",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def bisector_radius_angle(angle_b: int, angle_c: int) -> Fraction:
    """D is the midpoint of arc BC, so OD ⟂ BC and OA = OD makes ∠ADO = ∠OAD.
    ∠BAO = 90° − C and ∠BAD = A/2 give ∠OAD = |B − C|/2 (source: 70°, 50° → 10°)."""
    return Fraction(abs(angle_b - angle_c), 2)


@question_type(
    "math.bisector_circumradius_angle_olympiad",
    display_name={"th": "มุมระหว่างเส้นแบ่งครึ่งมุมกับรัศมีวงกลมล้อม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมล้อมรูปสามเหลี่ยม",
)
class BisectorCircumradiusAngle(WordProblem):
    def expr(self, rng: Random):
        while True:
            angle_b, angle_c = rng.randint(35, 85), rng.randint(35, 85)
            angle_a = 180 - angle_b - angle_c
            if angle_b != angle_c and 0 < angle_a < 90 and (angle_b - angle_c) % 2 == 0:
                break
        answer = bisector_radius_angle(angle_b, angle_c)
        wrong = [v for v in dict.fromkeys([Fraction(abs(angle_b - angle_c)), Fraction(angle_a, 2), Fraction(90 - angle_a), Fraction(abs(angle_b - angle_c), 4), Fraction(90 - max(angle_b, angle_c))]) if v != answer]
        return MathDraw(
            rf"\angle ABC={angle_b}^\circ,\quad \angle ACB={angle_c}^\circ",
            frac_tex(answer) + r"^\circ",
            prompt="รูปสามเหลี่ยม ABC แนบในวงกลมที่มี O เป็นจุดศูนย์กลาง เส้นแบ่งครึ่งมุม BAC ตัดวงกลมที่ D จงหาขนาดของมุม ADO",
            hint="D เป็นจุดกึ่งกลางส่วนโค้ง BC จึง OD ตั้งฉากกับ BC และ OA = OD หามุม BAO = 90° − C ก่อน",
            distractors=[frac_tex(v) + r"^\circ" for v in wrong],
        )
