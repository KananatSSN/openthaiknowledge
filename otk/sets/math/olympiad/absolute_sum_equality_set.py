"""Σ|x − k| = |Σ(x − k)| holds iff all x − k share a sign."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 5",))


def solution_tex(m: int) -> str:
    """√(x² − 2kx + k²) = |x − k| and the right side is |Σ_{k=1}^{m} (x − k)|;
    the triangle inequality is equality iff x ≤ 1 or x ≥ m
    (source: m = 2n)."""
    return rf"(-\infty,1]\cup[{m},\infty)"


@question_type(
    "math.absolute_sum_equality_set_olympiad",
    display_name={"th": "เซตคำตอบเมื่ออสมการสามเหลี่ยมเป็นสมการ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ค่าสัมบูรณ์และค่าสุดขีด",
)
class AbsoluteSumEqualitySet(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(2, 40)
        m = 2 * n
        answer = solution_tex(m)
        wrong = [rf"[1,{m}]", rf"(-\infty,0]\cup[{m + 1},\infty)", rf"\{{\tfrac{{{m + 1}}}{{2}}\}}", rf"(-\infty,1)\cup({m},\infty)", rf"[{m},\infty)"]
        rhs = f"|{m}x-{n}-{2 * n * n}|"
        return MathDraw(
            rf"\sum_{{k=1}}^{{{m}}}\sqrt{{x^2-2kx+k^2}}={rhs}",
            answer,
            prompt="จงหาเซตคำตอบของสมการต่อไปนี้",
            hint="√(x² − 2kx + k²) = |x − k| และด้านขวาคือ |Σ(x − k)| ใช้อสมการสามเหลี่ยม",
            distractors=[t for t in dict.fromkeys(wrong) if t != answer],
        )
