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
