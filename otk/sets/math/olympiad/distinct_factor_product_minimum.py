"""2k distinct nonzero integers have |product| ≥ (k!)², equality only for ±1, …, ±k."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 2",)
)


def smallest_product(count: int) -> int:
    """At most two of the integers have each absolute value j, so sorted by
    absolute value the i-th is at least ⌈i/2⌉."""
    k, odd = divmod(count, 2)
    return factorial(k) ** 2 * (k + 1 if odd else 1)


def integer_root_count_bound() -> int:
    """For Π(x − a_i) = (k!)² with 2k distinct a_i, a root x makes {x − a_i}
    = {±1, …, ±k}; two roots would give two shifts of the same set."""
    return 1


@question_type(
    "math.distinct_factor_product_minimum_olympiad",
    display_name={"th": "ผลคูณน้อยสุดของจำนวนเต็มไม่เป็นศูนย์ที่แตกต่างกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามสัมประสิทธิ์จำนวนเต็ม",
)
class DistinctFactorProductMinimum(WordProblem):
    def expr(self, rng: Random):
        count = rng.randint(4, 14)
        answer = smallest_product(count)
        k = count // 2
        wrong = [v for v in dict.fromkeys([
            factorial(count),  # treat them as 1, …, 2k
            factorial(k),
            factorial(k) ** 2 * 2**k,
            factorial(k + 1) ** 2,
            factorial(count) // factorial(k),
        ]) if v != answer]
        return MathDraw(
            rf"|d_{{1}}d_{{2}}\cdots d_{{{count}}}|",
            str(answer),
            prompt=f"d₁, d₂, …, d_{count} เป็นจำนวนเต็มไม่เป็นศูนย์ที่แตกต่างกันทั้งหมด ค่าน้อยที่สุดของค่าสัมบูรณ์ของผลคูณคือเท่าใด",
            hint="ค่าสัมบูรณ์แต่ละค่าใช้ได้ไม่เกินสองครั้ง (บวกและลบ) เรียงตามค่าสัมบูรณ์แล้วเทียบกับ 1, 1, 2, 2, 3, 3, …",
            distractors=[str(v) for v in wrong],
        )
