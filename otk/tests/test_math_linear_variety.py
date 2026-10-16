"""Check the new linear stories by enumerating their physical situations."""

from fractions import Fraction
from random import Random

import pytest

from otk.api import REGISTRY, catalog
from otk.kit.math_problems import frac_tex
from otk.sets.math.m1.linear_equations import (
    _fee_parameters,
    _remaining_parameters,
    _transfer_parameters,
)

KEYS = (
    "math.linear_fee_comparison_m1",
    "math.linear_remaining_fraction_m1",
    "math.linear_transfer_m1",
)


def _brute_answer(key, seed):
    if key == KEYS[0]:
        fee_a, rate_a, fee_b, rate_b = _fee_parameters(Random(seed))
        matches = [x for x in range(501) if fee_a + rate_a * x == fee_b + rate_b * x]
    elif key == KEYS[1]:
        numerator, denominator, extra, remaining = _remaining_parameters(Random(seed))
        matches = [x for x in range(501)
                   if x - Fraction(numerator * x, denominator) - extra == remaining]
    else:
        second, transferred, multiplier = _transfer_parameters(Random(seed))
        matches = [x for x in range(transferred, 501)
                   if second + transferred == multiplier * (x - transferred)]
    assert len(matches) == 1
    return matches[0]


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(100))
def test_story_answer_by_enumerating_original_situation(key, seed):
    expected = str(_brute_answer(key, seed))
    instance = REGISTRY[key]
    draw = instance.expr(Random(seed))
    assert draw.answer_tex == expected
    question = instance.generate(Random(seed))
    assert question.choices[question.answer].content[0].tex == expected
    assert len(question.choices) == 4
    assert any(question.mistakes)


@pytest.mark.parametrize("key", KEYS)
def test_stories_have_three_contexts_and_many_distinct_items(key):
    draws = [REGISTRY[key].expr(Random(seed)) for seed in range(300)]
    assert len({draw.prompt for draw in draws}) >= 250
    contexts = {draw.prompt.split(" ")[0] for draw in draws}
    assert len(contexts) == 3


def test_new_sets_are_application_in_the_existing_m1_unit():
    rows = {row["key"]: row for row in catalog()}
    for key in KEYS:
        row = rows[key]
        assert row["level"] == "ม.1"
        assert row["topic"] == "สมการเชิงเส้น"
        assert row["learning_stage"] == 3


def test_distractors_are_calculations_of_specific_mistakes():
    # Pin one example per story, including an operation-order slip and a
    # transfer that changes both containers. Fractions stay exact.
    for seed in range(30):
        a, r, b, s = _fee_parameters(Random(seed))
        draw = REGISTRY[KEYS[0]].expr(Random(seed))
        assert frac_tex(Fraction(a - b, r + s)) in draw.distractors
        n, d, extra, left = _remaining_parameters(Random(seed))
        draw = REGISTRY[KEYS[1]].expr(Random(seed))
        assert frac_tex(Fraction(left * d, d - n) + extra) in draw.distractors
        second, transferred, multiplier = _transfer_parameters(Random(seed))
        draw = REGISTRY[KEYS[2]].expr(Random(seed))
        assert frac_tex(Fraction(second + transferred, multiplier)) in draw.distractors
