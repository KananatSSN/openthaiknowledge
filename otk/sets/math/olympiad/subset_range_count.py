"""Subsets of {1, …, n} whose largest minus smallest is k: (n − k)·2^{k−1}."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 2",))


def range_count(n: int, k: int) -> int:
    """n − k choices of the smallest element m; the k − 1 numbers strictly
    between m and m + k are free."""
    return (n - k) * 2 ** (k - 1)


@question_type(
    "math.subset_range_count_olympiad",
    display_name={"th": "จำนวนเซตย่อยที่ผลต่างค่ามากสุดกับน้อยสุดคงที่"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class SubsetRangeCount(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(6, 20)
        k = rng.randint(2, n - 1)
        answer = range_count(n, k)
        wrong = [v for v in dict.fromkeys([(n - k) * 2**k, (n - k + 1) * 2 ** (k - 1), (n - k) * 2 ** (k - 2), 2 ** (k - 1), (n - k - 1) * 2 ** (k - 1)]) if v != answer and v > 0]
        return MathDraw(
            rf"n={n},\quad k={k}",
            str(answer),
            prompt="จงหาจำนวนเซตย่อยของ {1, 2, …, n} ที่ผลต่างระหว่างสมาชิกค่ามากสุดกับค่าน้อยสุดเท่ากับ k",
            hint="เลือกค่าน้อยสุด m แล้วค่ามากสุดคือ m + k และสมาชิกระหว่างกลางเลือกได้อิสระ",
            distractors=[str(v) for v in wrong],
        )
