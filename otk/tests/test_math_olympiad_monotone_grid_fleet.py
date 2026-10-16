"""Enumerate monotone routes and check an attaining construction."""

from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.monotone_grid_fleet import minimum_unvisited_squares


def _routes(size: int, row: int = 0, col: int = 0) -> list[tuple[tuple[int, int], ...]]:
    if (row, col) == (size - 1, size - 1):
        return [((row, col),)]
    tails = []
    if row < size - 1:
        tails += _routes(size, row + 1, col)
    if col < size - 1:
        tails += _routes(size, row, col + 1)
    return [((row, col),) + tail for tail in tails]


def _attaining_route(size: int, index: int) -> set[tuple[int, int]]:
    row = col = 0
    cells = {(row, col)}
    for direction, count in (
        ("right", index),
        ("up", size - 1 - index),
        ("right", size - 1 - index),
        ("up", index),
    ):
        for _ in range(count):
            if direction == "right":
                col += 1
            else:
                row += 1
            cells.add((row, col))
    assert (row, col) == (size - 1, size - 1)
    return cells


def test_exhaustive_small_grids():
    for size in range(2, 6):
        routes = [set(route) for route in _routes(size)]
        for vehicles in range(1, min(size, 4)):
            brute = min(
                size * size - len(set().union(*selection))
                for selection in combinations(routes, vehicles)
            )
            assert brute == minimum_unvisited_squares(size, vehicles)


def test_attaining_routes_and_generated_draws():
    for size in range(2, 16):
        for vehicles in range(1, size):
            route_indices = list(range(vehicles - 1)) + [size - 1]
            covered = set().union(*(_attaining_route(size, index) for index in route_indices))
            assert size * size - len(covered) == minimum_unvisited_squares(size, vehicles)

    key = "math.monotone_grid_fleet_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
