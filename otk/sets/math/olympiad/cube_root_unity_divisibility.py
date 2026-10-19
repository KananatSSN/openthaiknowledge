"""1 + x + x² | 2xP(x³) + Q(−x − x²) forces P(1) = Q(1) = 0, so x − 1 divides P − Q."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันที่สอง ข้อ 3",))


def difference_at(u: int, k: int, v: int, t: int) -> int:
    """At x = ω (ω³ = 1, −ω − ω² = 1) the identity gives 2ωP(1) + Q(1) = 0,
    and at ω² gives 2ω²P(1) + Q(1) = 0, so P(1) = Q(1) = 0. With
    P = x² + ax + u and Q = kx² + bx + v: a = −1 − u, b = −k − v."""
    a, b = -1 - u, -k - v
    return (t * t + a * t + u) - (k * t * t + b * t + v)


@question_type(
    "math.cube_root_unity_divisibility_olympiad",
    display_name={"th": "ค่าของ P − Q เมื่อพหุนามหารด้วย 1 + x + x² ลงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามและเศษเหลือ",
)
class CubeRootUnityDivisibility(WordProblem):
    def expr(self, rng: Random):
        while True:
            u, v, k = rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(1, 4)
            t = rng.randint(2, 9)
            answer = difference_at(u, k, v, t)
            if answer != 0 and u != v:
                break
        wrong = [v2 for v2 in dict.fromkeys([-answer, (t * t - u * t + u) - (k * t * t - v * t + v), (1 - k) * t * t + (u - v), difference_at(u, k, v, t + 1), 0]) if v2 != answer]
        kk = "" if k == 1 else str(k)
        return MathDraw(
            rf"P(x)=x^2+ax{u:+d},\quad Q(x)={kk}x^2+bx{v:+d},\quad 2xP(x^3)+Q(-x-x^2)=(1+x+x^2)R(x)",
            str(answer),
            prompt=f"a, b เป็นค่าคงตัว และมีพหุนาม R(x) ที่ทำให้สมการต่อไปนี้เป็นจริงทุก x จงหา P({t}) − Q({t})",
            hint="แทน x = ω ที่ ω³ = 1, ω ≠ 1 จะได้ −ω − ω² = 1 แล้วเทียบสองสมการจาก ω และ ω² ได้ P(1) = Q(1) = 0",
            distractors=[str(v2) for v2 in wrong],
        )
