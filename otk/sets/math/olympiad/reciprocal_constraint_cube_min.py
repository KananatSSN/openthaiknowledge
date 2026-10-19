"""Σa ≥ q²Σ(1/a) gives Σa ≥ nq, so Σa³ ≥ (Σa)³/n² ≥ nq³."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันที่สอง ข้อ 6",))


def cube_minimum(n: int, q: int) -> int:
    """Σ1/a ≥ n²/S gives S ≥ q²n²/S, so S ≥ nq; power means give
    Σa³ ≥ S³/n² ≥ nq³, with equality at every a = q (source: n = 3, q = 1:
    a³ + b³ + c³ ≥ a + b + c holds since both sides are ≥ 3)."""
    return n * q**3


@question_type(
    "math.reciprocal_constraint_cube_min_olympiad",
    display_name={"th": "ค่าต่ำสุดของผลบวกกำลังสามภายใต้เงื่อนไขส่วนกลับ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class ReciprocalConstraintCubeMin(WordProblem):
    def expr(self, rng: Random):
        n, q = rng.randint(2, 8), rng.randint(1, 6)
        answer = cube_minimum(n, q)
        wrong = [v for v in dict.fromkeys([n * q, n * q * q, q**3, 3 * q**3 if n != 3 else 2 * q**3, n**3 * q**3]) if v != answer]
        qq = "" if q == 1 else str(q * q)
        sum_a = "+".join(f"a_{{{i}}}" for i in range(1, n + 1))
        sum_inv = "+".join(rf"\frac{{1}}{{a_{{{i}}}}}" for i in range(1, n + 1))
        return MathDraw(
            rf"{sum_a}\ge {qq}\left({sum_inv}\right)",
            str(answer),
            prompt="a₁, …, aₙ เป็นจำนวนจริงบวกที่สอดคล้องเงื่อนไขต่อไปนี้ จงหาค่าต่ำสุดของ a₁³ + … + aₙ³",
            hint="ใช้ Σ1/a ≥ n²/Σa ได้ Σa ≥ nq แล้วใช้อสมการค่าเฉลี่ยกำลัง Σa³ ≥ (Σa)³/n²",
            distractors=[str(v) for v in wrong],
        )
