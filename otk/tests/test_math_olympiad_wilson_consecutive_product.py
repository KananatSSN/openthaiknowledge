"""Check Wilson reduction against products and the paper's obstruction."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.wilson_consecutive_product import consecutive_product_residue


def test_direct_product_and_quadratic_character():
    for prime in (7, 23, 31, 47, 71, 79, 103):
        squares = {value * value % prime for value in range(1, prime)}
        for first in (1, 2, 3):
            direct = 1
            for value in range(first, first + prime - 3):
                direct = direct * value % prime
            reduced = consecutive_product_residue(prime, first)
            assert reduced == direct
            assert (reduced in squares) == (first == 2)
            if first == 2:
                assert sum(range(first, first + prime - 3)) % prime == 0


def test_generated_draws():
    key = "math.wilson_consecutive_product_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
