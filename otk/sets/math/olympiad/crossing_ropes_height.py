"""Ropes from each pole top to the other's foot cross at height ab/(a + b), whatever the distance."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 20",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def crossing_height(a: int, b: int) -> Fraction:
    """Similar triangles: h/a + h/b = 1 (the two horizontal pieces add up to
    the distance), so h = ab/(a + b) (source: general a, b)."""
    return Fraction(a * b, a + b)


@question_type(
    "math.crossing_ropes_height_olympiad",
    display_name={"th": "ความสูงของจุดที่เชือกสองเส้นตัดกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อัตราส่วนและสัดส่วน",
)
class CrossingRopesHeight(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(2, 30), rng.randint(2, 30)
        answer = crossing_height(a, b)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(a + b, 2), Fraction(2 * a * b, a + b), Fraction(a + b, 4), Fraction(min(a, b), 2), Fraction(a * b, abs(a - b)) if a != b else Fraction(a, 4)]) if v != answer]
        return MathDraw(
            rf"a={a},\quad b={b}",
            frac_tex(answer),
            prompt="เสาสองต้นสูง a และ b หน่วยปักตั้งฉากกับพื้นราบ ขึงเชือกจากยอดเสาแต่ละต้นไปยังโคนเสาอีกต้นหนึ่ง จุดที่เชือกทั้งสองตัดกันอยู่สูงจากพื้นเท่าไร",
            hint="ใช้สามเหลี่ยมคล้าย: ถ้าจุดตัดสูง h แล้ว h/a + h/b = 1",
            distractors=wrong,
        )
