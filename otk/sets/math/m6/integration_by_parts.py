"""อินทิเกรตทีละส่วน

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม แคลคูลัส 1 ม.6/3

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType

PROVENANCE = Provenance("original")


_BY_PARTS = [
    (r"\int \, x \sin x \, dx", r"-x\cos x + \sin x + C"),
    (r"\int \, x \cos x \, dx", r"x\sin x + \cos x + C"),
    (r"\int \, x e^{x} \, dx", r"(x - 1)e^{x} + C"),
    (r"\int \, \ln x \, dx", r"x\ln x - x + C"),
    (r"\int \, x \ln x \, dx", r"\frac{x^{2}}{2}\ln x - \frac{x^{2}}{4} + C"),
]


@question_type("math.parts_choose_u", display_name={"th": "เลือก u ในการอินทิเกรตทีละส่วน"},
               level={"th": "ม.6"}, topic="อินทิเกรตทีละส่วน")
class PartsChooseU(ChoiceType):
    """LIATE: pick the u that gets *simpler* when differentiated."""

    ITEMS = [
        ("ในการหา ∫ x ln x dx ควรเลือก u เป็นอะไร", "u = ln x",
         ["u = x", "u = x ln x", "u = dx"]),
        ("ในการหา ∫ x eˣ dx ควรเลือก u เป็นอะไร", "u = x",
         ["u = eˣ", "u = x eˣ", "u = dx"]),
        ("ในการหา ∫ x sin x dx ควรเลือก u เป็นอะไร", "u = x",
         ["u = sin x", "u = x sin x", "u = cos x"]),
        ("ในการหา ∫ arctan x dx ควรเลือก u เป็นอะไร", "u = arctan x",
         ["u = x", "u = 1", "u = dx"]),
    ]

    def compose(self, rng: Random):
        return rng.choice(self.ITEMS)


@question_type("math.integration_by_parts",
               display_name={"th": "อินทิเกรตทีละส่วน"}, level={"th": "ม.6"},
               topic="อินทิเกรตทีละส่วน")
class IntegrationByParts(MathType):
    def expr(self, rng: Random):
        prob, ans = rng.choice(_BY_PARTS)
        return MathDraw(prob, ans, hint=r"\int f g' = fg - \int f' g")


@question_type("math.parts_x_exponential",
               display_name={"th": "อินทิเกรตทีละส่วน: x·eˣ"},
               level={"th": "ม.6"}, topic="อินทิเกรตทีละส่วน")
class PartsXExponential(MathType):
    def expr(self, rng: Random, coef_hi: int = 5):
        a = rng.choice([n for n in range(-coef_hi, coef_hi + 1) if n])
        # ∫ x·e^(ax) dx = e^(ax)(x/a − 1/a²) + C, for either sign of a.
        e = "e^{x}" if a == 1 else "e^{-x}" if a == -1 else f"e^{{{a}x}}"
        x_a = "x" if a == 1 else "-x" if a == -1 else (
            rf"\frac{{x}}{{{a}}}" if a > 0 else rf"-\frac{{x}}{{{-a}}}")
        sq = "1" if abs(a) == 1 else rf"\frac{{1}}{{{a * a}}}"
        x_1a = "x - 1" if a == 1 else "x + 1" if a == -1 else (
            rf"x - \frac{{1}}{{{a}}}" if a > 0 else rf"x + \frac{{1}}{{{-a}}}")
        return MathDraw(
            rf"\int x {e} \, dx", rf"{e}\left({x_a} - {sq}\right) + C",
            prompt="จงหาปริพันธ์",
            # The sign of the second term, integrating x alone, and 1/a once
            # where the second integration gives 1/a².
            distractors=[rf"{e}\left({x_a} + {sq}\right) + C",
                         rf"\frac{{x^2}}{{2}} {e} + C",
                         rf"{e}\left({x_1a}\right) + C"])
