"""The sets for gaps the (สสวท) จำนวนจริง exercises exposed: long division by
quadratics, partial fractions, and absolute-value statements — each re-solved
with SymPy, an independent route."""

from __future__ import annotations

import random
import re

import pytest
import sympy as sp

from otk.core import REGISTRY, generate
from otk.sets.math.m4 import absolute_value as tr
from otk.sets.math.m4.polynomial_division import pdivmod
from otk.sets._support.math_bank_textbook_real import ptex
from otk.sets.math.m4.rational_equations_and_inequalities import cover_up

KEYS = ("math.polynomial_long_division_m4", "math.partial_fractions_m4",
        "math.absolute_value_properties_m4")
x = sp.Symbol("x")


def _sp(p):
    return sp.Poly([sp.Rational(c) for c in p], x)


def test_long_division_matches_sympy():
    rng = random.Random(0)
    for _ in range(400):
        a = [rng.randint(-9, 9) for _ in range(rng.randint(1, 7))]
        b = [rng.choice([1, 2, 3])] + [rng.randint(-5, 5) for _ in range(rng.randint(0, 3))]
        q, r = pdivmod(a, b)
        sq, sr = sp.div(_sp(a), _sp(b))
        assert _sp(q).as_expr() == sq.as_expr() and _sp(r).as_expr() == sr.as_expr(), (a, b)


def test_ptex_drops_leading_zeros():
    assert ptex([0, 0, 1, -3, 0]) == "x^{2} - 3x"
    assert ptex([0]) == "0"


def test_cover_up_matches_sympy():
    A, B = sp.symbols("A B")
    for p in range(-4, 5):
        for q in range(-6, 7):
            for a, b in ((1, -2), (3, 0), (-4, 5)):
                got = cover_up(p, q, a, b)
                sol = sp.solve(sp.Poly((p * x + q) - A * (x - b) - B * (x - a), x).coeffs(), [A, B])
                assert (sol[A], sol[B]) == tuple(sp.Rational(v) for v in got)


def test_textbook_partial_fraction_reproduces():
    assert cover_up(5, -7, 3, -1) == (2, 3)      # (5x − 7)/((x − 3)(x + 1)), ท้ายบท 11.1


def test_absolute_value_claims_agree_with_symbolic_truth():
    a, b = sp.symbols("a b", real=True)
    truth = {r"|ab| = |a||b|": True, r"|a + b| \le |a| + |b|": True, r"|a + b| = |a| + |b|": False,
             r"|-a|^{2} = -(a^{2})": False, r"|a - b| \le |a| - |b|": False}
    claims = dict(tr._CLAIMS)
    for t, want in truth.items():
        assert tr.always(lambda a, b: True, claims[t]) is want, t
    # Under ab > 0 the triangle inequality is an equality; under ab < 0 it is strict.
    assert tr.always(lambda a, b: a * b > 0, claims[r"|a + b| = |a| + |b|"])
    assert tr.always(lambda a, b: a * b < 0, claims[r"|a + b| < |a| + |b|"])


def _answer(q) -> str:
    return q.choices[q.answer].content[0].tex


def _poly(tex: str):
    s = re.sub(r"(\d)x", r"\1*x", tex).replace("^{", "**(").replace("}", ")")
    return sp.expand(sp.sympify(s, locals={"x": x}))


def test_long_division_items_recompute():
    for seed in range(150):
        q = generate("math.polynomial_long_division_m4", rng=random.Random(seed))
        lead = q.stem[0].text
        maths = [_poly(b.tex) for b in q.stem if hasattr(b, "tex")]
        got = _poly(_answer(q))
        if lead.startswith("พหุนามที่"):                    # the dividend from b, q, r
            b, quo, rem = maths
            assert got == sp.expand(b * quo + rem)
        else:
            a, b = maths
            sq, sr = sp.div(a, b, x)
            assert got == (sq if lead.startswith("ผลหาร") else sr), seed


def _braced(s: str, i: int) -> tuple[str, int]:
    """The contents of the {...} group opening at s[i], and the index after it."""
    depth = 0
    for j in range(i, len(s)):
        depth += {"{": 1, "}": -1}.get(s[j], 0)
        if depth == 0:
            return s[i + 1:j], j + 1
    raise ValueError(s)


def _fracs(tex: str) -> list[tuple[str, str]]:
    out, i = [], 0
    while (i := tex.find(r"\frac", i)) >= 0:
        num, i = _braced(tex, i + 5)
        den, i = _braced(tex, i)
        out.append((num, den))
    return out


def _expr(tex: str):
    s = re.sub(r"([\dABC)])(x|\()", r"\1*\2", tex)
    s = re.sub(r"x\(", "x*(", s).replace("^{", "**(").replace("}", ")")
    return sp.sympify(s, locals={"x": x, "A": sp.Symbol("A"), "B": sp.Symbol("B"), "C": sp.Symbol("C")})


def test_partial_fraction_items_recompute():
    A, B, C = sp.symbols("A B C")
    for seed in range(150):
        q = generate("math.partial_fractions_m4", rng=random.Random(seed))
        (n0, d0), *parts = _fracs(q.stem[1].tex)
        rhs = sum(_expr(n) / _expr(d) for n, d in parts)
        diff = sp.numer(sp.together(_expr(n0) / _expr(d0) - rhs))
        sol = sp.solve(sp.Poly(sp.expand(diff), x).coeffs(), [s for s in (A, B, C) if diff.has(s)], dict=True)[0]
        ans = _answer(q)
        if "A + B + C" in q.stem[-1].text:
            assert int(ans) == sol[A] + sol[B] + sol[C], seed
        else:
            a, b = re.fullmatch(r"A = (-?\d+),\\ B = (-?\d+)", ans).groups()
            assert (int(a), int(b)) == (sol[A], sol[B]), seed


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    for seed in range(200):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
