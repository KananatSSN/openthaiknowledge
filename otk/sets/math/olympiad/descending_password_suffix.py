"""Find feasible password endings under parity and descending-order rules."""

from __future__ import annotations

from itertools import combinations
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def possible_suffixes(target: int) -> frozenset[str]:
    """Return feasible final-five strings for the ten-digit partition puzzle."""
    odds = (1, 3, 5, 7, 9)
    evens = (0, 2, 4, 6, 8)
    endings = set()
    for odd_prefix in combinations(odds, 4):
        for even_middle in combinations(evens, 3):
            tail = sorted(set(range(10)) - set(odd_prefix) - set(even_middle), reverse=True)
            if sum(tail) == target:
                suffix = sorted(even_middle, reverse=True)[1:] + tail
                endings.add("".join(map(str, suffix)))
    return frozenset(endings)


def mistaken_suffixes(valid: str) -> list[str]:
    """Make endings with wrong even order, tail order, uniqueness, or sum."""
    even_order = valid[1] + valid[0] + valid[2:]
    tail_order = valid[:2] + valid[3] + valid[2] + valid[4]
    repeated_digit = valid[:4] + valid[0]
    wrong_sum = valid[:4] + next(str(digit) for digit in range(10) if str(digit) not in valid)
    return [even_order, tail_order, repeated_digit, wrong_sum]


@question_type(
    "math.descending_password_suffix_olympiad",
    display_name={"th": "รหัสผ่านที่เรียงเลขโดดตามเงื่อนไข"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class DescendingPasswordSuffix(WordProblem):
    def expr(self, rng: Random):
        target = rng.choice(tuple(range(5, 22, 2)))
        valid = rng.choice(sorted(possible_suffixes(target)))
        return MathDraw(
            rf"S={target}",
            valid,
            prompt=("ใช้เลขโดด 0 ถึง 9 อย่างละหนึ่งครั้งสร้างรหัสสิบหลัก โดยสี่หลักแรกเป็นเลขคี่เรียงจากมากไปน้อย "
                    "สามหลักถัดมาเป็นเลขคู่เรียงจากมากไปน้อย และสามหลักสุดท้ายเรียงจากมากไปน้อย "
                    "โดยมีผลบวกเท่ากับ S ข้อใดอาจเป็นเลขโดดห้าหลักสุดท้ายของรหัส"),
            hint="เลือกเลขคี่สี่ตัวและเลขคู่สามตัวก่อน แล้วตรวจเลขที่เหลือสามตัว",
            distractors=mistaken_suffixes(valid),
        )
