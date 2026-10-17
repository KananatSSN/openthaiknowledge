"""f(xy + (c+1)(x + y) + c² − d) = f(x)f(y) + f(y) + x − d has the linear solution x + c."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 5",))


def shift_solution(c: int) -> tuple[int, int]:
    """f = px + q: the xy terms give p = p², so p = 1 (p = 0 leaves an x on one
    side); then the x terms give q = c. The source has c = 1, d = 2."""
    return 1, c


@question_type(
    "math.linear_shift_functional_olympiad",
    display_name={"th": "ฟังก์ชันเชิงเส้นในสมการ f(xy + 2x + 2y − 1)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class LinearShiftFunctional(WordProblem):
    def expr(self, rng: Random):
        c = rng.randint(1, 5)
        d = rng.randint(1, 6)
        n = rng.choice([v for v in range(-9, 10) if v not in (0, 1)])
        p, q = shift_solution(c)
        answer = p * n + q
        constant = c * c - d
        const_tex = "" if constant == 0 else (f"+{constant}" if constant > 0 else str(constant))
        wrong = [v for v in dict.fromkeys([n - c, n + c + 1, 2 * n + c, n + d, c * n + 1]) if v != answer]
        return MathDraw(
            rf"f\big(xy+{c + 1}x+{c + 1}y{const_tex}\big)=f(x)f(y)+f(y)+x-{d}",
            str(answer),
            prompt=f"f เป็นฟังก์ชันเชิงเส้นที่สอดคล้องสมการต่อไปนี้ทุกจำนวนจริง x, y จงหา f({n})",
            hint="แทน f(x) = px + q แล้วเทียบสัมประสิทธิ์ของ xy, x, y และค่าคงตัว",
            distractors=[str(v) for v in wrong],
        )
