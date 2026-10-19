"""n + 1 is coprime to n(n + 2) = (n + 1)² − 1, so n(n + 1)(n + 2) is never a square; its squarefree part measures how far."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันที่สอง ข้อ 1",))


def squarefree_part(n: int) -> int:
    out, f = 1, 2
    while f * f <= n:
        while n % (f * f) == 0:
            n //= f * f
        if n % f == 0:
            out *= f
            n //= f
        f += 1
    return out * n


def square_multiplier(n: int) -> int:
    """The least m with m·n(n + 1)(n + 2) a square is the squarefree part. It
    is never 1: n + 1 and n(n + 2) are coprime, so both would be squares, but
    n(n + 2) = (n + 1)² − 1 lies strictly between n² and (n + 1)²."""
    return squarefree_part(n * (n + 1) * (n + 2))


@question_type(
    "math.consecutive_product_square_kernel_olympiad",
    display_name={"th": "ตัวคูณน้อยสุดที่ทำให้ผลคูณจำนวนเรียงกันเป็นกำลังสอง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ตัวประกอบของจำนวนเต็ม",
)
class ConsecutiveProductSquareKernel(WordProblem):
    def expr(self, rng: Random):
        while True:
            n = rng.randint(2, 400)
            answer = square_multiplier(n)
            if answer < 10**6:
                break
        naive = squarefree_part(n) * squarefree_part(n + 1) * squarefree_part(n + 2)
        wrong = [v for v in dict.fromkeys([naive, squarefree_part(n * (n + 2)), squarefree_part(n + 1), squarefree_part(n) * squarefree_part(n + 2), 2 * answer]) if v != answer]
        return MathDraw(
            rf"m\cdot {n}\cdot {n + 1}\cdot {n + 2}",
            str(answer),
            prompt="จงหาจำนวนนับ m ที่น้อยที่สุดที่ทำให้จำนวนต่อไปนี้เป็นกำลังสองสมบูรณ์ (ผลคูณของจำนวนนับสามจำนวนเรียงกันไม่เป็นกำลังสองสมบูรณ์ จึงได้ m > 1 เสมอ)",
            hint="แยกตัวประกอบทั้งสามจำนวน รวมเลขชี้กำลังของจำนวนเฉพาะแต่ละตัว แล้วคูณจำนวนเฉพาะที่มีเลขชี้กำลังคี่",
            distractors=[str(v) for v in wrong],
        )
