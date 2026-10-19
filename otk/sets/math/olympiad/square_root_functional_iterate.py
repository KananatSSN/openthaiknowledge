"""(f(xy))² = f(x²)f(y²): y = 1 gives f(x²) = f(x)²/f(1)."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันที่สอง ข้อ 6",))


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def iterated_value(f1: int, fb: int, steps: int) -> Fraction:
    """f(b^{2^j}) = f(b^{2^{j−1}})²/f(1), so f(b^{2^j}) = fb^{2^j}/f1^{2^j − 1}."""
    return Fraction(fb ** (2**steps), f1 ** (2**steps - 1))


@question_type(
    "math.square_root_functional_iterate_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชัน (f(xy))² = f(x²)f(y²)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class SquareRootFunctionalIterate(WordProblem):
    def expr(self, rng: Random):
        f1, fb = rng.randint(1, 5), rng.randint(1, 6)
        base = rng.randint(2, 5)
        steps = rng.randint(1, 2)
        answer = iterated_value(f1, fb, steps)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(fb ** (2**steps)), Fraction(fb ** (2**steps), f1 ** (2**steps)), Fraction(fb * 2**steps), iterated_value(f1, fb, steps + 1), answer * f1]) if v != answer]
        return MathDraw(
            rf"\big(f(xy)\big)^2=f(x^2)f(y^2),\quad f(1)={f1},\ f({base})={fb}",
            frac_tex(answer),
            prompt=f"f : ℝ⁺ → ℝ⁺ สอดคล้องสมการทุก x, y > 0 จงหา f({base ** (2**steps)})",
            hint="ให้ y = 1 จะได้ f(x)² = f(x²)f(1)",
            distractors=wrong,
        )
