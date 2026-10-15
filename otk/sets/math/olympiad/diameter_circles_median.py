"""Use two diameter circles to locate a cevian intersection on a median."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 8",)
)

_RATIOS = (
    Fraction(1, 4),
    Fraction(1, 3),
    Fraction(2, 5),
    Fraction(1, 2),
    Fraction(3, 5),
    Fraction(2, 3),
    Fraction(3, 4),
)


def median_intersection_height(altitude: int, ratio: Fraction) -> Fraction:
    """Height of BD∩CE above BC when AD/AC=AE/AB=ratio."""
    if altitude <= 0 or not 0 < ratio < 1:
        raise ValueError("expected positive altitude and interior side ratio")
    return altitude * (1 - ratio) / (1 + ratio)


@question_type(
    "math.diameter_circles_median_olympiad",
    display_name={"th": "วงกลมเส้นผ่านศูนย์กลางคู่กับเส้นมัธยฐาน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class DiameterCirclesMedian(WordProblem):
    def expr(self, rng: Random):
        left = rng.randint(2, 8)
        right = rng.randint(2, 8)
        altitude = rng.randint(max(left, right) + 1, 2 * max(left, right) + 4)
        ratio = rng.choice(_RATIOS)
        answer = median_intersection_height(altitude, ratio)
        return MathDraw(
            (
                rf"A=(0,{altitude}),\quad B=(-{left},0),\quad C=({right},0),"
                rf"\quad \frac{{AD}}{{AC}}=\frac{{{ratio.numerator}}}{{{ratio.denominator}}}"
            ),
            str(answer),
            prompt=(
                "ให้ D อยู่ภายใน AC และ E อยู่ภายใน AB วงกลมที่มี BD และ CE "
                "เป็นเส้นผ่านศูนย์กลางตัดกันที่ S,T โดย A,S,T อยู่บนเส้นตรงเดียวกัน "
                "ถ้า P=BD∩CE จงหาระยะจาก P ถึงเส้นตรง BC"
            ),
            hint=(
                "เทียบกำลังของจุด A ต่อวงกลมสองวง จะได้ AD/AC=AE/AB "
                "จากนั้นหา P บนเส้นมัธยฐาน"
            ),
            distractors=[
                str(altitude * (1 - ratio)),  # stop at D's height
                str(altitude / (1 + ratio)),  # omit the numerator factor
                str(altitude * ratio / (1 + ratio)),  # use AP instead of P's height
                str(altitude * (1 - ratio) / (1 + 2 * ratio)),
                # count an extra side-ratio contribution
                str(altitude * ratio),  # use the side-point fraction directly
                str(altitude),  # leave P at A's height
            ],
        )
