"""O₁O₂ is constant when E on CD makes BE ∥ AD: it equals AB/(2 sin ∠ADC)."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2557, ข้อ 7",)
)

# sin of the reference angle as (rational, radicand): sin = q·√r
SINES = {30: (Fraction(1, 2), 1), 45: (Fraction(1, 2), 2), 60: (Fraction(1, 2), 3), 90: (Fraction(1), 1)}


def _reference(angle: int) -> int:
    return angle if angle <= 90 else 180 - angle


def surd_tex(q: Fraction, r: int) -> str:
    if q == 0:
        return "0"
    if r == 1:
        return str(q.numerator) if q.denominator == 1 else rf"\frac{{{q.numerator}}}{{{q.denominator}}}"
    top = ("" if q.numerator == 1 else str(q.numerator)) + rf"\sqrt{{{r}}}"
    return top if q.denominator == 1 else rf"\frac{{{top}}}{{{q.denominator}}}"


def over_two_sine(side: int, angle: int) -> tuple[Fraction, int]:
    """side/(2 sin angle), rationalised: 1/(q√r) = √r/(q·r)."""
    q, r = SINES[_reference(angle)]
    return Fraction(side) / (2 * q * r), r


def circumcenter_distance(side: int, angle: int) -> tuple[Fraction, int]:
    """∠BEP = ∠ADP, so PA = 2R₁ sin θ and PB = 2R₂ sin θ, and the radii make
    the same angle 90° − θ with the chords: a spiral similarity at P takes
    A, B to O₁, O₂ with ratio 1/(2 sin θ)."""
    return over_two_sine(side, angle)


@question_type(
    "math.parallel_chord_circumcenters_olympiad",
    display_name={"th": "ระยะระหว่างจุดศูนย์กลางวงกลมล้อมสองวงที่คงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมล้อมรูปสามเหลี่ยม",
)
class ParallelChordCircumcenters(WordProblem):
    def expr(self, rng: Random):
        side = rng.randint(2, 20)
        angle = rng.choice([30, 45, 60, 90, 120, 135, 150])
        answer = surd_tex(*circumcenter_distance(side, angle))
        q, r = SINES[_reference(angle)]
        cq, cr = SINES[90 - _reference(angle)] if _reference(angle) != 90 else (Fraction(0), 1)
        candidates = [
            surd_tex(Fraction(side), 1),
            surd_tex(Fraction(side, 2), 1),  # as if the angle were right
            surd_tex(side * q, r),  # multiply by sin instead of dividing
            surd_tex(*over_two_sine(2 * side, angle)),  # drop the factor 2
            surd_tex(Fraction(side) / (2 * cq * cr), cr) if cq else surd_tex(Fraction(2 * side), 1),  # cos for sin
            surd_tex(Fraction(side, 4), 1),
        ]
        wrong = [t for t in dict.fromkeys(candidates) if t != answer]
        return MathDraw(
            rf"AB={side},\quad \angle ADC={angle}^\circ",
            answer,
            prompt=(
                "ABCD เป็นรูปสี่เหลี่ยมนูน จุด E อยู่บนด้าน CD โดย BE ขนานกับ AD "
                "สำหรับจุด P บนด้าน CD ให้ O₁ และ O₂ เป็นจุดศูนย์กลางวงกลมล้อมรอบรูปสามเหลี่ยม APD และ BPE "
                "ความยาว O₁O₂ ไม่ขึ้นกับ P จงหาความยาวนี้"
            ),
            hint="∠BEP = ∠ADP ใช้กฎของไซน์ในวงกลมทั้งสองแล้วหาการหมุนขยายที่จุด P ซึ่งส่ง A, B ไป O₁, O₂",
            distractors=wrong,
        )
