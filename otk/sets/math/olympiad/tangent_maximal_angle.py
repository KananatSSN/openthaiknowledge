"""∠ABC is largest when BA touches the circle through M, C, A: BA² = BM·BC."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 6",))


def ratio_square(m: int, n: int) -> Fraction:
    """A runs over an arc through M and C (∠MAC fixed); ∠ABC is largest when
    BA is tangent to it, so BA² = BM·BC and (BC/BA)² = BC/BM = (m + n)/m."""
    return Fraction(m + n, m)


def sqrt_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return rf"\sqrt{{{v.numerator}}}"
    return rf"\sqrt{{\frac{{{v.numerator}}}{{{v.denominator}}}}}"


@question_type(
    "math.tangent_maximal_angle_olympiad",
    display_name={"th": "อัตราส่วนด้านเมื่อมุม B มากที่สุด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: เส้นสัมผัสวงกลม",
)
class TangentMaximalAngle(WordProblem):
    def expr(self, rng: Random):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        answer = sqrt_tex(ratio_square(m, n))
        wrong = [t for t in dict.fromkeys([sqrt_tex(ratio_square(n, m)), sqrt_tex(Fraction(m + n, n) * 2), rf"\frac{{{m + n}}}{{{m}}}", sqrt_tex(Fraction(2)), sqrt_tex(Fraction(m + n + 1, m))]) if t != answer]
        return MathDraw(
            rf"BM:MC={m}:{n},\quad \angle MAC=20^\circ",
            answer,
            prompt="M อยู่บนส่วนของเส้นตรง BC และ A เป็นจุดใด ๆ ที่ทำให้ ∠MAC = 20° ถ้า ∠ABC มีขนาดมากที่สุด จงหา BC/BA",
            hint="A อยู่บนส่วนโค้งของวงกลมผ่าน M, C มุม ABC มากที่สุดเมื่อ BA สัมผัสวงกลมนี้ แล้วใช้กำลังของจุด B",
            distractors=wrong,
        )
