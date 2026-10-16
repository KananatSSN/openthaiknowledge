"""Direct factorial gcd and constant enumeration for the polynomial theorem."""

from math import factorial, gcd
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.factorial_offset_polynomial_divisors import (
    polynomial_divisor_count,
)


def test_direct_constant_enumeration():
    for start in range(1, 8):
        for offset in range(1, 31):
            end = 30
            values = [factorial(index) + offset for index in range(start, end + 1)]
            common = 0
            for value in values:
                common = gcd(common, value)
            constants = [
                candidate
                for candidate in range(-offset, offset + 1)
                if candidate and all(value % candidate == 0 for value in values)
            ]
            assert common == gcd(factorial(start), offset)
            assert len(constants) == polynomial_divisor_count(start, offset)
    assert polynomial_divisor_count(1, 2) == 2


def test_generated_draws():
    key = "math.factorial_offset_polynomial_divisors_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
