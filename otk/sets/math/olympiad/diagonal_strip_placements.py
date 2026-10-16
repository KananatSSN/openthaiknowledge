"""Count independent strip placements on opposite sides of a diagonal."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def strip_placements(size: int, length: int, *, above: bool, allow_touch: bool = False) -> tuple[tuple[int, int, int, int], ...]:
    """List (row, column, height, width) placements fully on one side."""
    if size < 3 or not 1 < length < size:
        raise ValueError("invalid grid size or strip length")
    result = []
    for row in range(size):
        for column in range(size):
            for height, width in ((1, length), (length, 1)):
                if row + height > size or column + width > size:
                    continue
                gap = column - (row + height) if above else row - (column + width)
                if gap > 0 or allow_touch and gap >= 0:
                    result.append((row, column, height, width))
    return tuple(result)


def no_parallel_overlap(first: tuple[int, int, int, int], second: tuple[int, int, int, int]) -> bool:
    """No horizontal or vertical line intersects both strip interiors."""
    row_a, col_a, height_a, width_a = first
    row_b, col_b, height_b, width_b = second
    separate_rows = row_a + height_a <= row_b or row_b + height_b <= row_a
    separate_cols = col_a + width_a <= col_b or col_b + width_b <= col_a
    return separate_rows and separate_cols


def placement_probability(size: int, length: int, *, allow_touch: bool = False) -> Fraction:
    upper = strip_placements(size, length, above=True, allow_touch=allow_touch)
    lower = strip_placements(size, length, above=False, allow_touch=allow_touch)
    if not upper or not lower:
        raise ValueError("no placements on one or both sides")
    favorable = sum(no_parallel_overlap(a, b) for a in upper for b in lower)
    return Fraction(favorable, len(upper) * len(lower))


def _tex_fraction(value: Fraction) -> str:
    return rf"\frac{{{value.numerator}}}{{{value.denominator}}}"


@question_type(
    "math.diagonal_strip_placements_olympiad",
    display_name={"th": "ความน่าจะเป็นของแถบบนสองฝั่งเส้นทแยงมุม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ความน่าจะเป็น",
)
class DiagonalStripPlacements(WordProblem):
    def expr(self, rng: Random):
        size = rng.randint(8, 11)
        length = rng.randint(2, min(4, size - 3))
        upper = strip_placements(size, length, above=True)
        lower = strip_placements(size, length, above=False)
        favorable = sum(no_parallel_overlap(a, b) for a in upper for b in lower)
        total = len(upper) * len(lower)
        answer = Fraction(favorable, total)
        horizontal_only = Fraction(
            sum(a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] for a in upper for b in lower), total,
        )
        touching_upper = strip_placements(size, length, above=True, allow_touch=True)
        touching_lower = strip_placements(size, length, above=False, allow_touch=True)
        return MathDraw(
            rf"n={size},\quad \ell={length}",
            _tex_fraction(answer),
            prompt=("แบ่งตาราง n คูณ n ช่องด้วยเส้นทแยงมุมจากมุมซ้ายบนไปขวาล่าง วางแถบขนาด 1 คูณ ℓ ช่อง "
                    "หนึ่งแถบในแต่ละฝั่ง โดยแถบต้องอยู่บนช่องตารางทั้งหมดและห้ามสัมผัสเส้นทแยงมุม "
                    "ทุกวิธีวางในแต่ละฝั่งมีโอกาสเท่ากัน ความน่าจะเป็นที่ไม่มีเส้นแนวนอนและแนวตั้งเส้นใด "
                    "ตัดผ่านภายในแถบทั้งสองพร้อมกันเป็นเท่าใด"),
            hint="แจกแจงตำแหน่งตามมุมซ้ายบนและแนววาง แล้วเปรียบเทียบช่วงพิกัด x และ y ของสองแถบ",
            distractors=[
                _tex_fraction(horizontal_only),  # test only row projections
                _tex_fraction(placement_probability(size, length, allow_touch=True)),  # include diagonal-touching bars
                _tex_fraction(Fraction(total - favorable, total)),  # count overlapping pairs
                _tex_fraction(Fraction(favorable, len(touching_upper) * len(touching_lower))),  # wrong denominator
            ],
        )
