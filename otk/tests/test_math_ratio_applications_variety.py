"""Independent checks for added ม.1 ratio applications."""

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.api import REGISTRY, catalog
from otk.tests.test_math_chapters import _val

KEYS = (
    "math.inverse_work_proportion_m1",
    "math.map_area_scale_m1",
    "math.ratio_after_adding_m1",
)


def _solve_from_stem(key, stem):
    if key == KEYS[0]:
        old_workers, old_days, new_workers = map(int, re.search(
            r"ช่าง (\d+) คน.*ใน (\d+) วัน.*ช่าง (\d+) คน", stem).groups())
        # Simulate work one worker-day at a time; the task ends once all units are done.
        remaining = old_workers * old_days
        days = 0
        while remaining > 0:
            remaining -= new_workers
            days += 1
        assert remaining == 0
        return Fraction(days)
    if key == KEYS[1]:
        scale, length, width = re.search(
            r"1 : ([\d,]+).*ยาว (\d+) เซนติเมตร กว้าง (\d+) เซนติเมตร", stem).groups()
        scale = int(scale.replace(",", ""))
        length, width = int(length), int(width)
        real_length_m = Fraction(length * scale, 100)
        real_width_m = Fraction(width * scale, 100)
        return real_length_m * real_width_m / 1_000_000
    red, blue, added = map(int, re.search(
        r"น้ำสีแดง (\d+) ลิตร.*น้ำสีน้ำเงิน (\d+) ลิตร.*อีก (\d+) ลิตร", stem).groups())
    return Fraction(red + added, red + blue + added)


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(120))
def test_answer_and_named_choices(key, seed):
    q = REGISTRY[key].generate(Random(seed))
    expected = _solve_from_stem(key, q.stem[0].text)
    actual = _val(q.choices[q.answer].content[0].tex)
    assert math.isclose(actual, float(expected), rel_tol=1e-12)
    assert len(q.choices) == 4
    assert all(m is not None for i, m in enumerate(q.mistakes) if i != q.answer)
    assert all(not math.isclose(_val(choice.content[0].tex), float(expected), rel_tol=1e-12)
               for i, choice in enumerate(q.choices) if i != q.answer)


@pytest.mark.parametrize("key", KEYS)
def test_stage_and_variety(key):
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.1", "อัตราส่วนและสัดส่วน", 3,
    )
    stems = {REGISTRY[key].generate(Random(seed)).stem[0].text for seed in range(200)}
    assert len(stems) >= 90
