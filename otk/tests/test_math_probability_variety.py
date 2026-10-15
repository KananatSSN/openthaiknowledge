"""Enumerate the outcomes behind the new ม.3 probability sets."""

from fractions import Fraction
from random import Random

import pytest

from otk.api import REGISTRY, catalog
from otk.kit.math_problems import frac_tex
from otk.sets.math.m3.basic_probability import (
    _card_union_parameters,
    _target_probability_parameters,
    _two_draw_parameters,
)

KEYS = (
    "math.probability_number_card_or_m3",
    "math.probability_two_colours_without_replacement_m3",
    "math.probability_add_balls_m3",
)


def _answer_by_enumeration(key, seed):
    rng = Random(seed)
    if key == KEYS[0]:
        count, first, second = _card_union_parameters(rng)
        cards = range(1, count + 1)
        return frac_tex(Fraction(sum(n % first == 0 or n % second == 0 for n in cards), count))
    if key == KEYS[1]:
        red, blue, same = _two_draw_parameters(rng)
        colours = ["R"] * red + ["B"] * blue
        outcomes = [(colours[i], colours[j]) for i in range(len(colours))
                    for j in range(len(colours)) if i != j]
        hits = sum((a == b) == same for a, b in outcomes)
        return frac_tex(Fraction(hits, len(outcomes)))
    red, blue, added = _target_probability_parameters(rng)
    target = Fraction(red + added, red + blue + added)
    matches = [n for n in range(1, 101) if Fraction(red + n, red + blue + n) == target]
    assert matches == [added]
    return str(matches[0])


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(100))
def test_answers_match_enumeration(key, seed):
    expected = _answer_by_enumeration(key, seed)
    q = REGISTRY[key].generate(Random(seed))
    assert q.choices[q.answer].content[0].tex == expected
    assert len(q.choices) == 4
    assert q.mistakes and any(q.mistakes)


@pytest.mark.parametrize("key", KEYS)
def test_variety_and_curriculum_placement(key):
    stems = {tuple(block.text for block in REGISTRY[key].generate(Random(seed)).stem)
             for seed in range(300)}
    assert len(stems) >= 100
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.3", "ความน่าจะเป็นเบื้องต้น", 3,
    )
