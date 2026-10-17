"""x = √(x − k/x) + √(k − k/x) squares twice to (x² − x − k)² = 0."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 4",))


def root_tex(k: int, sign: int = 1, half: bool = True) -> str:
    """Move one root across and square twice: (x² + x − k)² = 4x(x² − k), which
    is (x² − x − k)² = 0. The positive root (1 + √(1 + 4k))/2 satisfies the
    original (checked in the tests; source k = 1 → (1 + √5)/2). The keyword
    arguments render the named mistakes."""
    inside, outside, f = 1 + 4 * k, 1, 2
    while f * f <= inside:
        while inside % (f * f) == 0:
            inside //= f * f
            outside *= f
        f += 1
    op = "+" if sign > 0 else "-"
    if inside == 1:
        value = Fraction(1 + sign * outside, 2 if half else 1)
        return str(value) if value.denominator == 1 else rf"\frac{{{value.numerator}}}{{{value.denominator}}}"
    o = "" if outside == 1 else str(outside)
    body = rf"1{op}{o}\sqrt{{{inside}}}"
    return rf"\frac{{{body}}}{{2}}" if half else body


@question_type(
    "math.nested_root_equation_olympiad",
    display_name={"th": "สมการรากซ้อนที่ได้อัตราส่วนทอง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การถอดกรณฑ์ซ้อน",
)
class NestedRootEquation(WordProblem):
    def expr(self, rng: Random):
        k = rng.choice([1, 2, 3, 4, 5, 6, 7, 9, 10, 11])
        answer = root_tex(k)
        wrong = [t for t in dict.fromkeys([root_tex(k, sign=-1), root_tex(k, half=False), root_tex(k + 1), root_tex(2 * k)]) if t != answer]
        return MathDraw(
            rf"x=\sqrt{{x-\frac{{{k}}}{{x}}}}+\sqrt{{{k}-\frac{{{k}}}{{x}}}}",
            answer,
            prompt="จงหาจำนวนจริง x ทั้งหมดที่สอดคล้องกับสมการต่อไปนี้",
            hint="ย้ายรากหนึ่งไปอีกข้างแล้วยกกำลังสองสองครั้ง จะได้กำลังสองสมบูรณ์ (x² − x − k)² = 0 แล้วตรวจคำตอบ",
            distractors=wrong,
        )
