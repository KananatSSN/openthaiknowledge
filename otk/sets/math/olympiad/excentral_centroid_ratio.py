"""I, the excentral centroid G and the intouch orthocentre H are collinear, IG : IH = 4R : 3r."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 11",)
)


def collinear_ratio(a: int, b: int, c: int) -> Fraction:
    """I is the circumcentre of XYZ, so IH is the Euler line of XYZ. The sides
    of the excentral triangle are parallel to those of XYZ (both are
    perpendicular to the bisectors), so the two triangles are homothetic and
    the centroid of one maps to the centroid of the other on that line.
    IG/IH = 4R/(3r) = abc/(3(s − a)(s − b)(s − c)), checked by coordinates."""
    s2 = a + b + c  # 2s
    return Fraction(8 * a * b * c, 3 * (s2 - 2 * a) * (s2 - 2 * b) * (s2 - 2 * c))


TRIANGLES = tuple(
    (a, b, c)
    for a in range(3, 15) for b in range(a, 15) for c in range(b, 15)
    if c < a + b and not (a == b == c)
)


def _tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


@question_type(
    "math.excentral_centroid_ratio_olympiad",
    display_name={"th": "อัตราส่วนบนเส้นตรงผ่านจุดศูนย์กลางวงกลมแนบใน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class ExcentralCentroidRatio(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(TRIANGLES)
        answer = collinear_ratio(a, b, c)
        r_over = answer * Fraction(3, 4)  # R/r
        wrong = [_tex(v) for v in dict.fromkeys([r_over, r_over * 2, answer / 2, answer * Fraction(3, 2), r_over + 1]) if v != answer]
        return MathDraw(
            rf"BC={a},\ CA={b},\ AB={c}",
            _tex(answer),
            prompt=(
                "I เป็นจุดศูนย์กลางวงกลมแนบในของรูปสามเหลี่ยม ABC ซึ่งสัมผัสด้านที่ X, Y, Z "
                "G เป็นจุดเซนทรอยด์ของรูปสามเหลี่ยมที่มีจุดยอดเป็นจุดศูนย์กลางวงกลมแนบนอกทั้งสาม "
                "และ H เป็นจุดออร์โทเซนเตอร์ของรูปสามเหลี่ยม XYZ ซึ่งสามจุดนี้อยู่บนเส้นตรงเดียวกัน จงหา IG/IH"
            ),
            hint="I เป็นจุดศูนย์กลางวงกลมล้อมรอบ XYZ ใช้เส้นออยเลอร์ของ XYZ และคำนวณด้วย R/r = abc/(4(s − a)(s − b)(s − c))",
            distractors=wrong,
        )
