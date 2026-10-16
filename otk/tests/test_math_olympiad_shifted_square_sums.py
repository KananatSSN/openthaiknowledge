"""Check shifted-square sums against direct expansion of actual values."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.shifted_square_sums import shifted_square_sum


def test_matches_direct_squaring():
    rng = Random(917)
    for count in range(1, 80):
        values = [rng.randint(-8, 8) for _ in range(count)]
        for shift in range(-4, 5):
            assert shifted_square_sum(count, sum(values), sum(x * x for x in values), shift) == sum(
                (x - shift) ** 2 for x in values
            )


def test_checked_source_case():
    assert shifted_square_sum(2569, 2026, 2569) == 1086


def test_generated_draws():
    key = "math.shifted_square_sums_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
