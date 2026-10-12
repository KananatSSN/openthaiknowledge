"""สมการเชิงอนุพันธ์เบื้องต้น

คณิตศาสตร์ · แคลคูลัส 2 · อุดมศึกษา
Indicators: —

Sets moved here from: math.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem

PROVENANCE = Provenance("original")


@question_type("math.ode_order",
               display_name={"th": "อันดับของสมการเชิงอนุพันธ์"},
               level={"th": "แคลคูลัส 2"}, topic="สมการเชิงอนุพันธ์เบื้องต้น")
class ODEOrder(WordProblem):
    def expr(self, rng: Random):
        eq, order = rng.choice([("y′ + 2y = 0", 1), ("y″ + 3y′ + y = 0", 2),
                                ("y‴ − y = 0", 3), ("(y″)² + y = x", 2)])
        return MathDraw("", str(order),
                        prompt=f"สมการ {eq} มีอันดับ (order) เท่าใด?",
                        distractors=[str(order + 1), str(max(1, order - 1)), "0"])


@question_type("math.separable_ode",
               display_name={"th": "สมการแยกตัวแปรได้"}, level={"th": "แคลคูลัส 2"},
               topic="สมการเชิงอนุพันธ์เบื้องต้น")
class SeparableODE(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        # k = 1 would make the answer the "forgot k" distractor, Ce^{x}.
        k = rng.choice([n for n in range(-4, 5) if n not in (0, 1)])
        return MathDraw(
            rf"\frac{{dy}}{{dx}} = {k}y", rf"y = Ce^{{{k}x}}",
            prompt="ผลเฉลยทั่วไปคือข้อใด",
            distractors=[r"y = Ce^{x}", rf"y = {k}x + C", rf"y = C \cdot {k}^{{x}}"])


@question_type("math.integrating_factor",
               display_name={"th": "ตัวประกอบปริพันธ์"}, level={"th": "แคลคูลัส 2"},
               topic="สมการเชิงอนุพันธ์เบื้องต้น")
class IntegratingFactor(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        a = rng.randint(2, 5)
        return MathDraw(
            rf"y' + {a}y = Q(x)", rf"e^{{{a}x}}",
            prompt="ตัวประกอบปริพันธ์คือข้อใด",
            distractors=[rf"e^{{-{a}x}}", rf"{a}x", r"e^{\int Q\,dx}", rf"-{a}x", rf"e^{{{a}}}"])


@question_type("math.exponential_growth",
               display_name={"th": "การเติบโตแบบเอกซ์โพเนนเชียล"},
               level={"th": "แคลคูลัส 2"}, topic="สมการเชิงอนุพันธ์เบื้องต้น")
class ExponentialGrowth(MathType):
    def expr(self, rng: Random):
        p0 = rng.randint(1, 10) * 100
        k = rng.randint(2, 5)
        return MathDraw(
            rf"\frac{{dP}}{{dt}} = {k}P,\ P_0 = {p0}", rf"{p0}e^{{{k}t}}",
            prompt="ประชากรหลังเวลา t เท่ากับข้อใด",
            distractors=[rf"{p0}(1 + {k}t)", rf"{p0}\cdot {k}^{{t}}",
                         rf"{p0} + {k}t"])
