"""Chains A₁ ⊆ A₂ ⊆ ⋯ ⊆ A_k ⊆ {1, …, n}: (k + 1)ⁿ."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 9",))


def chain_count(n: int, k: int) -> int:
    """Each element picks the first set it joins, or none: k + 1 choices."""
    return (k + 1) ** n


@question_type(
    "math.nested_subset_chain_count_olympiad",
    display_name={"th": "จำนวนลำดับเซตย่อยซ้อนกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class NestedSubsetChainCount(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(3, 12)
        k = rng.randint(2, 4)
        answer = chain_count(n, k)
        wrong = [v for v in dict.fromkeys([k**n, 2 ** (k * n), (k + 2) ** n, (k + 1) ** (n - 1), 2**n * k]) if v != answer]
        chain = r"\subseteq ".join(f"A_{{{i}}}" for i in range(1, k + 1))
        return MathDraw(
            rf"{chain}\subseteq\{{1,2,\ldots,{n}\}}",
            str(answer),
            prompt="จงหาจำนวนลำดับของเซต (A₁, …, A_k) ที่สอดคล้องเงื่อนไขต่อไปนี้",
            hint="พิจารณาแต่ละสมาชิกแยกกัน: เลือกว่าเข้าเซตแรกที่ตำแหน่งใด หรือไม่เข้าเลย",
            distractors=[str(v) for v in wrong],
        )
