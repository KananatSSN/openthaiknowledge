"""The linear solution of f(f(x) + x f(y)) = (a + 1)f(x) + a²xy is ax + 1."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 5",)
)


def linear_solution(a: int) -> tuple[int, int]:
    """f = px + q: the xy terms give p² = a², the constants q(p − a) = 0, and
    the x terms p² + pq = (a + 1)p; for a ≥ 2 only p = a, q = 1 survives."""
    return a, 1


@question_type(
    "math.linear_composite_functional_olympiad",
    display_name={"th": "ฟังก์ชันเชิงเส้นในสมการ f(f(x) + x f(y))"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class LinearCompositeFunctional(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(2, 7)
        n = rng.choice([v for v in range(-9, 10) if v not in (-1, 0, 1)])
        p, q = linear_solution(a)
        answer = p * n + q
        wrong = [v for v in dict.fromkeys([a * n, a * n - 1, (a + 1) * n + 1, -a * n, a * a * n + 1, a * n + 2]) if v != answer]
        return MathDraw(
            rf"f\big(f(x)+x\,f(y)\big)={a + 1}f(x)+{a * a}xy",
            str(answer),
            prompt=f"f เป็นฟังก์ชันเชิงเส้น f(x) = px + q ที่สอดคล้องสมการต่อไปนี้ทุกจำนวนจริง x, y จงหา f({n})",
            hint="แทน f(x) = px + q แล้วเทียบสัมประสิทธิ์ของ xy, x และค่าคงตัว",
            distractors=[str(v) for v in wrong],
        )
