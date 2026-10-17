"""(−1)ⁿxⁿ + a₁xⁿ⁻¹ + ⋯ + aₙ with {aᵢ} = {0, 1} and distinct real roots."""

from __future__ import annotations

from itertools import product
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันที่สอง ข้อ 6",))

# the three solutions: x² + x, −x³ + x, −x³ + x² + x
SOLUTIONS = ((1, 0), (0, 1, 0), (1, 1, 0))


def poly_tex(coeffs: tuple[int, ...]) -> str:
    n = len(coeffs)
    parts = [("-" if n % 2 else "") + f"x^{{{n}}}"]
    for i, c in enumerate(coeffs, start=1):
        power = n - i
        if c:
            parts.append("+" + ("1" if power == 0 else ("x" if power == 1 else f"x^{{{power}}}")))
    return "".join(parts)


def distinct_real_roots(coeffs: tuple[int, ...]) -> bool:
    """Sturm-free test by sign changes on a fine grid plus the degree: a
    polynomial of degree n with n sign changes on [−3, 3] has n distinct real
    roots (all roots lie in |x| < 2 here by the Cauchy bound)."""
    n = len(coeffs)

    def value(x: float) -> float:
        return (-1) ** n * x**n + sum(c * x ** (n - i) for i, c in enumerate(coeffs, start=1))

    xs = [-3 + 6 * i / 6000 + 1e-7 for i in range(6001)]
    changes = sum(1 for u, v in zip(xs, xs[1:]) if value(u) * value(v) < 0)
    return changes == n


CANDIDATES = tuple(
    c for n in (2, 3, 4) for c in product((0, 1), repeat=n) if set(c) == {0, 1} and c not in SOLUTIONS
)


@question_type(
    "math.zero_one_real_rooted_olympiad",
    display_name={"th": "พหุนามสัมประสิทธิ์ 0, 1 ที่มีรากจริงต่างกันทั้งหมด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รากของพหุนาม",
)
class ZeroOneRealRooted(WordProblem):
    def expr(self, rng: Random):
        answer = rng.choice(SOLUTIONS)
        wrong = rng.sample(CANDIDATES, 5)
        return MathDraw(
            "",
            poly_tex(answer),
            prompt="สัมประสิทธิ์ a₁, …, aₙ ของ P(x) = (−1)ⁿxⁿ + a₁xⁿ⁻¹ + ⋯ + aₙ เป็น 0 หรือ 1 (มีทั้งสองค่า) พหุนามใดต่อไปนี้มีรากเป็นจำนวนจริงที่แตกต่างกันทั้งหมด",
            hint="ใช้ผลบวกกำลังสองของราก (a₁)² − 2(±a₂) และผลคูณของราก เพื่อจำกัดดีกรี แล้วตรวจแต่ละตัวเลือก",
            distractors=[poly_tex(c) for c in wrong],
        )
