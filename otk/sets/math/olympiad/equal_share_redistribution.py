"""Recover an original equally shared population from two redistributions."""

from __future__ import annotations

from fractions import Fraction
from math import gcd, lcm
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def original_population(add_a: int, drop_a: int, add_b: int, drop_b: int) -> tuple[int, int, int]:
    """Return original containers, each share, and total from two observations."""
    if min(add_a, drop_a, add_b, drop_b) < 1 or add_a >= add_b:
        raise ValueError("invalid redistribution observations")
    denominator = add_b * drop_a - add_a * drop_b
    if denominator == 0:
        raise ValueError("observations do not determine a unique population")
    containers = Fraction(add_a * add_b * (drop_b - drop_a), denominator)
    share = Fraction(drop_a * (containers + add_a), add_a)
    total = containers * share
    if min(containers, share, total) <= 0 or any(x.denominator != 1 for x in (containers, share, total)):
        raise ValueError("observations do not give a positive whole-number population")
    return int(containers), int(share), int(total)


@question_type(
    "math.equal_share_redistribution_olympiad",
    display_name={"th": "หาจำนวนทั้งหมดจากการแบ่งใหม่สองครั้ง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงเส้น",
)
class EqualShareRedistribution(WordProblem):
    def expr(self, rng: Random):
        ratio = rng.randint(4, 8)
        added = rng.randint(2, 6)
        scale = rng.randint(1, 2)
        containers = ratio * added
        share = lcm(ratio + 1, (ratio + 2) // gcd(2, ratio + 2)) * scale
        drop_a = share // (ratio + 1)
        drop_b = 2 * share // (ratio + 2)
        _, _, answer = original_population(added, drop_a, 2 * added, drop_b)
        return MathDraw(
            rf"a={added},\quad d_1={drop_a},\quad d_2={drop_b}",
            str(answer),
            prompt=("เดิมแบ่งลูกไก่จำนวนหนึ่งลงกรงเท่า ๆ กัน ถ้าเพิ่มกรงอีก a กรงแล้วแบ่งใหม่ "
                    "จำนวนลูกไก่ต่อกรงจะลดลง d_1 ตัว ถ้าเพิ่มกรงจากเดิมอีก 2a กรงแล้วแบ่งใหม่ "
                    "จำนวนลูกไก่ต่อกรงจะลดลง d_2 ตัว เดิมมีลูกไก่ทั้งหมดกี่ตัว"),
            hint="ให้จำนวนกรงเดิมเป็น c และจำนวนต่อกรงเป็น k แล้วเทียบ ck=(c+a)(k-d_1)=(c+2a)(k-d_2)",
            distractors=[
                str(containers * (share - drop_a)),  # treat first new share as original
                str(containers * (share - drop_b)),  # treat second new share as original
                str((containers + added) * share),  # treat added cages as original
                str((containers + 2 * added) * share),  # count both extra groups with old share
            ],
        )
