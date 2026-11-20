"""The ม.2 factorising sets added for variety: every answer checked by SymPy, never by the set's own formula."""

from __future__ import annotations

import re
from random import Random

import sympy as sp

from otk.core import generate

SEEDS = range(300)
x, y = sp.symbols("x y")


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _sym(tex: str):
    """A small TeX polynomial as SymPy: (x - 3)(2x + 1), x^{2} + 5x, 3(x - 2)^{2}."""
    s = tex.replace("{,}", "").replace("−", "-").replace("^{", "**(").replace("}", ")")
    s = re.sub(r"(\d)\s*([xy(])", r"\1*\2", s)
    s = re.sub(r"\)\s*([xy(\d])", r")*\1", s)
    s = re.sub(r"([xy])\s*\(", r"\1*(", s)
    return sp.sympify(s, locals={"x": x, "y": y})


def _choices(q):
    return [_text(c.content) for c in q.choices], _text(q.choices[q.answer].content)


def _problem(q) -> str:
    return next(b.tex for b in q.stem if b.kind == "math")


def _is_factored(tex: str) -> bool:
    """A product of factors, not a sum: no + or − outside brackets after the first factor."""
    depth, outside = 0, ""
    for ch in tex:
        depth += ch == "("
        depth -= ch == ")"
        if depth == 0:
            outside += ch
    return not re.search(r"\S\s*[+-]\s*\S", outside.replace("^{2}", ""))


def test_factorisations_expand_back_and_only_the_answer_does():
    for key in ("difference_squares", "perfect_square", "leading_coeff", "grouping"):
        for seed in SEEDS:
            q = generate(f"math.factor_{key}_m2", Random(seed))
            target = sp.expand(_sym(_problem(q)))
            texts, right = _choices(q)
            assert sp.expand(_sym(right)) == target, (key, seed, right)
            assert _is_factored(right), (key, seed, right)
            for t in texts:
                if t != right:
                    # A wrong choice must really be wrong (or not factorised at all).
                    assert sp.expand(_sym(t)) != target or not _is_factored(t), (key, seed, t)


def test_identify_picks_the_expansion():
    for seed in SEEDS:
        q = generate("math.factor_identify_m2", Random(seed))
        target = sp.expand(_sym(_problem(q)))
        texts, right = _choices(q)
        assert sp.expand(_sym(right)) == target
        assert sum(sp.expand(_sym(t)) == target for t in texts) == 1


def test_missing_term_matches_the_factorisation():
    for seed in SEEDS:
        q = generate("math.factor_missing_term_m2", Random(seed))
        stem = _text(q.stem).replace("−", "-")
        p = int(re.search(r"\(x ([+-]) (\d+)\)\(x \+ \?\)", stem).group(0)[3] + re.search(r"\(x [+-] (\d+)\)", stem).group(1))
        k = int(_choices(q)[1])
        if "kx" in stem:
            c = int(re.search(r"kx ([+-]) (\d+)", stem).group(1) + re.search(r"kx [+-] (\d+)", stem).group(1))
            other = sp.Rational(c, p)
            assert other.is_integer and k == p + other, stem
        else:
            b = int(re.search(r"x² ([+-]) (\d+)x", stem).group(1) + re.search(r"x² [+-] (\d+)x", stem).group(1))
            assert k == p * (b - p), stem


def test_number_trick_values():
    for seed in SEEDS:
        q = generate("math.factor_number_trick_m2", Random(seed))
        a, b = (int(n) for n in re.findall(r"(\d+)\^\{2\}", _problem(q)))
        assert int(_choices(q)[1].replace("{,}", "")) == a * a - b * b
