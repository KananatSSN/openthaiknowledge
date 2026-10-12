"""เทคนิคการอินทิเกรตขั้นสูง

คณิตศาสตร์ · แคลคูลัส 2 · อุดมศึกษา
Indicators: —

Sets moved here from: math.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, frac_tex

PROVENANCE = Provenance("original")


@question_type("math.trig_integral",
               display_name={"th": "อินทิกรัลตรีโกณมิติ"},
               level={"th": "แคลคูลัส 2"}, topic="เทคนิคการอินทิเกรตขั้นสูง")
class TrigIntegral(MathType):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            return MathDraw(
                r"\int \sin^{2} x\,dx", r"\frac{x}{2} - \frac{\sin 2x}{4} + C",
                hint=r"\sin^2 x = \tfrac{1 - \cos 2x}{2}",
                distractors=[r"-\cos^{2} x + C", r"\frac{\sin^{3} x}{3} + C",
                             r"\frac{x}{2} - \sin 2x + C"])
        return MathDraw(
            r"\int \cos^{2} x\,dx", r"\frac{x}{2} + \frac{\sin 2x}{4} + C",
            hint=r"\cos^2 x = \tfrac{1 + \cos 2x}{2}",
            distractors=[r"\sin^{2} x + C", r"\frac{\cos^{3} x}{3} + C",
                         r"\frac{x}{2} + \sin 2x + C"])


@question_type("math.trig_substitution",
               display_name={"th": "การแทนค่าด้วยตรีโกณมิติ"},
               level={"th": "แคลคูลัส 2"}, topic="เทคนิคการอินทิเกรตขั้นสูง")
class TrigSubstitution(ConceptBankType):
    ITEMS = [
        Concept("สำหรับ √(a²−x²) ควรแทน x ด้วยอะไร?", "x = a·sinθ",
                ("x = a·tanθ", "x = a·secθ", "x = a·cosθ")),
        Concept("สำหรับ √(a²+x²) ควรแทน x ด้วยอะไร?", "x = a·tanθ",
                ("x = a·sinθ", "x = a·secθ", "x = a·cosθ")),
        Concept("สำหรับ √(x²−a²) ควรแทน x ด้วยอะไร?", "x = a·secθ",
                ("x = a·sinθ", "x = a·tanθ", "x = a·cosθ")),
    ]


@question_type("math.partial_fractions",
               display_name={"th": "เศษส่วนย่อย"}, level={"th": "แคลคูลัส 2"},
               topic="เทคนิคการอินทิเกรตขั้นสูง")
class PartialFractions(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        a, b = rng.sample(range(1, 7), 2)
        return MathDraw(
            rf"\frac{{1}}{{(x - {a})(x - {b})}}", frac_tex(Fraction(1, a - b)),
            prompt=f"แยกเป็น A/(x−{a}) + B/(x−{b}) แล้ว A เท่ากับเท่าใด?",
            distractors=[frac_tex(Fraction(1, b - a)),
                         frac_tex(Fraction(1, a * b)), str(a - b)])


@question_type("math.improper_integral",
               display_name={"th": "ปริพันธ์ไม่ตรงแบบ"}, level={"th": "แคลคูลัส 2"},
               topic="เทคนิคการอินทิเกรตขั้นสูง")
class ImproperIntegral(ChoiceType):
    def compose(self, rng: Random):
        p = rng.choice(["1/2", "1", "2", "3"])
        converges = p in ("2", "3")
        stem = f"∫₁^∞ x^(−p) dx เมื่อ p = {p} ลู่เข้าหรือลู่ออก?"
        if converges:
            return stem, "ลู่เข้า (p > 1)", ["ลู่ออก (p ≤ 1)"]
        return stem, "ลู่ออก (p ≤ 1)", ["ลู่เข้า (p > 1)"]
