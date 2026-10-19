"""Bubble sort uses exactly as many adjacent swaps as there are inversions; count permutations with M − k inversions."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันที่สอง ข้อ 3",))


def inversion_counts(n: int) -> list[int]:
    """Mahonian numbers: inserting the i-th tallest adds 0..i − 1 inversions."""
    counts = [1]
    for i in range(1, n + 1):
        new = [0] * (len(counts) + i - 1)
        for k, v in enumerate(counts):
            for j in range(i):
                new[k + j] += v
        counts = new
    return counts


def orders_with_swaps(n: int, swaps: int) -> int:
    """Each adjacent swap of a wrongly ordered pair removes one inversion, so
    the swaps equal the inversions (source: n = 18, 150 = 153 − 3 → 951)."""
    return inversion_counts(n)[swaps]


@question_type(
    "math.inversion_count_orders_olympiad",
    display_name={"th": "จำนวนการเข้าแถวที่ต้องสลับตำแหน่งตามจำนวนครั้งที่กำหนด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class InversionCountOrders(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(5, 20)
        top = n * (n - 1) // 2
        k = rng.randint(1, 5)
        swaps = top - k
        answer = orders_with_swaps(n, swaps)
        counts = inversion_counts(n)
        wrong = [v for v in dict.fromkeys([comb(n - 1 + k, k), counts[k - 1] if k > 1 else n, counts[k + 1], comb(n, k), comb(top, k) if comb(top, k) < 10**7 else counts[k] + n]) if v != answer]
        return MathDraw(
            rf"n={n},\quad \text{{swaps}}={swaps}",
            str(answer),
            prompt=f"นักเรียน {n} คนที่สูงต่างกันทั้งหมดยืนเข้าแถวตอน ครูเดินตรวจแถว ถ้าพบนักเรียนที่ยืนติดกันเรียงลำดับความสูงไม่ถูกต้องจะสลับตำแหน่งคู่นั้น จนเรียงจากเตี้ยไปสูงทั้งหมด ถ้าครูต้องสลับทั้งหมด {swaps} ครั้งและสลับน้อยกว่านี้ไม่ได้ นักเรียนเข้าแถวได้แตกต่างกันกี่วิธี",
            hint=f"จำนวนครั้งที่สลับเท่ากับจำนวนคู่ที่เรียงผิด (inversion) ซึ่งมากสุด {top} นับการเรียงที่มี inversion {swaps} คู่ ซึ่งเท่ากับจำนวนที่มี {k} คู่",
            distractors=[str(v) for v in wrong],
        )
