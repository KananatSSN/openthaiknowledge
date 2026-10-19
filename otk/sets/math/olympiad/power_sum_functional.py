"""(x² + y²)ᵏ f(xy) = f(x)f(y)f(x² + y²): f = ±xᵏ, ±xᵏ⁻¹|x| or 0."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 6",)
)


def solutions(k: int):
    """f = xᵏh: h(xy) = h(x)h(y)h(x² + y²). y = 1 makes h constant c = ±1 on
    [1, ∞), so g = ch is multiplicative and 1 there, hence 1 or sign(x).
    sign(x)·xᵏ = xᵏ⁻¹|x| is |x|ᵏ for odd k and sign(x)|x|ᵏ for even k."""
    return (
        lambda x: x**k,
        lambda x: -(x**k),
        lambda x: x ** (k - 1) * abs(x),
        lambda x: -(x ** (k - 1) * abs(x)),
        lambda x: 0,
    )


@question_type(
    "math.power_sum_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชัน (x² + y²)ᵏ f(xy) = f(x)f(y)f(x² + y²)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class PowerSumFunctional(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(1, 3)
        a = rng.randint(2, 5)
        b = rng.choice([v for v in range(2, 10) if v != a])
        sign = rng.choice([1, -1])
        given = sign * a**k
        values = {f(b) for f in solutions(k) if f(a) == given}
        assert len(values) == 1, f"f({a}) = {given} leaves f({b}) undetermined: {values}"
        answer = values.pop()
        wrong = [v for v in dict.fromkeys([-answer, sign * b ** (k + 1), sign * b * a ** (k - 1), sign * b, answer + sign, sign * (b**k + a**k)]) if v != answer]
        power = "" if k == 1 else f"^{k}"
        return MathDraw(
            rf"\left(x^2+y^2\right){power}f(xy)=f(x)\,f(y)\,f\!\left(x^2+y^2\right),\quad f({a})={given}",
            str(answer),
            prompt=f"ฟังก์ชัน f : ℝ → ℝ สอดคล้องสมการต่อไปนี้ทุกจำนวนจริง x, y จงหา f({b})",
            hint="ให้ x = y = 0 ได้ f(0) = 0 แล้วเขียน f(x) = xᵏh(x) และใช้ y = 1",
            distractors=[str(v) for v in wrong],
        )
