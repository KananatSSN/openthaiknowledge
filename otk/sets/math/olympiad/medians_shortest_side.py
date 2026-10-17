"""From the medians, a² = (4/9)(2m_b² + 2m_c² − m_a²); the longest median gives the shortest side."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 3",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def surd_tex(square: Fraction) -> str:
    """TeX for √square in the form (k/d)√m with m squarefree."""
    inside = square.numerator * square.denominator
    outside, f = 1, 2
    while f * f <= inside:
        while inside % (f * f) == 0:
            inside //= f * f
            outside *= f
        f += 1
    coef = Fraction(outside, square.denominator)
    if inside == 1:
        return frac_tex(coef)
    root = rf"\sqrt{{{inside}}}"
    top = ("" if coef.numerator == 1 else str(coef.numerator)) + root
    return top if coef.denominator == 1 else rf"\frac{{{top}}}{{{coef.denominator}}}"


def side_square(m_own: int, m_other1: int, m_other2: int) -> Fraction:
    """Apollonius: m_a² = (2b² + 2c² − a²)/4, inverted:
    a² = (4/9)(2m_b² + 2m_c² − m_a²) (source: 3, 4, 5 → shortest side 10/3)."""
    return Fraction(4, 9) * (2 * m_other1**2 + 2 * m_other2**2 - m_own**2)


@question_type(
    "math.medians_shortest_side_olympiad",
    display_name={"th": "ความยาวด้านที่สั้นที่สุดจากความยาวเส้นมัธยฐาน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สามเหลี่ยมและเส้นมัธยฐาน",
)
class MediansShortestSide(WordProblem):
    def expr(self, rng: Random):
        while True:
            m1, m2, m3 = sorted(rng.sample(range(2, 16), 3))
            if m1 + m2 > m3:
                break
        answer = side_square(m3, m1, m2)
        wrong = [surd_tex(v) for v in dict.fromkeys([side_square(m1, m2, m3), side_square(m2, m1, m3), Fraction(4, 9) * m1 * m1, Fraction(2 * m1**2 + 2 * m2**2 - m3**2, 4)]) if v != answer]
        return MathDraw(
            rf"m_a={m1},\quad m_b={m2},\quad m_c={m3}",
            surd_tex(answer),
            prompt="รูปสามเหลี่ยมรูปหนึ่งมีเส้นมัธยฐานทั้งสามยาวดังนี้ จงหาความยาวของด้านที่สั้นที่สุดของรูปสามเหลี่ยมนี้",
            hint="กลับสูตรของอพอลโลเนียส a² = (4/9)(2m_b² + 2m_c² − m_a²) ด้านที่สั้นที่สุดอยู่ตรงข้ามกับเส้นมัธยฐานที่ยาวที่สุด",
            distractors=wrong,
        )
