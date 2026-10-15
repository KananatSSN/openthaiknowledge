"""Sum perimeters of three triangles cut off by parallels through an incenter."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def parallel_incenter_perimeter_sum(area: int, inradius: int) -> int:
    """Each of the three O-vertex triangles has perimeter of one ABC side."""
    if area <= 0 or inradius <= 0 or (2 * area) % inradius:
        raise ValueError("expected a positive integral perimeter")
    return 2 * area // inradius


@question_type(
    "math.incenter_parallel_perimeter_sum_olympiad",
    display_name={"th": "ผลรวมเส้นรอบรูปสามเหลี่ยมจากเส้นขนานผ่านจุดศูนย์กลางใน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สามเหลี่ยม",
)
class IncenterParallelPerimeterSum(WordProblem):
    def expr(self, rng: Random):
        leg1, leg2, hypotenuse = rng.choice(((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)))
        scale = rng.randint(1, 4)
        area = leg1 * leg2 * scale**2 // 2
        inradius = (leg1 + leg2 - hypotenuse) * scale // 2
        answer = parallel_incenter_perimeter_sum(area, inradius)
        return MathDraw(
            rf"T={area},\quad r={inradius}",
            str(answer),
            prompt=("สามเหลี่ยมรูปหนึ่งมีพื้นที่ T และวงกลมแนบในรัศมี r "
                    "ลากเส้นผ่านจุดศูนย์กลางวงกลมแนบในให้ขนานกับด้านทั้งสาม "
                    "บนแต่ละด้านจะได้จุดตัดสองจุดจากเส้นขนานกับอีกสองด้าน "
                    "นำจุดตัดทั้งคู่กับจุดศูนย์กลางมาสร้างสามเหลี่ยม "
                    "ผลรวมเส้นรอบรูปของสามเหลี่ยมทั้งสามเป็นเท่าใด"),
            hint=r"T=rs,\qquad \text{perimeter of each small triangle equals one side of the original}",
            distractors=[
                str(area // inradius),  # report semiperimeter
                str(Fraction(area, 2 * inradius)),  # use diameter for inradius and halve again
                str(3 * area // inradius),  # count three semiperimeters
                str(2 * area * inradius),  # multiply rather than divide by inradius
            ],
        )
