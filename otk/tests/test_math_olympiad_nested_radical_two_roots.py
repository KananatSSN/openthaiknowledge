"""Check the root threshold and substitute both roots into the radical equation."""

from math import isqrt, sqrt
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.nested_radical_two_roots import first_two_root_parameter


def _direct_equation(offset: int, inner_root: int, parameter: int, t: float) -> float:
    x = t * t + offset
    inner = x + inner_root * (inner_root + 2) - parameter * sqrt(x - offset)
    return x + 2 * sqrt(inner) - parameter * sqrt(x - offset)


def test_root_threshold_and_direct_substitution():
    for offset in range(4, 16):
        for inner_root in range(1, 5):
            answer = first_two_root_parameter(offset, inner_root)
            constant = offset + 2 * inner_root
            assert answer**2 > 4 * constant
            assert (answer - 1) ** 2 <= 4 * constant
            discriminant = answer**2 - 4 * constant
            roots = ((answer - sqrt(discriminant)) / 2, (answer + sqrt(discriminant)) / 2)
            assert 0 < roots[0] < roots[1]
            assert all(abs(_direct_equation(offset, inner_root, answer, t)) < 1e-10 for t in roots)


def test_checked_source_case():
    assert first_two_root_parameter(7, 1) == 7
    assert isqrt(4 * (7 + 2)) == 6


def test_generated_draws():
    key = "math.nested_radical_two_roots_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
