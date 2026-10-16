"""Cross-check new quadratic-domain sets against SymPy and enumeration."""

from random import Random

import pytest
from sympy import Interval, oo, symbols
from sympy.calculus.util import function_range

from otk.api import REGISTRY, catalog
from otk.sets.math.m4.quadratic import (
    _half_line_parameters,
    _integer_optimum_parameters,
    _open_interval_parameters,
)

KEYS = (
    "math.quadratic_range_half_line_m4",
    "math.quadratic_range_open_domain_m4",
    "math.quadratic_integer_optimum_m4",
)


def _interval_tex(interval):
    left = r"-\infty" if interval.start == -oo else str(interval.start)
    right = r"\infty" if interval.end == oo else str(interval.end)
    return f"{'(' if interval.left_open else '['}{left}, {right}{')' if interval.right_open else ']'}"


def _answer_independently(key, seed):
    x = symbols("x", real=True)
    if key == KEYS[0]:
        a, h, k, boundary, rightward = _half_line_parameters(Random(seed))
        domain = Interval(boundary, oo) if rightward else Interval(-oo, boundary)
        return _interval_tex(function_range(a * (x - h) ** 2 + k, x, domain))
    if key == KEYS[1]:
        a, h, k, left, right = _open_interval_parameters(Random(seed))
        return _interval_tex(function_range(a * (x - h) ** 2 + k, x, Interval.open(left, right)))
    a, twice_vertex, left, right, height = _integer_optimum_parameters(Random(seed))
    return str(max(height - a * (2 * n - twice_vertex) ** 2 for n in range(left, right + 1)))


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(100))
def test_answer_matches_independent_solver(key, seed):
    expected = _answer_independently(key, seed)
    draw = REGISTRY[key].expr(Random(seed))
    assert draw.answer_tex == expected
    q = REGISTRY[key].generate(Random(seed))
    assert q.choices[q.answer].content[0].tex == expected
    assert len(q.choices) == 4
    assert q.mistakes and any(q.mistakes)


@pytest.mark.parametrize("key", KEYS)
def test_variety_and_stage_placement(key):
    draws = [REGISTRY[key].expr(Random(seed)) for seed in range(300)]
    assert len({(draw.prompt, draw.problem_tex) for draw in draws}) >= 180
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.4", "เรนจ์ของฟังก์ชันกำลังสอง", 3,
    )
