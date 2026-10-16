"""Independent checks for added ม.3 similarity applications."""

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.api import REGISTRY, catalog
from otk.tests.test_math_chapters import _val

KEYS = (
    "math.similar_parallel_segment_m3",
    "math.similar_remaining_area_m3",
    "math.similar_side_from_areas_m3",
)


def _solve_from_stem(key, stem):
    if key == KEYS[0]:
        ad, db, ae = map(int, re.search(r"AD = (\d+), DB = (\d+), AE = (\d+)", stem).groups())
        return Fraction(db * ae, ad)
    if key == KEYS[1]:
        inner, whole = map(int, re.search(r"AD : AB = (\d+) : (\d+)", stem).groups())
        return Fraction(whole * whole - inner * inner, whole * whole)
    small_area, large_area, small_side = map(int, re.search(
        r"รูปเล็กมีพื้นที่ (\d+).*รูปใหญ่มีพื้นที่ (\d+).*รูปเล็กยาว (\d+)", stem).groups())
    ratio_squared = Fraction(large_area, small_area)
    root_num, root_den = math.isqrt(ratio_squared.numerator), math.isqrt(ratio_squared.denominator)
    assert root_num ** 2 == ratio_squared.numerator
    assert root_den ** 2 == ratio_squared.denominator
    return Fraction(small_side * root_num, root_den)


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(120))
def test_answer_and_distractors(key, seed):
    q = REGISTRY[key].generate(Random(seed))
    expected = float(_solve_from_stem(key, q.stem[0].text))
    assert math.isclose(_val(q.choices[q.answer].content[0].tex), expected, rel_tol=1e-12)
    assert len(q.choices) == 4
    assert all(m is not None for i, m in enumerate(q.mistakes) if i != q.answer)
    assert all(not math.isclose(_val(choice.content[0].tex), expected, rel_tol=1e-12)
               for i, choice in enumerate(q.choices) if i != q.answer)


@pytest.mark.parametrize("key", KEYS)
def test_catalog_stage_and_variety(key):
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.3", "ความคล้าย", 3,
    )
    stems = {REGISTRY[key].generate(Random(seed)).stem[0].text for seed in range(200)}
    assert len(stems) >= 90
