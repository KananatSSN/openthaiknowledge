"""ทฤษฎีบทหลักมูลของแคลคูลัส

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex

PROVENANCE = Provenance("original")


@question_type("math.ftc_part1",
               display_name={"th": "ทฤษฎีบทหลักมูล (Part 1)"},
               level={"th": "แคลคูลัส 1"}, topic="ทฤษฎีบทหลักมูลของแคลคูลัส")
class FTCPart1(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(1, 4), rng.choice([n for n in range(-4, 5) if n])
        integrand = poly_tex((a, "t^{2}"), (b, ""))
        return MathDraw(
            rf"g(x) = \int_{{0}}^{{x}} ({integrand})\,dt",
            poly_tex((a, "x^{2}"), (b, "")),
            prompt="จงหา g′(x)",
            distractors=[rf"\frac{{{a}}}{{3}}x^{{3}} + {b}x",
                         poly_tex((2 * a, "x")), poly_tex((a, "x^{2}"))])


@question_type("math.ftc_part2_evaluate", display_name={"th": "ทฤษฎีบทหลักมูล (Part 2)"},
               level={"th": "แคลคูลัส 1"}, topic="ทฤษฎีบทหลักมูลของแคลคูลัส")
class FtcPart2Evaluate(MathType):
    def expr(self, rng: Random, coef_hi: int = 4, bound_hi: int = 4):
        a, b = rng.randint(1, coef_hi), rng.randint(-6, 6)
        lo, hi = sorted(rng.sample(range(-bound_hi, bound_hi + 1), 2))

        def antideriv(x):
            return Fraction(a, 3) * x ** 3 + Fraction(b, 2) * x ** 2

        value = antideriv(hi) - antideriv(lo)
        shown = poly_tex((a, "x^2"), (b, "x"), (0, ""))
        return MathDraw(
            rf"\int_{{{lo}}}^{{{hi}}} ({shown}) \, dx", frac_tex(value),
            prompt="จงหาค่าปริพันธ์จำกัดเขต",
            distractors=[frac_tex(-value),
                         frac_tex(antideriv(hi) + antideriv(lo)),
                         frac_tex(antideriv(lo) - antideriv(hi))])
