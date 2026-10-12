"""กระจายทวินาม

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.3/*

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, binomial_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.expand_binomials",
               display_name={"th": "กระจายทวินาม"}, level={"th": "ม.3"},
               topic="กระจายทวินาม")
class ExpandBinomials(MathType):
    def expr(self, rng: Random, root_hi: int = 9):
        a = rng.choice([1, -1]) * rng.randint(1, root_hi)
        b = rng.choice([1, -1]) * rng.randint(1, root_hi)
        return MathDraw(
            rf"{binomial_tex(a)}{binomial_tex(b)}",
            poly_tex((1, "x^{2}"), (a + b, "x"), (a * b, "")),
            prompt="จงกระจาย")


@question_type("math.expand_formula",
               display_name={"th": "กระจายด้วยสูตร"}, level={"th": "ม.3"},
               topic="กระจายทวินาม")
class ExpandFormula(MathType):
    def expr(self, rng: Random, a_hi: int = 9):
        a = rng.randint(1, a_hi)
        kind = rng.choice(["sq+", "sq-", "diff"])
        if kind == "sq+":
            return MathDraw(rf"(x + {a})^{{2}}",
                            poly_tex((1, "x^{2}"), (2 * a, "x"), (a * a, "")),
                            hint=r"(a+b)^2 = a^2 + 2ab + b^2", prompt="จงกระจาย")
        if kind == "sq-":
            return MathDraw(rf"(x - {a})^{{2}}",
                            poly_tex((1, "x^{2}"), (-2 * a, "x"), (a * a, "")),
                            hint=r"(a-b)^2 = a^2 - 2ab + b^2", prompt="จงกระจาย")
        return MathDraw(rf"(x + {a})(x - {a})",
                        poly_tex((1, "x^{2}"), (-a * a, "")),
                        hint=r"(a+b)(a-b) = a^2 - b^2", prompt="จงกระจาย")


@question_type("math.expand_three_terms", display_name={"th": "กระจายพหุนามสองวงเล็บ"},
               level={"th": "ม.3"}, topic="กระจายทวินาม")
class ExpandThreeTerms(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 5, const_hi: int = 9):
        a, b = rng.randint(1, coef_hi), _nonzero(rng, -const_hi, const_hi)
        c, d = rng.randint(1, coef_hi), _nonzero(rng, -const_hi, const_hi)
        # (ax + b)(cx + d)
        p, q, r = a * c, a * d + b * c, b * d
        shown = (rf"({poly_tex((a, 'x'), (b, ''))})"
                 rf"({poly_tex((c, 'x'), (d, ''))})")
        return MathDraw(
            shown, poly_tex((p, "x^2"), (q, "x"), (r, "")),
            prompt="จงกระจายและจัดรูป",
            # Multiplying only the matching terms — the "FOIL without the OI" slip.
            distractors=[poly_tex((p, "x^2"), (r, "")),
                         poly_tex((p, "x^2"), (a * d - b * c, "x"), (r, "")),
                         poly_tex((p, "x^2"), (q, "x"), (-r, ""))])
