"""Enumerate small exact flag partitions and construct prime-power examples."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.regular_polygon_flag_classes import minimum_smallest_color_classes


def _partitions(vertices: int):
    classes = [
        frozenset(range(residue, vertices, step))
        for step in range(2, vertices)
        if vertices % step == 0 and vertices // step >= 3
        for residue in range(step)
    ]
    all_vertices = frozenset(range(vertices))

    def visit(uncovered, chosen):
        if not uncovered:
            yield chosen
            return
        first = min(uncovered)
        for color_class in classes:
            if first in color_class and color_class <= uncovered:
                yield from visit(uncovered - color_class, chosen + (color_class,))

    yield from visit(all_vertices, ())


def test_exhaustive_small_odd_polygons():
    for vertices in (9, 15, 21, 25, 27):
        partitions = list(_partitions(vertices))
        assert partitions
        for partition in partitions:
            smallest = min(map(len, partition))
            assert sum(len(group) == smallest for group in partition) >= 3
            if vertices in (9, 25, 27):
                prime = 5 if vertices == 25 else 3
                assert sum(len(group) == smallest for group in partition) >= prime


def test_prime_power_construction_and_draws():
    for prime in (3, 5, 7, 11):
        vertices = prime**3
        classes = [set(range(residue, vertices, prime)) for residue in range(prime)]
        assert len(classes) == minimum_smallest_color_classes(prime)
        assert set.union(*classes) == set(range(vertices))
        assert all(len(group) == prime**2 for group in classes)
        assert all(not (classes[i] & classes[j]) for i in range(prime) for j in range(i + 1, prime))
    key = "math.regular_polygon_flag_classes_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
