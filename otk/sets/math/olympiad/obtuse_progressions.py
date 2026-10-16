"""Probability that a fixed-gap triple is an obtuse triangle."""

from __future__ import annotations

from fractions import Fraction
from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def obtuse_progression_probability(limit: int, gap: int) -> Fraction:
    """Choose three numbers from 1..limit without replacement."""
    if limit < 3 or gap < 1:
        raise ValueError("expected limit>=3 and gap>=1")
    # A triple a,a+d,a+2d is a triangle iff a>d. It is obtuse iff
    # (a+2d)^2 > a^2+(a+d)^2, equivalently a<3d.
    upper = min(3 * gap - 1, limit - 2 * gap)
    favorable = max(0, upper - gap)
    return Fraction(favorable, comb(limit, 3))


@question_type(
    "math.obtuse_progression_probability_olympiad",
    display_name={"th": "ความน่าจะเป็นของสามจำนวนห่างเท่ากันที่เป็นสามเหลี่ยมมุมป้าน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ความน่าจะเป็น",
)
class ObtuseProgressionProbability(WordProblem):
    def expr(self, rng: Random):
        gap = rng.randint(1, 4)
        limit = rng.randint(3 * gap + 1, 5 * gap + 12)
        probability = obtuse_progression_probability(limit, gap)
        answer = probability.numerator + probability.denominator
        total = comb(limit, 3)
        favorable = probability * total
        return MathDraw(
            rf"N={limit},\quad d={gap}",
            str(answer),
            prompt=("สุ่มเลือกจำนวนต่างกัน 3 จำนวนจาก 1 ถึง N อย่างเท่าเทียมกัน "
                    "ถ้าความน่าจะเป็นที่จำนวนทั้งสามเรียงเป็นลำดับเลขคณิตที่มีผลต่าง d "
                    "และเป็นความยาวด้านของสามเหลี่ยมมุมป้านเท่ากับ p/q ในรูปอย่างต่ำ "
                    "จงหา p+q"),
            hint=r"a>d,\qquad a<3d,\qquad a+2d\le N",
            distractors=[
                str(Fraction(favorable + 1, total).numerator + Fraction(favorable + 1, total).denominator),  # include boundary
                str(Fraction(max(0, favorable - 1), total).numerator + Fraction(max(0, favorable - 1), total).denominator),  # omit boundary
                str(favorable + total),  # forget to reduce
                str(probability.denominator),  # omit numerator
                str(Fraction(min(3 * gap - 1, limit - 2 * gap), total).numerator
                    + Fraction(min(3 * gap - 1, limit - 2 * gap), total).denominator),  # omit triangle inequality
            ],
        )
