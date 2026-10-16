"""Pigeonhole bounds obtained by partitioning a grid into small blocks."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def block_upper_bound(rows: int, columns: int) -> int:
    """Bound active cells when every disjoint 2-by-2 block holds at most one.

    With no edge-adjacent active cells, two active cells in one block would
    occupy opposite corners. Either diagonal pair sends two signals to a
    third cell in that block (left/right from one, upward from the other).
    Hence the no-double-signal rule permits at most one active cell per block.
    """
    if rows % 2 or columns % 2:
        raise ValueError("both grid dimensions must be even")
    return (rows // 2) * (columns // 2)


@question_type(
    "math.grid_block_pigeonhole_olympiad",
    display_name={"th": "ขอบเขตจากบล็อก 2×2"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class GridBlockPigeonhole(WordProblem):
    def expr(self, rng: Random):
        block_rows = rng.randint(3, 12)
        block_columns = rng.randint(3, 12)
        rows, columns = 2 * block_rows, 2 * block_columns
        answer = block_upper_bound(rows, columns)
        return MathDraw(
            rf"{rows}\times{columns}",
            str(answer),
            prompt=("บนตารางขนาดที่กำหนด จุดเปิดใช้งานส่งสัญญาณไปยังช่องซ้าย "
                    "ขวา และช่องเหนือขึ้นไปหนึ่งช่อง ไม่มีจุดเปิดใช้งานสองจุด"
                    "ที่ติดกันในแนวนอนหรือแนวตั้ง และทุกช่องรับสัญญาณจาก"
                    "ไม่เกินหนึ่งจุด จงหาขอบเขตบนของจำนวนจุดเปิดใช้งาน"
                    "ที่พิสูจน์ได้โดยแบ่งตารางเป็นบล็อก 2×2 ไม่ซ้อนกัน"),
            hint=(r"\text{สองจุดในบล็อกเดียวกันต้องอยู่คนละมุมทแยง "
                  r"และจะส่งสัญญาณถึงช่องเดียวกัน}"),
            distractors=[
                str(2 * answer),  # allow two active cells per block
                str(4 * answer),  # ignore every restriction
                str(answer + 1),  # confuse upper bound with first impossible count
                str((block_rows + 1) * (block_columns + 1)),  # overlap blocks
            ],
        )
