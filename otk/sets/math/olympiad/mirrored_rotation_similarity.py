"""A similarity from opposite rays and equal outward rotations."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def mirrored_rotation_ratio(ab: int, ac: int) -> Fraction:
    """Return FR/EP when AE/AF = AC/AB and AP/AR = AC/AB."""
    if ab <= 0 or ac <= 0:
        raise ValueError("lengths must be positive")
    return Fraction(ab, ac)


@question_type(
    "math.mirrored_rotation_similarity_olympiad",
    display_name={"th": "อัตราส่วนจากการหมุนออกนอกมุมสองด้าน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต",
)
class MirroredRotationSimilarity(WordProblem):
    def expr(self, rng: Random):
        ab, ac = rng.sample(range(3, 13), 2)
        angle = rng.choice((30, 40, 50, 60))
        rotation = rng.choice((20, 30, 45, 60))
        answer = mirrored_rotation_ratio(ab, ac)
        return MathDraw(
            rf"AB={ab},\quad AC={ac},\quad \angle BAC={angle}^\circ,\quad \phi={rotation}^\circ",
            str(answer),
            prompt=(
                "ให้ E อยู่บนรังสีตรงข้าม AB และ F อยู่บนรังสีตรงข้าม AC "
                "โดย AE/AF=AC/AB หมุนเวกเตอร์ AC รอบ A ออกนอกมุม BAC "
                "ไปยัง AP ด้วยมุม φ และหมุน AB ออกอีกด้านไปยัง AR ด้วยมุม φ "
                "จงหาอัตราส่วน FR/EP"
            ),
            hint="เปรียบเทียบสามเหลี่ยม AEP และ AFR โดยใช้ด้านสองคู่กับมุมระหว่างด้าน",
            distractors=[
                str(Fraction(ac, ab)),  # reverse the corresponding sides
                "1",  # mistake equal rotations for equal opposite segments
                str(Fraction(ab + ac, ac)),  # add a side to the numerator
                str(Fraction(ab, ab + ac)),  # use a sum for the denominator
            ],
        )
