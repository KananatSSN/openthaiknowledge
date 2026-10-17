"""s²/r² = s³/((s − a)(s − b)(s − c)) from r² = (s − a)(s − b)(s − c)/s."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันที่สอง ข้อ 6",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def semiperimeter_ratio(a: int, b: int, c: int) -> Fraction:
    """Heron gives Δ² = s(s − a)(s − b)(s − c) and r = Δ/s, so
    s²/r² = s³/((s − a)(s − b)(s − c)). The source bounds 3/4 + Σ r/s_a by
    s²/(12r²) with r/s_a = sin(A/2)."""
    s = Fraction(a + b + c, 2)
    return s ** 3 / ((s - a) * (s - b) * (s - c))


@question_type(
    "math.incircle_vertex_ratio_olympiad",
    display_name={"th": "อัตราส่วนกึ่งเส้นรอบรูปกับรัศมีวงกลมแนบใน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class IncircleVertexRatio(WordProblem):
    def expr(self, rng: Random):
        while True:
            a, b, c = sorted(rng.randint(2, 15) for _ in range(3))
            if a + b > c and not a == b == c:
                break
        answer = semiperimeter_ratio(a, b, c)
        s = Fraction(a + b + c, 2)
        rest = (s - a) * (s - b) * (s - c)
        wrong = [frac_tex(v) for v in dict.fromkeys([s * s / rest, s ** 4 / rest, 4 * answer, s ** 3 / (a * b * c), Fraction(27)]) if v != answer]
        return MathDraw(
            rf"a={a},\quad b={b},\quad c={c}",
            frac_tex(answer),
            prompt="รูปสามเหลี่ยมมีด้านยาว a, b, c กึ่งเส้นรอบรูป s และรัศมีวงกลมแนบใน r จงหา s²/r²",
            hint="ใช้สูตรเฮรอน Δ² = s(s − a)(s − b)(s − c) และ r = Δ/s",
            distractors=wrong,
        )
