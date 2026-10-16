"""A sharp Cauchy and AM–GM bound for cyclic denominators."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def minimum_cyclic_expression(product: int) -> int:
    """The minimum is attained by equal a, b, c and any positive x, y."""
    if product <= 0:
        raise ValueError("positive product required")
    return 9 * product * product


@question_type(
    "math.weighted_cyclic_inequality_olympiad",
    display_name={"th": "ค่าต่ำสุดของผลบวกเศษส่วนแบบวนรอบ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class WeightedCyclicInequality(WordProblem):
    def expr(self, rng: Random):
        product = rng.randint(2, 12)
        answer = minimum_cyclic_expression(product)
        return MathDraw(
            (
                rf"abc={product},\quad F=(x+y)(a^2+b^2+c^2)"
                r"\left(\frac{a^5}{xc+yb}+\frac{b^5}{xa+yc}"
                r"+\frac{c^5}{xb+ya}\right)"
            ),
            str(answer),
            prompt="เมื่อ a,b,c,x,y เป็นจำนวนจริงบวก จงหาค่าต่ำสุดของ F",
            hint=(
                "ใช้คอชี–ชวาร์ซกับผลบวกเศษส่วน แล้วใช้ AM–GM "
                "และ a²+b²+c² ≥ (abc)^(1/3)(a+b+c)"
            ),
            distractors=[
                str(9 * product),  # scale by abc once instead of twice
                str(3 * product * product),  # omit the factor from Cauchy
                str(9 * product**3),  # overcount the homogeneous degree
                str(product * product),  # use only the equal-product term
                str(3 * product),  # combine both common omissions
                str(answer + product),  # treat the bound as unattained
            ],
        )
