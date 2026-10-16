"""Check conditional switch passes by an independent set-count formula."""

from itertools import permutations
from math import lcm
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.conditional_switch_passes import switches_on


def _formula(total: int, first: int, second: int, third: int) -> int:
    half = total // 2
    multiples = lambda divisor, bound: bound // divisor
    first_half = (
        half - multiples(first, half) - multiples(third, half)
        + multiples(lcm(first, third), half)
        + multiples(lcm(first, second), half)
        - multiples(lcm(first, second, third), half)
    )
    second_half = (
        multiples(second, total) - multiples(second, half)
        - multiples(lcm(second, third), total)
        + multiples(lcm(second, third), half)
    )
    return first_half + second_half


def test_matches_set_count_formula():
    for total in range(20, 102, 2):
        for first, second, third in permutations(range(2, 7), 3):
            assert switches_on(total, first, second, third) == _formula(total, first, second, third)


def test_checked_source_case():
    assert switches_on(2026, 2, 3, 4) == _formula(2026, 2, 3, 4) == 845


def test_generated_draws():
    key = "math.conditional_switch_passes_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
