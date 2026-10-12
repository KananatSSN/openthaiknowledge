"""Second formats for drill-only topics: each answer re-derived from the stem."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.render.assets import is_diagram
from otk.sets.math.p5 import types_of_quadrilaterals as mf

SEEDS = range(300)
KEYS = keys_from("math_formats")


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _nums(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace(",", ""))]


def test_six_sets_and_every_figure_ships():
    assert len(KEYS) == 6
    assert all(is_diagram(p.asset_id) for p in mf.QUAD_PICTURES)


@pytest.mark.parametrize("key", KEYS)
def test_four_distinct_choices(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        choices = [_choice(c) for c in q.choices]
        assert len(choices) == REGISTRY[key].max_choices and len(set(choices)) == REGISTRY[key].max_choices, (key, seed, choices)


def test_missing_digit_makes_the_sentence_true_and_only_it_does():
    for seed in SEEDS:
        q = generate("math.missing_digit_p2", Random(seed))
        tex = [b.tex for b in q.stem if b.kind == "math"][0].replace(r"\square ", "?")
        a, op, b, c = re.fullmatch(r"([\d?]+) ([+-]) ([\d?]+) = ([\d?]+)", tex).groups()

        def holds(d):
            x, y, z = (int(t.replace("?", str(d))) for t in (a, b, c))
            return x + y == z if op == "+" else x - y == z
        assert [d for d in range(10) if holds(d)] == [int(_answer(q))], (seed, tex)
        assert max(int(t.replace("?", "9")) for t in (a, b, c)) <= 1000


def test_division_check():
    for seed in SEEDS:
        q = generate("math.division_check_p3", Random(seed))
        stem = _stem(q)
        if stem.startswith("การหารครั้งหนึ่ง"):
            d, quo, r = _nums(stem)
            assert int(_answer(q)) == d * quo + r and r < d
        elif stem.startswith("แบ่ง"):
            d, quo, r = _nums(stem)
            assert int(_answer(q)) == d * quo + r and r < d
        else:
            n, d = _nums(stem)
            lhs, _, quo, r = _nums(_answer(q))
            assert lhs == n and n == d * quo + r and r < d


def test_partial_products_equal_the_product():
    for seed in SEEDS:
        q = generate("math.multiply_partial_products_p4", Random(seed))
        a, b = _nums(_stem(q))[:2]
        if _stem(q).startswith("ข้อใด"):
            x, y, z, w = _nums(_answer(q))
            assert x * y + z * w == a * b and {y, w} == {b // 10 * 10, b % 10}
        else:
            assert int(_answer(q)) == a * b


def test_quadrilateral_names_and_parallel_pairs():
    for seed in SEEDS:
        q = generate("math.quadrilateral_picture_p5", Random(seed))
        [img] = [b for b in q.stem if b.kind == "image"]
        quad = next(p.quad for p in mf.QUAD_PICTURES if p.asset_id == img.asset_id)
        if "กี่คู่" in _stem(q):
            assert _answer(q) == f"{sum(1 for m in quad.parallel if m) // 2} คู่"
        else:
            assert _answer(q) == quad.thai


def test_factor_lists():
    for seed in SEEDS:
        q = generate("math.factors_p6", Random(seed))
        n = _nums(_stem(q))[-1]
        if "ทั้งหมด" in _stem(q):
            assert _nums(_answer(q)) == [d for d in range(1, n + 1) if n % d == 0]
        else:
            assert n % int(_answer(q)) != 0
            assert all(n % int(_choice(c)) == 0 for i, c in enumerate(q.choices) if i != q.answer)


def test_decimal_division_in_context():
    for seed in SEEDS:
        q = generate("math.decimal_word_problem_p6", Random(seed))
        values = [float(v) for v in re.findall(r"\d+(?:\.\d+)?", _stem(q).replace(",", ""))]
        ans = float(_answer(q).replace(",", ""))
        stem = _stem(q)
        if "กิโลกรัมละ" in stem:
            price, paid = values
            assert abs(price * ans - paid) < 1e-6
        else:
            first, second = values
            total, parts = (second, first) if stem.startswith("เพื่อน") else (first, second)
            assert abs(ans * parts - total) < 1e-6, (seed, stem)
