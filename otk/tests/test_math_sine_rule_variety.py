"""Independent trigonometric checks for the added ม.5 sine-rule questions."""

import math
import re
from random import Random

import pytest

from otk.api import REGISTRY, catalog
from otk.sets.math.m5.law_of_sines import (
    _SSA_LABELS,
    _ssa_parameters,
)
from otk.tests.test_math_chapters import _val

KEYS = (
    "math.sine_rule_circumradius_m5",
    "math.sine_rule_area_from_angles_m5",
    "math.sine_rule_ambiguous_case_m5",
)


def _triangles_from_ssa(angle, a, b):
    ratio = b * math.sin(math.radians(angle)) / a
    if ratio > 1 and not math.isclose(ratio, 1, abs_tol=1e-12):
        return []
    if math.isclose(ratio, 1, abs_tol=1e-12):
        return [90.0]
    acute = math.degrees(math.asin(ratio))
    return [candidate for candidate in (acute, 180 - acute)
            if angle + candidate < 180 - 1e-10]


@pytest.mark.parametrize("seed", range(120))
def test_circumradius_from_extended_sine_rule(seed):
    q = REGISTRY[KEYS[0]].generate(Random(seed))
    angle, side = map(int, re.search(r"∠A = (\d+)°.*ยาว (\d+) เซนติเมตร", q.stem[0].text).groups())
    expected = side / (2 * math.sin(math.radians(angle)))
    actual = _val(q.choices[q.answer].content[0].tex)
    assert math.isclose(actual, expected, rel_tol=1e-12)
    assert all(not math.isclose(_val(choice.content[0].tex), expected, rel_tol=1e-12)
               for i, choice in enumerate(q.choices) if i != q.answer)
    assert len(q.choices) == 4 and any(q.mistakes)


@pytest.mark.parametrize("seed", range(120))
def test_area_from_ordinary_sines(seed):
    q = REGISTRY[KEYS[1]].generate(Random(seed))
    A, B, a = map(int, re.search(r"∠A = (\d+)°, ∠B = (\d+)°.*ยาว (\d+) เซนติเมตร",
                               q.stem[0].text).groups())
    C = 180 - A - B
    sine = lambda degrees: math.sin(math.radians(degrees))
    expected = a * a * sine(B) * sine(C) / (2 * sine(A))
    actual = _val(q.choices[q.answer].content[0].tex)
    assert math.isclose(actual, expected, rel_tol=1e-12)
    assert all(not math.isclose(_val(choice.content[0].tex), expected, rel_tol=1e-12)
               for i, choice in enumerate(q.choices) if i != q.answer)
    assert len(q.choices) == 4 and any(q.mistakes)


@pytest.mark.parametrize("seed", range(160))
def test_ambiguous_case_by_solving_both_candidate_angles(seed):
    angle, a, b, _ = _ssa_parameters(Random(seed))
    angles = _triangles_from_ssa(angle, a, b)
    if not angles:
        expected = _SSA_LABELS[0]
    elif len(angles) == 2:
        expected = _SSA_LABELS[3]
    elif math.isclose(angles[0], 90):
        expected = _SSA_LABELS[2]
    else:
        assert angles[0] < 90
        expected = _SSA_LABELS[1]
    q = REGISTRY[KEYS[2]].generate(Random(seed))
    assert q.choices[q.answer].content[0].text == expected
    assert len(q.choices) == 4 and any(q.mistakes)


@pytest.mark.parametrize("key", KEYS)
def test_variety_and_application_stage(key):
    stems = {REGISTRY[key].generate(Random(seed)).stem[0].text for seed in range(300)}
    assert len(stems) >= 90
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.5", "กฎของไซน์", 3,
    )


def test_all_ssa_outcomes_are_drawn():
    outcomes = {_ssa_parameters(Random(seed))[3] for seed in range(200)}
    assert outcomes == {0, 1, 2, 3}
