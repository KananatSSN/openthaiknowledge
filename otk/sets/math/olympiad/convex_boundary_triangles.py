"""Count triangles formed by marked points on a convex polygon boundary."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def count_boundary_triangles(sides: int, marks_per_side: int) -> int:
    """Count noncollinear triples among equal numbers of interior edge marks.

    A line intersects the boundary of a convex polygon in at most two points
    unless it contains an edge. Thus the only collinear triples have all
    three marks on the same edge. Marks exclude polygon vertices, so the
    bad triples from different edges are disjoint.
    """
    if sides < 3 or marks_per_side < 1:
        raise ValueError("expected at least three sides and one mark per side")
    return comb(sides * marks_per_side, 3) - sides * comb(marks_per_side, 3)


@question_type(
    "math.convex_boundary_triangles_olympiad",
    display_name={"th": "นับสามเหลี่ยมจากจุดบนด้านรูปหลายเหลี่ยม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class ConvexBoundaryTriangles(WordProblem):
    def expr(self, rng: Random):
        sides = rng.randint(3, 8)
        marks = rng.randint(4, 10)
        answer = count_boundary_triangles(sides, marks)
        all_triples = comb(sides * marks, 3)
        return MathDraw(
            rf"k={sides},\quad m={marks}",
            str(answer),
            prompt=("รูปหลายเหลี่ยมนูนที่ไม่มีมุมตรงมีจำนวนด้าน k "
                    "ทำเครื่องหมายจุดภายในแต่ละด้าน m จุด โดยไม่ทำเครื่องหมายที่จุดยอด "
                    "มีสามเหลี่ยมกี่รูปที่เลือกจุดยอดทั้งสามจากจุดที่ทำเครื่องหมาย"),
            hint=r"\binom{km}{3}-k\binom{m}{3}",
            distractors=[
                str(all_triples),  # include triples on an edge
                str(all_triples - comb(marks, 3)),  # subtract only one edge
                str(all_triples - sides * comb(marks - 1, 3)),  # miss one mark per edge
                str(all_triples - sides * comb(marks + 1, 3)),  # count a vertex as a mark
            ],
        )
