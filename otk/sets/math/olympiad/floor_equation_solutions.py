"""x + ⌊x/a⌋ = ⌊bx/c⌋ + ⌊dx/e⌋: x must be an integer and the solutions are bounded."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 3",))

FAMILIES = ((3, 2, 3, 3, 5), (2, 1, 2, 4, 5), (4, 1, 2, 2, 3), (3, 1, 2, 3, 4), (5, 2, 3, 1, 2), (2, 2, 3, 2, 5), (4, 3, 4, 1, 3))


def floor_solutions(a: int, b: int, c: int, d: int, e: int) -> list[int]:
    """The right side and ⌊x/a⌋ are integers, so x is one. The linear parts
    have slope b/c + d/e − 1/a < 1, and each floor is within 1 of its value,
    so x − (slope)x ≤ 2 bounds every solution."""
    slope = Fraction(b, c) + Fraction(d, e) - Fraction(1, a)
    bound = int(3 / (1 - slope)) + 3
    return [x for x in range(1, bound + 1) if x + x // a == (b * x) // c + (d * x) // e]


@question_type(
    "math.floor_equation_solutions_olympiad",
    display_name={"th": "สมการที่มีฟังก์ชันจำนวนเต็มมากสุด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการและอสมการ",
)
class FloorEquationSolutions(WordProblem):
    def expr(self, rng: Random):
        while True:
            a, b, c, d, e = rng.choice(FAMILIES)
            found = floor_solutions(a, b, c, d, e)
            if found:
                break
        answer = sum(found)
        wrong = [v for v in dict.fromkeys([max(found), len(found), answer + 1, answer + max(found), answer - 1]) if v != answer and v > 0]
        bx = "x" if b == 1 else f"{b}x"
        dx = "x" if d == 1 else f"{d}x"
        return MathDraw(
            rf"x+\left\lfloor\frac{{x}}{{{a}}}\right\rfloor=\left\lfloor\frac{{{bx}}}{{{c}}}\right\rfloor+\left\lfloor\frac{{{dx}}}{{{e}}}\right\rfloor",
            str(answer),
            prompt="จงหาผลบวกของจำนวนจริงบวก x ทั้งหมดที่สอดคล้องสมการ เมื่อ ⌊t⌋ คือจำนวนเต็มที่มากที่สุดที่ไม่เกิน t",
            hint="ทุกพจน์ยกเว้น x เป็นจำนวนเต็ม จึง x เป็นจำนวนเต็ม และเทียบความชันเพื่อจำกัดขนาดของ x",
            distractors=[str(v) for v in wrong],
        )
