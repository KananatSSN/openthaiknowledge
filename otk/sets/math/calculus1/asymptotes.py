"""เส้นกำกับ

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, poly_tex
from otk.sets._support.math_calculus import _nonzero, _signed

PROVENANCE = Provenance("original")


@question_type("math.vertical_asymptote",
               display_name={"th": "เส้นกำกับแนวดิ่ง"}, level={"th": "แคลคูลัส 1"},
               topic="เส้นกำกับ")
class VerticalAsymptote(MathType):
    def expr(self, rng: Random):
        a = rng.randint(1, 6)
        return MathDraw(
            rf"f(x) = \frac{{1}}{{x - {a}}}", rf"x = {a}",
            prompt="เส้นกำกับแนวดิ่งของฟังก์ชันนี้คือเส้นใด",
            distractors=[rf"y = {a}", "x = 0", "y = 0"])


@question_type("math.horizontal_asymptote", display_name={"th": "เส้นกำกับแนวนอน"},
               level={"th": "แคลคูลัส 1"}, topic="เส้นกำกับ")
class HorizontalAsymptote(ChoiceType):
    """Equal degrees → the ratio of leading coefficients; numerator smaller →
    y = 0; numerator bigger → none at all.

    A :class:`ChoiceType` rather than a ``MathType`` because one of the answers
    is "there isn't one", which is Thai prose — and Thai may never appear inside
    a MathBlock. The options are therefore plain text, notation and all.
    """

    NONE = "ไม่มีเส้นกำกับแนวนอน"

    @staticmethod
    def _ratio(a: int, c: int) -> str:
        f = Fraction(a, c)
        return str(f.numerator) if f.denominator == 1 else \
            f"{f.numerator}/{f.denominator}"

    def compose(self, rng: Random):
        a, c = rng.randint(1, 9), rng.randint(1, 9)
        b, d = rng.randint(-9, 9), rng.randint(-9, 9)
        case = rng.choice(["equal", "lower", "higher"])
        if case == "equal":
            num = poly_tex((a, "x^2"), (b, "x"), (0, ""))
            den = poly_tex((c, "x^2"), (d, ""))
            answer = f"y = {self._ratio(a, c)}"
            wrong = [f"y = {self._ratio(c, a)}", "y = 0", self.NONE]
        elif case == "lower":
            num = poly_tex((a, "x"), (b, ""))
            den = poly_tex((c, "x^2"), (d, ""))
            answer = "y = 0"
            wrong = [f"y = {self._ratio(a, c)}", self.NONE, "x = 0"]
        else:
            num = poly_tex((a, "x^2"), (b, ""))
            den = poly_tex((c, "x"), (d, ""))
            answer = self.NONE
            wrong = ["y = 0", f"y = {self._ratio(a, c)}", "x = 0"]
        shown = (num + " / " + den).replace("^2", "²")
        return f"เส้นกำกับแนวนอนของ f(x) = ({shown}) คือข้อใด", answer, wrong


@question_type("math.removable_discontinuity",
               display_name={"th": "รูโหว่หรือเส้นกำกับแนวดิ่ง"},
               level={"th": "แคลคูลัส 1"}, topic="เส้นกำกับ")
class RemovableDiscontinuity(ChoiceType):
    """A zero of the denominator that the numerator cancels is a hole, not an
    asymptote — the distinction the ε–δ definition is quietly about."""

    def compose(self, rng: Random):
        r = _nonzero(rng, -6, 6)
        s = rng.choice([n for n in range(-6, 7) if n != r])
        num = f"(x{_signed(-r)})(x{_signed(-s)})"
        if rng.random() < 0.5:
            stem = (f"ฟังก์ชัน f(x) = {num} / (x{_signed(-r)}) "
                    f"มีลักษณะอย่างไรที่ x = {r}")
            return stem, f"มีรูโหว่ (ช่องว่าง) ที่ x = {r}", [
                f"มีเส้นกำกับแนวดิ่งที่ x = {r}",
                f"ต่อเนื่องที่ x = {r}", "หาค่าไม่ได้ทุกจุด"]
        stem = (f"ฟังก์ชัน f(x) = (x{_signed(-s)}) / (x{_signed(-r)}) "
                f"มีลักษณะอย่างไรที่ x = {r}")
        return stem, f"มีเส้นกำกับแนวดิ่งที่ x = {r}", [
            f"มีรูโหว่ (ช่องว่าง) ที่ x = {r}",
            f"ต่อเนื่องที่ x = {r}", "หาค่าไม่ได้ทุกจุด"]
