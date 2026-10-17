"""Ordered k-tuples of sets with union {1, …, n}: (2^k − 1)^n."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 16",))


def cover_base(k: int) -> int:
    """Each element picks a non-empty subset of the k sets to lie in:
    2^k − 1 ways, independently (source: k = 3, n = 2549 → 7^2549)."""
    return 2**k - 1


@question_type(
    "math.set_union_cover_count_olympiad",
    display_name={"th": "จำนวนวิธีสร้างเซตที่ยูเนียนเป็นเซตที่กำหนด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class SetUnionCoverCount(WordProblem):
    def expr(self, rng: Random):
        k, n = rng.randint(2, 5), rng.randint(5, 3000)
        answer = f"{cover_base(k)}^{{{n}}}"
        wrong = [t for t in dict.fromkeys([f"{2**k}^{{{n}}}", f"{2**k - 2}^{{{n}}}" if k > 2 else f"{k + 1}^{{{n}}}", f"{k}^{{{n}}}", f"{cover_base(k)}^{{{n - 1}}}"]) if t != answer]
        names = ", ".join("ABCDE"[:k])
        cup = r"\cup ".join("ABCDE"[:k])
        return MathDraw(
            rf"{cup}=\{{1,2,3,\ldots,{n}\}}",
            answer,
            prompt=f"จงหาจำนวนวิธีทั้งหมดที่จะสร้างเซต {names} (เรียงลำดับ) ที่สอดคล้องเงื่อนไขต่อไปนี้",
            hint="สมาชิกแต่ละตัวเลือกได้ว่าจะอยู่ในเซตใดบ้าง โดยต้องอยู่อย่างน้อยหนึ่งเซต",
            distractors=wrong,
        )
