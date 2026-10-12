"""ปฏิยานุพันธ์

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType

PROVENANCE = Provenance("original")


@question_type("math.antiderivative_power",
               display_name={"th": "ปฏิยานุพันธ์ของพหุนาม"},
               level={"th": "แคลคูลัส 1"}, topic="ปฏิยานุพันธ์")
class AntiderivativePower(MathType):
    def expr(self, rng: Random):
        a, n = rng.randint(2, 6), rng.randint(2, 4)
        return MathDraw(
            rf"\int {a}x^{{{n}}}\,dx",
            rf"\frac{{{a}}}{{{n + 1}}}x^{{{n + 1}}} + C",
            prompt="จงหาปฏิยานุพันธ์ (+C)",
            distractors=[rf"\frac{{{a}}}{{{n}}}x^{{{n}}} + C",
                         rf"{a * n}x^{{{n - 1}}} + C",
                         rf"{a}x^{{{n + 1}}} + C"])


@question_type("math.antiderivative_trig", display_name={"th": "ปฏิยานุพันธ์ของตรีโกณมิติ"},
               level={"th": "แคลคูลัส 1"}, topic="ปฏิยานุพันธ์")
class AntiderivativeTrig(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 9):
        a = rng.randint(2, coef_hi)
        if rng.random() < 0.5:
            return MathDraw(
                rf"\int \sin {a}x \, dx", rf"-\frac{{1}}{{{a}}}\cos {a}x + C",
                prompt="จงหาปริพันธ์",
                distractors=[rf"\frac{{1}}{{{a}}}\cos {a}x + C",
                             rf"-{a}\cos {a}x + C", rf"-\cos {a}x + C"])
        return MathDraw(
            rf"\int \cos {a}x \, dx", rf"\frac{{1}}{{{a}}}\sin {a}x + C",
            prompt="จงหาปริพันธ์",
            distractors=[rf"-\frac{{1}}{{{a}}}\sin {a}x + C",
                         rf"{a}\sin {a}x + C", rf"\sin {a}x + C"])
