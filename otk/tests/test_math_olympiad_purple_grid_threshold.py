"""Check the block construction and brute-force two small grids."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.purple_grid_threshold import minimum_purple_cells


def _valid(mask: int, rows: int, columns: int, threshold: int) -> bool:
    row_counts = [sum((mask >> (i * columns + j)) & 1 for j in range(columns)) for i in range(rows)]
    column_counts = [sum((mask >> (i * columns + j)) & 1 for i in range(rows)) for j in range(columns)]
    return all(
        row_counts[i] * column_counts[j] >= threshold
        for i in range(rows)
        for j in range(columns)
        if not ((mask >> (i * columns + j)) & 1)
    )


def test_brute_small_grids():
    for blocks, height, width in ((2, 1, 2), (2, 1, 3)):
        rows, columns, threshold = blocks * height, blocks * width, height * width
        minimum = min(
            mask.bit_count()
            for mask in range(1 << (rows * columns))
            if _valid(mask, rows, columns, threshold)
        )
        assert minimum == minimum_purple_cells(blocks, height, width)


def test_block_construction_and_lower_bound():
    for blocks, height, width in ((11, 8, 23), (4, 2, 5), (6, 4, 8)):
        rows, columns, threshold = blocks * height, blocks * width, height * width
        marked = {
            (i, j)
            for i in range(rows)
            for j in range(columns)
            if i // height == j // width
        }
        assert len(marked) == minimum_purple_cells(blocks, height, width)
        assert len(marked) == blocks * threshold
        assert all(
            width * height == threshold
            for i in range(rows)
            for j in range(columns)
            if (i, j) not in marked
        )
        lower_if_one_fewer = ((blocks - 1) * width + 1) * (height + 1)
        assert lower_if_one_fewer > blocks * height * width


def test_generated_draws():
    key = "math.purple_grid_threshold_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
