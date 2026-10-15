"""Check the functional-equation classification on finite subdomains."""

from fractions import Fraction
from itertools import product
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.multiplicative_additive_function import (
    sum_of_solution_squares,
)


def test_exhaustive_small_domain():
    domain = (1, 2, 3, 4)
    relevant_pairs = tuple(
        (x, y) for x in domain for y in domain if x * y in domain and x + y in domain
    )
    for scale in range(1, 10):
        options = (Fraction(-1, scale), Fraction(0), Fraction(1, scale))
        solutions = []
        for assigned in product(options, repeat=len(domain)):
            f = dict(zip(domain, assigned, strict=True))
            if all(
                f[x * y] == scale * scale * f[x] * f[y] * f[x + y]
                for x, y in relevant_pairs
            ):
                solutions.append(f)
        assert len(solutions) == 3
        assert all(len(set(solution.values())) == 1 for solution in solutions)
        assert sum(solution[2] ** 2 for solution in solutions) == sum_of_solution_squares(scale)


def test_constant_solutions_on_rational_inputs():
    inputs = (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(3, 2), 2, 7)
    for scale in range(1, 10):
        for value in (Fraction(0), Fraction(-1, scale), Fraction(1, scale)):
            for x, y in product(inputs, repeat=2):
                assert value == scale * scale * value**3


def test_generated_draws():
    key = "math.multiplicative_additive_function_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
