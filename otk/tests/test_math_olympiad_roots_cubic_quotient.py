"""Check the symmetric quotient by direct evaluation at distinct roots."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.roots_cubic_quotient import cubic_root_quotient


def test_matches_direct_root_substitution():
    for a in range(-10, 11):
        for b in range(-10, 11):
            if a == b:
                continue
            direct = Fraction(a**3 + b, a - b) + Fraction(b**3 + a, b - a)
            assert cubic_root_quotient(a + b, a * b) == direct


def test_checked_source_case():
    assert cubic_root_quotient(20, -26) == 425


def test_generated_draws():
    key = "math.roots_cubic_quotient_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
