"""AD ∥ BC iff AB/CD = MP/NQ, so in a trapezoid NQ = MP·CD/AB."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 9",)
)


def midpoint_distance(ab: int, cd: int, mp: int) -> Fraction:
    """MP·CD = [ACD] + [BCD] and NQ·AB = [ABC] + [ABD]; with
    [ABC] + [ACD] = [ABD] + [BCD], the two agree iff [ABC] = [BCD], that is,
    iff AD ∥ BC."""
    return Fraction(mp * cd, ab)


def _num(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


@question_type(
    "math.trapezoid_midpoint_distances_olympiad",
    display_name={"th": "ระยะจากจุดกึ่งกลางด้านถึงด้านตรงข้ามในรูปสี่เหลี่ยมคางหมู"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สี่เหลี่ยมคางหมู",
)
class TrapezoidMidpointDistances(WordProblem):
    def expr(self, rng: Random):
        ab = rng.randint(3, 15)
        cd = rng.choice([v for v in range(3, 16) if v != ab])
        mp = rng.randint(2, 12)
        answer = midpoint_distance(ab, cd, mp)
        wrong = [_num(v) for v in dict.fromkeys([
            Fraction(mp * ab, cd),  # ratio upside down
            Fraction(mp),  # assume the distances are equal
            Fraction(mp * (ab + cd), 2 * ab),
            Fraction(mp * cd, ab) + 1,
            Fraction(cd * ab, mp),
        ]) if v != answer]
        return MathDraw(
            rf"AB={ab},\quad CD={cd},\quad MP={mp}",
            _num(answer),
            prompt=(
                "ABCD เป็นรูปสี่เหลี่ยมนูนที่ AD ขนานกับ BC ให้ M, N เป็นจุดกึ่งกลางของ AB, CD "
                "MP ตั้งฉากกับเส้นตรง CD ที่ P และ NQ ตั้งฉากกับเส้นตรง AB ที่ Q จงหา NQ"
            ),
            hint="MP·CD = [ACD] + [BCD] และ NQ·AB = [ABC] + [ABD] เมื่อ AD ∥ BC จะได้ [ABC] = [BCD]",
            distractors=wrong,
        )
