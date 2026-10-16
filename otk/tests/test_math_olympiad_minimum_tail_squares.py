"""Compare the distinct-label dynamic program with brute combinations."""

from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.minimum_tail_squares import max_earlier_square_sum, tail_square_extremes


def test_matches_direct_combinations():
    for limit in range(5, 11):
        for picks in range(2, min(5, limit)):
            grouped: dict[int, list[int]] = {}
            for subset in combinations(range(1, limit + 1), picks):
                grouped.setdefault(sum(subset), []).append(sum(x * x for x in subset))
            total_squares = sum(x * x for x in range(1, limit + 1))
            for target, square_sums in grouped.items():
                assert tail_square_extremes(limit, picks, target) == (min(square_sums), max(square_sums))
                assert max_earlier_square_sum(limit, picks, target) == total_squares - min(square_sums)


def test_checked_source_case():
    assert tail_square_extremes(9, 3, 15)[0] == 4**2 + 5**2 + 6**2 == 77
    assert max_earlier_square_sum(9, 3, 15) == 208


def test_generated_draws():
    key = "math.minimum_tail_squares_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
