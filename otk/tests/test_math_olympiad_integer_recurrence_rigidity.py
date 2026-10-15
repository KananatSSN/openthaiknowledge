"""Check the unique integer recurrence against direct finite searches."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.integer_recurrence_rigidity import unique_term


def _next_term(n: int, current: int, constant: int, shift: int) -> int | None:
    rhs = n**3 + (shift + 1) * n * n + (constant - 1) * n
    rhs += constant + shift * (constant - 1)
    quotient, remainder = divmod(current + rhs, n * n + constant)
    return quotient if remainder == 0 and quotient > 0 else None


def test_direct_recurrence_and_finite_search():
    for constant in (1, 2, 3, 5, 7):
        for shift in (0, 2, 5):
            value = unique_term(constant, shift, 1)
            for n in range(1, 12):
                value = _next_term(n, value, constant, shift)
                assert value == unique_term(constant, shift, n + 1)
            survivors = []
            for first in range(1, 10001):
                value = first
                for n in range(1, 6):
                    value = _next_term(n, value, constant, shift)
                    if value is None:
                        break
                else:
                    survivors.append(first)
            assert survivors == [1 + shift]


def test_generated_draws():
    key = "math.integer_recurrence_rigidity_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
