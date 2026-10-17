"""f(x + 2y) + k f(y − 2x) = linear: the substitution is invertible, so f is linear."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 15",))


def solved_value(a: int, b: int, n: int) -> int:
    """Put y = 2x: f(5x) + k f(0) = (rhs at y = 2x), so f is linear, and
    matching coefficients gives f(t) = at + b (source: f(t) = −t + 2,
    f(2548) = −2546)."""
    return a * n + b


def rhs(a: int, b: int, k: int) -> tuple[int, int, int]:
    # a(x + 2y) + b + k(a(y − 2x) + b)
    return a * (1 - 2 * k), a * (2 + k), b * (1 + k)


@question_type(
    "math.linear_substitution_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันที่แทนค่าเชิงเส้น"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class LinearSubstitutionFunctional(WordProblem):
    def expr(self, rng: Random):
        a, b, k = rng.choice([-3, -2, -1, 1, 2, 3]), rng.randint(-9, 9), rng.randint(2, 4)
        n = rng.randint(50, 3000)
        cx, cy, c0 = rhs(a, b, k)
        answer = solved_value(a, b, n)
        wrong = [v for v in dict.fromkeys([-answer, a * n - b, a * n + c0, cx * n + c0, a * n]) if v != answer]

        def term(coef: int, var: str, first: bool = False) -> str:
            if coef == 0:
                return ""
            sign = "-" if coef < 0 else ("" if first else "+")
            mag = "" if abs(coef) == 1 else str(abs(coef))
            return f"{sign}{mag}{var}"

        right = term(cx, "x", True) + term(cy, "y") + (f"{c0:+d}" if c0 else "")
        return MathDraw(
            rf"f(x+2y)+{k}f(y-2x)={right}",
            str(answer),
            prompt=f"f : ℝ → ℝ สอดคล้องสมการต่อไปนี้สำหรับทุก x, y ∈ ℝ จงหา f({n})",
            hint="แทน y = 2x จะได้ y − 2x = 0 แล้วหา f(0) และ f(5x) หรือสมมติ f(t) = at + b แล้วเทียบสัมประสิทธิ์",
            distractors=[str(v) for v in wrong],
        )
