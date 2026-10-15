"""Count codes with an initial digit, nonadjacent digits, and unique letters."""

from __future__ import annotations

from math import comb, perm
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def count_leading_digit_codes(letters: int, pool: int, digits: int) -> int:
    """Count codes with two repeatable digits and `letters` distinct letters."""
    if letters < 2 or pool < letters or digits < 1:
        raise ValueError("expected letters>=2, pool>=letters, digits>=1")
    # First digit is fixed at position 1; second digit has `letters`
    # possible positions from 3 through letters+2.
    return letters * perm(pool, letters) * digits**2


@question_type(
    "math.leading_digit_nonadjacent_codes_olympiad",
    display_name={"th": "นับรหัสขึ้นต้นด้วยตัวเลขและตัวเลขไม่ติดกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class LeadingDigitNonadjacentCodes(WordProblem):
    def expr(self, rng: Random):
        letters = rng.randint(3, 5)
        pool = rng.randint(letters, 7)
        digits = rng.randint(4, 10)
        ordered_letters = perm(pool, letters)
        answer = count_leading_digit_codes(letters, pool, digits)
        return MathDraw(
            rf"m={letters},\quad v={pool},\quad d={digits}",
            str(answer),
            prompt=("รหัสยาว m+2 ตำแหน่งประกอบด้วยตัวอักษร m ตัวจากตัวเลือก v ตัว "
                    "โดยตัวอักษรไม่ซ้ำ และตัวเลข 2 ตัวจากตัวเลือก d ตัว โดยตัวเลขซ้ำได้ "
                    "รหัสขึ้นต้นด้วยตัวเลข และตัวเลขสองตัวไม่อยู่ติดกัน "
                    "มีรหัสได้กี่แบบ"),
            hint="กำหนดตำแหน่งเลขตัวแรก แล้วเลือกตำแหน่งเลขตัวที่สอง",
            distractors=[
                str((letters + 1) * ordered_letters * digits**2),  # allow adjacent digits
                str(letters * ordered_letters * digits * (digits - 1)),  # forbid repeated digits
                str(letters * pool**letters * digits**2),  # allow repeated letters
                str(comb(letters + 1, 2) * ordered_letters * digits**2),  # omit leading-digit rule
            ],
        )
