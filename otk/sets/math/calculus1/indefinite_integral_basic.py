"""ปริพันธ์ไม่จำกัดเขต

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType

PROVENANCE = Provenance("original")


@question_type("math.indefinite_integral_basic",
               display_name={"th": "ปริพันธ์ไม่จำกัดเขตพื้นฐาน"},
               level={"th": "แคลคูลัส 1"}, topic="ปริพันธ์ไม่จำกัดเขต")
class IndefiniteIntegralBasic(MathType):
    def expr(self, rng: Random):
        kind = rng.choice(["recip", "exp", "cos"])
        table = {
            "recip": (r"\frac{1}{x}", r"\ln|x| + C",
                      [r"-\frac{1}{x^{2}} + C", r"\frac{1}{x^{2}} + C",
                       r"\ln x^{2} + C"]),
            "exp": (r"e^{x}", r"e^{x} + C",
                    [r"x e^{x-1} + C", r"\frac{e^{x}}{x} + C", r"e^{x+1} + C"]),
            "cos": (r"\cos x", r"\sin x + C",
                    [r"-\sin x + C", r"\cos x + C", r"-\cos x + C"]),
        }
        fn, ans, wrong = table[kind]
        return MathDraw(rf"\int {fn}\,dx", ans, distractors=wrong)
