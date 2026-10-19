"""Most cells in an r × c grid with no 2 × 2 combinatorial rectangle (Zarankiewicz)."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันที่สอง ข้อ 5",))


def rectangle_free_maximum(rows: int, cols: int) -> int:
    """Each column picks a set of rows; two columns may share at most one row
    (a shared pair of rows makes a rectangle), so every pair of rows is used
    by at most one column. The source applies this to 5 days × 16 books."""
    subsets = [tuple(s) for size in range(rows + 1) for s in combinations(range(rows), size)]

    @lru_cache(maxsize=None)
    def best(col: int, used: frozenset) -> int:
        if col == cols:
            return 0
        top = 0
        for s in subsets:
            pairs = frozenset(combinations(s, 2))
            if pairs & used:
                continue
            top = max(top, len(s) + best(col + 1, used | pairs))
        return top

    return best(0, frozenset())


TABLE = {(r, c): rectangle_free_maximum(r, c) for r in range(2, 5) for c in range(2, 7)}


@question_type(
    "math.rectangle_free_grid_olympiad",
    display_name={"th": "จำนวนช่องมากสุดในตารางที่ไม่มีสี่เหลี่ยม 2 × 2"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class RectangleFreeGrid(WordProblem):
    def expr(self, rng: Random):
        rows, cols = rng.choice(tuple(TABLE))
        answer = TABLE[(rows, cols)]
        wrong = [v for v in dict.fromkeys([answer + 1, answer - 1, rows + cols, rows * cols - 1, answer + 2]) if v != answer and v > 0]
        return MathDraw(
            rf"{rows}\times{cols}",
            str(answer),
            prompt=(
                "เลือกช่องในตารางขนาดดังกล่าว (แถว × หลัก) โดยไม่มีสองแถวและสองหลักที่ช่องตรงกันทั้งสี่ถูกเลือกหมด "
                "เลือกได้มากที่สุดกี่ช่อง"
            ),
            hint="แต่ละหลักเลือกเซตของแถว และคู่แถวใด ๆ ใช้ได้ในหลักเดียวเท่านั้น",
            distractors=[str(v) for v in wrong],
        )
