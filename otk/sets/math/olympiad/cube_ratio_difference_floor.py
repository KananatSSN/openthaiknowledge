"""(n + d)³/((n − d)n) − (n − d)³/(n(n + d)) = 8d + 16d³/(n² − d²)."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 9",))


def floor_value(n: int, d: int) -> int:
    """Over the common denominator (n − d)n(n + d) the numerator is
    (n + d)⁴ − (n − d)⁴ = 8n³d + 8nd³, so the difference is
    8d(n² + d²)/(n² − d²) = 8d + 16d³/(n² − d²) (source: n = 2548, d = 1 → 8)."""
    return 8 * d + (16 * d**3) // (n * n - d * d)


@question_type(
    "math.cube_ratio_difference_floor_olympiad",
    display_name={"th": "จำนวนเต็มที่มากที่สุดไม่เกินผลต่างของเศษส่วนกำลังสาม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดรูปพีชคณิต",
)
class CubeRatioDifferenceFloor(WordProblem):
    def expr(self, rng: Random):
        d = rng.randint(1, 4)
        n = rng.choice([rng.randint(d + 1, 6 * d), rng.randint(d + 1, 40), rng.randint(100, 3000)])
        answer = floor_value(n, d)
        wrong = [v for v in dict.fromkeys([answer + 1, 8 * d if answer != 8 * d else 8 * d - 1, 4 * d + (16 * d**3) // (n * n - d * d), 8 * d + (16 * d**3) // (n * n), 16 * d]) if v != answer]
        return MathDraw(
            rf"\frac{{{n + d}^3}}{{{n - d}\cdot {n}}}-\frac{{{n - d}^3}}{{{n}\cdot {n + d}}}",
            str(answer),
            prompt="จงหาจำนวนเต็มที่มีค่ามากที่สุดและมีค่าไม่เกินจำนวนต่อไปนี้",
            hint="ให้ตัวกลางเป็น n แล้วรวมเศษส่วนด้วยตัวส่วน (n − d)n(n + d) ใช้ (n + d)⁴ − (n − d)⁴",
            distractors=[str(v) for v in wrong],
        )
