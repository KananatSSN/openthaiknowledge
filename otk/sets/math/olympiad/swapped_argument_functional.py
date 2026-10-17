"""x ↦ 1 − x swaps x² + x + 3 and x² − 3x + 5, so the two values solve a 2 × 2 system."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 9",))


def linear_value(alpha: int, beta: int, n: int) -> int:
    """With u = x² + x + 3 and v = x² − 3x + 5, replacing x by 1 − x swaps u, v;
    solving f(u) + k f(v) = R(x), f(v) + k f(u) = R(1 − x) gives f(u) linear in
    u (source: f(t) = 2t − 3, f(85) = 167)."""
    return alpha * n + beta


def rhs_tex(alpha: int, beta: int, k: int) -> str:
    # α(x² + x + 3) + β + k(α(x² − 3x + 5) + β)
    a2 = alpha * (1 + k)
    a1 = alpha * (1 - 3 * k)
    a0 = alpha * (3 + 5 * k) + beta * (1 + k)
    parts = [f"{a2}x^2"]
    parts.append(("+" if a1 >= 0 else "-") + f"{abs(a1)}x" if a1 else "")
    parts.append(("+" if a0 >= 0 else "-") + str(abs(a0)) if a0 else "")
    return "".join(parts)


@question_type(
    "math.swapped_argument_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันที่สลับอาร์กิวเมนต์ด้วย x ↦ 1 − x"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class SwappedArgumentFunctional(WordProblem):
    def expr(self, rng: Random):
        alpha, beta, k = rng.randint(1, 4), rng.randint(-6, 6), rng.choice([2, 3, 4])
        n = rng.randint(20, 120)
        answer = linear_value(alpha, beta, n)
        wrong = [v for v in dict.fromkeys([alpha * n - beta, alpha * n, (alpha + 1) * n + beta, answer + alpha, alpha * n + beta * (1 + k)]) if v != answer]
        kk = "" if k == 1 else str(k)
        return MathDraw(
            rf"f(x^2+x+3)+{kk}f(x^2-3x+5)={rhs_tex(alpha, beta, k)}",
            str(answer),
            prompt=f"f : ℝ → ℝ สอดคล้องสมการต่อไปนี้ทุกจำนวนจริง x จงหา f({n})",
            hint="แทน x ด้วย 1 − x จะสลับ x² + x + 3 กับ x² − 3x + 5 แล้วแก้ระบบสมการสองตัวแปร",
            distractors=[str(v) for v in wrong],
        )
