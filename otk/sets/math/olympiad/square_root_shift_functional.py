"""f(x + y·f(x) + m²y²) = f(x) + 2m²y forces f(x)² − 4m²x to be constant."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 3",)
)


def shifted_value(m: int, a: int, value: int, b: int) -> int:
    """f(b) from f(a) = value, using f(b)² − f(a)² = 4m²(b − a)."""
    square = value * value + 4 * m * m * (b - a)
    root = isqrt(square)
    if root * root != square or root <= 0:
        raise ValueError("f(b) is not a positive integer here")
    return root


@question_type(
    "math.square_root_shift_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันที่ f² ลบเชิงเส้นคงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class SquareRootShiftFunctional(WordProblem):
    def expr(self, rng: Random):
        m = rng.randint(1, 3)
        a = rng.randint(1, 12)
        # f(x)² − 4m²x must stay ≥ 0 so that f is positive on all of ℝ⁺.
        low = isqrt(4 * m * m * a - 1) + 1
        value = rng.randint(low, low + 6)
        t = rng.randint(1, 3)
        b = a + t * (value + m * m * t)
        answer = shifted_value(m, a, value, b)
        wrong = []
        for candidate in (
            value + m * m * t,  # lose the factor 2 of 2m²y
            value + 4 * m * m * t,  # double the shift twice
            value + 2 * t,  # forget the m²
            answer + 1,
            answer - 1,
            answer + 2,
        ):
            if candidate > 0 and candidate != answer and candidate not in wrong:
                wrong.append(candidate)
        coefficient = "" if m == 1 else str(m * m)
        return MathDraw(
            (
                rf"f\left(x+y\,f(x)+{coefficient}y^2\right)=f(x)+{2 * m * m}y,"
                rf"\quad f({a})={value}"
            ),
            str(answer),
            prompt=(
                "ให้ f เป็นฟังก์ชันจากจำนวนจริงบวกไปจำนวนจริงบวก "
                f"ที่สอดคล้องสมการต่อไปนี้สำหรับทุก x, y > 0 จงหา f({b})"
            ),
            hint=(
                "สำหรับ z > x เลือก y > 0 ที่ x + y f(x) + m²y² = z "
                "แล้วแสดงว่า f(z)² − f(x)² = 4m²(z − x)"
            ),
            distractors=[str(candidate) for candidate in wrong],
        )
