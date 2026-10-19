"""MNOP is a rhombus of side PA/2, so its area is (PA/2)²·sin∠APB."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันที่สอง ข้อ 1",))


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def rhombus_area(tangent: int, chord: int) -> Fraction:
    """MN ∥ PB (midline of triangle APB) and MN = PB/2 = PA/2 = PM; the
    construction makes NO ∥ PA with PO = PA/2, so MNOP is a rhombus with
    side t/2 and angle ∠APB. sin∠APB = c√(4t² − c²)/(2t²) for PA = PB = t and
    AB = c, so the area is c√(4t² − c²)/8."""
    root = isqrt(4 * tangent * tangent - chord * chord)
    if root * root != 4 * tangent * tangent - chord * chord:
        raise ValueError("choose 4t² − c² a square")
    return Fraction(chord * root, 8)


CASES = tuple(
    (t, c) for t in range(2, 40) for c in range(1, 2 * t)
    if isqrt(4 * t * t - c * c) ** 2 == 4 * t * t - c * c
)


@question_type(
    "math.tangent_midpoint_rhombus_area_olympiad",
    display_name={"th": "พื้นที่รูปสี่เหลี่ยมขนมเปียกปูนจากเส้นสัมผัสสองเส้น"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สี่เหลี่ยมขนมเปียกปูน",
)
class TangentMidpointRhombusArea(WordProblem):
    def expr(self, rng: Random):
        t, c = rng.choice(CASES)
        answer = rhombus_area(t, c)
        root = isqrt(4 * t * t - c * c)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(c * root, 4), Fraction(c * root, 16), Fraction(t * t, 4), Fraction(c * root, 2), answer + 1]) if v != answer]
        return MathDraw(
            rf"PA=PB={t},\quad AB={c}",
            frac_tex(answer),
            prompt=(
                "PA, PB สัมผัสวงกลม ω ที่ A, B ให้ M, N เป็นจุดกึ่งกลางของ AP และ AB ต่อ MN ตัด ω ที่ C "
                "PC ตัด ω อีกครั้งที่ D และต่อ ND ตัด PB ที่ O ซึ่งทำให้ MNOP เป็นรูปสี่เหลี่ยมขนมเปียกปูน จงหาพื้นที่ของ MNOP"
            ),
            hint="ด้านของรูปขนมเปียกปูนยาว PA/2 และมุมที่ P คือ ∠APB หา sin∠APB จากรูปสามเหลี่ยมหน้าจั่ว APB",
            distractors=wrong,
        )
