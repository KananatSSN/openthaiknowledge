"""Apex 36°, base angles 72°: AB/BC = φ, so (AB/BC)ⁿ = (Lₙ + Fₙ√5)/2."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 3",))


def lucas_fib(n: int) -> tuple[int, int]:
    lucas, fib = (2, 1), (0, 1)
    for _ in range(n):
        lucas, fib = (lucas[1], lucas[0] + lucas[1]), (fib[1], fib[0] + fib[1])
    return lucas[0], fib[0]


def golden_power_tex(n: int, sign: int = 1, swap: bool = False) -> str:
    """5x = 180° gives apex 36°; the bisector of a base angle cuts a similar
    triangle, so AB/BC = φ = (1 + √5)/2 and φⁿ = (Lₙ + Fₙ√5)/2
    (source: n = 1)."""
    lucas, fib = lucas_fib(n)
    if swap:
        lucas, fib = fib, lucas
    coef = "" if fib == 1 else str(fib)
    op = "+" if sign > 0 else "-"
    if lucas % 2 == 0 and fib % 2 == 0:
        c2 = "" if fib // 2 == 1 else str(fib // 2)
        return rf"{lucas // 2}{op}{c2}\sqrt{{5}}"
    return rf"\frac{{{lucas}{op}{coef}\sqrt{{5}}}}{{2}}"


@question_type(
    "math.golden_isosceles_power_olympiad",
    display_name={"th": "อัตราส่วนทองในรูปสามเหลี่ยมหน้าจั่ว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต",
)
class GoldenIsoscelesPower(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(1, 9)
        answer = golden_power_tex(n)
        wrong = [t for t in dict.fromkeys([golden_power_tex(n, sign=-1), golden_power_tex(n, swap=True), golden_power_tex(n + 1), golden_power_tex(n - 1) if n > 1 else golden_power_tex(3)]) if t != answer]
        power = "" if n == 1 else f"^{{{n}}}"
        return MathDraw(
            rf"\left(\frac{{AB}}{{BC}}\right){power}",
            answer,
            prompt="ABC เป็นรูปสามเหลี่ยมหน้าจั่วที่มี A เป็นจุดยอด และมุมที่ฐานมีขนาดเป็นสองเท่าของมุมที่จุดยอด จงหาค่าต่อไปนี้",
            hint="มุมยอด 36° ลากเส้นแบ่งครึ่งมุมที่ฐานจะได้สามเหลี่ยมคล้าย ได้ AB/BC = (1 + √5)/2 แล้วใช้ φ² = φ + 1",
            distractors=wrong,
        )
