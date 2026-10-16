"""Check three-box probabilities by enumerating every labeled draw."""

from fractions import Fraction
from itertools import product
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.overlapping_boxes_probability import distinct_box_probability


def test_matches_direct_draws():
    for first in range(2, 6):
        for second in range(2, 6):
            for extra in range(4):
                box_a = range(1, first + 1)
                box_b = (1, *range(first + 1, first + second))
                box_c = range(1, first + second + extra)
                outcomes = list(product(box_a, box_b, box_c))
                favorable = sum(len(set(draw)) == 3 for draw in outcomes)
                probability = distinct_box_probability(first, second, extra)
                assert probability.numerator * len(outcomes) == favorable * probability.denominator


def test_checked_source_case():
    assert distinct_box_probability(2, 2, 2) == Fraction(9, 20)


def test_generated_draws():
    key = "math.overlapping_boxes_probability_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
