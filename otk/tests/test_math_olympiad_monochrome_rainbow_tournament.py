"""Construct direction colorings and check every triangle independently."""

from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.monochrome_rainbow_tournament import maximum_players


def _color(a: tuple[int, int], b: tuple[int, int], prime: int) -> int:
    dx = (b[0] - a[0]) % prime
    dy = (b[1] - a[1]) % prime
    return prime if dx == 0 else dy * pow(dx, -1, prime) % prime


def test_affine_plane_construction():
    for prime in (3, 5, 7):
        points = [(x, y) for x in range(prime) for y in range(prime)]
        assert len(points) == maximum_players(prime + 1)
        colors = {_color(a, b, prime) for a, b in combinations(points, 2)}
        assert len(colors) == prime + 1
        for a, b, c in combinations(points, 3):
            edge_colors = (_color(a, b, prime), _color(a, c, prime), _color(b, c, prime))
            assert len(set(edge_colors)) in (1, 3)


def test_generated_draws():
    key = "math.monochrome_rainbow_tournament_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
