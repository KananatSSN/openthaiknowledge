"""Median AD, centroid P, ∠CAD = α and ∠APB = β fix AB/BC: AC = 4 sin β/sin(β − α) for AD = 3."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 9",))

# (α, β) → (AB/BC)² = (p + q√3)/r
TABLE = {
    (15, 60): (4, -1, 13),
    (30, 60): (1, 0, 7),
    (30, 90): (7, 0, 19),
    (45, 90): (5, 0, 17),
    (30, 75): (34, -15, 37),
    (30, 105): (109, 6, 193),
    (15, 120): (5, 2, 5),
    (30, 120): (1, 0, 1),
    (45, 135): (1, 0, 1),
}


def ratio_squared(alpha: int, beta: int) -> tuple[int, int, int]:
    """With A at the origin, AD = 3 along the x-axis and P = (2, 0), C at
    angle α and B = 2D − C, ∠APB = β gives AC = 4 sin β/sin(β − α); then
    AB² = 36 − 12·AC cos α + AC², BC² = 36 − 24·AC cos α + 4AC²."""
    return TABLE[(alpha, beta)]


def ratio_tex(p: int, q: int, r: int) -> str:
    if q == 0:
        v = Fraction(p, r)
        if v == 1:
            return "1"
        num, den = v.numerator, v.denominator
        return rf"\sqrt{{\frac{{{num}}}{{{den}}}}}"
    sign = "+" if q > 0 else "-"
    coef = "" if abs(q) == 1 else str(abs(q))
    return rf"\sqrt{{\frac{{{p}{sign}{coef}\sqrt{{3}}}}{{{r}}}}}"


@question_type(
    "math.centroid_angle_ratio_olympiad",
    display_name={"th": "อัตราส่วนด้านจากมุมที่จุดเซนทรอยด์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต",
)
class CentroidAngleRatio(WordProblem):
    def expr(self, rng: Random):
        alpha, beta = rng.choice(tuple(TABLE))
        answer = ratio_tex(*ratio_squared(alpha, beta))
        others = [ratio_tex(*v) for k, v in TABLE.items() if k != (alpha, beta)]
        wrong = [t for t in dict.fromkeys(others) if t != answer]
        rng.shuffle(wrong)
        return MathDraw(
            rf"\angle CAD={alpha}^\circ,\quad \angle APB={beta}^\circ",
            answer,
            prompt="D, E เป็นจุดกึ่งกลางของ BC และ AC และ AD ตัด BE ที่ P จงหา AB/BC",
            hint="P เป็นจุดเซนทรอยด์ AP = 2PD ตั้งพิกัดให้ AD อยู่บนแกน x แล้วใช้มุมทั้งสองหา AC",
            distractors=wrong[:5],
        )
