"""ลิมิต

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType

PROVENANCE = Provenance("original")


@question_type("math.epsilon_delta",
               display_name={"th": "บทนิยามลิมิต ε–δ (เชิงเส้น)"},
               level={"th": "แคลคูลัส 1"}, topic="ลิมิต")
class EpsilonDelta(MathType):
    def expr(self, rng: Random):
        m = rng.randint(2, 5)
        return MathDraw(
            rf"f(x) = {m}x", rf"\frac{{\varepsilon}}{{{m}}}",
            prompt=f"สำหรับ f(x) = {m}x ค่า δ ที่มากที่สุดที่ทำให้ "
                   f"|f(x) − L| < ε คือข้อใด?",
            distractors=[rf"{m}\varepsilon", r"\varepsilon",
                         rf"\frac{{{m}}}{{\varepsilon}}"])


@question_type("math.squeeze_theorem",
               display_name={"th": "ทฤษฎีบทบีบ"}, level={"th": "แคลคูลัส 1"},
               topic="ลิมิต")
class SqueezeTheorem(ChoiceType):
    def compose(self, rng: Random):
        f = rng.choice([r"x²·sin(1/x)", r"x²·cos(1/x)", r"x·sin(1/x)"])
        return (f"lim(x→0) {f} = ? (ใช้ทฤษฎีบทบีบ)", "0",
                ["1", "∞", "หาค่าไม่ได้"])
