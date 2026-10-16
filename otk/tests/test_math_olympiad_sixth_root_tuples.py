"""Enumerate root choices independently of the multinomial formula."""

from itertools import product
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.sixth_root_tuples import sixth_root_tuple_count


def _enumerate(m: int, n: int) -> int:
    # Twice the real coefficient and the imaginary sqrt(3) coefficient.
    roots = ((2, 0), (1, 1), (1, -1))
    return sum(
        1
        for entries in product(roots, repeat=m)
        if sum(real for real, _ in entries) == 2 * n
        and sum(imaginary for _, imaginary in entries) == 0
    )


def test_all_small_source_cases():
    for n in range(1, 5):
        for m in range(n, 2 * n + 1):
            assert sixth_root_tuple_count(m, n) == _enumerate(m, n)


def test_generated_draws():
    key = "math.sixth_root_tuples_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
