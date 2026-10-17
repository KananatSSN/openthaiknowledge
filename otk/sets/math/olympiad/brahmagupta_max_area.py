"""The largest area for given sides is the cyclic quadrilateral's, √((s − a)(s − b)(s − c)(s − d)), and is at most Σ side²/4."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันที่สอง ข้อ 4",))


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


def max_area_square(a: int, b: int, c: int, d: int) -> Fraction:
    """Bretschneider: area² = Π(s − x) − abcd·cos²((A + C)/2), largest when the
    quadrilateral is cyclic. The source bound: area ≤ (ab + cd)/2 ≤ Σ x²/4."""
    s = Fraction(a + b + c + d, 2)
    return (s - a) * (s - b) * (s - c) * (s - d)


@question_type(
    "math.brahmagupta_max_area_olympiad",
    display_name={"th": "พื้นที่มากสุดของรูปสี่เหลี่ยมนูนเมื่อกำหนดความยาวด้าน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: พื้นที่รูปสี่เหลี่ยม",
)
class BrahmaguptaMaxArea(WordProblem):
    def expr(self, rng: Random):
        while True:
            sides = [rng.randint(2, 12) for _ in range(4)]
            if 2 * max(sides) < sum(sides) and len(set(sides)) > 1:
                break
        a, b, c, d = sides
        answer = max_area_square(a, b, c, d)
        bound = Fraction(a * a + b * b + c * c + d * d, 4)
        wrong = [surd_tex(v) for v in dict.fromkeys([bound**2, Fraction((a * b + c * d) ** 2, 4), Fraction((a + c) * (b + d), 2) ** 2, answer * 4, Fraction(a * b * c * d)]) if v != answer]
        return MathDraw(
            rf"AB={a},\ BC={b},\ CD={c},\ DA={d}",
            surd_tex(answer),
            prompt="ABCD เป็นรูปสี่เหลี่ยมนูนที่มีความยาวด้านดังนี้ จงหาพื้นที่ที่มากที่สุดที่เป็นไปได้ (พื้นที่นี้ไม่เกิน (AB² + BC² + CD² + DA²)/4 เสมอ)",
            hint="พื้นที่มากสุดเมื่อรูปสี่เหลี่ยมแนบในวงกลม ใช้สูตรของพรหมคุปต์ √((s − a)(s − b)(s − c)(s − d))",
            distractors=wrong,
        )
