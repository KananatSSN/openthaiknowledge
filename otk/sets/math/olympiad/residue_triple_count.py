"""Three numbers from {1, …, 3n} with sum ≡ r (mod 3), counted by residue classes."""

from __future__ import annotations

from itertools import combinations_with_replacement
from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 10",))


def triple_count(n: int, r: int) -> int:
    """Each residue class has n members. Sum over multisets of residues
    (i ≤ j ≤ k) with i + j + k ≡ r, choosing within classes
    (source: r = 0 gives 3C(n, 3) + n³)."""
    total = 0
    for i, j, k in combinations_with_replacement(range(3), 3):
        if (i + j + k) % 3 == r:
            counts = {c: (i, j, k).count(c) for c in set((i, j, k))}
            ways = 1
            for c in counts.values():
                ways *= comb(n, c)
            total += ways
    return total


@question_type(
    "math.residue_triple_count_olympiad",
    display_name={"th": "จำนวนวิธีเลือกสามจำนวนที่ผลบวกหารด้วย 3 ตามเงื่อนไข"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class ResidueTripleCount(WordProblem):
    def expr(self, rng: Random):
        n, r = rng.randint(3, 400), rng.choice([0, 0, 1, 2])
        answer = triple_count(n, r)
        wrong = [v for v in dict.fromkeys([comb(3 * n, 3) // 3, 3 * comb(n, 3), n**3, 3 * comb(n, 3) + n**3 if r else comb(3 * n, 3) - answer, answer + n]) if v != answer]
        rest = "หารด้วย 3 ลงตัว" if r == 0 else f"หารด้วย 3 เหลือเศษ {r}"
        return MathDraw(
            rf"\{{1,2,3,\ldots,{3 * n}\}}",
            str(answer),
            prompt=f"จงหาจำนวนวิธีเลือกจำนวนสามจำนวนที่แตกต่างกันจากเซตต่อไปนี้ โดยผลบวกของสามจำนวนนั้น{rest}",
            hint="แบ่งเซตตามเศษจากการหารด้วย 3 ได้สามกลุ่ม กลุ่มละ n ตัว แล้วแยกกรณีตามเศษของสามจำนวน",
            distractors=[str(v) for v in wrong],
        )
