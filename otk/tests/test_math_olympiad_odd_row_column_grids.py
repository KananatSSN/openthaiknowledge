"""Exhaustively count small binary grids with odd row and column parity."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.odd_row_column_grids import count_odd_row_column_grids


def _brute_count(rows: int, columns: int) -> int:
    total = 0
    for grid in range(1 << (rows * columns)):
        if any(
            sum((grid >> (r * columns + c)) & 1 for c in range(columns)) % 2 != 1
            for r in range(rows)
        ):
            continue
        if any(
            sum((grid >> (r * columns + c)) & 1 for r in range(rows)) % 2 != 1
            for c in range(columns)
        ):
            continue
        total += 1
    return total


def test_small_grids_by_full_enumeration():
    for rows, columns in ((1, 1), (2, 2), (2, 3), (2, 4), (3, 3), (3, 4), (4, 4)):
        assert count_odd_row_column_grids(rows, columns) == _brute_count(rows, columns)
    assert count_odd_row_column_grids(21, 21) == 1 << 400


def test_generated_draws():
    key = "math.odd_row_column_grids_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
