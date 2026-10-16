"""Minimum marked cells under a missing-cell degree-product condition."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def minimum_purple_cells(blocks: int, rows_per_block: int, columns_per_block: int) -> int:
    """A block construction attains the low-degree-row lower bound."""
    if blocks < rows_per_block + 1 or rows_per_block < 1 or columns_per_block < 2:
        raise ValueError("require blocks >= rows per block + 1 and positive block sizes")
    return blocks * rows_per_block * columns_per_block


@question_type(
    "math.purple_grid_threshold_olympiad",
    display_name={"th": "จำนวนช่องสีม่วงน้อยที่สุดในตาราง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class PurpleGridThreshold(WordProblem):
    def expr(self, rng: Random):
        rows_per_block = rng.randint(2, 7)
        columns_per_block = rng.randint(rows_per_block + 1, rows_per_block + 9)
        blocks = rng.randint(rows_per_block + 1, rows_per_block + 4)
        rows = blocks * rows_per_block
        columns = blocks * columns_per_block
        threshold = rows_per_block * columns_per_block
        answer = minimum_purple_cells(blocks, rows_per_block, columns_per_block)
        return MathDraw(
            rf"R={rows},\quad C={columns},\quad T={threshold}",
            str(answer),
            prompt=(
                "ตาราง R แถว C หลักมีช่องสีม่วงหรือสีเหลือง ทุกช่องสีเหลืองมี "
                "(จำนวนช่องสีม่วงในแถวเดียวกัน) × (จำนวนช่องสีม่วงในหลักเดียวกัน) ≥ T "
                "จงหาจำนวนช่องสีม่วงน้อยที่สุด"
            ),
            hint="ดูแถวที่มีช่องสีม่วงน้อยที่สุด แล้วสร้างตารางเป็นบล็อกสี่เหลี่ยมเต็ม",
            distractors=[
                str(rows * rows_per_block),  # swap the row degree with block height
                str(columns * columns_per_block),  # swap the column degree with block width
                str(answer - 1),  # miss the sharp integer lower bound
                str(answer + threshold),  # count one extra purple block
            ],
        )
