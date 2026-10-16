"""Assign progressively slower elves to progressively nearer houses."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 2",)
)


def minimum_elf_delivery_time(houses: int) -> int:
    """Minimum possible maximum of elf index times assigned distance."""
    if houses < 1:
        raise ValueError("number of houses must be positive")
    return (houses + 1) ** 2 // 4


@question_type(
    "math.elf_delivery_minimax_olympiad",
    display_name={"th": "จับคู่เอลฟ์กับบ้านให้เสร็จเร็วสุด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class ElfDeliveryMinimax(WordProblem):
    def expr(self, rng: Random):
        houses = rng.randint(9, 49)
        answer = minimum_elf_delivery_time(houses)
        return MathDraw(
            rf"N={houses}",
            str(answer),
            prompt=(
                "มีบ้าน N หลังอยู่ห่างจุดเริ่มต้น 1,2,…,N กิโลเมตร "
                "เอลฟ์ E_i ใช้เวลา i นาทีต่อกิโลเมตรและส่งของได้คนละหนึ่งหลัง "
                "ทุกคนออกเดินทางพร้อมกัน จงหาเวลาน้อยที่สุดที่ส่งถึงทุกบ้าน"
            ),
            hint=(
                "หากเอลฟ์ที่เร็วกว่าถูกส่งไปบ้านใกล้กว่า "
                "สลับงานกันแล้วเวลาสูงสุดไม่เพิ่ม จึงจับคู่ i กับระยะ N+1−i"
            ),
            distractors=[
                str(answer - 1),  # underestimate the central pair by one minute
                str(answer + 1),  # round the central pair upward
                str(houses * houses),  # assign the slowest elf to the farthest house
                str(houses * (houses + 1) // 2),  # use a total rather than the makespan
                str(houses),  # count only the farthest travel distance
                str((houses + 1) ** 2 // 2),  # omit division by two in pairing
            ],
        )
