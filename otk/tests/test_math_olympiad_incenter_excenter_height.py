"""Check exact excenter coordinates and the complementary incenter height."""

from fractions import Fraction
from math import isqrt, sqrt
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.incenter_excenter_height import _TRIPLES, excenter_height


def test_barycentric_excenter_and_incenter():
    for c, a, d in _TRIPLES:
        ac = isqrt(a * a + c * c)
        cd = isqrt(d * d + c * c)
        assert ac * ac == a * a + c * c
        assert cd * cd == d * d + c * c
        excenter_from_signed_side_weights = Fraction(c * (a - d), ac + a - d - cd)
        incenter_from_side_weights = Fraction(c * (a + d), ac + cd + a + d)
        assert excenter_height(a, d, c) == excenter_from_signed_side_weights
        assert excenter_from_signed_side_weights + incenter_from_side_weights == c
    rng = Random(2566)
    for _ in range(100):
        a = rng.uniform(2, 20)
        d = rng.uniform(0.1, a - 0.1)
        c = rng.uniform(1, 20)
        ac, cd = sqrt(a * a + c * c), sqrt(d * d + c * c)
        in_height = c * (a + d) / (ac + cd + a + d)
        ex_height = c * (a - d) / (ac + a - d - cd)
        assert abs(in_height + ex_height - c) < 1e-9


def test_generated_draws():
    key = "math.incenter_excenter_height_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
