"""Direct small-grid checks for the block pigeonhole argument."""

from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.grid_pigeonhole import block_upper_bound


def _valid(rows: int, columns: int, active: tuple[tuple[int, int], ...]) -> bool:
    if any(abs(r - s) + abs(c - d) == 1
           for (r, c), (s, d) in combinations(active, 2)):
        return False
    received: dict[tuple[int, int], int] = {}
    for row, column in active:
        for target in ((row, column - 1), (row, column + 1), (row - 1, column)):
            if 0 <= target[0] < rows and 0 <= target[1] < columns:
                received[target] = received.get(target, 0) + 1
                if received[target] >= 2:
                    return False
    return True


def test_bound_matches_exhaustive_small_grids():
    for rows, columns in ((2, 2), (2, 4), (4, 2), (4, 4)):
        cells = [(r, c) for r in range(rows) for c in range(columns)]
        largest = max(
            length
            for length in range(len(cells) + 1)
            for active in combinations(cells, length)
            if _valid(rows, columns, active)
        )
        assert largest == block_upper_bound(rows, columns)


def test_source_grid_exceeds_the_block_bound():
    assert block_upper_bound(60, 60) == 900
    assert 901 > block_upper_bound(60, 60)


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.grid_block_pigeonhole_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
