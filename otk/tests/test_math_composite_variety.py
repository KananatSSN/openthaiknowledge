"""Independent algebra checks for added ม.4 composition sets."""

import math
import re
from fractions import Fraction
from random import Random

import pytest
from sympy import Interval, oo, solve, solve_univariate_inequality, symbols

from otk.api import REGISTRY, catalog
from otk.kit.math_problems import frac_tex
from otk.tests.test_math_chapters import _val

KEYS = (
    "math.composite_equation_m4",
    "math.composite_sqrt_domain_m4",
    "math.composite_recover_inner_m4",
)


def _linear(tex):
    if "x" not in tex:
        return 0, int(tex)
    match = re.fullmatch(r"(-?\d*|)x(?: ([+-]) (\d+))?", tex)
    assert match, tex
    a = -1 if match.group(1) == "-" else 1 if match.group(1) == "" else int(match.group(1))
    b = int(match.group(3) or 0)
    return a, -b if match.group(2) == "-" else b


def _expected(key, q):
    x = symbols("x", real=True)
    formula = q.stem[1].tex
    if key == KEYS[0]:
        f_tex, g_tex = formula.split(r",\quad g(x)=")
        a, b = _linear(f_tex.removeprefix("f(x)="))
        c, d = _linear(g_tex)
        target = int(re.search(r"= (-?\d+) แล้ว", q.stem[2].text).group(1))
        return solve(a * (c * x + d) + b - target, x)[0]
    if key == KEYS[1]:
        radicand, g_tex = formula.split(r"},\quad g(x)=")
        inner = radicand.removeprefix(r"f(x)=\sqrt{")
        offset = int(re.search(r"x ([+-]) (\d+)", inner).group(2)) if inner != "x" else 0
        if " - " in inner:
            offset = -offset
        a, c = _linear(g_tex)
        domain = solve_univariate_inequality(a * x + c + offset >= 0, x, relational=False)
        assert isinstance(domain, Interval)
        if domain.end == oo:
            return rf"[{frac_tex(Fraction(domain.start))}, \infty)"
        return rf"(-\infty, {frac_tex(Fraction(domain.end))}]"
    f_tex, composed_tex = formula.split(r",\quad (f\circ g)(x)=")
    a, b = _linear(f_tex.removeprefix("f(x)="))
    slope, intercept = _linear(composed_tex)
    recovered = (slope * x + intercept - b) / a
    return _linear(q.choices[q.answer].content[0].tex), recovered


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(120))
def test_independent_answer_and_named_choices(key, seed):
    q = REGISTRY[key].generate(Random(seed))
    expected = _expected(key, q)
    answer_tex = q.choices[q.answer].content[0].tex
    if key == KEYS[0]:
        assert math.isclose(_val(answer_tex), float(expected), rel_tol=1e-12)
        assert all(not math.isclose(_val(choice.content[0].tex), float(expected), rel_tol=1e-12)
                   for i, choice in enumerate(q.choices) if i != q.answer)
    elif key == KEYS[1]:
        assert answer_tex == expected
        assert all(choice.content[0].tex != expected
                   for i, choice in enumerate(q.choices) if i != q.answer)
    else:
        (slope, intercept), recovered = expected
        x = symbols("x", real=True)
        assert slope * x + intercept == recovered
        assert all(_linear(choice.content[0].tex)[0] * x + _linear(choice.content[0].tex)[1] != recovered
                   for i, choice in enumerate(q.choices) if i != q.answer)
    assert len(q.choices) == 4
    assert all(m is not None for i, m in enumerate(q.mistakes) if i != q.answer)


@pytest.mark.parametrize("key", KEYS)
def test_catalog_stage_and_variety(key):
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.4", "ฟังก์ชันประกอบ", 3,
    )
    stems = {tuple((block.kind, getattr(block, "text", getattr(block, "tex", "")))
                   for block in REGISTRY[key].generate(Random(seed)).stem)
             for seed in range(200)}
    assert len(stems) >= 100
