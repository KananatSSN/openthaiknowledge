"""Check row-group sizes by brute force over integral headcounts."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.contiguous_group_fraction import possible_group_sizes


def _brute(front: Fraction, back: Fraction, low: int, high: int) -> tuple[int, ...]:
    result = set()
    for total in range(1, 1001):
        front_count = total * front
        back_count = total * back
        if front_count.denominator != 1 or back_count.denominator != 1:
            continue
        group = total - int(front_count) - int(back_count)
        if low <= group <= high:
            result.add(group)
    return tuple(sorted(result))


def test_matches_integral_headcount_search():
    cases = [
        (Fraction(1, 5), Fraction(8, 13), 20, 30),
        (Fraction(1, 4), Fraction(3, 8), 6, 30),
        (Fraction(2, 7), Fraction(3, 7), 4, 35),
        (Fraction(1, 3), Fraction(2, 5), 1, 40),
    ]
    for front, back, low, high in cases:
        assert possible_group_sizes(front, back, low, high) == _brute(front, back, low, high)


def test_checked_source_case():
    assert possible_group_sizes(Fraction(1, 5), Fraction(8, 13), 20, 30) == (24,)
    assert 130 // 5 == 26 and 130 * 8 // 13 == 80 and 130 - 26 - 80 == 24


def test_generated_draws():
    key = "math.contiguous_group_fraction_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
