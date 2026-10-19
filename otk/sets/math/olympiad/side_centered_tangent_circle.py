"""A circle centred on BC touching AB and AC has radius 2Δ/(AB + AC)."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 2",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def surd_tex(square: Fraction) -> str:
    """TeX for √square in the form (k/d)√m with m squarefree."""
    inside = square.numerator * square.denominator
    outside, f = 1, 2
    while f * f <= inside:
        while inside % (f * f) == 0:
            inside //= f * f
            outside *= f
        f += 1
    coef = Fraction(outside, square.denominator)
    if inside == 1:
        return frac_tex(coef)
    root = rf"\sqrt{{{inside}}}"
    top = ("" if coef.numerator == 1 else str(coef.numerator)) + root
    return top if coef.denominator == 1 else rf"\frac{{{top}}}{{{coef.denominator}}}"


def radius_square(a: int, b: int, c: int) -> Fraction:
    """The centre is the foot of the bisector from A; splitting ABC there gives
    Δ = r(AB + AC)/2. With 16Δ² from Heron, r² = 16Δ²/(4(b + c)²)
    (source: 2, 3, 4 → r = 3√15/10)."""
    heron = (a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c)
    return Fraction(heron, 4 * (b + c) ** 2)


@question_type(
    "math.side_centered_tangent_circle_olympiad",
    display_name={"th": "รัศมีวงกลมที่มีจุดศูนย์กลางบนด้านและสัมผัสอีกสองด้าน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: เส้นแบ่งครึ่งมุม",
)
class SideCenteredTangentCircle(WordProblem):
    def expr(self, rng: Random):
        while True:
            a, b, c = rng.randint(3, 14), rng.randint(2, 12), rng.randint(2, 12)
            if b + c > a and a + b > c and a + c > b and b != c:
                break
        answer = radius_square(a, b, c)
        heron = (a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c)
        wrong = [surd_tex(v) for v in dict.fromkeys([Fraction(heron, 4 * (a + b + c) ** 2), Fraction(heron, 16 * (b + c) ** 2), Fraction(heron, 4 * a * a), Fraction(heron, (b + c) ** 2)]) if v != answer]
        return MathDraw(
            rf"AB={c},\quad CA={b},\quad BC={a}",
            surd_tex(answer),
            prompt="รูปสามเหลี่ยม ABC มีความยาวด้านดังนี้ จงหารัศมีของวงกลมที่มีจุดศูนย์กลางอยู่บนด้าน BC และสัมผัสด้าน AB และ AC",
            hint="แบ่งรูปสามเหลี่ยมด้วยเส้นจาก A ไปยังจุดศูนย์กลาง พื้นที่ = r(AB + AC)/2 และหาพื้นที่จากสูตรเฮรอน",
            distractors=wrong,
        )
