"""กฎการหาอนุพันธ์

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType

PROVENANCE = Provenance("original")


@question_type("math.product_rule_power",
               display_name={"th": "กฎผลคูณ (กำลัง)"}, level={"th": "แคลคูลัส 1"},
               topic="กฎการหาอนุพันธ์")
class ProductRulePower(MathType):
    def expr(self, rng: Random):
        m, n = rng.randint(2, 5), rng.randint(2, 5)
        return MathDraw(
            rf"\frac{{d}}{{dx}}\left[x^{{{m}}} \cdot x^{{{n}}}\right]",
            rf"{m + n}x^{{{m + n - 1}}}",
            distractors=[rf"{m * n}x^{{{m + n}}}", rf"x^{{{m + n}}}",
                         rf"{m + n}x^{{{m + n}}}"])


@question_type("math.derivative_trig_rule",
               display_name={"th": "อนุพันธ์ของฟังก์ชันตรีโกณมิติ"},
               level={"th": "แคลคูลัส 1"}, topic="กฎการหาอนุพันธ์")
class DerivativeTrigRule(MathType):
    def expr(self, rng: Random):
        kind = rng.choice(["sin", "cos", "tan"])
        table = {
            "sin": (r"\sin x", r"\cos x",
                    [r"-\sin x", r"-\cos x", r"\sec^{2} x"]),
            "cos": (r"\cos x", r"-\sin x",
                    [r"\sin x", r"\cos x", r"-\sec^{2} x"]),
            "tan": (r"\tan x", r"\sec^{2} x",
                    [r"\sec x \tan x", r"-\sec^{2} x", r"\csc^{2} x"]),
        }
        fn, ans, wrong = table[kind]
        return MathDraw(rf"\frac{{d}}{{dx}}\left[{fn}\right]", ans,
                        distractors=wrong)


@question_type("math.derivative_exp_log",
               display_name={"th": "อนุพันธ์ของเลขชี้กำลังและลอการิทึม"},
               level={"th": "แคลคูลัส 1"}, topic="กฎการหาอนุพันธ์")
class DerivativeExpLog(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        kind = rng.choice(["exp", "ln", "a^x"])
        table = {
            "exp": (r"e^{x}", r"e^{x}",
                    [r"x e^{x-1}", r"e^{x-1}", r"\frac{e^{x}}{x}"]),
            "ln": (r"\ln x", r"\frac{1}{x}",
                   [r"\frac{1}{\ln x}", r"\ln x", r"-\frac{1}{x^{2}}"]),
            "a^x": (r"a^{x}", r"a^{x}\ln a",
                    [r"a^{x}", r"x a^{x-1}", r"\frac{a^{x}}{\ln a}"]),
        }
        fn, ans, wrong = table[kind]
        return MathDraw(rf"\frac{{d}}{{dx}}\left[{fn}\right]", ans,
                        distractors=wrong)
