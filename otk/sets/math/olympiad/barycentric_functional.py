"""A multiplicative functional equation at noncollinear barycentres."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def count_barycentric_functions(arity: int, coefficient: int) -> int:
    """Count real functions satisfying f(mean)=coefficient*product(f(points)).

    The identity is imposed when the first three points are noncollinear.
    If f vanishes once, varying a noncollinear tuple through that point makes
    it vanish everywhere. Otherwise, compare tuples with the same centroid
    to show f(x)f(y)/f(0) depends only on x+y. A generic auxiliary point then
    gives f(x)f(y)=f(0)f(x+y) for all x,y. After normalization this is an
    additive-group character into nonzero reals. The original identity makes
    every character value an (arity-1)-st root of unity. A real character on
    the divisible group R^2 is positive, so it is identically 1. Thus all
    solutions are constants c with c=coefficient*c**arity.
    """
    if arity < 3 or coefficient == 0:
        raise ValueError("arity must be at least 3 and coefficient nonzero")
    if arity % 2 == 0:
        return 2  # zero and one nonzero real root
    return 3 if coefficient > 0 else 1  # zero and two roots, or zero only


@question_type(
    "math.barycentric_functional_olympiad",
    display_name={"th": "จำนวนคำตอบของสมการเชิงฟังก์ชันที่จุดศูนย์กลาง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class BarycentricFunctional(WordProblem):
    def expr(self, rng: Random):
        arity = rng.randint(3, 7)
        coefficient = rng.choice((-4, -2, -1, 1, 2, 4))
        answer = count_barycentric_functions(arity, coefficient)
        return MathDraw(
            rf"f\!\left(\frac{{v_1+\cdots+v_{arity}}}{{{arity}}}\right)"
            rf"={coefficient}\prod_{{i=1}}^{{{arity}}}f(v_i),"
            rf"\quad v_i\in\mathbb{{R}}^2",
            str(answer),
            prompt=("ให้ f เป็นฟังก์ชันจากระนาบจำนวนจริงไปยังจำนวนจริง "
                    "และสมการที่กำหนดเป็นจริงสำหรับจุดทุกชุดที่สามจุดแรกไม่อยู่บนเส้นตรงเดียวกัน "
                    "มีฟังก์ชัน f ที่เป็นไปได้ทั้งหมดกี่ฟังก์ชัน"),
            hint=r"f(x)f(y)\overset{?}{=}f(0)f(x+y)",
            distractors=[
                "0",  # wrongly reject the always-valid zero function
                "1",  # count only the zero function
                "2",  # assume exactly one nonzero constant
                "3",  # assume both signs of a nonzero constant always work
            ],
        )
