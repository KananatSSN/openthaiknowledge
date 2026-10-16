"""Check coefficient swaps with the rational-root theorem."""

from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.swapped_quadratic_coefficients import valid_swapped_constants


def _divisors(value: int) -> list[int]:
    return [candidate for candidate in range(1, abs(value) + 1) if value % candidate == 0]


def _has_rational_root(leading: int, middle: int, constant: int) -> bool:
    return any(
        leading * numerator**2 + middle * numerator * denominator + constant * denominator**2 == 0
        for numerator_abs in _divisors(constant)
        for numerator in (numerator_abs, -numerator_abs)
        for denominator in _divisors(leading)
    )


def _brute_constants(leading: int, magnitude: int) -> tuple[int, ...]:
    answers = []
    for constant in range(1, magnitude**2 // (4 * leading) + 1):
        coefficients = (leading, -magnitude, constant)
        if not _has_rational_root(*coefficients):
            continue
        if all(
            _has_rational_root(*tuple(
                coefficients[index] if index not in (left, right)
                else coefficients[right if index == left else left]
                for index in range(3)
            ))
            for left, right in combinations(range(3), 2)
        ):
            answers.append(constant)
    return tuple(answers)


def test_matches_rational_root_theorem():
    for leading in range(2, 7):
        for magnitude in range(leading + 3, 20):
            assert valid_swapped_constants(leading, magnitude) == _brute_constants(leading, magnitude)


def test_checked_source_case():
    assert valid_swapped_constants(5, 16) == (11,)


def test_generated_draws():
    key = "math.swapped_quadratic_coefficients_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
