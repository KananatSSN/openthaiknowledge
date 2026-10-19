"""PD = PE on two angle bisectors forces ∠A = 60°; extremal 30–60–90 sides."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 2",)
)

# value = r^power · (rational + coefficient·√3)
QUANTITIES = {
    "BC": (1, Fraction(3), Fraction(1)),  # the asked maximum r(3 + √3)
    "AB": (1, Fraction(1), Fraction(1)),  # r(1 + √3), opposite the 30° angle
    "CA": (1, Fraction(2), Fraction(2)),  # hypotenuse 2r(1 + √3)
    "area": (2, Fraction(3), Fraction(2)),  # r²(3 + 2√3)
}
NAMES = {"BC": "ความยาวด้าน BC ที่มากที่สุด", "AB": "ความยาวด้าน AB เมื่อ BC ยาวที่สุด",
         "CA": "ความยาวด้าน CA เมื่อ BC ยาวที่สุด", "area": "พื้นที่ของรูปสามเหลี่ยมเมื่อ BC ยาวที่สุด"}


def extremal_value(asked: str, radius: int) -> tuple[Fraction, Fraction]:
    """PD = PE with ∠B ≠ ∠C makes AEPD cyclic, so ∠BPC = 180° − A = 90° + A/2
    and A = 60°. Then BC = r(cot(B/2) + cot(C/2)) with B + C = 120° is largest
    at the boundary C = 30°, the right triangle with B = 90°."""
    power, rational, root = QUANTITIES[asked]
    scale = radius**power
    return rational * scale, root * scale


def surd3_tex(rational: Fraction, root: Fraction) -> str:
    def num(v: Fraction) -> str:
        return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"

    root_part = ("" if root == 1 else num(root)) + r"\sqrt{3}"
    if rational == 0:
        return root_part
    return f"{num(rational)}+{root_part}"


@question_type(
    "math.equal_bisector_segments_triangle_olympiad",
    display_name={"th": "ด้านมากสุดเมื่อส่วนของเส้นแบ่งครึ่งมุมจากจุดศูนย์กลางวงกลมแนบในเท่ากัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class EqualBisectorSegmentsTriangle(WordProblem):
    def expr(self, rng: Random):
        radius = rng.randint(1, 9)
        asked = rng.choice(tuple(QUANTITIES))
        answer = surd3_tex(*extremal_value(asked, radius))
        candidates = [surd3_tex(*extremal_value(other, radius)) for other in QUANTITIES if other != asked]
        candidates += [
            surd3_tex(Fraction(0), Fraction(2 * radius)),  # the equilateral limit C → 60°: 2r√3
            surd3_tex(Fraction(radius), Fraction(radius)),
        ]
        wrong = [t for t in dict.fromkeys(candidates) if t != answer]
        return MathDraw(
            rf"\angle ABC>\angle BCA\ge 30^\circ,\quad PD=PE,\quad r={radius}",
            answer,
            prompt=(
                "ในรูปสามเหลี่ยม ABC เส้นแบ่งครึ่งมุม B และมุม C ตัดด้านตรงข้ามที่ D และ E "
                "และตัดกันที่ P โดย PD = PE และวงกลมแนบในมีรัศมี r "
                f"จงหา{NAMES[asked]}"
            ),
            hint="ระยะจาก P ถึง AB และ AC เท่ากัน ใช้รูปสามเหลี่ยมมุมฉากที่เท่ากันทุกประการแสดงว่า AEPD เป็นรูปสี่เหลี่ยมแนบในวงกลม จึง ∠A = 60°",
            distractors=wrong,
            variant=asked,
        )
