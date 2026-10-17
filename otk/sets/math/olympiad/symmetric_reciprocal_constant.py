"""t + u/(ab + bc + ca) ≥ k/(a + b + c) holds for all positives iff k ≤ 2√(3tu)."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันที่สอง ข้อ 6",))


def best_constant(t: int, u: int) -> int:
    """With S = a + b + c, ab + bc + ca ≤ S²/3, so the left side is at least
    t + 3u/S², and S(t + 3u/S²) = tS + 3u/S ≥ 2√(3tu) by AM–GM, with
    equality at a = b = c (source: t = 1, u = 3 → 6)."""
    return 2 * isqrt(3 * t * u)


CASES = tuple((t, u) for t in range(1, 10) for u in range(1, 61) if isqrt(3 * t * u) ** 2 == 3 * t * u)


@question_type(
    "math.symmetric_reciprocal_constant_olympiad",
    display_name={"th": "ค่าคงตัวที่ดีที่สุดในอสมการส่วนกลับสมมาตร"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class SymmetricReciprocalConstant(WordProblem):
    def expr(self, rng: Random):
        t, u = rng.choice(CASES)
        answer = best_constant(t, u)
        wrong = [v for v in dict.fromkeys([answer // 2, 3 * t + u, 2 * (t + u), answer * 2, t + u]) if v != answer]
        return MathDraw(
            rf"{t}+\frac{{{u}}}{{ab+bc+ca}}\ge\frac{{k}}{{a+b+c}}",
            str(answer),
            prompt="จงหาค่า k ที่มากที่สุดที่ทำให้อสมการต่อไปนี้เป็นจริงสำหรับทุกจำนวนจริงบวก a, b, c",
            hint="ใช้ ab + bc + ca ≤ (a + b + c)²/3 แล้วใช้อสมการ AM–GM กับ tS + 3u/S เมื่อ S = a + b + c",
            distractors=[str(v) for v in wrong],
        )
