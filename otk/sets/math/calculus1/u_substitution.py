"""เทคนิคการอินทิเกรต

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex
from otk.sets._support.math_calculus import _linear

PROVENANCE = Provenance("original")


@question_type("math.u_substitution",
               display_name={"th": "การอินทิเกรตโดยแทนค่า u"},
               level={"th": "แคลคูลัส 1"}, topic="เทคนิคการอินทิเกรต")
class USubstitution(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        c, n = rng.randint(1, 5), rng.randint(2, 4)
        base = rf"x^{{2}}+{c}"
        return MathDraw(
            rf"\int 2x({base})^{{{n}}}\,dx",
            rf"\frac{{({base})^{{{n + 1}}}}}{{{n + 1}}} + C",
            hint=rf"u = {base}",
            distractors=[rf"({base})^{{{n + 1}}} + C",
                         rf"\frac{{({base})^{{{n}}}}}{{{n}}} + C",
                         rf"\frac{{2({base})^{{{n + 1}}}}}{{{n + 1}}} + C"])


@question_type("math.u_substitution_definite",
               display_name={"th": "อินทิเกรตโดยแทนค่า (จำกัดเขต)"},
               level={"th": "แคลคูลัส 1"}, topic="เทคนิคการอินทิเกรต")
class USubstitutionDefinite(MathType):
    """∫ (ax+b)ⁿ dx over an interval — the bounds must be substituted too."""
    break_convergence = True  # one-part slips cluster round the answer

    def expr(self, rng: Random, power_lo: int = 2, power_hi: int = 4):
        a = rng.randint(1, 4)
        b = rng.randint(-4, 4)
        n = rng.randint(power_lo, power_hi)
        lo, hi = sorted(rng.sample(range(-3, 4), 2))
        upper = Fraction((a * hi + b) ** (n + 1), a * (n + 1))
        lower = Fraction((a * lo + b) ** (n + 1), a * (n + 1))
        value = upper - lower
        inner = _linear(a, b)
        return MathDraw(
            rf"\int_{{{lo}}}^{{{hi}}} ({inner})^{{{n}}} \, dx", frac_tex(value),
            prompt="จงหาค่าปริพันธ์",
            # Forgetting the 1/a from du = a dx.
            distractors=[frac_tex(value * a), frac_tex(-value),
                         frac_tex(Fraction((a * hi + b) ** (n + 1), n + 1))])
