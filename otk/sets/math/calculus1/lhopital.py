"""กฎของโลปิตาล

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex
from otk.sets._support.math_calculus import _nonzero, _signed

PROVENANCE = Provenance("original")


@question_type("math.lhopital",
               display_name={"th": "กฎของโลปิตาล"}, level={"th": "แคลคูลัส 1"},
               topic="กฎของโลปิตาล")
class LHopital(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(2, 9)
        return MathDraw("", str(a),
                        prompt=f"lim(x→0) sin({a}x)/x = ?",
                        distractors=["1", "0", str(a + 1)])


@question_type("math.lhopital_trig", display_name={"th": "โลปิตาลกับตรีโกณมิติ"},
               level={"th": "แคลคูลัส 1"}, topic="กฎของโลปิตาล")
class LhopitalTrig(MathType):
    def expr(self, rng: Random, coef_hi: int = 9):
        a, b = rng.randint(1, coef_hi), rng.randint(1, coef_hi)
        return MathDraw(
            rf"\lim_{{x \to 0}} \frac{{\sin {a}x}}{{{b}x}}",
            frac_tex(Fraction(a, b)), prompt="จงหาค่าลิมิต",
            distractors=[frac_tex(Fraction(b, a)), "0", "1"])


@question_type("math.lhopital_polynomial", display_name={"th": "โลปิตาลกับพหุนาม"},
               level={"th": "แคลคูลัส 1"}, topic="กฎของโลปิตาล")
class LhopitalPolynomial(MathType):
    def expr(self, rng: Random, root_hi: int = 6):
        r = _nonzero(rng, -root_hi, root_hi)
        s = rng.choice([n for n in range(-root_hi, root_hi + 1) if n != r])
        # (x − r)(x − s) / (x − r) → r − s as x → r
        value = r - s
        return MathDraw(
            rf"\lim_{{x \to {r}}} \frac{{(x{_signed(-r)})(x{_signed(-s)})}}"
            rf"{{x{_signed(-r)}}}", str(value), prompt="จงหาค่าลิมิต",
            distractors=[str(-value), "0", str(r + s)])
