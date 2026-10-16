"""Check hexagon closure with independent exact direction vectors."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.notched_hexagon_perimeter import notched_hexagon_lengths


def _direction_vectors(longest: int, shortest: int, sloping: int, base: int):
    # Coordinates are (2*x, 2*y/sqrt(3)), preserving exact integer arithmetic.
    return [
        (2 * base, 0),
        (-longest, longest),
        (-shortest, -shortest),
        (shortest, -shortest),
        (-sloping, -sloping),
        (shortest, -shortest),
    ]


def test_vector_closure_and_side_order():
    for shortest in range(1, 10):
        for longest in range(5 * shortest, 11 * shortest):
            sloping, base, perimeter = notched_hexagon_lengths(longest, shortest)
            vectors = _direction_vectors(longest, shortest, sloping, base)
            assert sum(x for x, _ in vectors) == sum(y for _, y in vectors) == 0
            lengths = [base, longest, shortest, shortest, sloping, shortest]
            assert all(x * x + 3 * y * y == 4 * length * length for (x, y), length in zip(vectors, lengths))
            assert shortest < sloping < base < longest
            assert perimeter == sum(lengths)


def test_checked_source_case():
    assert notched_hexagon_lengths(30, 5) == (15, 20, 80)


def test_generated_draws():
    key = "math.notched_hexagon_perimeter_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
