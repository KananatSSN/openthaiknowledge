"""งานและแรงของไหล

คณิตศาสตร์ · แคลคูลัส 2 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex

PROVENANCE = Provenance("original")


@question_type("math.work_spring",
               display_name={"th": "งานในการยืดสปริง"}, level={"th": "แคลคูลัส 2"},
               topic="งานและแรงของไหล")
class WorkSpring(WordProblem):
    def expr(self, rng: Random):
        k = rng.choice([2, 4, 6, 8, 10])
        d = rng.randint(2, 6)
        return MathDraw("", str(k * d * d // 2),
                        prompt=f"งานในการยืดสปริง (ค่าคงที่ {k}) จาก 0 ถึง {d} "
                               f"เท่ากับเท่าใด?",
                        distractors=[str(k * d), str(k * d * d), str(k * d // 2)])


@question_type("math.work_lifting_rope", display_name={"th": "งานในการดึงเชือกขึ้น"},
               level={"th": "แคลคูลัส 2"}, topic="งานและแรงของไหล")
class WorkLiftingRope(WordProblem):
    """A uniform rope's centre of mass rises L/2, so W = ρgL²/2 — here with
    weight per metre, so the answer is an integer."""

    def expr(self, rng: Random, length_lo: int = 4, length_hi: int = 30,
             density_lo: int = 1, density_hi: int = 8):
        length = rng.randrange(length_lo, length_hi, 2)   # even → L²/2 is whole
        density = rng.randint(density_lo, density_hi)
        work = density * length * length // 2
        return MathDraw(
            "", str(work),
            prompt=(f"เชือกยาว {length} เมตร หนักเมตรละ {density} นิวตัน "
                    "ห้อยอยู่จากดาดฟ้า ต้องใช้งานเท่าใด (จูล) "
                    "ในการดึงเชือกขึ้นมาทั้งหมด"),
            hint=r"W = \int_0^L \rho x \, dx",
            distractors=[str(density * length), str(density * length * length),
                         str(length * length // 2)])


@question_type("math.work_variable_force", display_name={"th": "งานของแรงที่แปรค่า"},
               level={"th": "แคลคูลัส 2"}, topic="งานและแรงของไหล")
class WorkVariableForce(MathType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random, coef_hi: int = 6, bound_hi: int = 5):
        a = rng.randint(1, coef_hi)
        lo, hi = sorted(rng.sample(range(0, bound_hi + 1), 2))
        # ∫ a·x dx from lo to hi
        work = Fraction(a, 2) * (hi * hi - lo * lo)
        return MathDraw(
            rf"F(x) = {a}x, \quad x: {lo} \to {hi}", frac_tex(work),
            prompt="จงหางานที่แรงนี้ทำ",
            hint=r"W = \int_a^b F(x)\,dx",
            distractors=[frac_tex(Fraction(a * (hi - lo))),
                         frac_tex(work * 2), frac_tex(Fraction(a * hi * hi, 2))])
