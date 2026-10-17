"""P(x + 1) − P(x) = ax + b with P(0) = c forces P = (a/2)x² + (b − a/2)x + c."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 5",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def difference_value(a: int, b: int, c: int, n: int) -> Fraction:
    """Telescoping: P(n) = c + Σ_{k<n}(ak + b) = c + a·n(n − 1)/2 + bn. In the
    source, distinct roots αᵢ with P(αᵢ + 1) = 1 make P(x + 1) − 1 − P(x)
    vanish at n points with degree < n, so P(x + 1) − P(x) = 1 and P is linear."""
    return c + Fraction(a * n * (n - 1), 2) + b * n


@question_type(
    "math.polynomial_difference_equation_olympiad",
    display_name={"th": "พหุนามจากผลต่าง P(x + 1) − P(x)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนาม",
)
class PolynomialDifferenceEquation(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.randint(0, 6), rng.randint(-5, 6), rng.randint(-9, 9)
        n = rng.randint(3, 20)
        answer = difference_value(a, b, c, n)
        wrong = [frac_tex(v) for v in dict.fromkeys([answer + a * n, answer - b, Fraction(c + a * n * n, 2) + b * n, answer + c, Fraction(a * n * n + b * n + c)]) if v != answer]
        a_tex = "" if a == 1 else str(a)
        rhs = (f"{a_tex}x" if a else "") + (f"+{b}" if b > 0 and a else (str(b) if b else ""))
        return MathDraw(
            rf"P(x+1)-P(x)={rhs or '0'},\quad P(0)={c}",
            frac_tex(answer),
            prompt=f"P เป็นพหุนามที่สอดคล้องเงื่อนไขต่อไปนี้ จงหา P({n})",
            hint="บวกแบบยุบตัว P(n) − P(0) = Σ (P(k + 1) − P(k)) สำหรับ k = 0 ถึง n − 1",
            distractors=wrong,
        )
