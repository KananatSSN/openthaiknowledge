"""Tangents PA, PB; BO meets line PA at Q; QA : AP = p : q gives sin²∠CAQ = p/(2(p + q))."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 4",))


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


def sine_square(p: int, q: int) -> Fraction:
    """QB ⟂ PB, so QB² = (p + q)² − q²; QA² = QC·QB; ∠CAQ = ∠ABC and
    AC/AB = QA/QB give sin²∠CAQ = p/(2(p + q)) (source: 2 : 3 → 1/√5)."""
    return Fraction(p, 2 * (p + q))


@question_type(
    "math.tangent_diameter_sine_olympiad",
    display_name={"th": "ไซน์ของมุมระหว่างเส้นสัมผัสกับคอร์ด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: เส้นสัมผัสวงกลม",
)
class TangentDiameterSine(WordProblem):
    def expr(self, rng: Random):
        p, q = rng.randint(1, 9), rng.randint(1, 9)
        answer = sine_square(p, q)
        wrong = [surd_tex(v) for v in dict.fromkeys([sine_square(q, p), Fraction(p, p + q), Fraction(p * p, (p + q) ** 2), Fraction(p + 2 * q, 2 * (p + q)), Fraction(p, p + 2 * q)]) if v != answer]
        return MathDraw(
            rf"QA:AP={p}:{q}",
            surd_tex(answer),
            prompt="P เป็นจุดภายนอกวงกลมที่มี O เป็นจุดศูนย์กลาง จาก P ลากเส้นสัมผัสวงกลมที่ A และ B ต่อ BO ไปตัดวงกลมที่ C และตัดเส้นที่ต่อจาก PA ที่ Q จงหา sin∠CAQ",
            hint="QB ตั้งฉากกับ PB และ PA = PB ใช้ QA² = QC·QB และมุมระหว่างเส้นสัมผัสกับคอร์ด ∠CAQ = ∠ABC",
            distractors=wrong,
        )
