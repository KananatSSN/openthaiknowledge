"""Cover a square grid with several monotone corner-to-corner routes."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 9",)
)


def minimum_unvisited_squares(size: int, vehicles: int) -> int:
    """Each northeast diagonal can be visited at most once per route."""
    if size < 2 or not 1 <= vehicles < size:
        raise ValueError("expected a square grid with 1 <= vehicles < size")
    return (size - vehicles) ** 2


@question_type(
    "math.monotone_grid_fleet_olympiad",
    display_name={"th": "รถไถหลายคันครอบคลุมตารางด้วยทางขึ้นและขวา"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class MonotoneGridFleet(WordProblem):
    def expr(self, rng: Random):
        size = rng.randint(5, 16)
        vehicles = rng.randint(1, size - 1)
        answer = minimum_unvisited_squares(size, vehicles)
        return MathDraw(
            rf"n={size},\quad k={vehicles}",
            str(answer),
            prompt=(
                "ตาราง n×n มีรถไถ k คัน แต่ละคันเริ่มช่องซ้ายล่าง "
                "เดินได้เฉพาะขึ้นหรือขวาไปยังช่องที่ติดกันจนถึงช่องขวาบน "
                "จงหาจำนวนช่องที่รถทุกคันไม่ผ่านให้น้อยที่สุด"
            ),
            hint=(
                "แบ่งช่องตามผลบวกพิกัด แต่ละเส้นทางผ่านได้หนึ่งช่องในแต่ละแนวทแยง "
                "แล้วสร้างเส้นทางเลียบขอบกับเส้นทางรูปตัวแอลซ้อนกัน"
            ),
            distractors=[
                str(size * size - vehicles * (2 * size - 1)),  # ignore shared endpoints
                str(size - vehicles),  # count the middle diagonal only
                str((size - vehicles) * (size - vehicles + 1)),  # miss a diagonal layer
                str(max(0, size * size - vehicles * (2 * size - 3) - 2)),  # assume only endpoints overlap
                str(answer + 1),  # leave an avoidable central cell
                str(max(0, answer - 1)),  # overcover a diagonal by one
            ],
        )
