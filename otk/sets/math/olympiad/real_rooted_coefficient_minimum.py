"""Real-rooted P with positive coefficients and P(0) = 1: aₖ ≥ C(n, k), P(t) ≥ (t + 1)ⁿ."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 9",)
)


def coefficient_minimum(n: int, k: int) -> int:
    """Roots are −rᵢ with rᵢ > 0 and Π rᵢ = 1; aₖ = e_{n−k}(r) is a sum of
    C(n, k) terms with product 1, so AM–GM gives aₖ ≥ C(n, k)."""
    return comb(n, k)


def value_minimum(n: int, t: int) -> int:
    """Π(t + rᵢ) ≥ (t + (Π rᵢ)^{1/n})ⁿ = (t + 1)ⁿ by Hölder."""
    return (t + 1) ** n


@question_type(
    "math.real_rooted_coefficient_minimum_olympiad",
    display_name={"th": "ค่าน้อยสุดของสัมประสิทธิ์พหุนามที่มีรากจริงทั้งหมด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามสมมาตร",
)
class RealRootedCoefficientMinimum(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(3, 10)
        setup = (
            f"P(x) = xⁿ + aₙ₋₁xⁿ⁻¹ + ⋯ + a₁x + 1 มีดีกรี n = {n} สัมประสิทธิ์ทุกตัวเป็นจำนวนจริงบวก "
            "และรากทุกตัวเป็นจำนวนจริง "
        )
        if rng.randrange(2):
            k = rng.randint(1, n - 1)
            answer = coefficient_minimum(n, k)
            wrong = [v for v in dict.fromkeys([n, k, comb(n, k - 1), comb(n + 1, k), 2**k, n * k]) if v != answer]
            return MathDraw(
                rf"a_{{{k}}}",
                str(answer),
                prompt=setup + "ค่าน้อยที่สุดที่เป็นไปได้ของสัมประสิทธิ์ต่อไปนี้คือเท่าใด",
                hint="รากเป็น −r₁, …, −rₙ โดย rᵢ > 0 และ r₁r₂⋯rₙ = 1 แล้วใช้อสมการ AM–GM",
                distractors=[str(v) for v in wrong],
                variant="coefficient",
            )
        t = rng.randint(1, 4)
        answer = value_minimum(n, t)
        wrong = [v for v in dict.fromkeys([t**n + 1, (t + 1) ** (n - 1), 2**n, n * t + 1, (t + 2) ** n, (t + 1) ** n + 1]) if v != answer]
        return MathDraw(
            rf"P({t})",
            str(answer),
            prompt=setup + "ค่าน้อยที่สุดที่เป็นไปได้ของค่าต่อไปนี้คือเท่าใด",
            hint="P(t) = (t + r₁)⋯(t + rₙ) กับ r₁⋯rₙ = 1 ใช้อสมการของเฮิลเดอร์",
            distractors=[str(v) for v in wrong],
            variant="value",
        )
