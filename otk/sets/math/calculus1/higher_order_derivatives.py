"""อนุพันธ์อันดับสูง

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, poly_tex
from otk.sets._support.math_calculus import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.higher_order_derivative",
               display_name={"th": "อนุพันธ์อันดับสอง"}, level={"th": "แคลคูลัส 1"},
               topic="อนุพันธ์อันดับสูง")
class HigherOrderDerivative(MathType):
    def expr(self, rng: Random):
        a = rng.randint(1, 5)
        return MathDraw(rf"f(x) = {a}x^{{3}}", rf"{6 * a}x",
                        prompt="จงหา f″(x)",
                        distractors=[rf"{3 * a}x^{{2}}", str(6 * a),
                                     rf"{6 * a}x^{{2}}"])


@question_type("math.third_derivative", display_name={"th": "อนุพันธ์อันดับสาม"},
               level={"th": "แคลคูลัส 1"}, topic="อนุพันธ์อันดับสูง")
class ThirdDerivative(MathType):
    def expr(self, rng: Random, coef_hi: int = 5):
        a, b = (_nonzero(rng, -coef_hi, coef_hi) for _ in range(2))
        c, d = rng.randint(-9, 9), rng.randint(-9, 9)
        # f = ax⁴ + bx³ + cx² + d  →  f‴ = 24ax + 6b
        shown = poly_tex((a, "x^4"), (b, "x^3"), (c, "x^2"), (d, ""))
        return MathDraw(
            rf"f(x) = {shown}", poly_tex((24 * a, "x"), (6 * b, "")),
            prompt="จงหา f‴(x)",
            distractors=[poly_tex((12 * a, "x^2"), (6 * b, "x"), (2 * c, "")),
                         poly_tex((4 * a, "x"), (3 * b, "")),
                         poly_tex((24 * a, "x"), (6 * b, ""), (2 * c, ""))])


@question_type("math.nth_derivative_pattern",
               display_name={"th": "อนุพันธ์อันดับที่ n ของฟังก์ชันวน"},
               level={"th": "แคลคูลัส 1"}, topic="อนุพันธ์อันดับสูง")
class NthDerivativePattern(MathType):
    """sin cycles with period 4 — the nth derivative is a lookup, not 40 steps."""

    CYCLE_SIN = [r"\sin x", r"\cos x", r"-\sin x", r"-\cos x"]
    CYCLE_COS = [r"\cos x", r"-\sin x", r"-\cos x", r"\sin x"]

    def expr(self, rng: Random, n_lo: int = 5, n_hi: int = 40):
        n = rng.randint(n_lo, n_hi)
        cycle = rng.choice([self.CYCLE_SIN, self.CYCLE_COS])
        base = cycle[0]
        answer = cycle[n % 4]
        return MathDraw(
            rf"f(x) = {base}", answer, prompt=f"จงหาอนุพันธ์อันดับที่ {n} ของ f",
            distractors=[c for c in cycle if c != answer])
