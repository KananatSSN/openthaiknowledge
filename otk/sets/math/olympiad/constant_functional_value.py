"""Σ f(xᵢ + xᵢ₊₁) + f(Σ xᵢ) ≤ Σ f(2xᵢ) for all reals forces f constant."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันที่สอง ข้อ 1",))


def forced_value(f0: int, n_vars: int, x: int) -> int:
    """Let g = f − f(0) and n even, n ≥ 4. x₁ = x₂ = a, the rest 0, gives
    2g(2a) + g(a) ≤ 2g(2a), so g(a) ≤ 0. The alternating x = (t, −t, …)
    makes every pair sum and the total 0, so 0 ≤ (n/2)(g(2t) + g(−2t)).
    Hence g ≡ 0: f(x) = f(0) for every x, and a constant gives equality."""
    return f0


@question_type(
    "math.constant_functional_value_olympiad",
    display_name={"th": "ค่าของฟังก์ชันที่สอดคล้องอสมการเชิงฟังก์ชัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class ConstantFunctionalValue(WordProblem):
    def expr(self, rng: Random):
        f0, n_vars, x = rng.randint(2, 40), 2 * rng.randint(2, 1275), rng.randint(2, 60)
        answer = forced_value(f0, n_vars, x)
        wrong = [v for v in dict.fromkeys([f0 + x, f0 * x, 2 * f0, f0 + 2 * x, x]) if v != answer]
        return MathDraw(
            rf"\sum_{{i=1}}^{{{n_vars - 1}}}f(x_i+x_{{i+1}})+f\Big(\sum_{{i=1}}^{{{n_vars}}}x_i\Big)\le\sum_{{i=1}}^{{{n_vars}}}f(2x_i),\quad f(0)={f0}",
            str(answer),
            prompt=f"f : ℝ → ℝ สอดคล้องอสมการต่อไปนี้สำหรับทุกจำนวนจริง x₁, …, xₙ เมื่อ n = {n_vars} จงหา f({x})",
            hint="ให้ g = f − f(0) แทน x₁ = x₂ = a ที่เหลือเป็น 0 จะได้ g(a) ≤ 0 แล้วแทนค่าสลับเครื่องหมาย t, −t, t, … เพื่อบีบให้ g = 0",
            distractors=[str(v) for v in wrong],
        )
