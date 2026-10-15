"""Exhaust small signed lists and check the sharp construction."""

from itertools import product
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.prefix_pigeonhole import minimum_positive_prefix_values


def _positive_prefixes(values: tuple[int, ...]) -> set[int]:
    seen = set()
    running = 0
    for value in values:
        running += value
        if running > 0:
            seen.add(running)
    return seen


def test_exhaustive_short_lists_satisfy_pigeonhole_lower_bound():
    short_lists = [()] + [(a,) for a in (-1, 1)] + list(product((-1, 1), repeat=2))
    for lists in product(short_lists, repeat=4):
        total = sum(map(sum, lists))
        if total < 1:
            continue
        seen = set().union(*(_positive_prefixes(values) for values in lists))
        assert len(seen) >= minimum_positive_prefix_values(total)


def test_balanced_positive_lists_attain_the_bound():
    for total in range(1, 201):
        q, r = divmod(total, 4)
        lengths = [q + (j < r) for j in range(4)]
        lists = [tuple([1] * length) for length in lengths]
        seen = set().union(*(_positive_prefixes(values) for values in lists))
        assert len(seen) == minimum_positive_prefix_values(total)


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.prefix_pigeonhole_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
