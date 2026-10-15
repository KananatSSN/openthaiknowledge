"""Distinct sums of a few powers when their exponents may repeat."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def count_distinct_power_sums(base: int, labels: int, picks: int) -> int:
    """Count sums of `picks` powers drawn from base**0,...,base**(labels-1).

    When picks<base, the count of each power is a base digit, so the sum
    identifies the multiset of picks. At picks=base, a carry is possible
    only when all picks use the same power; these sums are distinct powers
    and cannot equal any uncarried sum of base picks. Hence the multiset map
    stays injective for picks<=base, and stars-and-bars counts the sums.
    """
    if base < 2 or labels < 1 or not 1 <= picks <= base:
        raise ValueError("expected base>=2, labels>=1, and 1<=picks<=base")
    return comb(labels + picks - 1, picks)


@question_type(
    "math.distinct_power_sums_olympiad",
    display_name={"th": "จำนวนผลบวกต่างกันของกำลังฐานเดียวกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class DistinctPowerSums(WordProblem):
    def expr(self, rng: Random):
        base = rng.randint(3, 6)
        labels = rng.randint(4, 10)
        picks = rng.randint(2, min(4, base))
        answer = count_distinct_power_sums(base, labels, picks)
        return MathDraw(
            rf"b={base},\quad k={labels},\quad t={picks},\quad"
            r"\mathcal{W}=\{b^0,b^1,\ldots,b^{k-1}\}",
            str(answer),
            prompt=("เลือกจำนวนจากเซต W ทั้งหมด t ครั้ง โดยเลือกค่าเดิมซ้ำได้ "
                    "ผลบวกของจำนวนที่เลือกมีค่าต่างกันได้ทั้งหมดกี่ค่า"),
            hint=r"t\le b,\qquad c_0+\cdots+c_{k-1}=t",
            distractors=[
                str(labels**picks),  # count ordered draws
                str(comb(labels, picks)),  # prohibit repetitions
                str(comb(labels + picks - 2, picks)),  # omit one label
                str(comb(labels + picks, picks)),  # add one label
            ],
        )
