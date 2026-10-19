"""Area of BGH when AD (D the midpoint of BC) cuts BE and BF, E, F on AC."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 4",))

SPLITS = ((Fraction(1, 3), Fraction(2, 3)), (Fraction(1, 4), Fraction(1, 2)), (Fraction(1, 4), Fraction(3, 4)),
          (Fraction(1, 5), Fraction(2, 5)), (Fraction(2, 5), Fraction(4, 5)), (Fraction(1, 2), Fraction(3, 4)),
          (Fraction(1, 3), Fraction(1, 2)), (Fraction(1, 6), Fraction(1, 2)))


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def _intersect(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])


def _area(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) / 2


def area_ratio(f: Fraction, e: Fraction) -> Fraction:
    """Ratios of areas are affine invariants, so a unit right triangle with
    A = (0, 0), B = (1, 0), C = (0, 1) gives the answer exactly; F and E sit
    at AF/AC = f and AE/AC = e (1/3 and 2/3 in the source: 3/20)."""
    a, b, c = (Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))
    d = (Fraction(1, 2), Fraction(1, 2))
    point_f, point_e = (Fraction(0), f), (Fraction(0), e)
    g = _intersect(a, d, b, point_e)
    h = _intersect(a, d, b, point_f)
    return _area(b, g, h) / _area(a, b, c)


@question_type(
    "math.cevian_division_area_olympiad",
    display_name={"th": "อัตราส่วนพื้นที่จากเส้นมัธยฐานตัดเส้นจากจุดยอด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สามเหลี่ยมและเส้นมัธยฐาน",
)
class CevianDivisionArea(WordProblem):
    def expr(self, rng: Random):
        f, e = rng.choice(SPLITS)
        answer = area_ratio(f, e)
        wrong = [frac_tex(v) for v in dict.fromkeys([(e - f) / 2, (e - f) / 4, answer * 2, answer / 2, (e - f) * Fraction(1, 3)]) if v != answer and v > 0]
        return MathDraw(
            rf"\frac{{AF}}{{AC}}={frac_tex(f)},\quad \frac{{AE}}{{AC}}={frac_tex(e)}",
            frac_tex(answer),
            prompt="D เป็นจุดกึ่งกลางของ BC จุด F และ E อยู่บน AC ตามอัตราส่วนต่อไปนี้ AD ตัด BE ที่ G และตัด BF ที่ H จงหาพื้นที่ △BGH ต่อพื้นที่ △ABC",
            hint="อัตราส่วนพื้นที่ไม่เปลี่ยนภายใต้การแปลงอะฟฟีน เลือกพิกัด A, B, C ที่สะดวก หรือใช้วิธีมวลจุด",
            distractors=wrong,
        )
