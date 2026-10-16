"""Directed diagonal intersection from equal arm lengths in a triangle."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def diagonal_intersection_parameter(ab: int, ad: int, arm: int) -> Fraction:
    """P=B+lambda(D-B) for P=ST intersect BD."""
    if ab <= 0 or ad <= 0 or ab == ad or not 0 < arm < min(ab, ad):
        raise ValueError("distinct positive sides and an interior arm are required")
    return Fraction(ab - arm, ab - ad)


@question_type(
    "math.equal_arm_diagonal_intersection_olympiad",
    display_name={"th": "จุดตัดเส้นทแยงมุมจากแขนยาวเท่ากัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รูปหลายเหลี่ยม",
)
class EqualArmDiagonalIntersection(WordProblem):
    def expr(self, rng: Random):
        while True:
            ab, ad = rng.sample(range(4, 21), 2)
            arm = rng.randint(1, min(ab, ad) - 1)
            answer = diagonal_intersection_parameter(ab, ad, arm)
            distractors = [
                Fraction(ab - arm, ad - arm),  # use unsigned BP/PD instead of lambda
                Fraction(ad - arm, ab - ad),  # swap the two unmarked side tails
                Fraction(arm, ab - ad),  # use AT rather than BT
                Fraction(ab - arm, ad - ab),  # reverse the directed diagonal
            ]
            if len({answer, *distractors}) == 5:
                break
        return MathDraw(
            rf"AB={ab},\quad AD={ad},\quad AT=AS={arm}",
            str(answer),
            prompt=(
                "ในสามเหลี่ยม ABD จุด T และ S อยู่ภายในด้าน AB และ AD ตามลำดับ "
                "โดย AT=AS ให้เส้นตรง ST ตัดเส้นตรง BD ที่ P และกำหนด "
                "P=B+λ(D−B) จงหา λ"
            ),
            hint="เทียบพิกัดของ S,T ในฐาน A,B,D แล้วให้สัมประสิทธิ์ของ A เป็นศูนย์ที่ P",
            distractors=[str(value) for value in distractors],
        )
