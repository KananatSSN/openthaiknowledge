"""Alternating sums over all non-empty subsets of {1, …, n} total n·2^(n − 1)."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 8",))


def alternating_total(n: int) -> int:
    """Pair each subset T without n with T ∪ {n}: their results add to n, and
    there are 2^(n − 1) pairs ({n} pairs with ∅) (source: n = 7 → 448)."""
    return n * 2 ** (n - 1)


@question_type(
    "math.alternating_subset_sum_olympiad",
    display_name={"th": "ผลบวกของผลลัพธ์สลับเครื่องหมายของทุกสับเซต"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เพาเวอร์เซตและการนับสับเซต",
)
class AlternatingSubsetSum(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(3, 14)
        answer = alternating_total(n)
        wrong = [v for v in dict.fromkeys([n * (n + 1) // 2 * 2 ** (n - 1), n * 2**n, 2 ** (n - 1), (n + 1) * 2 ** (n - 2), n * 2 ** (n - 1) - n]) if v != answer]
        return MathDraw(
            rf"S=\{{1,2,3,\ldots,{n}\}}",
            str(answer),
            prompt="จัดเรียงสมาชิกในแต่ละสับเซตที่ไม่ใช่เซตว่างของ S จากมากไปน้อย ใส่เครื่องหมายบวกและลบสลับกัน เริ่มด้วยบวกที่จำนวนมากสุด แล้วหาผลบวก (เช่น {7, 4, 2} ได้ 7 − 4 + 2 = 5) จงหาผลบวกของผลลัพธ์ของทุกสับเซต",
            hint="จับคู่สับเซต T ที่ไม่มี n กับ T ∪ {n} ผลลัพธ์ของคู่นี้รวมกันได้ n เสมอ",
            distractors=[str(v) for v in wrong],
        )
