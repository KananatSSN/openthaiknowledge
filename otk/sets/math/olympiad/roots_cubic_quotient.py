"""Simplify a symmetric cubic quotient using quadratic-root identities."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def cubic_root_quotient(root_sum: int, root_product: int) -> int:
    """Value of (a^3+b)/(a-b)+(b^3+a)/(b-a)."""
    return root_sum**2 - root_product - 1


@question_type(
    "math.roots_cubic_quotient_olympiad",
    display_name={"th": "ผลหารกำลังสามจากรากสมการกำลังสอง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการกำลังสอง",
)
class RootsCubicQuotient(WordProblem):
    def expr(self, rng: Random):
        roots = tuple(value for value in range(-12, 13) if value != 0)
        a, b = rng.sample(roots, 2)
        root_sum = a + b
        root_product = a * b
        answer = cubic_root_quotient(root_sum, root_product)
        mistaken = [
            root_sum**2 - root_product,  # omit the -1 from linear terms
            root_sum**2 + root_product - 1,  # use wrong sign for ab
            root_sum**2 - 2 * root_product - 1,  # use a^2+b^2 in place of a^2+ab+b^2
            root_sum**2 - root_product + 1,  # wrong sign for the constant
            root_sum**2 - root_product - 2,  # subtract both linear terms separately
        ]
        distractors = [str(value) for value in dict.fromkeys(mistaken) if value != answer]
        return MathDraw(
            rf"x^2-({root_sum})x+({root_product})=0",
            str(answer),
            prompt=("ให้ a และ b เป็นรากจริงที่แตกต่างกันของสมการกำลังสองต่อไปนี้ "
                    "จงหาค่า (a^3+b)/(a-b)+(b^3+a)/(b-a)"),
            hint="รวมเศษส่วนโดยใช้ b-a=-(a-b) แล้วแทน a+b และ ab",
            distractors=distractors,
        )
