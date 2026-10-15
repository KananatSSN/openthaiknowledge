"""Independent checks for the infinite rational-recurrence set."""

from fractions import Fraction
from math import isqrt
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.rational_recurrence import starting_value_sum


def _integer_successors(value: int) -> tuple[int, ...]:
    discriminant = 1 + 4 * value
    if discriminant < 0 or isqrt(discriminant) ** 2 != discriminant:
        return ()
    root = isqrt(discriminant)
    return tuple(x for numerator in (1 + root, 1 - root)
                 if numerator % 2 == 0 for x in (numerator // 2,))


def test_only_zero_and_two_have_long_integer_paths():
    surviving = set(range(-100, 101))
    for _ in range(12):
        surviving = {value for value in surviving
                     if any(next_value in surviving
                            for next_value in _integer_successors(value))}
    assert surviving == {0, 2}
    for shift in range(2, 11):
        assert starting_value_sum(shift) == sum(value + shift for value in surviving)


def test_shifted_equation_is_exact_conjugate_over_rationals():
    for shift in range(2, 11):
        for numerator in range(-5, 6):
            for denominator in range(1, 6):
                a_next = Fraction(numerator, denominator)
                b_next = a_next + shift
                b_now = b_next**2 - (2 * shift + 1) * b_next + shift**2 + 2 * shift
                assert b_now - shift == a_next**2 - a_next


def test_2565_source_case_and_generated_draws():
    assert starting_value_sum(0) == 2
    key = "math.rational_recurrence_starts_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
