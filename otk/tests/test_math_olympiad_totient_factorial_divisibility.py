"""Check totient values and the cycle-group divisibility route."""

from itertools import permutations
from math import factorial, gcd
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.totient_factorial_divisibility import (
    euler_totient,
    factorial_totient_quotient,
)


def _cycle_powers(mapping: tuple[int, ...]) -> frozenset[tuple[int, ...]]:
    identity = tuple(range(len(mapping)))
    powers = {identity}
    current = identity
    for _ in range(1, len(mapping)):
        current = tuple(mapping[value] for value in current)
        powers.add(current)
    return frozenset(powers)


def _is_long_cycle(mapping: tuple[int, ...]) -> bool:
    seen = set()
    value = 0
    while value not in seen:
        seen.add(value)
        value = mapping[value]
    return len(seen) == len(mapping) and value == 0


def test_residue_enumeration_and_cycle_groups():
    for number in range(1, 101):
        direct = sum(gcd(value, number) == 1 for value in range(1, number + 1))
        assert euler_totient(number) == direct
    for index in range(2, 7):
        long_cycles = [
            mapping
            for mapping in permutations(range(index))
            if _is_long_cycle(mapping)
        ]
        groups = {_cycle_powers(mapping) for mapping in long_cycles}
        assert len(long_cycles) == factorial(index - 1)
        assert len(groups) * euler_totient(index) == len(long_cycles)
    for index in range(1, 101):
        direct_phi = sum(gcd(value, 2 * index) == 1 for value in range(1, 2 * index + 1))
        assert factorial_totient_quotient(index) * direct_phi == factorial(index)


def test_generated_draws():
    key = "math.totient_factorial_divisibility_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
