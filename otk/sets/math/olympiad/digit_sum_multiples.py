"""Digit sums of multiples and a modular obstruction."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def count_cofinite_digit_sum_moduli(limit: int) -> int:
    """Count n<=limit whose multiples attain all sufficiently large digit sums.

    Digit sum and number agree modulo 9. If 3 divides n, no multiple of n
    has digit sum congruent to 1 or 2 modulo 3, so infinitely many sums are
    absent. Otherwise n is invertible modulo 9. The nine multiples j*n,
    j=1..9, supply all digit-sum residues modulo 9. For every large k with
    10**k>n, the multiple n*(10**k-1) has digit sum 9*k. Concatenating it
    after an appropriate j*n yields every sufficiently large target sum.
    Thus exactly the n not divisible by 3 qualify.
    """
    return limit - limit // 3


@question_type(
    "math.digit_sum_cofinite_olympiad",
    display_name={"th": "ผลบวกเลขโดดของพหุคูณ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: เลขโดด",
)
class DigitSumCofinite(WordProblem):
    def expr(self, rng: Random):
        limit = rng.randint(30, 150)
        answer = count_cofinite_digit_sum_moduli(limit)
        return MathDraw(
            rf"1\le n\le {limit}",
            str(answer),
            prompt=("สำหรับจำนวนเต็มบวก n ให้ Sₙ เป็นเซตของผลบวกเลขโดดของ"
                    "พหุคูณบวกทั้งหมดของ n ในช่วงที่กำหนด มี n กี่ค่าที่ Sₙ "
                    "ขาดจำนวนเต็มบวกไปเพียงจำนวนจำกัด"),
            hint=(r"s(N)\equiv N\pmod 9;\quad "
                  r"s\!\left(n(10^k-1)\right)=9k\text{ เมื่อ }10^k>n"),
            distractors=[
                str(limit // 3),  # count the excluded multiples instead
                str(limit - limit // 9),  # exclude multiples of 9 only
                str(answer - 1),  # endpoint off by one
                str(limit),  # miss the mod-3 obstruction
            ],
        )
