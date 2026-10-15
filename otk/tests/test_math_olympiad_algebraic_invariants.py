"""Independent checks for original algebraic-invariant question sets."""

from random import Random
from itertools import combinations

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.algebraic_invariants import (
    cubic_root_sum,
    minimum_signed_pair_sum,
    shifted_square_sum,
)


def test_shifted_square_sum_matches_direct_evaluation():
    rng = Random(20269)
    for count in range(5, 16):
        for _ in range(30):
            values = [rng.randint(-9, 12) for _ in range(count)]
            shift = rng.randint(1, 6)
            direct = sum((value - shift) ** 2 for value in values)
            assert shifted_square_sum(
                count,
                sum(values),
                sum(value * value for value in values),
                shift,
            ) == direct


def test_cubic_root_sum_matches_direct_evaluation():
    for a in range(-9, 10):
        for b in range(-9, 10):
            assert cubic_root_sum(a + b, a * b) == a**3 + b**3


def test_signed_pair_minimum_matches_exhaustive_assignments():
    for count in range(2, 15):
        indices = range(1, count + 1)
        best = min(
            sum(i * j * (1 if (i in plus) == (j in plus) else -1)
                for i in indices for j in indices if i < j)
            for chosen in combinations(indices, (count + 1) // 2)
            for plus in [set(chosen)]
        )
        assert minimum_signed_pair_sum(count) == best


def test_signed_pair_minimum_reproduces_2565_source_answer():
    assert minimum_signed_pair_sum(2565) == -2814263707


def test_generated_choices_are_distinct_and_reproducible():
    for key in ("math.moment_shift_olympiad", "math.symmetric_cubic_olympiad",
                "math.signed_pair_minimum_olympiad"):
        for seed in range(50):
            question = generate(key, rng=Random(seed))
            choices = [choice.model_dump_json() for choice in question.choices]
            assert len(choices) == REGISTRY[key].max_choices
            assert len(choices) == len(set(choices))
            assert question.model_dump_json() == generate(
                key, rng=Random(seed)
            ).model_dump_json()
