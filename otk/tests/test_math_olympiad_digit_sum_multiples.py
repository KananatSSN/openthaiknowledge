"""Check the digit-sum construction behind the cofinite criterion."""

from math import gcd
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.digit_sum_multiples import count_cofinite_digit_sum_moduli


def _digit_sum(number: int) -> int:
    return sum(int(digit) for digit in str(number))


def _construct_multiple(n: int, target_sum: int) -> int:
    assert gcd(n, 9) == 1
    for j in range(1, 10):
        prefix = j * n
        extra = target_sum - _digit_sum(prefix)
        if extra < 0 or extra % 9:
            continue
        exponent = extra // 9
        if 10**exponent <= n:
            continue
        suffix = n * (10**exponent - 1)
        return prefix * 10 ** len(str(suffix)) + suffix
    raise AssertionError((n, target_sum))


def test_constructs_every_sufficiently_large_digit_sum_for_small_moduli():
    for n in range(1, 36):
        if n % 3 == 0:
            assert all(_digit_sum(j * n) % 3 == 0 for j in range(1, 61))
            continue
        threshold = max(_digit_sum(j * n) for j in range(1, 10)) + 9 * len(str(n))
        for target in range(threshold, threshold + 36):
            number = _construct_multiple(n, target)
            assert number % n == 0
            assert _digit_sum(number) == target


def test_count_matches_direct_modulus_classification():
    for limit in range(30, 151):
        assert count_cofinite_digit_sum_moduli(limit) == sum(
            n % 3 != 0 for n in range(1, limit + 1)
        )


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.digit_sum_cofinite_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
