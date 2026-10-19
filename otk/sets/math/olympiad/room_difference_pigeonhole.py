"""N students in R rooms of L seats force two rooms to share a seat difference once N ≥ R + L."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 4",)
)


def forcing_count(rooms: int, seats: int) -> int:
    """A room with b students gives b − 1 distinct differences from its lowest
    seat, all in 1..L − 1. If no difference repeats across rooms,
    Σ(b − 1) ≤ L − 1, so N ≤ R + L − 1; filling one room completely and
    putting one student in every other room shows R + L − 1 is not enough."""
    return rooms + seats


@question_type(
    "math.room_difference_pigeonhole_olympiad",
    display_name={"th": "หลักรังนกพิราบกับผลต่างของเลขที่ในห้องเรียน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class RoomDifferencePigeonhole(WordProblem):
    def expr(self, rng: Random):
        rooms = rng.randint(3, 40)
        seats = rng.randint(5, 40)
        answer = forcing_count(rooms, seats)
        wrong = [v for v in dict.fromkeys([answer - 1, answer + 1, rooms * 2, rooms + seats - 2, seats + 1, 2 * seats]) if v != answer]
        return MathDraw(
            rf"R={rooms},\quad L={seats}",
            str(answer),
            prompt=(
                "มีห้องเรียน R ห้อง แต่ละห้องมีเลขที่ 1 ถึง L วางนักเรียน N คนลงในเลขที่ต่าง ๆ (ห้องละไม่เกิน L คน) "
                "ค่า N ที่น้อยที่สุดที่รับประกันว่ามีสองห้อง ซึ่งแต่ละห้องมีนักเรียนสองคนที่ผลต่างของเลขที่เท่ากัน คือเท่าใด"
            ),
            hint="ในห้องที่มี b คน ผลต่างจากเลขที่น้อยสุดถึงคนอื่น ๆ มี b − 1 ค่าที่ต่างกัน ใช้หลักรังนกพิราบกับค่า 1 ถึง L − 1",
            distractors=[str(v) for v in wrong],
        )
