"""อนุพันธ์โดยใช้ลอการิทึม

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType
from otk.sets._support.math_calculus import _linear, _nonzero, _signed

PROVENANCE = Provenance("original")


@question_type("math.log_diff_setup", display_name={"th": "ขั้นแรกของการหาอนุพันธ์ด้วย ln"},
               level={"th": "แคลคูลัส 1"}, topic="อนุพันธ์โดยใช้ลอการิทึม")
class LogDiffSetup(MathType):
    """Take ln of both sides first: products become sums and exponents come
    down, which is the only reason the technique exists."""

    def expr(self, rng: Random, power_hi: int = 6):
        m, n = rng.randint(2, power_hi), rng.randint(2, power_hi)
        a, b = rng.randint(1, 9), rng.randint(1, 9)
        shown = rf"y = (x{_signed(a)})^{{{m}}}(x{_signed(b)})^{{{n}}}"
        answer = (rf"{m}\ln(x{_signed(a)}) + {n}\ln(x{_signed(b)})")
        return MathDraw(
            shown, answer, prompt="จงเขียน ln y ในรูปผลบวกของลอการิทึม",
            distractors=[rf"\ln(x{_signed(a)})^{{{m}}} \cdot "
                         rf"\ln(x{_signed(b)})^{{{n}}}",
                         rf"{m + n}\ln(x{_signed(a)})(x{_signed(b)})",
                         rf"{m}\ln(x{_signed(a)}) \cdot {n}\ln(x{_signed(b)})"])


@question_type("math.derivative_ln_linear", display_name={"th": "อนุพันธ์ของ ln"},
               level={"th": "แคลคูลัส 1"}, topic="อนุพันธ์โดยใช้ลอการิทึม")
class DerivativeLnLinear(MathType):
    def expr(self, rng: Random, coef_hi: int = 8):
        a = _nonzero(rng, -coef_hi, coef_hi)
        b = rng.randint(-9, 9)
        inner = _linear(a, b)
        return MathDraw(
            rf"f(x) = \ln({inner})", rf"\frac{{{a}}}{{{inner}}}",
            prompt="จงหา f′(x)",
            distractors=[rf"\frac{{1}}{{{inner}}}", rf"\frac{{{a}}}{{x}}",
                         rf"\frac{{{inner}}}{{{a}}}"])
