"""Find same-material lighted paths among near-diameter chords."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 4",)
)


def guaranteed_lighted_same_material_paths(gates: int) -> int:
    """At least this many near-diameter chords share one path material."""
    if gates < 5 or gates % 2 != 1:
        raise ValueError("expected an odd number of gates at least five")
    return (gates + 1) // 2


@question_type(
    "math.circular_gate_crossings_olympiad",
    display_name={"th": "ทางเดินสวนวงกลมกับกระถางสองชนิด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class CircularGateCrossings(WordProblem):
    def expr(self, rng: Random):
        side = rng.randint(5, 15)
        gates = 2 * side + 1
        crossings = side * (side - 1)
        threshold = crossings // 2
        answer = guaranteed_lighted_same_material_paths(gates)
        return MathDraw(
            rf"n={gates},\quad T={threshold}",
            str(answer),
            prompt=(
                "สวนวงกลมมีประตู n บาน เชื่อมประตูทุกคู่ด้วยทางเดินเส้นตรง "
                "โดยไม่มีทางเดินสามเส้นตัดกันในจุดเดียวภายในสวน "
                "ทางเดินแต่ละเส้นใช้วัสดุชนิดใดชนิดหนึ่งจากสองชนิด "
                "จุดตัดมีหนึ่งกระถางจากสองชนิดตามวัสดุของทางเดินที่ตัดกัน "
                "ทางเดินติดไฟเมื่อมีกระถางชนิดเดียวกันอย่างน้อย T กระถาง "
                "รับประกันทางเดินติดไฟอย่างน้อยกี่เส้นที่ใช้วัสดุชนิดเดียวกัน"
            ),
            hint=(
                "ทางเดินใกล้เส้นผ่านศูนย์กลางแต่ละเส้นมีจุดตัด r(r−1) จุด "
                "ใช้หลักช่องนกพิราบกับชนิดกระถาง แล้วกับวัสดุของทางเดิน"
            ),
            distractors=[
                str(side),  # round half the odd number of paths down
                str(answer + 1),  # overcount one same-material path
                str(gates),  # assume all central paths use one material
                str(gates - 1),  # leave only one central path out
                str(side - 1),  # miss two central paths
                str(2 * side - 1),  # allow just two paths of the other material
            ],
        )
