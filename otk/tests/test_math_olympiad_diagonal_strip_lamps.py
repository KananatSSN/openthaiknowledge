"""Search small strips and check the diagonal construction."""

from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.diagonal_strip_lamps import minimum_strip_lamps


def _points(length: int) -> list[tuple[int, int]]:
    return [
        (x, y)
        for x in range(length + 1)
        for y in range(length + 1)
        if abs(x - y) <= 1
    ]


def _covers(lamp: tuple[int, int], point: tuple[int, int]) -> bool:
    return (lamp[0] - point[0]) ** 2 + (lamp[1] - point[1]) ** 2 <= 1


def test_exhaustive_small_strips():
    for length in range(1, 6):
        points = _points(length)
        for count in range(1, len(points) + 1):
            if any(
                all(any(_covers(lamp, point) for lamp in lamps) for point in points)
                for lamps in combinations(points, count)
            ):
                assert count == minimum_strip_lamps(length)
                break


def test_diagonal_construction_and_draws():
    for length in range(1, 31):
        lamps = [(index, index) for index in range(length + 1)]
        assert len(lamps) == minimum_strip_lamps(length)
        assert all(any(_covers(lamp, point) for lamp in lamps) for point in _points(length))
    key = "math.diagonal_strip_lamps_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
