"""Check root filtering against exact roots of the composed polynomial."""

from fractions import Fraction
from random import Random

from sympy import Poly, prod, simplify, symbols

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.composed_polynomial_roots import real_root_product


def test_solver_matches_independent_exact_real_root_enumeration():
    x = symbols("x")
    cases = [
        (2, 1, (-5, 0, 2)),
        (3, 1, (Fraction(-3, 2), 1, 3)),
        (0, 2, (-3, -2, 1)),
        (4, 3, (-4, -3, 2)),
    ]
    for shift in range(2, 6):
        for depth in range(1, 4):
            cases.append((shift, depth, (-depth - 2, -depth + 2, -depth + 5)))
    for shift, depth, roots in cases:
        inner = (x + shift) ** 2 - depth
        composed = Poly(prod(inner - root for root in roots), x)
        actual = prod(set(composed.real_roots()))
        assert simplify(actual - real_root_product(shift, depth, roots)) == 0


def test_source_case_and_threshold_root():
    assert real_root_product(3, 1, (Fraction(-3, 2), 1, 3)) == 35
    assert real_root_product(0, 2, (-2, 1)) == 0


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.composed_polynomial_real_roots_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
