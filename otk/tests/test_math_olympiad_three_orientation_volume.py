"""Check inferred capacity against explicit boxes in all orientations."""

from fractions import Fraction
from itertools import combinations
from math import prod
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.three_orientation_volume import capacity_from_water_depths


def test_matches_physical_box_orientations():
    for dimensions in combinations(range(3, 13), 3):
        capacity = prod(dimensions)
        for denominator in (2, 3, 4):
            water = Fraction(capacity, denominator)
            if water.denominator != 1:
                continue
            depths = tuple(Fraction(side, denominator) for side in dimensions)
            for side, depth in zip(dimensions, depths):
                assert water == depth * (capacity // side)
            assert capacity_from_water_depths(int(water), depths) == capacity


def test_checked_source_case():
    depths = (Fraction(5, 2), Fraction(4), Fraction(6))
    assert capacity_from_water_depths(240, depths) == 480
    assert [Fraction(240, depth) for depth in depths] == [96, 60, 40]
    assert 12 * 8 * 5 == 480


def test_generated_draws():
    key = "math.three_orientation_box_volume_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
