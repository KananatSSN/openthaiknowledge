"""DE a diameter of the incircle, F = AE ∩ BC: [DEF]/[ABC] = (c − b)/s."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 6",))


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def antipode_area_ratio(a: int, b: int, c: int) -> Fraction:
    """The homothety at A taking the incircle to the excircle sends E to the
    extouch point, so F is it: BF = s − c, BD = s − b, DF = c − b. Triangle
    DEF is right at D with legs 2r and c − b, and [ABC] = rs."""
    return Fraction(2 * (c - b), a + b + c)


TRIANGLES = tuple(
    (a, b, c) for a in range(3, 20) for b in range(3, 20) for c in range(3, 20)
    if c > b and a < b + c and b < a + c and c < a + b
)


@question_type(
    "math.incircle_antipode_area_olympiad",
    display_name={"th": "อัตราส่วนพื้นที่จากจุดตรงข้ามจุดสัมผัสวงกลมแนบใน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class IncircleAntipodeArea(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(TRIANGLES)
        answer = antipode_area_ratio(a, b, c)
        s2 = a + b + c
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(c - b, s2), Fraction(c - b, a), Fraction(4 * (c - b), s2), Fraction(2 * (c - b), a + b), Fraction(2 * (c - b + 1), s2)]) if v != answer and v > 0]
        return MathDraw(
            rf"BC={a},\ CA={b},\ AB={c}",
            frac_tex(answer),
            prompt="วงกลมแนบในของรูปสามเหลี่ยม ABC สัมผัส BC ที่ D และ DE เป็นเส้นผ่านศูนย์กลาง เส้นตรง AE ตัด BC ที่ F จงหาพื้นที่ △DEF ต่อพื้นที่ △ABC",
            hint="การขยายที่ A ส่งวงกลมแนบในไปยังวงกลมแนบนอก จึง F เป็นจุดสัมผัสของวงกลมแนบนอกบน BC",
            distractors=wrong,
        )
