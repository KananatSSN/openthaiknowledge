"""Σ_k C(k, a)C(n − k, b) = C(n + 1, a + b + 1)."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 14",))


def binomial_sum(n: int, a: int, b: int) -> tuple[int, int]:
    """Choose a + b + 1 numbers from {0, …, n}; the (a + 1)-th smallest is k,
    with C(k, a) choices below and C(n − k, b) above. Returns (top, bottom) of
    C(n + 1, a + b + 1) (source: n = 8084, a = b = 84 gives C(8085, 169))."""
    return n + 1, a + b + 1


def binom_tex(top: int, bottom: int) -> str:
    return rf"\binom{{{top}}}{{{bottom}}}"


@question_type(
    "math.vandermonde_shifted_sum_olympiad",
    display_name={"th": "ผลบวกผลคูณสัมประสิทธิ์ทวินามแบบเลื่อน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การนับเชิงการจัด",
)
class VandermondeShiftedSum(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(2, 99), rng.randint(2, 99)
        n = rng.randint(a + b + 20, 9000)
        top, bottom = binomial_sum(n, a, b)
        answer = binom_tex(top, bottom)
        wrong = [t for t in dict.fromkeys([binom_tex(n, a + b), binom_tex(n + 1, a + b), binom_tex(n, a + b + 1), binom_tex(n + 1, a + b + 2), binom_tex(n + 2, a + b + 1)]) if t != answer]
        return MathDraw(
            rf"\sum_{{k={a}}}^{{{n - b}}}\binom{{k}}{{{a}}}\binom{{{n}-k}}{{{b}}}",
            answer,
            prompt="จงหาค่าของผลบวกต่อไปนี้ในรูปสัมประสิทธิ์ทวินามตัวเดียว",
            hint="นับการเลือกจำนวน a + b + 1 ตัวจาก {0, 1, …, n} โดยแยกกรณีตามตัวที่ a + 1 จากน้อยไปมาก",
            distractors=wrong,
        )
