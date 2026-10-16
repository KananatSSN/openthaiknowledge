"""Check new ม.6 multi-region areas by independent symbolic integration."""

import math
import re
from random import Random

import pytest
from sympy import integrate, symbols

from otk.api import REGISTRY, catalog
from otk.tests.test_math_chapters import _val

KEYS = (
    "math.area_absolute_line_parabola_m6",
    "math.area_cubic_axis_lobes_m6",
    "math.area_crossing_curves_bounded_m6",
)


def _expected_from_question(key, question):
    x = symbols("x", real=True)
    stem = " ".join(block.tex if block.kind == "math" else block.text for block in question.stem)
    if key == KEYS[0]:
        a = int(re.search(r"y=(\d+)\|x\|", stem).group(1))
        return integrate(a * x - x**2, (x, 0, a)) * 2
    if key == KEYS[1]:
        a2 = int(re.search(r"y=x\^\{3\}-(\d+)x", stem).group(1))
        a = int(a2**0.5)
        assert a * a == a2
        return 2 * integrate(a2 * x - x**3, (x, 0, a))
    a2 = int(re.search(r"y=(\d+)", stem).group(1))
    a = int(a2**0.5)
    assert a * a == a2
    inside = integrate(a2 - x**2, (x, -a, a))
    outside = 2 * integrate(x**2 - a2, (x, a, 2 * a))
    return inside + outside


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(40))
def test_area_matches_independent_integral(key, seed):
    question = REGISTRY[key].generate(Random(seed))
    expected = _expected_from_question(key, question)
    answer = question.choices[question.answer].content[0].tex
    assert math.isclose(_val(answer), float(expected), rel_tol=1e-12)
    assert len(question.choices) == 4
    assert all(mistake is not None for i, mistake in enumerate(question.mistakes) if i != question.answer)
    assert all(not math.isclose(_val(choice.content[0].tex), float(expected), rel_tol=1e-12)
               for i, choice in enumerate(question.choices) if i != question.answer)


@pytest.mark.parametrize("key", KEYS)
def test_catalog_stage_and_variety(key):
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.6", "พื้นที่ระหว่างเส้นโค้ง", 3,
    )
    stems = {tuple((block.kind, getattr(block, "text", getattr(block, "tex", "")))
                   for block in REGISTRY[key].generate(Random(seed)).stem)
             for seed in range(100)}
    assert len(stems) >= 6
