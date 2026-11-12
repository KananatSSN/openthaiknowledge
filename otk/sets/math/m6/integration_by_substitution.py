"""อินทิเกรตโดยการแทนค่า

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม แคลคูลัส 1 ม.6/3

Sets moved here from: math, math_thin_topics.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex
from otk.sets._support.math_chapters import _distinct
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_thin_topics import M6

PROVENANCE = Provenance("original")


# (integral, the right u, three tempting wrong u); "@n" is the item's power.
_SUBSTITUTIONS = (
    (r"\int 2x\,(x^{2} + 1)^{@n}\,dx", "u = x^{2} + 1", ("u = 2x", "u = x^{2}", "u = (x^{2} + 1)^{@n}")),
    (r"\int x\,e^{x^{2}}\,dx", "u = x^{2}", ("u = x", "u = e^{x}", "u = e^{x^{2}}")),
    (r"\int \cos x\,\sin^{@n} x\,dx", r"u = \sin x", (r"u = \cos x", r"u = \sin^{@n} x", "u = x")),
    (r"\int \frac{2x + 3}{x^{2} + 3x + 1}\,dx", "u = x^{2} + 3x + 1", ("u = 2x + 3", "u = x^{2}", "u = 3x + 1")),
    (r"\int 3x^{2}\,(x^{3} - 2)^{@n}\,dx", "u = x^{3} - 2", ("u = 3x^{2}", "u = x^{3}", "u = (x^{3} - 2)^{@n}")),
    (r"\int \frac{\ln x}{x}\,dx", r"u = \ln x", ("u = x", r"u = \frac{1}{x}", r"u = x\ln x")),
)


# u = g(x) on [a, b]: (g, g', a, b)
_DEFINITE_U = (
    ("x^{2} + 1", "2x", 0, 1, lambda x: x * x + 1),
    ("x^{3} + 1", "3x^{2}", 0, 1, lambda x: x ** 3 + 1),
    ("x^{2} - 1", "2x", 1, 2, lambda x: x * x - 1),
    ("x^{2} + 3", "2x", 0, 1, lambda x: x * x + 3),
)


@question_type("math.substitution_setup_m6", display_name={"th": "เลือกตัวแปร u สำหรับการอินทิเกรตโดยการแทนค่า"},
               level=M6, topic="อินทิเกรตโดยการแทนค่า")
class SubstitutionSetupM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        integral, right, wrongs = rng.choice(_SUBSTITUTIONS)
        n = str(rng.randint(3, 7))
        fill = lambda s: s.replace("@n", n)
        return _maths([text("ควรเลือก u ในข้อใด จึงหาปริพันธ์ต่อไปนี้ได้โดยการแทนค่า"),
                       content_math(fill(integral))], fill(right), [fill(w) for w in wrongs], self.topic)


@question_type("math.integral_substitution",
               display_name={"th": "อินทิเกรตโดยการแทนค่า"}, level={"th": "ม.6"},
               topic="อินทิเกรตโดยการแทนค่า")
class IntegralSubstitution(MathType):
    def expr(self, rng: Random):
        kind = rng.choice(["power", "trig", "exp"])
        if kind == "power":
            a = rng.choice([2, 3])
            b = rng.randint(1, 5)
            n = rng.choice([2, 3, 4])
            return MathDraw(
                rf"\int \, ({a}x + {b})^{{{n}}} \, dx",
                rf"\frac{{({a}x + {b})^{{{n + 1}}}}}{{{a * (n + 1)}}} + C",
                hint=rf"u = {a}x + {b}")
        a = rng.randint(2, 5)
        if kind == "trig":
            if rng.random() < 0.5:
                return rf"\int \, \cos {a}x \, dx", rf"\frac{{\sin {a}x}}{{{a}}} + C"
            return rf"\int \, \sin {a}x \, dx", rf"-\frac{{\cos {a}x}}{{{a}}} + C"
        return rf"\int \, e^{{{a}x}} \, dx", rf"\frac{{e^{{{a}x}}}}{{{a}}} + C"


@question_type("math.substitution_definite_m6", display_name={"th": "อินทิกรัลจำกัดเขตโดยการแทนค่า"},
               level=M6, topic="อินทิเกรตโดยการแทนค่า")
class SubstitutionDefiniteM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        g, dg, a, b, fn = rng.choice(_DEFINITE_U)
        n = rng.randint(1, 3)
        lo, hi = fn(a), fn(b)
        val = Fraction(hi ** (n + 1) - lo ** (n + 1), n + 1)
        # The x-limits kept after substituting, the 1/(n + 1) forgotten, 1/n.
        wrongs = [Fraction(b ** (n + 1) - a ** (n + 1), n + 1), Fraction(hi ** (n + 1) - lo ** (n + 1)),
                  Fraction(hi ** (n + 1) - lo ** (n + 1), n), Fraction(hi ** n - lo ** n, n)]
        return _maths([text("จงหาค่าของ"), content_math(rf"\int_{{{a}}}^{{{b}}} {dg}\,({g})^{{{n}}}\,dx")],
                      frac_tex(val), _distinct(frac_tex(val), *[frac_tex(w) for w in wrongs])[:3], self.topic)


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.kit.math_problems import poly_tex  # noqa: E402
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

# ── More integration by substitution (2026-11): (ax + b)ⁿ, a definite (ax + b)², 2x(x² + 1)ⁿ, e^(kx), which u
# to choose, a definite 2x(x² + 1), and cos(kx) ──


@question_type("math.sub_linear_power_m6", display_name={"th": "ปริพันธ์ของ (ax + b)ⁿ"}, level=LEVEL, topic="อินทิเกรตโดยการแทนค่า")
class SubLinearPowerM6(MathType):
    def expr(self, rng: Random):
        a, b, n = rng.randint(2, 5), _nz6(rng, 1, 9), rng.randint(2, 6)
        inner = poly_tex((a, "x"), (b, ""))
        right = rf"\frac{{({inner})^{{{n + 1}}}}}{{{a * (n + 1)}}} + C"
        wrongs = [rf"\frac{{({inner})^{{{n + 1}}}}}{{{n + 1}}} + C", rf"\frac{{({inner})^{{{n + 1}}}}}{{{a}}} + C",
                  rf"{a * n}({inner})^{{{n - 1}}} + C", rf"\frac{{({inner})^{{{n}}}}}{{{a * n}}} + C"]
        return MathDraw(rf"\int ({inner})^{{{n}}} \, dx", right, prompt="จงหาปริพันธ์", distractors=_tk6(*wrongs, answer=right))


@question_type("math.sub_linear_square_definite_m6", display_name={"th": "อินทิกรัลจำกัดเขตของ (ax + b)²"}, level=LEVEL,
               topic="อินทิเกรตโดยการแทนค่า")
class SubLinearSquareDefiniteM6(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(1, 4), rng.randint(-3, 5)
        right = Fraction((a + b) ** 3 - b ** 3, 3 * a)
        inner = poly_tex((a, "x"), (b, ""))
        # Not divided by a; not divided by three; the inside squared at the top only.
        return MathDraw(rf"\int_{{0}}^{{1}} ({inner})^{{2}} \, dx", frac_tex(right), prompt="จงหาค่า",
                        distractors=_fk6(Fraction((a + b) ** 3 - b ** 3, 3), Fraction((a + b) ** 3 - b ** 3, a), (a + b) ** 2,
                                         right + 1, answer=right))


@question_type("math.sub_chain_power_m6", display_name={"th": "ปริพันธ์ของ 2x(x² + c)ⁿ"}, level=LEVEL, topic="อินทิเกรตโดยการแทนค่า")
class SubChainPowerM6(MathType):
    def expr(self, rng: Random):
        c, n = rng.randint(1, 9), rng.randint(2, 5)
        inner = poly_tex((1, "x^{2}"), (c, ""))
        right = rf"\frac{{({inner})^{{{n + 1}}}}}{{{n + 1}}} + C"
        wrongs = [rf"\frac{{({inner})^{{{n + 1}}}}}{{{2 * (n + 1)}}} + C", rf"x^{{2}}\frac{{({inner})^{{{n + 1}}}}}{{{n + 1}}} + C",
                  rf"{n}({inner})^{{{n - 1}}} + C", rf"\frac{{({inner})^{{{n}}}}}{{{n}}} + C"]
        return MathDraw(rf"\int 2x({inner})^{{{n}}} \, dx", right, prompt="จงหาปริพันธ์", distractors=_tk6(*wrongs, answer=right))


@question_type("math.sub_exp_linear_m6", display_name={"th": "ปริพันธ์ของ e^(kx)"}, level=LEVEL, topic="อินทิเกรตโดยการแทนค่า")
class SubExpLinearM6(MathType):
    def expr(self, rng: Random):
        k = rng.choice((2, 3, 4, 5, -2, -3))
        right = rf"\frac{{1}}{{{k}}}e^{{{k}x}} + C" if k > 0 else rf"-\frac{{1}}{{{-k}}}e^{{{k}x}} + C"
        wrongs = [rf"{k}e^{{{k}x}} + C", rf"e^{{{k}x}} + C", rf"\frac{{e^{{{k + 1}x}}}}{{{k + 1}}} + C",
                  rf"\frac{{1}}{{{abs(k)}}}e^{{{k}x}} + C" if k < 0 else rf"-\frac{{1}}{{{k}}}e^{{{k}x}} + C"]
        return MathDraw(rf"\int e^{{{k}x}} \, dx", right, prompt="จงหาปริพันธ์", distractors=_tk6(*wrongs, answer=right))


@question_type("math.sub_pick_u_m6", display_name={"th": "เลือก u สำหรับการอินทิเกรตโดยการแทนค่า"}, level=LEVEL,
               topic="อินทิเกรตโดยการแทนค่า")
class SubPickUM6(ConceptBankType):
    ITEMS = [
        Concept("ในการหา ∫ sin³x cos x dx ควรให้ u เป็นอะไร", "sin x", ("cos x", "sin³x", "x")),
        Concept("ในการหา ∫ x/(x² + 1) dx ควรให้ u เป็นอะไร", "x² + 1", ("x", "1/x", "x²")),
        Concept("ในการหา ∫ (ln x)/x dx ควรให้ u เป็นอะไร", "ln x", ("x", "1/x", "(ln x)/x")),
        Concept("ในการหา ∫ 2x√(x² + 3) dx ควรให้ u เป็นอะไร", "x² + 3", ("2x", "√(x² + 3)", "x")),
    ]


@question_type("math.sub_chain_definite_m6", display_name={"th": "อินทิกรัลจำกัดเขตของ 2x(x² + 1)"}, level=LEVEL,
               topic="อินทิเกรตโดยการแทนค่า")
class SubChainDefiniteM6(MathType):
    def expr(self, rng: Random):
        a = rng.randint(1, 5)
        right = Fraction((a * a + 1) ** 2 - 1, 2)
        return MathDraw(rf"\int_{{0}}^{{{a}}} 2x(x^{{2}} + 1) \, dx", frac_tex(right), prompt="จงหาค่า",
                        distractors=_fk6((a * a + 1) ** 2 - 1, Fraction((a * a + 1) ** 2, 2), a * a + 1, right + a, answer=right))


@question_type("math.sub_cos_linear_m6", display_name={"th": "ปริพันธ์ของ cos(kx)"}, level=LEVEL, topic="อินทิเกรตโดยการแทนค่า")
class SubCosLinearM6(MathType):
    def expr(self, rng: Random):
        k = rng.randint(2, 6)
        right = rf"\frac{{1}}{{{k}}}\sin {k}x + C"
        wrongs = [rf"{k}\sin {k}x + C", rf"-\frac{{1}}{{{k}}}\sin {k}x + C", rf"\sin {k}x + C", rf"-{k}\sin {k}x + C"]
        return MathDraw(rf"\int \cos {k}x \, dx", right, prompt="จงหาปริพันธ์", distractors=_tk6(*wrongs, answer=right))
