"""The common chord of two circles meets the line of centres at P with PA·PC = PB·PD."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันที่สอง ข้อ 3",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def radical_point(ab: int, ac: int, ad: int) -> Fraction:
    """With A at 0 on the line of centres, P = p has equal power to both
    circles: p(c − p) = (p − b)(d − p), so AP = AB·AD/(AB + AD − AC)."""
    return Fraction(ab * ad, ab + ad - ac)


@question_type(
    "math.radical_axis_point_olympiad",
    display_name={"th": "ตำแหน่งที่คอร์ดร่วมตัดเส้นผ่านจุดศูนย์กลาง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: กำลังของจุด",
)
class RadicalAxisPoint(WordProblem):
    def expr(self, rng: Random):
        while True:
            ab = rng.randint(1, 12)
            ac = rng.randint(ab + 1, ab + 15)
            ad = rng.randint(ac + 1, ac + 15)
            if ad + ab - ac != ac:
                break
        answer = radical_point(ab, ac, ad)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(ab + ac, 2), Fraction(ab * ad, ab + ad), Fraction(ab * ad, ac), Fraction(ac * ad, ac + ad - ab), Fraction(ac + ad - ab, 2)]) if v != answer]
        return MathDraw(
            rf"AB={ab},\quad AC={ac},\quad AD={ad}",
            frac_tex(answer),
            prompt="วงกลมสองวงตัดกันที่ X และ Y เส้นตรงผ่านจุดศูนย์กลางทั้งสองตัดวงแรกที่ A, C และตัดวงที่สองที่ B, D โดยเรียงเป็น A, B, C, D คอร์ดร่วม XY ตัดเส้นตรงนี้ที่ P จงหา AP",
            hint="P อยู่บนแกนกำลังของวงกลมทั้งสอง จึงได้ PA·PC = PB·PD",
            distractors=wrong,
        )
