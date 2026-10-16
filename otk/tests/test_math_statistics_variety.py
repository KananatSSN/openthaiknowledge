"""Independent checks for the ม.2 statistics situations."""

from fractions import Fraction
from random import Random
from statistics import median

import pytest

from otk.api import REGISTRY, catalog
from otk.sets.math.m2.statistics import (
    _corrected_mean_data,
    _missing_frequency_data,
    _new_median_data,
)

KEYS = (
    "math.missing_frequency_mean_m2",
    "math.corrected_mean_m2",
    "math.median_after_new_value_m2",
)


def _independent_answer(key, seed):
    rng = Random(seed)
    if key == KEYS[0]:
        values, frequencies, hidden = _missing_frequency_data(rng)
        average = Fraction(sum(v * f for v, f in zip(values, frequencies)), sum(frequencies))
        visible = sum(v * f for i, (v, f) in enumerate(zip(values, frequencies)) if i != hidden)
        count = sum(f for i, f in enumerate(frequencies) if i != hidden)
        matches = [guess for guess in range(1, 101)
                   if Fraction(visible + values[hidden] * guess, count + guess) == average]
        assert matches == [frequencies[hidden]]
        return str(matches[0])
    if key == KEYS[1]:
        count, average, recorded, actual = _corrected_mean_data(rng)
        recorded_data = [recorded, *([Fraction(count * average - recorded, count - 1)] * (count - 1))]
        recorded_data[0] = actual
        corrected = sum(recorded_data) / count
        assert corrected.denominator == 1
        return str(corrected.numerator)
    data, newcomer = _new_median_data(rng)
    return str(median([*data, newcomer]))


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(100))
def test_answers_match_independent_reconstruction(key, seed):
    expected = _independent_answer(key, seed)
    draw = REGISTRY[key].expr(Random(seed))
    assert draw.answer_tex == expected
    question = REGISTRY[key].generate(Random(seed))
    assert question.choices[question.answer].content[0].tex == expected
    assert len(question.choices) == 4


@pytest.mark.parametrize("key", KEYS)
def test_variety_and_application_placement(key):
    prompts = {REGISTRY[key].expr(Random(seed)).prompt for seed in range(300)}
    assert len(prompts) >= 250
    row = next(row for row in catalog() if row["key"] == key)
    assert row["level"] == "ม.2"
    assert row["topic"] == "สถิติ"
    assert row["learning_stage"] == 3
