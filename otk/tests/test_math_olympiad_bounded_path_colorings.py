"""Cross-check bounded proper colorings by enumerating labeled assignments."""

from itertools import product
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.bounded_path_colorings import count_bounded_path_colorings


def test_matches_direct_colorings():
    for colors in range(1, 5):
        for cap in range(1, 4):
            for length in range(1, 8):
                direct = sum(
                    all(row[i] != row[i + 1] for i in range(length - 1))
                    and all(row.count(color) <= cap for color in range(colors))
                    for row in product(range(colors), repeat=length)
                )
                assert count_bounded_path_colorings(length, colors, cap) == direct


def test_checked_source_case():
    assert count_bounded_path_colorings(5, 3, 2) == 36


def test_generated_draws():
    key = "math.bounded_path_colorings_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
