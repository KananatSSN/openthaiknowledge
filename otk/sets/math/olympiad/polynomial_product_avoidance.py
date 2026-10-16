"""Degrees of integer polynomials whose value sets avoid products."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def count_product_avoiding_degrees(limit: int) -> int:
    """Count 1<=n<=limit admitting a product-avoiding monic integer polynomial.

    For P(x)=x+t, the range is all integers. For P(x)=x^2+ux+v,
    P(0)P(1-u)=P(-v). Conversely, when n>=3, the monic polynomial
    x^(n-3)*(x^3-x)+2 takes only values 2 modulo 3, whose pairwise
    products are 1 modulo 3. Thus precisely the degrees at least 3 work.
    """
    if limit < 1:
        raise ValueError("limit must be positive")
    return max(0, limit - 2)


@question_type(
    "math.polynomial_product_avoidance_olympiad",
    display_name={"th": "ดีกรีของพหุนามที่หลีกเลี่ยงผลคูณ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามและเศษเหลือ",
)
class PolynomialProductAvoidance(WordProblem):
    def expr(self, rng: Random):
        limit = rng.randint(12, 100)
        answer = count_product_avoiding_degrees(limit)
        return MathDraw(
            rf"1\le n\le {limit},\quad P\in\mathbb{{Z}}[x],\quad "
            r"\deg P=n,\quad P\text{ monic}",
            str(answer),
            prompt=("นับดีกรี n ในช่วงที่กำหนดซึ่งสามารถเลือกพหุนาม P ตามเงื่อนไข "
                    "ให้ค่าของ P บนจำนวนเต็มไม่รวมผลคูณของค่าสองค่าใด ๆ "
                    "กล่าวคือ P(a)P(b) ไม่เท่ากับ P(c) สำหรับจำนวนเต็ม a,b,c ทุกชุด"),
            hint=r"x^3-x\equiv0\pmod 3;\qquad P(0)P(1-u)=P(-v)\ "
                 r"\text{เมื่อ }P(x)=x^2+ux+v",
            distractors=[
                str(limit - 3),  # wrongly reject degree 3
                str(limit - 1),  # wrongly admit quadratic degree 2
                str(limit),  # wrongly admit all positive degrees
            ],
        )
