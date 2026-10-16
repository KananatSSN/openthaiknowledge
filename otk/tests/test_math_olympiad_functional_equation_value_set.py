"""Enumerate finite-field functions and substitute the real solutions."""

from itertools import product
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.functional_equation_value_set import possible_values


def test_exhaustive_small_fields():
    for prime in (3, 5):
        for scale in (1, 2):
            coefficient = scale * scale % prime
            solutions = []
            for values in product(range(prime), repeat=prime):
                if all(
                    values[x] * values[y] * values[(x - y) % prime] % prime
                    == coefficient * (x * x * values[y] - y * y * values[x]) % prime
                    for x in range(prime)
                    for y in range(prime)
                ):
                    solutions.append(values)
            expected = {
                tuple(0 for _ in range(prime)),
                tuple(scale * x % prime for x in range(prime)),
                tuple(-scale * x % prime for x in range(prime)),
            }
            assert set(solutions) == expected


def test_values_and_generated_draws():
    key = "math.functional_equation_value_set_olympiad"
    for scale in range(1, 13):
        for point in range(-9, 10):
            if point:
                assert set(possible_values(scale, point)) == {
                    0,
                    scale * point,
                    -scale * point,
                }
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
