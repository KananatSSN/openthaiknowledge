"""b(a² + 2) + c(a + 2) = S: AM–GM on b, c, then a/((a² + 2)(a + 2)) peaks at a = 1."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 18",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def best_product(total: int) -> Fraction:
    """For fixed a, AM–GM gives bc ≤ S²/(4(a² + 2)(a + 2)). The derivative of
    a/((a² + 2)(a + 2)) vanishes at a³ + a² − 2 = 0, a = 1, where b = c = S/6;
    so abc ≤ S²/36 (source: S = 12 → a = 1, b = c = 2, abc = 4)."""
    return Fraction(total * total, 36)


@question_type(
    "math.constrained_product_max_olympiad",
    display_name={"th": "ค่าสูงสุดของ abc ภายใต้เงื่อนไขไม่เชิงเส้น"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class ConstrainedProductMax(WordProblem):
    def expr(self, rng: Random):
        total = rng.randint(6, 60)
        answer = best_product(total)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(total**3, 216), Fraction(total * total, 24), Fraction(total * total, 48), Fraction(total, 6), Fraction(total * total, 27)]) if v != answer]
        return MathDraw(
            rf"b(a^2+2)+c(a+2)={total}",
            frac_tex(answer),
            prompt="a, b, c เป็นจำนวนจริงบวกที่สอดคล้องเงื่อนไขต่อไปนี้ จงหาค่าสูงสุดของ abc",
            hint="ตรึง a แล้วใช้ AM–GM กับสองพจน์ b(a² + 2) และ c(a + 2) จากนั้นหาค่าสูงสุดของ a/((a² + 2)(a + 2))",
            distractors=wrong,
        )
