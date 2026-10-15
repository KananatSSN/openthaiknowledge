"""Cross-check factorization and the unique source divisibility triple."""

from random import Random

from sympy import factor, primerange, symbols

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.sophie_germain_prime_power import smaller_sophie_factor


def test_symbolic_factorization_and_direct_values():
    u, v = symbols("u v")
    assert factor(u**4 + 4 * v**4) == (
        u**2 - 2 * u * v + 2 * v**2
    ) * (u**2 + 2 * u * v + 2 * v**2)
    for odd_base in range(1, 20, 2):
        for odd_exponent in range(1, 12, 2):
            whole = odd_base**4 + 4**odd_exponent
            lower = smaller_sophie_factor(odd_base, odd_exponent)
            assert whole % lower == 0
            assert lower <= whole // lower
            assert lower == 1 if (odd_base, odd_exponent) == (1, 1) else lower > 1


def test_source_divisibility_by_brute_force():
    found = []
    for prime in primerange(2, 101):
        for odd_m in range(1, 102, 2):
            for odd_k in range(1, 10, 2):
                divisor = odd_m**4 + 4**odd_k * prime**4
                dividend = odd_m**2 * (odd_m**4 - 4**odd_k * prime**4)
                if dividend % divisor == 0:
                    found.append((prime, odd_m, odd_k))
    assert found == [(5, 5, 1)]
    assert (5**2 * (5**4 - 4 * 5**4)) // (5**4 + 4 * 5**4) == -15


def test_generated_draws():
    key = "math.sophie_germain_prime_power_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
