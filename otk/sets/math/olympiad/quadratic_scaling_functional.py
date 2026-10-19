"""f(3x + y) + f(3x − y) = f(x + y) + f(x − y) + 16f(x): f(4x) = 16f(x), f = cx² for polynomials."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 6",)
)


def scaled_value(given: int, steps: int) -> int:
    """x = y = 0 gives f(0) = 0; y = x gives f(4x) + f(2x) = f(2x) + f(0) + 16f(x),
    so f(4x) = 16f(x) and f(4ᵏx) = 16ᵏf(x)."""
    return given * 16**steps


def polynomial_value(a: int, value: int, b: int) -> Fraction:
    """Polynomial solutions are f = cx² (and every cx² works)."""
    return Fraction(value * b * b, a * a)


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


@question_type(
    "math.quadratic_scaling_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชัน f(3x + y) + f(3x − y) = f(x + y) + f(x − y) + 16f(x)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class QuadraticScalingFunctional(WordProblem):
    def expr(self, rng: Random):
        equation = r"f(3x+y)+f(3x-y)=f(x+y)+f(x-y)+16f(x)"
        if rng.randrange(2):
            x0 = rng.randint(1, 5)
            given = rng.choice([v for v in range(-9, 10) if v])
            steps = rng.randint(1, 2)
            answer = scaled_value(given, steps)
            wrong = [v for v in dict.fromkeys([given * 4**steps, given * 16**steps * 4, given * 8**steps, given * (16 * steps), answer + 16]) if v != answer]
            return MathDraw(
                rf"{equation},\quad f({x0})={given}",
                str(answer),
                prompt=f"f : ℝ → ℝ สอดคล้องสมการต่อไปนี้ทุก x, y ∈ ℝ จงหา f({x0 * 4**steps})",
                hint="ให้ x = y = 0 ได้ f(0) และให้ y = x ได้ความสัมพันธ์ระหว่าง f(4x) กับ f(x)",
                distractors=[str(v) for v in wrong],
                variant="scaling",
            )
        a = rng.randint(1, 4)
        b = rng.choice([v for v in range(2, 10) if v != a])
        value = a * a * rng.randint(1, 5)
        answer = polynomial_value(a, value, b)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(value * b, a), Fraction(value * b**4, a**4), Fraction(value * b**3, a**3), answer + 1, -answer]) if v != answer]
        return MathDraw(
            rf"{equation},\quad f({a})={value}",
            frac_tex(answer),
            prompt=f"f เป็นพหุนามที่สอดคล้องสมการต่อไปนี้ทุก x, y ∈ ℝ จงหา f({b})",
            hint="เทียบสัมประสิทธิ์ของพหุนาม จะพบว่ามีเพียง f(x) = cx² ที่ใช้ได้",
            distractors=wrong,
            variant="polynomial",
        )
