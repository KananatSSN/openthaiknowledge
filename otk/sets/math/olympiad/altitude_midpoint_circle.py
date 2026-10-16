"""Circle through an altitude foot and a side midpoint meets another side."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def second_intersection_distance(base: int, opposite_midpoint: int, side: int) -> Fraction:
    """Return AE where AB=side, BC=base, CA=opposite_midpoint."""
    if min(base, opposite_midpoint, side) <= 0:
        raise ValueError("side lengths must be positive")
    if not abs(opposite_midpoint - side) < base < opposite_midpoint + side:
        raise ValueError("side lengths must form a triangle")
    foot = Fraction(side**2 + base**2 - opposite_midpoint**2, 2 * base)
    if foot <= 0 or foot >= base or foot == Fraction(base, 2):
        raise ValueError("altitude foot must be distinct from B, C, and midpoint")
    # A circle through D=(foot,0) and M=(base/2,0) has constant term
    # foot*base/2. Its intersections with AB, parametrized from B, have
    # one parameter 1 (A) and the other foot*base/(2*side**2).
    second_parameter = foot * base / (2 * side**2)
    if not 0 < second_parameter < 1:
        raise ValueError("second intersection is not inside AB")
    return side * (1 - second_parameter)


@lru_cache(maxsize=1)
def _candidate_triangles() -> tuple[tuple[int, int, int], ...]:
    candidates = []
    for base in range(5, 20):
        for opposite_midpoint in range(5, 20):
            for side in range(5, 20):
                try:
                    second_intersection_distance(base, opposite_midpoint, side)
                except ValueError:
                    continue
                candidates.append((base, opposite_midpoint, side))
    return tuple(candidates)


@question_type(
    "math.altitude_midpoint_circle_intersection_olympiad",
    display_name={"th": "วงกลมผ่านเท้าสูงและจุดกึ่งกลางตัดด้านสามเหลี่ยม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="วงกลม",
)
class AltitudeMidpointCircleIntersection(WordProblem):
    def expr(self, rng: Random):
        base, opposite_midpoint, side = rng.choice(_candidate_triangles())
        answer = second_intersection_distance(base, opposite_midpoint, side)
        foot = Fraction(side**2 + base**2 - opposite_midpoint**2, 2 * base)
        be = side - answer
        return MathDraw(
            rf"BC={base},\quad CA={opposite_midpoint},\quad AB={side}",
            str(answer),
            prompt=("ในสามเหลี่ยม ABC ให้ D เป็นเท้าของเส้นตั้งฉากจาก A ลงบน BC "
                    "และ M เป็นจุดกึ่งกลางของ BC วงกลมที่ผ่าน A, D, M "
                    "ตัดเส้น AB อีกครั้งที่ E จงหาความยาว AE"),
            hint=r"BD=\frac{AB^2+BC^2-CA^2}{2BC},\qquad BE\cdot BA=BD\cdot BM",
            distractors=[
                str(be),  # report BE instead of AE
                str(side - foot * base / side),  # use BC instead of BM
                str(side - base**2 / (4 * side)),  # substitute midpoint for altitude foot
                str(side - base**2 / (2 * side)),  # substitute C for the altitude foot
            ],
        )
