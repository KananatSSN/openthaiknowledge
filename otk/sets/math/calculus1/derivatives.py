"""อนุพันธ์

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, poly_tex

PROVENANCE = Provenance("original")


@question_type("math.derivative_definition",
               display_name={"th": "อนุพันธ์จากนิยาม"}, level={"th": "แคลคูลัส 1"},
               topic="อนุพันธ์")
class DerivativeDefinition(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        a = rng.randint(1, 5)
        b = rng.choice([n for n in range(-5, 6) if n])
        return MathDraw(
            rf"f(x) = {poly_tex((a, 'x^{2}'), (b, 'x'))}",
            poly_tex((2 * a, "x"), (b, "")),
            prompt="ใช้นิยามหา f′(x)",
            distractors=[poly_tex((a, "x"), (b, "")), poly_tex((2 * a, "x")),
                         poly_tex((2 * a, "x"), (2 * b, ""))])


@question_type("math.logarithmic_diff",
               display_name={"th": "การหาอนุพันธ์โดยใช้ลอการิทึม"},
               level={"th": "แคลคูลัส 1"}, topic="อนุพันธ์")
class LogarithmicDiff(MathType):
    def expr(self, rng: Random):
        return MathDraw(
            r"\frac{d}{dx}\left[x^{x}\right]", r"x^{x}(\ln x + 1)",
            distractors=[r"x \cdot x^{x-1}", r"x^{x}\ln x", r"x^{x}"])
