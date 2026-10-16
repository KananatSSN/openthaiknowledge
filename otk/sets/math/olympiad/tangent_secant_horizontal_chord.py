"""Circle area from a horizontal chord through a tangent point."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def circle_area_from_tangent_triangle_coefficient(coefficient: int) -> int:
    """Triangle BCE has area coefficient*sqrt(3)/pi when DA=AB/2."""
    if coefficient <= 0:
        raise ValueError("expected positive coefficient")
    # Set the radius to R, A=(0,0), B=(2R,0), D=(-R,0).
    # The upper tangent point is C=(R/2,sqrt(3)R/2), and the
    # same-height point is E=(3R/2,sqrt(3)R/2). Hence [BCE]=sqrt(3)R^2/4.
    return 4 * coefficient


@question_type(
    "math.tangent_horizontal_chord_circle_area_olympiad",
    display_name={"th": "พื้นที่วงกลมจากเส้นสัมผัสและคอร์ดขนานเส้นผ่านศูนย์กลาง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class TangentHorizontalChordCircleArea(WordProblem):
    def expr(self, rng: Random):
        coefficient = rng.randint(5, 40)
        answer = circle_area_from_tangent_triangle_coefficient(coefficient)
        return MathDraw(
            rf"T=\frac{{{coefficient}\sqrt{{3}}}}{{\pi}}",
            str(answer),
            prompt=("AB เป็นเส้นผ่านศูนย์กลางของวงกลม จุด D อยู่บนแนว AB เลย A ออกไป "
                    "โดย DA=AB/2 เส้นสัมผัสจาก D สัมผัสวงกลมด้านบนที่ C "
                    "เส้นผ่าน C ที่ขนานกับ AB พบวงกลมอีกครั้งที่ E "
                    "ถ้าสามเหลี่ยม BCE มีพื้นที่ T จงหาพื้นที่วงกลม"),
            hint=r"[BCE]=\frac{\sqrt{3}}{4}R^2,\qquad [\text{circle}]=\pi R^2",
            distractors=[
                str(coefficient),  # omit geometric factor four
                str(2 * coefficient),  # treat CE as half its actual length
                str(8 * coefficient),  # double triangle height
                str(3 * coefficient),  # confuse sqrt(3) factor with 3
            ],
        )
