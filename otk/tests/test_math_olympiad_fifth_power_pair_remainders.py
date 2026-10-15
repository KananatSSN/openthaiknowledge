"""Compare modular reduction with direct fifth powers and source search."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.fifth_power_pair_remainders import fifth_power_pair_remainders


def test_direct_modular_arithmetic():
    for m in range(1, 61):
        for n in range(1, 61):
            modulus = m * m + n * n
            expected = ((m**5 + n) % modulus, (n**5 + m) % modulus)
            assert fifth_power_pair_remainders(m, n) == expected


def test_source_integrality_search():
    solutions = [
        (m, n)
        for m in range(1, 201)
        for n in range(1, 201)
        if fifth_power_pair_remainders(m, n) == (0, 0)
    ]
    assert solutions == [(1, 1)]


def test_generated_draws():
    key = "math.fifth_power_pair_remainders_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
