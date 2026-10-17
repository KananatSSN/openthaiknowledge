"""AB a diameter of the unit circle, DC = k·AD: AD = (√(k² + 8) − k)/2."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 1",))


def leg_tex(k: int, extra: int = 8, sign: int = -1, half: bool = True) -> str:
    """With D = (−c, s), C = (c, s): AD² = 2 − 2c and DC = 2c = k·AD give
    AD² + k·AD − 2 = 0, so AD = (√(k² + 8) − k)/2 (source: k = 4 → √6 − 2).
    The keyword arguments render the named mistakes."""
    inside, outside, f = k * k + extra, 1, 2
    while f * f <= inside:
        while inside % (f * f) == 0:
            inside //= f * f
            outside *= f
        f += 1
    op = "-" if sign < 0 else "+"
    if inside == 1:
        value = Fraction(outside + sign * k, 2 if half else 1)
        return str(value) if value.denominator == 1 else rf"\frac{{{value.numerator}}}{{{value.denominator}}}"
    if half and outside % 2 == 0 and k % 2 == 0:
        o = "" if outside // 2 == 1 else str(outside // 2)
        return rf"{o}\sqrt{{{inside}}}{op}{k // 2}"
    o = "" if outside == 1 else str(outside)
    body = rf"{o}\sqrt{{{inside}}}{op}{k}"
    return rf"\frac{{{body}}}{{2}}" if half else body


@question_type(
    "math.inscribed_trapezoid_leg_olympiad",
    display_name={"th": "ความยาวขาของรูปสี่เหลี่ยมคางหมูแนบในครึ่งวงกลม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class InscribedTrapezoidLeg(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(2, 9)
        answer = leg_tex(k)
        wrong = [t for t in dict.fromkeys([leg_tex(k, sign=1), leg_tex(k, half=False), leg_tex(k, extra=4), leg_tex(k, extra=16)]) if t != answer]
        return MathDraw(
            rf"DC={k}\,AD",
            answer,
            prompt="ABCD เป็นรูปสี่เหลี่ยมคางหมูแนบในวงกลมรัศมี 1 หน่วย โดยที่ AB เป็นเส้นผ่านศูนย์กลาง จงหาระยะ AD",
            hint="วาง A = (−1, 0), B = (1, 0), D = (−c, s), C = (c, s) แล้วใช้ AD² = 2 − 2c และ DC = 2c",
            distractors=wrong,
        )
