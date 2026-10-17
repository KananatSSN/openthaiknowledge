"""√(a² + b² − √2ab) + √(b² + c² − √2bc) ≥ √(a² + c²): equality at b = √2ac/(a + c)."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 4",))


def equality_b(a: int, c: int) -> Fraction:
    """Points at distances a, b, c on rays at 0°, 45°, 90°: the left side is a
    broken path from the first to the third, the right side the straight
    segment. Equality when the middle point lies on that segment, i.e. b is
    the 45° bisector length √2·ac/(a + c). Returns the coefficient of √2."""
    return Fraction(a * c, a + c)


def sqrt2_tex(v: Fraction) -> str:
    top = ("" if v.numerator == 1 else str(v.numerator)) + r"\sqrt{2}"
    return top if v.denominator == 1 else rf"\frac{{{top}}}{{{v.denominator}}}"


@question_type(
    "math.folded_angle_distance_equality_olympiad",
    display_name={"th": "กรณีเท่ากันในอสมการระยะทางสองช่วงมุม 45°"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class FoldedAngleDistanceEquality(WordProblem):
    def expr(self, rng: Random):
        a, c = rng.randint(1, 12), rng.randint(1, 12)
        answer = equality_b(a, c)
        wrong = [sqrt2_tex(v) for v in dict.fromkeys([Fraction(a + c, 2), Fraction(a * c, a + c) * 2, Fraction(a * c, 2 * (a + c)), Fraction(a + c, 4)]) if v != answer]
        wrong.append(rf"\sqrt{{{a * c}}}")
        return MathDraw(
            rf"a={a},\quad c={c}",
            sqrt2_tex(answer),
            prompt="สำหรับ a, c ที่กำหนด จงหา b > 0 ที่ทำให้ √(a² + b² − √2·ab) + √(b² + c² − √2·bc) = √(a² + c²)",
            hint="มอง √(a² + b² − √2ab) เป็นระยะระหว่างจุดบนรังสีที่ทำมุม 45° แล้วใช้อสมการสามเหลี่ยม",
            distractors=list(dict.fromkeys(wrong)),
        )
