"""Count binary grids with odd parity in every row and column."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 6",)
)


def count_odd_row_column_grids(rows: int, columns: int) -> int:
    """Number of two-color grids having odd first-color count in every line."""
    if rows < 1 or columns < 1:
        raise ValueError("grid dimensions must be positive")
    if (rows - columns) % 2:
        return 0
    return 1 << ((rows - 1) * (columns - 1))


@question_type(
    "math.odd_row_column_grids_olympiad",
    display_name={"th": "ระบายสีตารางให้ทุกแถวและหลักมีจำนวนคี่"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class OddRowColumnGrids(WordProblem):
    def expr(self, rng: Random):
        rows = rng.randint(3, 9)
        columns = rng.choice(tuple(n for n in range(3, 10) if n % 2 == rows % 2))
        exponent = (rows - 1) * (columns - 1)
        answer = count_odd_row_column_grids(rows, columns)
        assert answer == 1 << exponent

        def power(value: int) -> str:
            return rf"2^{{{value}}}"

        return MathDraw(
            rf"{rows}\times {columns}",
            power(exponent),
            prompt=(
                "ระบายแต่ละช่องในตารางเป็นสีน้ำเงินหรือสีเหลือง "
                "โดยทุกแถวและทุกหลักต้องมีช่องสีน้ำเงินเป็นจำนวนคี่ "
                "มีวิธีระบายสีทั้งหมดกี่วิธี"
            ),
            hint=(
                "เลือกสีในช่องที่ไม่อยู่แถวสุดท้ายหรือหลักสุดท้ายก่อน "
                "แล้วใช้เงื่อนไขจำนวนคี่กำหนดช่องที่เหลือ"
            ),
            distractors=[
                power(exponent + 1),  # treat the bottom-right cell as free
                power(exponent - 1),  # impose the last condition twice
                power((rows - 1) * columns),  # overlook column parity
                power(rows * (columns - 1)),  # overlook row parity
                power(rows * columns),  # treat every cell as free
            ],
        )
