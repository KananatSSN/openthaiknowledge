"""Independent subset search for the balanced signed partition construction."""

from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.balanced_signed_partition import balanced_sizes_sum


def _feasible(n: int) -> bool:
    signed = tuple(range(-n, 0)) + tuple(range(1, n + 1))
    return any(sum(group) == 0 for group in combinations(signed, n))


def test_brute_classification_and_sum():
    feasible = [_feasible(n) for n in range(1, 9)]
    assert feasible == [False] + [True] * 7
    for limit in range(1, 9):
        assert balanced_sizes_sum(limit) == sum(n for n in range(1, limit + 1) if feasible[n - 1])


def test_constructed_subsets_at_larger_sizes():
    for n in range(2, 100):
        if n % 2 == 0:
            chosen = [value for j in range(1, n // 2 + 1) for value in (-j, j)]
        else:
            chosen = [-2, -1, 3]
            chosen += [value for j in range(4, (n + 1) // 2 + 2) for value in (-j, j)]
        assert len(chosen) == n
        assert len(set(chosen)) == n
        assert all(1 <= abs(value) <= n for value in chosen)
        assert sum(chosen) == 0


def test_generated_draws():
    key = "math.balanced_signed_partition_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
