"""f(m² + n²) = (f(m) − f(n))² + f(2mn) forces f(1) − f(0) ∈ {0, 1}."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 5",))


def seed_value(alpha: int, beta: int, total: int) -> int | None:
    """m = 1, n = 0 gives f(1) − f(0) = (f(1) − f(0))², so f(1) = f(0) + d with
    d ∈ {0, 1}; then (α + β)f(0) + βd = N (source: 8, 9, 2006 → 118)."""
    found = [(total - beta * d) // (alpha + beta) for d in (0, 1) if (total - beta * d) % (alpha + beta) == 0 and total - beta * d >= 0]
    return found[0] if len(found) == 1 else None


@question_type(
    "math.sum_of_squares_functional_seed_olympiad",
    display_name={"th": "หา f(0) จากสมการเชิงฟังก์ชันบนจำนวนเต็มไม่ลบ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class SumOfSquaresFunctionalSeed(WordProblem):
    def expr(self, rng: Random):
        while True:
            alpha, beta = rng.randint(2, 12), rng.randint(2, 12)
            a, d = rng.randint(20, 300), rng.randint(0, 1)
            total = alpha * a + beta * (a + d)
            if seed_value(alpha, beta, total) == a:
                break
        wrong = [v for v in dict.fromkeys([a + d if d else a + 1, total // (alpha + beta) + (1 if d == 0 else -1), total // alpha, a - 1, total // beta]) if v != a]
        return MathDraw(
            rf"f(m^2+n^2)=\big(f(m)-f(n)\big)^2+f(2mn),\quad {alpha}f(0)+{beta}f(1)={total}",
            str(a),
            prompt="f : ℕ ∪ {0} → ℕ ∪ {0} สอดคล้องสมการต่อไปนี้สำหรับทุก m, n ∈ ℕ ∪ {0} จงหาค่าของ f(0)",
            hint="แทน m = 1, n = 0 จะได้ f(1) − f(0) = (f(1) − f(0))² จึง f(1) − f(0) เป็น 0 หรือ 1",
            distractors=[str(v) for v in wrong],
        )
