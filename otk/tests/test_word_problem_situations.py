"""The word-problem sets enriched in batch D: enough situations, and answers
re-derived for the sets that had no check of their own."""

from __future__ import annotations

import re
from decimal import Decimal
from fractions import Fraction
from random import Random

import pytest

from otk.core import generate
from otk.kit import story as _story

SEEDS = range(300)
ENRICHED = [
    "math.length_word_problem_p2", "math.fraction_word_problem_p4",
    "math.rectangle_word_problem_p4", "math.decimal_word_problem_p5",
    "math.percent_of_quantity_p5", "math.fraction_word_muldiv_p5",
    "math.gcd_word_problem_p6", "math.ratio_word_problem_p6", "math.circle_word_problem_p6",
    "math.percent_word_problem_m1", "math.prism_cylinder_volume_word_m2",
    "math.system_setup_m3", "math.solid_word_problem_m3", "math.arithmetic_sequence_word_m5",
]
_NAMES = sorted(set(_story.NAMES), key=len, reverse=True)


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _answer(q) -> str:
    c = q.choices[q.answer]
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _nums(s: str) -> list[Decimal]:
    return [Decimal(n) for n in re.findall(r"\d+(?:\.\d+)?", s.replace(",", ""))]


def _shape(s: str) -> str:
    for n in _NAMES:
        s = s.replace(n, "N")
    return re.sub(r"\d+(?:[.,]\d+)*", "#", s)


@pytest.mark.parametrize("key", ENRICHED)
def test_at_least_five_situations(key):
    shapes = {_shape(_stem(generate(key, Random(seed)))) for seed in SEEDS}
    assert len(shapes) >= 5, (key, len(shapes))


def test_decimal_two_step_p5():
    for seed in SEEDS:
        q = generate("math.decimal_word_problem_p5", Random(seed))
        s, ans = _stem(q), Decimal(_answer(q).replace(",", ""))
        n = _nums(s)
        if "วิ่งรอบ" in s:
            assert ans == n[0] * n[1] * n[2]
        elif "ราคารวม" in s:
            assert ans == n[1] / n[0] * n[2]
        elif "ด้าย" in s:
            assert ans == n[0] * n[1] + n[2]


def test_volumes_m2():
    for seed in SEEDS:
        q = generate("math.prism_cylinder_volume_word_m2", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = [int(x) for x in _nums(s.replace("22/7", ""))]
        if "ครึ่งถัง" in s:
            assert ans == Fraction(22, 7) * n[0] ** 2 * n[1] / 2
        elif "รางน้ำ" in s:
            assert ans == Fraction(n[0] + n[1], 2) * n[2] * n[3]
        elif "ตู้ปลา" in s:
            assert ans * n[0] * n[1] == n[2]


def test_system_setup_m3():
    for seed in SEEDS:
        q = generate("math.system_setup_m3", Random(seed))
        s, eqs = _stem(q), _answer(q)
        n = [int(x) for x in _nums(s)]
        if "บัตร" in s:
            people, money, pa, pc = n[:4]
            assert eqs == rf"x + y = {people},\quad {pa}x + {pc}y = {money}"
        elif "อายุพ่อ" in s:
            total, times = n[:2]
            assert eqs == rf"x + y = {total},\quad x = {times}y"
        elif "รูปสี่เหลี่ยมผืนผ้า" in s:
            per, extra = n[:2]
            assert eqs == rf"2x + 2y = {per},\quad x - y = {extra}"


def test_solids_m3():
    for seed in SEEDS:
        q = generate("math.solid_word_problem_m3", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = [int(x) for x in _nums(s.replace("22/7", ""))]
        if "น้ำในทรงกระบอกสูง" in s:
            r, h = n[:2]
            assert ans * 3 == h                       # ⅓πr²h = πr²·x
        elif "หล่อเป็นกรวย" in s:
            r = n[0]
            assert Fraction(4, 3) * r ** 3 == Fraction(1, 3) * r ** 2 * ans
        elif "ถ้วยน้ำดื่ม" in s:
            r, h = n[:2]
            assert ans == Fraction(1, 3) * Fraction(22, 7) * r * r * h


def test_sequences_m5():
    for seed in SEEDS:
        q = generate("math.arithmetic_sequence_word_m5", Random(seed))
        s = _stem(q)
        ans = int(_answer(q).replace("{,}", ""))
        n = [int(x) for x in _nums(s)]
        if "ท่อนไม้" in s:
            bottom, _, rows = n[:3]
            assert ans == sum(bottom - k for k in range(rows))
        elif "ขึ้นเงินเดือน" in s:
            start, rise, year = n[:3]
            assert ans == start + (year - 1) * rise
        elif "ฝึกวิ่ง" in s:
            first, step, goal = n[:3]
            assert first + (ans - 1) * step == goal
