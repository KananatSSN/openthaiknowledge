"""With z = a² + ib², z³ = (a⁶ − 3a²b⁴) + i(3a⁴b² − b⁶), so a⁴ + b⁴ = |z|² = (p² + q²)^(1/3).

The source writes b⁶ − 3a⁴b² = 3√2, which has no real solution (z³ would lie
in the fourth quadrant); this set uses the consistent sign.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 2",))


def _cases():
    out = []
    for d, tag in ((1, ""), (2, r"\sqrt{2}"), (3, r"\sqrt{3}")):
        for p in range(1, 120):
            for r in range(1, 120):
                total = p * p + r * r * d
                m = round(total ** (1 / 3))
                if m**3 == total and (d > 1 or p != r):
                    out.append((p, r, d, tag, m))
    return tuple(out)


CASES = _cases()


def fourth_power_sum(p: int, r: int, d: int) -> int:
    """|z|⁶ = p² + q² with q = r√d, so a⁴ + b⁴ = |z|² = (p² + r²d)^(1/3)
    (source: 3 and 3√2 → 3)."""
    total = p * p + r * r * d
    return round(total ** (1 / 3))


@question_type(
    "math.complex_cube_modulus_olympiad",
    display_name={"th": "หา a⁴ + b⁴ จากระบบสมการกำลังหก"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ระบบสมการไม่เชิงเส้น",
)
class ComplexCubeModulus(WordProblem):
    def expr(self, rng: Random):
        p, r, d, tag, m = rng.choice(CASES)
        answer = fourth_power_sum(p, r, d)
        q_tex = ("" if r == 1 and tag else str(r)) + tag
        wrong = [v for v in dict.fromkeys([answer * answer, p + r, answer**3, 2 * answer, answer + 1]) if v != answer]
        return MathDraw(
            rf"a^6-3a^2b^4={p},\quad 3a^4b^2-b^6={q_tex}",
            str(answer),
            prompt="a และ b เป็นจำนวนจริง จงหาค่าของ a⁴ + b⁴",
            hint="ให้ z = a² + ib² แล้วกระจาย z³ ส่วนจริงและส่วนจินตภาพคือสองสมการ จึงได้ |z|⁶ = p² + q²",
            distractors=[str(v) for v in wrong],
        )
