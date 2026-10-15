"""Brute-check the CRT block and the binomial divisibility lemma."""

from itertools import permutations
from math import comb, isqrt
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.consecutive_nonpowers_crt import nonpower_block_start


def _perfect_power(value: int) -> bool:
    for base in range(2, isqrt(value) + 1):
        power = base * base
        while power < value:
            power *= base
        if power == value:
            return True
    return False


def test_crt_minimum_and_nonpowers():
    primes = (2, 3, 5, 7)
    for size in (2, 3):
        for selected in permutations(primes, size):
            answer = nonpower_block_start(selected)
            modulus = 1
            for prime in selected:
                modulus *= prime * prime
            brute = next(
                start
                for start in range(modulus)
                if all((start + i - prime) % (prime * prime) == 0 for i, prime in enumerate(selected, 1))
            )
            assert answer == brute
            for i, prime in enumerate(selected, 1):
                value = answer + i
                assert value >= 2
                assert value % prime == 0 and value % (prime * prime) != 0
                assert not _perfect_power(value)


def test_binomial_divisibility_lemma():
    for divisor in range(2, 100):
        a = divisor - 1
        assert comb(2 * a, a) % divisor == 0


def test_generated_draws():
    key = "math.consecutive_nonpowers_crt_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
