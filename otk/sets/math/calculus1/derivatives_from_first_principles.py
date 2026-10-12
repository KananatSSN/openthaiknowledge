"""อนุพันธ์จากนิยาม

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, poly_tex
from otk.sets._support.math_calculus import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.difference_quotient", display_name={"th": "ผลหารเชิงผลต่าง"},
               level={"th": "แคลคูลัส 1"}, topic="อนุพันธ์จากนิยาม")
class DifferenceQuotient(MathType):
    """(f(x+h) − f(x))/h for f = ax² + bx + c simplifies to 2ax + ah + b — the
    expression whose limit as h → 0 *is* the derivative."""
    break_convergence = True  # one-part slips cluster round the answer

    def expr(self, rng: Random, coef_hi: int = 6):
        a = _nonzero(rng, -coef_hi, coef_hi)
        b = rng.randint(-9, 9)
        c = rng.randint(-9, 9)
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        answer = poly_tex((2 * a, "x"), (a, "h"), (b, ""))
        return MathDraw(
            rf"f(x) = {shown}", answer,
            prompt="จงจัดรูปผลหารเชิงผลต่าง (f(x + h) − f(x)) / h",
            distractors=[poly_tex((2 * a, "x"), (b, "")),
                         poly_tex((a, "x"), (a, "h"), (b, "")),
                         poly_tex((2 * a, "x"), (a, "h"), (c, "")),
                         # Two slips at once.
                         *[d for d in (poly_tex((a, "x"), (b, "")), poly_tex((a, "x"), (a, "h"), (c, "")))
                           if d != answer]])


@question_type("math.derivative_from_definition_value",
               display_name={"th": "อนุพันธ์จากนิยาม ณ จุดหนึ่ง"},
               level={"th": "แคลคูลัส 1"}, topic="อนุพันธ์จากนิยาม")
class DerivativeFromDefinitionValue(MathType):
    def expr(self, rng: Random, coef_hi: int = 6, point_hi: int = 5):
        a = _nonzero(rng, -coef_hi, coef_hi)
        b = rng.randint(-9, 9)
        c = rng.randint(-9, 9)
        x0 = rng.randint(-point_hi, point_hi)
        value = 2 * a * x0 + b
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        return MathDraw(
            rf"f(x) = {shown}", str(value),
            prompt=f"จงใช้นิยามของอนุพันธ์หาค่า f′({x0})",
            distractors=[str(a * x0 * x0 + b * x0 + c), str(2 * a * x0),
                         str(a * x0 + b)])
