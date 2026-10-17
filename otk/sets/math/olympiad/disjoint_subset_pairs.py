"""Unordered pairs of disjoint non-empty subsets of an n-set: (3ⁿ − 2ⁿ⁺¹ + 1)/2."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 13",))


def disjoint_pairs(n: int) -> int:
    """Each element goes to A, B or neither (3ⁿ); remove A = ∅ or B = ∅
    (2·2ⁿ − 1) and halve for order (source: n = 8 gives 3025)."""
    return (3 ** n - 2 ** (n + 1) + 1) // 2


@question_type(
    "math.disjoint_subset_pairs_olympiad",
    display_name={"th": "จำนวนคู่เซตย่อยไม่ว่างที่ไม่มีสมาชิกร่วมกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เพาเวอร์เซตและการนับสับเซต",
)
class DisjointSubsetPairs(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(3, 12)
        answer = disjoint_pairs(n)
        wrong = [v for v in dict.fromkeys([3 ** n - 2 ** (n + 1) + 1, (3 ** n + 1) // 2, (3 ** n - 2 ** n) // 2, (3 ** n - 2 ** (n + 1)) // 2 + 2 ** n, 3 ** n // 2]) if v != answer]
        return MathDraw(
            rf"S=\{{1,2,\ldots,{n}\}}",
            str(answer),
            prompt="จงหาจำนวนวิธีเลือกเซตย่อยที่ไม่ใช่เซตว่างสองเซตของ S ซึ่งไม่มีสมาชิกร่วมกัน (ไม่สนใจลำดับของสองเซต)",
            hint="สมาชิกแต่ละตัวอยู่ใน A, ใน B หรือไม่อยู่ในทั้งสอง ตัดกรณีเซตว่างออกแล้วหารด้วย 2",
            distractors=[str(v) for v in wrong],
        )
