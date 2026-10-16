"""Independently check symmetrization, the stationary point, and a grid."""

from fractions import Fraction
from itertools import product
from random import Random

from sympy import Rational, diff, log, simplify, sqrt, symbols

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.cyclic_cube_product_maximum import cyclic_cube_product_maximum


def test_concavity_and_exact_witness():
    x, fixed = symbols("x fixed", positive=True)
    concavity = diff(log(x) + log(x**3 + fixed), x, 2)
    assert simplify(concavity + (2 * x**3 - fixed) ** 2 / (x**2 * (x**3 + fixed) ** 2)) == 0

    u = symbols("u", positive=True)
    reduced = u**6 * (8 - 6 * u) ** 4
    assert simplify(diff(reduced, u).subs(u, Rational(4, 5))) == 0
    high = 1 + 1 / sqrt(5)
    low = 1 - 1 / sqrt(5)
    assert simplify(2 * high + 2 * low - 4) == 0
    witness = (high * low) ** 6 * (high**3 + low**3) ** 4
    assert simplify(witness - Rational(4**14, 5**10)) == 0


def test_grid_below_exact_bound_and_scaling():
    bound = cyclic_cube_product_maximum(1)
    for x, y, z in product(range(1, 16), repeat=3):
        w = 16 - x - y - z
        if w <= 0:
            continue
        a, b, c, d = [Fraction(value, 4) ** 3 for value in (x, y, z, w)]
        expression = a * b * c * d * (a + b) * (b + c) * (c + d) * (d + a)
        assert expression <= bound
    for scale in range(1, 6):
        assert cyclic_cube_product_maximum(scale) == bound * scale**24


def test_generated_draws():
    key = "math.cyclic_cube_product_maximum_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
