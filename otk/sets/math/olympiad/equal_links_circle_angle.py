"""Central angle from four equal links on a circle chord."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def central_angle_from_equal_links(apex_angle: int) -> int:
    """A,B,D,E are collinear, AB=BC=CD=DE, and A,C,E are on a circle."""
    if not 0 < apex_angle < 180:
        raise ValueError("expected angle strictly between 0 and 180 degrees")
    # Isosceles BCD has base angles (180-alpha)/2. The adjoining
    # isosceles triangles ABC and CDE each contribute an angle
    # (180-alpha)/4 at C.
    # So ACE=alpha+(180-alpha)/2=90+alpha/2, and the minor
    # central angle AOE is 360-2*ACE=180-alpha.
    return 180 - apex_angle


@question_type(
    "math.equal_links_circle_central_angle_olympiad",
    display_name={"th": "มุมที่จุดศูนย์กลางจากด้านเท่ากันสี่ช่วง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class EqualLinksCircleCentralAngle(WordProblem):
    def expr(self, rng: Random):
        apex_angle = rng.choice([angle for angle in range(35, 90) if angle != 60])
        answer = central_angle_from_equal_links(apex_angle)
        return MathDraw(
            rf"\angle BCD={apex_angle}^\circ",
            str(answer),
            prompt=("จุด A, B, D, E เรียงอยู่บนเส้นตรงเดียวกันตามลำดับ "
                    "และ AB=BC=CD=DE โดย C อยู่ด้านหนึ่งของเส้นตรง "
                    "วงกลมที่ผ่าน A, C, E มีจุดศูนย์กลาง O อยู่อีกด้านของเส้น AE "
                    "ถ้ามุม BCD ตามที่กำหนด มุม AOE ที่เล็กกว่า 180° มีขนาดกี่องศา"),
            hint=r"\angle ACE=90^\circ+\frac12\angle BCD",
            distractors=[
                str(apex_angle),  # confuse apex and central angle
                str(180 - apex_angle // 2),  # halve only apex angle
                str(2 * apex_angle),  # double rather than supplement
                str(Fraction(180 + apex_angle, 2)),  # report inscribed angle ACE
            ],
        )
