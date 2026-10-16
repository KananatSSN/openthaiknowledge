"""Check the squarefree-kernel solver against direct gcd/lcm enumeration."""

from math import gcd, isqrt, lcm
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.gcd_lcm_square import (
    squarefree_kernel,
    sum_fixed_gcd_square_lcm,
)


def _square(value: int) -> bool:
    return isqrt(value) ** 2 == value


def test_solver_matches_independent_bounded_enumeration():
    for modulus in range(2, 101):
        for fixed_gcd in range(1, modulus + 1):
            if modulus % fixed_gcd:
                continue
            limit = min(300, 8 * modulus)
            expected = sum(
                n for n in range(1, limit + 1)
                if gcd(n, modulus) == fixed_gcd and _square(lcm(n, modulus))
            )
            assert sum_fixed_gcd_square_lcm(modulus, fixed_gcd, limit) == expected


def test_kernel_reconstructs_square_part_and_source_case():
    for value in range(1, 1000):
        kernel = squarefree_kernel(value)
        assert value % kernel == 0
        assert _square(value // kernel)
    assert sum_fixed_gcd_square_lcm(180, 60, 2026) == 1500


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.gcd_lcm_square_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
