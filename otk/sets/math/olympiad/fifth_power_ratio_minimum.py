"""Σ a⁵/(bc²) ≥ a² + b² + c²: with a + b + c = s the minimum is s²/3."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 7",)
)


def ratio_minimum(total: int) -> Fraction:
    """Weighted AM–GM: a⁵/(bc²) + b²/2 + c² ≥ (5/2)a²; summing cyclically gives
    Σa⁵/(bc²) ≥ Σa² ≥ (Σa)²/3, with equality at a = b = c = s/3."""
    return Fraction(total * total, 3)


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


@question_type(
    "math.fifth_power_ratio_minimum_olympiad",
    display_name={"th": "ค่าต่ำสุดของ Σ a⁵/(bc²)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class FifthPowerRatioMinimum(WordProblem):
    def expr(self, rng: Random):
        total = 3 * rng.randint(1, 12) if rng.randrange(2) else rng.randint(2, 30)
        answer = ratio_minimum(total)
        wrong = [frac_tex(v) for v in dict.fromkeys([
            Fraction(total * total, 9), Fraction(total**2), Fraction(total, 3), Fraction(total**5, 243), Fraction(total * total, 3) + 1,
        ]) if v != answer]
        return MathDraw(
            rf"a+b+c={total},\quad S=\frac{{a^5}}{{bc^2}}+\frac{{b^5}}{{ca^2}}+\frac{{c^5}}{{ab^2}}",
            frac_tex(answer),
            prompt="a, b, c เป็นจำนวนจริงบวกที่สอดคล้องเงื่อนไขต่อไปนี้ จงหาค่าต่ำสุดของ S",
            hint="พิสูจน์ S ≥ a² + b² + c² ด้วย AM–GM แบบถ่วงน้ำหนัก แล้วใช้ a² + b² + c² ≥ (a + b + c)²/3",
            distractors=wrong,
        )
