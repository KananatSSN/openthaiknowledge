"""BH = 2R cos B, so BH = t·R gives A′B/AB = cos B = t/2."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 2",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def foot_ratio(t: Fraction) -> Fraction:
    """BH = 2R cos B in an acute triangle, and A′B = AB cos B in the right
    triangle ABA′ (source: BH = R → 1/2)."""
    return t / 2


@question_type(
    "math.orthocenter_altitude_ratio_olympiad",
    display_name={"th": "อัตราส่วนจากระยะจุดยอดถึงจุดออร์โทเซนเตอร์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมล้อมรูปสามเหลี่ยม",
)
class OrthocenterAltitudeRatio(WordProblem):
    def expr(self, rng: Random):
        while True:
            q = rng.randint(1, 9)
            t = Fraction(rng.randint(1, 2 * q - 1), q)
            if t.denominator == q:
                break
        answer = foot_ratio(t)
        wrong = [frac_tex(v) for v in dict.fromkeys([t, 1 - t / 2, t / 4, 2 * t, Fraction(1, 2) if answer != Fraction(1, 2) else Fraction(1, 3)]) if v != answer and v > 0]
        tt = "" if t == 1 else frac_tex(t)
        return MathDraw(
            rf"BH={tt}\,R",
            frac_tex(answer),
            prompt="ABC เป็นรูปสามเหลี่ยมมุมแหลมแนบในวงกลมรัศมี R จาก A และ B ลากเส้นตั้งฉากกับด้านตรงข้ามที่ A′ และ B′ ตามลำดับ เส้นตั้งฉากทั้งสองตัดกันที่ H จงหา A′B/AB",
            hint="ระยะจากจุดยอดถึงจุดออร์โทเซนเตอร์ BH = 2R cos B และในสามเหลี่ยมมุมฉาก ABA′ ได้ A′B = AB cos B",
            distractors=wrong,
        )
