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

from fractions import Fraction  # noqa: E402

from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m6 import M6 as LEVEL  # noqa: E402


def _nz6(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk6(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk6(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk6(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt6(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk6(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk6(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))


def _num6(v) -> str:
    """A terminating decimal without trailing zeros: Fraction(25, 2) -> 12.5."""
    v = Fraction(v)
    sign = "-" if v < 0 else ""
    v = abs(v)
    whole, rem = divmod(v.numerator, v.denominator)
    if not rem:
        return f"{sign}{whole}"
    digits = ""
    for _ in range(6):
        rem *= 10
        d, rem = divmod(rem, v.denominator)
        digits += str(d)
        if not rem:
            break
    return f"{sign}{whole}.{digits.rstrip('0')}"


def _dk6(*values, answer) -> list[str]:
    """Distinct decimal distractors, the answer left out."""
    return _tk6(*(_num6(v) for v in values), answer=_num6(answer))

# ── More integration by parts (2026-11): definite trig integrals, x eˣ from 0 to a, k ln x, xⁿ ln x, a x² eˣ,
# which part to call u, and the formula ──


@question_type("math.parts_definite_trig_m6", display_name={"th": "อินทิกรัลจำกัดเขตทีละส่วนของ x sin x และ x cos x"}, level=LEVEL,
               topic="อินทิเกรตทีละส่วน")
class PartsDefiniteTrigM6(MathType):
    _CASES = ((r"\int_{0}^{\pi} x \sin x \, dx", r"\pi", (r"-\pi", "0", "2")),
              (r"\int_{0}^{\frac{\pi}{2}} x \cos x \, dx", r"\frac{\pi}{2} - 1", (r"\frac{\pi}{2}", "1", r"\frac{\pi}{2} + 1")),
              (r"\int_{0}^{\frac{\pi}{2}} x \sin x \, dx", "1", (r"\frac{\pi}{2}", "0", r"\frac{\pi}{2} - 1")),
              (r"\int_{0}^{\pi} x \cos x \, dx", "-2", ("2", "0", r"\pi")))

    def expr(self, rng: Random):
        problem, right, wrongs = rng.choice(self._CASES)
        return MathDraw(problem, right, prompt="จงหาค่า", distractors=list(wrongs))


@question_type("math.parts_x_exp_definite_m6", display_name={"th": "อินทิกรัลจำกัดเขตของ x eˣ"}, level=LEVEL, topic="อินทิเกรตทีละส่วน")
class PartsXExpDefiniteM6(MathType):
    def expr(self, rng: Random):
        a = rng.randint(2, 5)
        lead = "" if a == 2 else str(a - 1)
        right = rf"{lead}e^{{{a}}} + 1"
        wrongs = [rf"{a}e^{{{a}}} - 1", rf"{lead}e^{{{a}}} - 1", rf"{a + 1}e^{{{a}}} + 1", rf"{lead}e^{{{a}}}"]
        return MathDraw(rf"\int_{{0}}^{{{a}}} x e^{{x}} \, dx", right, prompt="จงหาค่า", distractors=_tk6(*wrongs, answer=right))


@question_type("math.parts_ln_m6", display_name={"th": "ปริพันธ์ของ k ln x"}, level=LEVEL, topic="อินทิเกรตทีละส่วน")
class PartsLnM6(MathType):
    def expr(self, rng: Random):
        k = rng.randint(1, 6)
        lead = "" if k == 1 else str(k)
        right = rf"{lead}x\ln x - {lead}x + C"
        wrongs = [rf"\frac{{{k}}}{{x}} + C", rf"{lead}x\ln x + {lead}x + C", rf"{lead}\ln x - {lead}x + C", rf"{lead}x\ln x + C"]
        return MathDraw(rf"\int {lead}\ln x \, dx", right, prompt="จงหาปริพันธ์", distractors=_tk6(*wrongs, answer=right))


@question_type("math.parts_power_ln_m6", display_name={"th": "ปริพันธ์ของ xⁿ ln x"}, level=LEVEL, topic="อินทิเกรตทีละส่วน")
class PartsPowerLnM6(MathType):
    def expr(self, rng: Random):
        n = rng.randint(1, 3)
        m = n + 1
        xn = "x" if n == 1 else f"x^{{{n}}}"
        right = rf"\frac{{x^{{{m}}}\ln x}}{{{m}}} - \frac{{x^{{{m}}}}}{{{m * m}}} + C"
        wrongs = [rf"\frac{{x^{{{m}}}\ln x}}{{{m}}} + \frac{{x^{{{m}}}}}{{{m * m}}} + C", rf"\frac{{x^{{{m}}}\ln x}}{{{m}}} - \frac{{x^{{{m}}}}}{{{m}}} + C",
                  rf"x^{{{m}}}\ln x - x^{{{m}}} + C"]
        return MathDraw(rf"\int {xn}\ln x \, dx", right, prompt="จงหาปริพันธ์", distractors=_tk6(*wrongs, answer=right))


@question_type("math.parts_x_squared_exp_m6", display_name={"th": "ปริพันธ์ของ x² eˣ"}, level=LEVEL, topic="อินทิเกรตทีละส่วน")
class PartsXSquaredExpM6(MathType):
    def expr(self, rng: Random):
        k = rng.randint(1, 5)
        lead = "" if k == 1 else str(k)
        right = rf"{lead}e^{{x}}(x^{{2}} - 2x + 2) + C"
        wrongs = [rf"{lead}e^{{x}}(x^{{2}} + 2x + 2) + C", rf"{lead}e^{{x}}(x^{{2}} - 2x) + C", rf"{lead}x^{{2}}e^{{x}} + C",
                  rf"{lead}e^{{x}}(x^{{2}} - 2) + C"]
        return MathDraw(rf"\int {lead}x^{{2}} e^{{x}} \, dx", right, prompt="จงหาปริพันธ์", distractors=_tk6(*wrongs, answer=right))


@question_type("math.parts_pick_u_m6", display_name={"th": "เลือก u สำหรับการอินทิเกรตทีละส่วน"}, level=LEVEL, topic="อินทิเกรตทีละส่วน")
class PartsPickUM6(ConceptBankType):
    ITEMS = [
        Concept("ในการหา ∫ x ln x dx ควรเลือก u เป็นอะไร", "ln x", ("x", "x ln x", "1/x")),
        Concept("ในการหา ∫ x² cos x dx ควรเลือก u เป็นอะไร", "x²", ("cos x", "sin x", "2x")),
        Concept("ในการหา ∫ ln x dx ควรเลือก u เป็นอะไร", "ln x", ("1", "x", "1/x")),
        Concept("ในการหา ∫ x sin 2x dx ควรเลือก u เป็นอะไร", "x", ("sin 2x", "cos 2x", "x sin 2x")),
    ]


@question_type("math.parts_formula_m6", display_name={"th": "สูตรการอินทิเกรตทีละส่วน"}, level=LEVEL, topic="อินทิเกรตทีละส่วน")
class PartsFormulaM6(ConceptBankType):
    ITEMS = [
        Concept("สูตรการอินทิเกรตทีละส่วนคือข้อใด", "∫ u dv = uv − ∫ v du", ("∫ u dv = uv + ∫ v du", "∫ u dv = u dv − ∫ du dv", "∫ u dv = ∫ u ∫ dv")),
        Concept("ถ้า u = x และ dv = eˣ dx แล้ว v เท่ากับเท่าใด", "eˣ", ("xeˣ", "eˣ/x", "x²/2")),
        Concept("ถ้า u = x และ dv = cos x dx แล้ว v เท่ากับเท่าใด", "sin x", ("−sin x", "cos x", "−cos x")),
        Concept("ถ้า u = ln x แล้ว du เท่ากับเท่าใด", "(1/x) dx", ("x dx", "ln x dx", "eˣ dx")),
    ]
