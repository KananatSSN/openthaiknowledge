"""Check strict diagonal exclusion and line-projection independence."""

from fractions import Fraction
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.diagonal_strip_placements import (
    no_parallel_overlap,
    placement_probability,
    strip_placements,
)


def _independent_placements(size: int, length: int, above: bool):
    result = []
    for row in range(size):
        for col in range(size):
            for dr, dc in ((0, 1), (1, 0)):
                cells = {(row + step * dr, col + step * dc) for step in range(length)}
                if any(r >= size or c >= size for r, c in cells):
                    continue
                if all((c > r + 1) if above else (r > c + 1) for r, c in cells):
                    result.append(cells)
    return result


def test_matches_cell_set_enumeration():
    for size in range(6, 10):
        for length in range(2, min(size - 1, 5)):
            upper = _independent_placements(size, length, True)
            lower = _independent_placements(size, length, False)
            if not upper or not lower:
                continue
            assert len(strip_placements(size, length, above=True)) == len(upper)
            assert len(strip_placements(size, length, above=False)) == len(lower)
            good = sum(
                {r for r, _ in a}.isdisjoint({r for r, _ in b})
                and {c for _, c in a}.isdisjoint({c for _, c in b})
                for a in upper for b in lower
            )
            assert placement_probability(size, length) == Fraction(good, len(upper) * len(lower))


def test_checked_source_case():
    above = strip_placements(8, 4, above=True)
    below = strip_placements(8, 4, above=False)
    assert len(above) == len(below) == 12
    assert sum(no_parallel_overlap(a, b) for a in above for b in below) == 86
    probability = placement_probability(8, 4)
    assert probability == Fraction(43, 72)
    assert 100 * probability.numerator + probability.denominator == 4372


def test_generated_draws():
    key = "math.diagonal_strip_placements_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
