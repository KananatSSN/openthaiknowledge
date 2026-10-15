"""Independent finite sums and SymPy limits for added ม.6 series sets."""

import math
import re
from fractions import Fraction
from random import Random

import pytest
from sympy import Rational, oo, summation, symbols

from otk.api import REGISTRY, catalog
from otk.tests.test_math_chapters import _val

KEYS = (
    "math.alternating_geometric_sum_m6",
    "math.finite_telescoping_fraction_m6",
    "math.weighted_geometric_infinite_m6",
)


def _solve_from_stem(key, tex):
    if key == KEYS[1]:
        limit, numerator = map(int, re.search(r"\^\{(\d+)\}\\frac\{(\d+)\}", tex).groups())
        return sum((Fraction(numerator, k * (k + 1)) for k in range(1, limit + 1)), Fraction())
    numerator, p, q = map(int, re.search(r" (\d+)(?:n)?\\left\(-?\\frac\{(\d+)\}\{(\d+)\}", tex).groups())
    n = symbols("n", integer=True, nonnegative=True)
    ratio = Rational(p, q)
    if key == KEYS[0]:
        return summation(numerator * (-ratio) ** n, (n, 0, oo))
    return summation(numerator * n * ratio ** (n - 1), (n, 1, oo))


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(120))
def test_sum_and_named_choices(key, seed):
    q = REGISTRY[key].generate(Random(seed))
    expected = float(_solve_from_stem(key, q.stem[1].tex))
    assert math.isclose(_val(q.choices[q.answer].content[0].tex), expected, rel_tol=1e-12)
    assert len(q.choices) == 4
    assert all(m is not None for i, m in enumerate(q.mistakes) if i != q.answer)
    assert all(not math.isclose(_val(choice.content[0].tex), expected, rel_tol=1e-12)
               for i, choice in enumerate(q.choices) if i != q.answer)


@pytest.mark.parametrize("key", KEYS)
def test_stage_and_variety(key):
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.6", "อนุกรม", 3,
    )
    stems = {REGISTRY[key].generate(Random(seed)).stem[1].tex for seed in range(200)}
    assert len(stems) >= 100
