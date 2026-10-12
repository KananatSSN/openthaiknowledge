"""กฎลูกโซ่

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType
from otk.sets._support.math_calculus import _linear, _nonzero

PROVENANCE = Provenance("original")


@question_type("math.chain_rule",
               display_name={"th": "กฎลูกโซ่"}, level={"th": "แคลคูลัส 1"},
               topic="กฎลูกโซ่")
class ChainRule(MathType):
    def expr(self, rng: Random):
        a, b, n = rng.randint(2, 4), rng.randint(1, 5), rng.randint(2, 4)
        inner = rf"{a}x + {b}"
        return MathDraw(
            rf"\frac{{d}}{{dx}}\left[({inner})^{{{n}}}\right]",
            rf"{n * a}({inner})^{{{n - 1}}}",
            hint=r"\text{multiply by the inner derivative}",
            distractors=[rf"{n}({inner})^{{{n - 1}}}",
                         rf"{n * a}({inner})^{{{n}}}",
                         rf"{n}({inner})^{{{n}}}"])


@question_type("math.chain_rule_power", display_name={"th": "กฎลูกโซ่กับกำลัง"},
               level={"th": "แคลคูลัส 1"}, topic="กฎลูกโซ่")
class ChainRulePower(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 6, power_lo: int = 2,
             power_hi: int = 6):
        a = _nonzero(rng, -coef_hi, coef_hi)
        b = rng.randint(-9, 9)
        n = rng.randint(power_lo, power_hi)
        inner = _linear(a, b)
        return MathDraw(
            rf"f(x) = ({inner})^{{{n}}}", rf"{n * a}({inner})^{{{n - 1}}}",
            prompt="จงหา f′(x)",
            # Forgetting the inner derivative is the whole point of the item.
            distractors=[rf"{n}({inner})^{{{n - 1}}}",
                         rf"{n * a}({inner})^{{{n}}}",
                         rf"{a}({inner})^{{{n - 1}}}"])


@question_type("math.chain_rule_trig", display_name={"th": "กฎลูกโซ่กับตรีโกณมิติ"},
               level={"th": "แคลคูลัส 1"}, topic="กฎลูกโซ่")
class ChainRuleTrig(MathType):
    def expr(self, rng: Random, coef_hi: int = 7):
        a = _nonzero(rng, -coef_hi, coef_hi)
        b = rng.randint(-9, 9)
        inner = _linear(a, b)
        if rng.random() < 0.5:
            return MathDraw(
                rf"f(x) = \sin({inner})", rf"{a}\cos({inner})",
                prompt="จงหา f′(x)",
                distractors=[rf"\cos({inner})", rf"{-a}\cos({inner})",
                             rf"{a}\sin({inner})"])
        return MathDraw(
            rf"f(x) = \cos({inner})", rf"{-a}\sin({inner})",
            prompt="จงหา f′(x)",
            distractors=[rf"-\sin({inner})", rf"{a}\sin({inner})",
                         rf"{-a}\cos({inner})"])
