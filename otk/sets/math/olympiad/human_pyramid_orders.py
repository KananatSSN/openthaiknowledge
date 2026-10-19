"""Weight orders for a human pyramid are the linear extensions of its triangular poset."""

from __future__ import annotations

from math import factorial, prod
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 17",))


SHAPES = ((1, 2), (1, 3), (1, 4), (2, 2), (2, 3), (3, 2), (3, 3), (4, 2))


def pyramid(top: int, rows: int) -> tuple[int, list[tuple[int, int]]]:
    """Row i has top + i people; person j of row i stands on persons j and
    j + 1 of row i + 1. Returns the size and the (above, below) pairs."""
    index, starts = 0, []
    for i in range(rows):
        starts.append(index)
        index += top + i
    pairs = [(starts[i] + j, starts[i + 1] + j + d) for i in range(rows - 1) for j in range(top + i) for d in (0, 1)]
    return index, pairs


def orders(size: int, pairs: list[tuple[int, int]]) -> int:
    """Linear extensions by a DP over the set already placed, lightest first:
    a person may be placed once everyone above them is placed
    (source: top 1, three rows → 16)."""
    need = [0] * size
    for upper, lower in pairs:
        need[lower] |= 1 << upper
    ways = [0] * (1 << size)
    ways[0] = 1
    for mask in range(1 << size):
        if ways[mask]:
            for v in range(size):
                if not mask >> v & 1 and need[v] & mask == need[v]:
                    ways[mask | 1 << v] += ways[mask]
    return ways[-1]


@question_type(
    "math.human_pyramid_orders_olympiad",
    display_name={"th": "จำนวนวิธีต่อตัวเมื่อคนเบากว่าต้องอยู่ข้างบน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class HumanPyramidOrders(WordProblem):
    def expr(self, rng: Random):
        top, rows = rng.choice(SHAPES)
        size, pairs = pyramid(top, rows)
        answer = orders(size, pairs)
        row_sizes = [top + i for i in range(rows)]
        by_rows = prod(factorial(r) for r in row_sizes)
        lower_only = orders(size, [pq for pq in pairs if pq[0] >= top])
        wrong = [v for v in dict.fromkeys([factorial(size), by_rows, factorial(size) // by_rows, lower_only, answer * 2]) if v != answer]
        shape = " + ".join(map(str, row_sizes))
        return MathDraw(
            rf"{shape}={size}",
            str(answer),
            prompt=f"มีคน {size} คนที่มีน้ำหนักแตกต่างกันหมด ต่อตัวเป็นรูปสามเหลี่ยม {rows} ชั้น ชั้นบนสุดมี {top} คน แต่ละชั้นถัดลงมามีมากกว่าชั้นบนหนึ่งคน และแต่ละคนยืนบนสองคนที่อยู่ใต้ตนพอดี โดยคนที่หนักกว่าห้ามอยู่เหนือคนที่เบากว่า จะต่อตัวได้กี่วิธี",
            hint="เรียงคนจากเบาไปหนัก คนหนึ่งจะวางได้เมื่อคนที่ยืนบนเขาถูกวางไปแล้วทั้งหมด นับแบบแยกกรณีทีละขั้น",
            distractors=[str(v) for v in wrong],
        )
