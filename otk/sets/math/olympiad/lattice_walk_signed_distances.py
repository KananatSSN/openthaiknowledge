"""Signed distances recorded along a lattice walk telescope to Δ(xy)."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2557, ข้อ 3",)
)


def recorded_sum(start: tuple[int, int], end: tuple[int, int]) -> int:
    """A horizontal step records ±y = Δ(xy), a vertical one ±x = Δ(xy)."""
    return end[0] * end[1] - start[0] * start[1]


@question_type(
    "math.lattice_walk_signed_distances_olympiad",
    display_name={"th": "ผลรวมระยะที่บันทึกตามทางเดินบนจุดแลตทิซ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดรูปพีชคณิต",
)
class LatticeWalkSignedDistances(WordProblem):
    def expr(self, rng: Random):
        start = (rng.randint(0, 9), rng.randint(0, 9))
        end = (rng.randint(0, 12), rng.randint(0, 12))
        while end == start:
            end = (rng.randint(0, 12), rng.randint(0, 12))
        answer = recorded_sum(start, end)
        wrong = []
        for value in (
            -answer,  # signs reversed
            (end[0] + end[1]) - (start[0] + start[1]),  # count steps, not distances
            end[0] * end[1],  # forget the start
            end[0] * end[1] + start[0] * start[1],
            0,  # the source walk's value, from axis to axis
            answer + 1,
            answer - 1,
        ):
            if value != answer and value not in wrong:
                wrong.append(value)
        return MathDraw(
            rf"({start[0]},{start[1]})\ \to\ ({end[0]},{end[1]})",
            str(answer),
            prompt=(
                "เดินทีละ 1 หน่วยขนานแกน X หรือแกน Y อยู่ในจตุภาคที่หนึ่ง (x, y ≥ 0) "
                "ทุกก้าววัดระยะจากตัวถึงแกนที่เดินขนาน บันทึกเป็นบวกถ้าก้าวนั้นพาออกห่างจุดกำเนิด "
                "และเป็นลบถ้าพาเข้าใกล้ จากจุดเริ่มถึงจุดสิ้นสุดต่อไปนี้ ผลรวมที่บันทึกคือเท่าใด (ทางเดินใดก็ได้)"
            ),
            hint="ก้าวในแนวนอนบันทึก ±y ซึ่งเท่ากับการเปลี่ยนแปลงของ xy พอดี ก้าวในแนวตั้งก็เช่นกัน",
            distractors=[str(value) for value in wrong],
        )
