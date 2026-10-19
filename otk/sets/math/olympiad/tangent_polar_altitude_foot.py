"""In the tangent configuration of the circle on BC, S is the foot from A."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 11",)
)


def foot_distance(a: int, b: int, c: int) -> Fraction:
    """QR is the A-altitude, so S is its foot and BS = c·cos B
    = (a² + c² − b²)/(2a); QS then bisects ∠DSE since S sees the chord of
    contact DE symmetrically (the polar of A passes through Q)."""
    return Fraction(a * a + c * c - b * b, 2 * a)


TRIANGLES = tuple(
    (a, b, c)
    for a in range(5, 18) for b in range(4, 18) for c in range(4, 18)
    if a * a < b * b + c * c and b * b < a * a + c * c and c * c < a * a + b * b and b != c
)


def _tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


@question_type(
    "math.tangent_polar_altitude_foot_olympiad",
    display_name={"th": "จุดตัดในรูปเส้นสัมผัสวงกลมที่มี BC เป็นเส้นผ่านศูนย์กลาง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: เส้นสัมผัสวงกลม",
)
class TangentPolarAltitudeFoot(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(TRIANGLES)
        answer = foot_distance(a, b, c)
        wrong = [_tex(v) for v in dict.fromkeys([
            Fraction(a, 2),  # the centre of the circle
            Fraction(a * a + b * b - c * c, 2 * a),  # CS instead
            Fraction(c * c, a),  # B's projection the other way
            Fraction(a + c - b, 2),  # the incircle touch point
            Fraction(a * c, b + c),  # the angle-bisector foot
        ]) if v != answer and v > 0]
        return MathDraw(
            rf"BC={a},\ CA={b},\ AB={c}",
            _tex(answer),
            prompt=(
                "รูปสามเหลี่ยมมุมแหลม ABC มี CP เป็นส่วนสูงจาก C วงกลม ω มี BC เป็นเส้นผ่านศูนย์กลาง "
                "จาก A ลากเส้นสัมผัส ω ที่ D และ E ซึ่งตัด BC ที่ M และ N CP ตัด DE ที่ Q, ME ตัด ND ที่ R "
                "และเส้นตรง QR ตัด BC ที่ S จงหา BS"
            ),
            hint="DE เป็นเส้นโพลาร์ของ A เทียบกับ ω แสดงว่า Q และ R อยู่บนส่วนสูงจาก A",
            distractors=wrong,
        )
