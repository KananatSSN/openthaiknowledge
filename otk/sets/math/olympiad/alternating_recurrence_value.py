"""f(n) = 2f(n − 1) − f(n − 2) + (−1)ⁿ(2n − 4): the second difference alternates, so f splits by parity."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 7",))


def term(n: int, f0: int, f1: int) -> int:
    """Iterate the recurrence (source: f(0) = 0, f(1) = 1 gives f(n) = n for
    even n and 1 for odd n)."""
    a, b = f0, f1
    if n == 0:
        return a
    for k in range(2, n + 1):
        a, b = b, 2 * b - a + (-1) ** k * (2 * k - 4)
    return b


@question_type(
    "math.alternating_recurrence_value_olympiad",
    display_name={"th": "ค่าของลำดับเวียนเกิดที่มีพจน์สลับเครื่องหมาย"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ฟังก์ชันเวียนเกิด",
)
class AlternatingRecurrenceValue(WordProblem):
    def expr(self, rng: Random):
        f0, f1 = rng.randint(-5, 5), rng.randint(-5, 5)
        n = rng.randint(10, 400)
        answer = term(n, f0, f1)
        wrong = [v for v in dict.fromkeys([term(n + 1, f0, f1), term(n - 1, f0, f1), f0 + n * (f1 - f0), -answer if answer else 1, term(n, 0, 1) if (f0, f1) != (0, 1) else n + 1]) if v != answer]
        return MathDraw(
            rf"f(0)={f0},\ f(1)={f1},\quad f(n)=2f(n-1)-f(n-2)+(-1)^n(2n-4)",
            str(answer),
            prompt=f"ลำดับ f สอดคล้องความสัมพันธ์ต่อไปนี้สำหรับทุกจำนวนเต็ม n ≥ 2 จงหา f({n})",
            hint="ให้ g(n) = f(n) − f(n − 1) จะได้ g(n) − g(n − 1) = (−1)ⁿ(2n − 4) แยกคิด n คู่และคี่",
            distractors=[str(v) for v in wrong],
        )
