"""R/r = 2abc/((−a + b + c)(a − b + c)(a + b − c)); scan integer third sides."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 21",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def radius_ratio(a: int, b: int, c: int) -> Fraction:
    """R = abc/(4Δ), r = Δ/s and Δ² = s(s − a)(s − b)(s − c)."""
    return Fraction(2 * a * b * c, (-a + b + c) * (a - b + c) * (a + b - c))


def _cases():
    out = []
    for a in range(2, 15):
        for b in range(a + 1, 16):
            for c in range(b - a + 1, a + b):
                ratio = radius_ratio(a, b, c)
                matches = [z for z in range(b - a + 1, a + b) if radius_ratio(a, b, z) == ratio]
                if matches == [c] and ratio != 2:
                    out.append((a, b, c, ratio))
    return tuple(out)


CASES = _cases()


@question_type(
    "math.circumradius_inradius_side_olympiad",
    display_name={"th": "ด้านที่สามจากอัตราส่วนรัศมีวงกลมล้อมกับวงกลมแนบใน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class CircumradiusInradiusSide(WordProblem):
    def expr(self, rng: Random):
        a, b, c, ratio = rng.choice(CASES)
        answer = c
        others = [z for z in range(b - a + 1, a + b) if z != c]
        wrong = [v for v in dict.fromkeys(others[:2] + others[-2:] + [a + b - 1]) if v != answer][:4]
        return MathDraw(
            rf"\frac{{R}}{{r}}={frac_tex(ratio)},\quad a={a},\ b={b}",
            str(answer),
            prompt="รัศมีของวงกลมล้อมรอบสามเหลี่ยม R และรัศมีของวงกลมแนบใน r มีอัตราส่วนตามที่กำหนด สองด้านยาวตามที่กำหนด และอีกด้านยาวเป็นจำนวนเต็ม จงหาความยาวด้านที่เหลือ",
            hint="R/r = abc/(4(s − a)(s − b)(s − c)) จากสูตร R = abc/(4Δ), r = Δ/s และสูตรเฮรอน",
            distractors=[str(v) for v in wrong],
        )
