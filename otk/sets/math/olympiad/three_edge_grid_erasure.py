"""Classify square grids erasable three sides at a time."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 5",)
)


def erasable_grid_size(size: int) -> bool:
    """Exactly 2 and the positive sizes congruent to 3 or 5 modulo 6 work."""
    return size == 2 or (size >= 3 and size % 6 in (3, 5))


def count_erasable_sizes(limit: int) -> int:
    if limit < 1:
        raise ValueError("limit must be positive")
    return sum(erasable_grid_size(size) for size in range(1, limit + 1))


@question_type(
    "math.three_edge_grid_erasure_olympiad",
    display_name={"th": "ขนาดตารางที่ลบด้านทีละสามด้านได้หมด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class ThreeEdgeGridErasure(WordProblem):
    def expr(self, rng: Random):
        limit = rng.randint(12, 80)
        answer = count_erasable_sizes(limit)
        divisible_only = sum(
            size >= 2 and size * (size + 1) % 3 == 0
            for size in range(1, limit + 1)
        )
        odd_only = sum(size % 2 == 1 for size in range(1, limit + 1))
        one_residue = 1 + sum(size % 6 == 3 for size in range(3, limit + 1))
        other_residue = 1 + sum(size % 6 == 5 for size in range(3, limit + 1))
        return MathDraw(
            rf"1\leq n\leq {limit}",
            str(answer),
            prompt=(
                "ตาราง n×n มีด้านของช่องทุกด้านอยู่ครบ แต่ละครั้งเลือกช่องที่ยังมี"
                "ด้านอย่างน้อยสามด้าน แล้วลบด้านที่ยังอยู่ของช่องนั้นสามด้าน "
                "จงนับจำนวนค่า n ในช่วงที่กำหนดซึ่งสามารถลบทุกด้านจนหมดได้"
            ),
            hint=(
                "จำนวนด้านทั้งหมดต้องหารด้วย 3 ลงตัว "
                "และเมื่อจัดการวงแหวนช่องริมตารางแล้ว "
                "ช่องตามขอบของตารางด้านในต้องสลับเลือกกับไม่เลือก"
            ),
            distractors=[
                str(divisible_only),  # use only edge divisibility
                str(odd_only),  # use only parity
                str(one_residue),  # omit sizes 5 mod 6
                str(other_residue),  # omit sizes 3 mod 6
                str(answer - 1),  # omit the exceptional 2-by-2 grid
                str(answer + 1),  # include one impossible boundary size
            ],
        )
