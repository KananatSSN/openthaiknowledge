"""Monic P of even degree d with P(k) = αk + β for k = 1..d − 1: P(d) + P(0) = αd + 2β + d!."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 19",))


def endpoint_sum(d: int, alpha: int, beta: int) -> int:
    """P(x) = αx + β + (x − 1)⋯(x − (d − 1))(x − r). At x = d the product is
    (d − 1)!(d − r); at x = 0 it is (−1)^d (d − 1)! r. For even d the r
    terms cancel (source: d = 4, P(k) = k → 28)."""
    return alpha * d + 2 * beta + factorial(d)


@question_type(
    "math.monic_interpolation_value_olympiad",
    display_name={"th": "ค่าของพหุนามโมนิกที่กำหนดเศษจากการหาร"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามและเศษเหลือ",
)
class MonicInterpolationValue(WordProblem):
    def expr(self, rng: Random):
        d = rng.choice([2, 4, 6, 8])
        alpha, beta = rng.randint(-5, 5), rng.randint(-9, 9)
        answer = endpoint_sum(d, alpha, beta)
        wrong = [v for v in dict.fromkeys([alpha * d + 2 * beta, alpha * d + beta + factorial(d), alpha * d + 2 * beta + factorial(d - 1), alpha * d + 2 * beta + 2 * factorial(d), answer + d]) if v != answer]
        rem = ("k" if alpha == 1 else ("-k" if alpha == -1 else f"{alpha}k")) if alpha else ""
        rem = (rem + (f"{beta:+d}" if beta else "")) if rem else str(beta)
        return MathDraw(
            rf"\deg P={d},\quad P(x)\bmod (x-k)={rem}\quad (k=1,\ldots,{d - 1})",
            str(answer),
            prompt=f"P(x) เป็นพหุนามดีกรี {d} ที่มีสัมประสิทธิ์ของ x^{d} เท่ากับ 1 และ x − k หาร P(x) เหลือเศษตามที่กำหนด จงหาค่า P({d}) + P(0)",
            hint="เขียน P(x) = (เศษ) + (x − 1)(x − 2)⋯(x − (d − 1))(x − r) แล้วคำนวณ P(d) + P(0) จะเห็นว่า r หักล้างกัน",
            distractors=[str(v) for v in wrong],
        )
