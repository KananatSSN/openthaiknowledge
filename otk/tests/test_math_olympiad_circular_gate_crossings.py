"""Check chord intersections by cyclic endpoint order and pot colourings."""

from itertools import product
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.circular_gate_crossings import (
    guaranteed_lighted_same_material_paths,
)


def _crossings(gates: int) -> int:
    endpoint = (gates - 1) // 2
    count = 0
    for first in range(gates):
        for second in range(first + 1, gates):
            if first in (0, endpoint) or second in (0, endpoint):
                continue
            if (first < endpoint) != (second < endpoint):
                count += 1
    return count


def test_direct_chord_enumeration_and_two_colours():
    for gates in range(5, 32, 2):
        count = _crossings(gates)
        assert count == ((gates - 1) // 2) * ((gates - 3) // 2)
        assert guaranteed_lighted_same_material_paths(gates) == (gates + 1) // 2
    assert _crossings(21) == 90
    assert guaranteed_lighted_same_material_paths(21) == 11
    for gates in (5, 7, 9):
        count = _crossings(gates)
        least_largest_colour_class = min(
            max(colours.count(0), colours.count(1))
            for colours in product((0, 1), repeat=count)
        )
        assert least_largest_colour_class == _crossings(gates) // 2
        least_same_material = min(
            max(materials.count(0), materials.count(1))
            for materials in product((0, 1), repeat=gates)
        )
        assert least_same_material == guaranteed_lighted_same_material_paths(gates)


def test_generated_draws():
    key = "math.circular_gate_crossings_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
