"""f(m + n) = f(m) + f(n) + 2mn − C on ℕ gives f(n) = n² + cn + C."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 14",))


def value_at(shift: int, anchor_value: int, t: int) -> int:
    """h(n) = f(n) − n² − C is additive on ℕ, so h(n) = n·h(1) and
    f(n) = n² + cn + C; f(C) = D fixes c = (D − C² − C)/C
    (source: C = 2548, f(2548) = −2548 → c = −2550, f(2) = −2548)."""
    c = (anchor_value - shift * shift - shift) // shift
    return t * t + c * t + shift


@question_type(
    "math.quadratic_cauchy_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันบนจำนวนนับที่มีพจน์ 2mn"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class QuadraticCauchyFunctional(WordProblem):
    def expr(self, rng: Random):
        shift = rng.randint(5, 3000)
        c = rng.randint(-shift - 10, 10)
        anchor = shift * shift + c * shift + shift
        t = rng.randint(2, 12)
        answer = value_at(shift, anchor, t)
        wrong = [v for v in dict.fromkeys([t * t + c * t, answer - 2 * shift, c * t + shift, t * t + c * t - shift, answer + t]) if v != answer]
        return MathDraw(
            rf"f(m+n)=f(m)+f(n)+2mn-{shift},\quad f({shift})={anchor}",
            str(answer),
            prompt=f"f : ℕ → ℤ สอดคล้องสมการต่อไปนี้สำหรับทุก m, n ∈ ℕ จงหา f({t})",
            hint="ให้ h(n) = f(n) − n² − C จะได้ h(m + n) = h(m) + h(n) บนจำนวนนับ จึง h(n) = n·h(1)",
            distractors=[str(v) for v in wrong],
        )
