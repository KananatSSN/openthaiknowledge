"""Second formats for drill-only secondary topics: answers re-derived here."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.render.assets import is_diagram
from otk.sets.math.m3 import trigonometric_ratios as mh
from otk.sets.math.m2.congruence import CONGRUENT_PAIRS
from otk.sets.math.m1.prime_factorisation import FACTOR_TREES, _nodes
from otk.sets.math.m1.geometric_constructions import _NOT_REACHABLE, _constructible
from otk.sets.math.m5.combinations import _ORDERED, _UNORDERED

SEEDS = range(300)
KEYS = keys_from("math_formats_hi")


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _nums(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"-?\d+", s.replace(",", ""))]


def test_ten_sets_and_every_figure_ships():
    assert len(KEYS) == 10
    ids = ([t.asset_id for t in FACTOR_TREES] + [p.asset_id for p in CONGRUENT_PAIRS]
           + [t.asset_id for t in mh.SPECIAL_TRIANGLES])
    assert len(set(ids)) == len(ids)
    assert all(is_diagram(i) for i in ids)


@pytest.mark.parametrize("key", KEYS)
def test_four_distinct_choices(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        choices = [_choice(c) for c in q.choices]
        assert len(choices) == REGISTRY[key].max_choices and len(set(choices)) == REGISTRY[key].max_choices, (key, seed, choices)


def _sci_value(tex: str) -> float:
    m, e = re.fullmatch(r"([\d.]+) \\times 10\^\{(-?\d+)\}", tex).groups()
    return float(m) * 10 ** int(e)


def test_scientific_comparison():
    for seed in SEEDS:
        q = generate("math.scientific_compare_m1", Random(seed))
        values = [_sci_value(_choice(c)) for c in q.choices]
        pick = max if "มากที่สุด" in _stem(q) else min
        assert values[q.answer] == pick(values)


def test_factor_trees_multiply_out():
    for t in FACTOR_TREES:
        for node in _nodes(t.tree):
            if node.children:
                assert math.prod(c.value for c in node.children) == node.value
            else:
                assert all(node.value % d for d in range(2, node.value))
    for seed in SEEDS:
        q = generate("math.factor_tree_m1", Random(seed))
        [img] = [b for b in q.stem if b.kind == "image"]
        t = next(x for x in FACTOR_TREES if x.asset_id == img.asset_id)
        if t.hidden:
            assert int(_answer(q)) == _nodes(t.tree)[t.hidden].value
        else:
            product = 1
            for base, _, exp in re.findall(r"(\d+)(\^\{(\d+)\})?", _answer(q)):
                product *= int(base) ** int(exp or 1)
            assert product == t.n


def test_constructed_angles():
    reachable = _constructible()
    assert not set(_NOT_REACHABLE) & reachable
    for seed in SEEDS:
        q = generate("math.construct_angle_m1", Random(seed))
        if "สร้างไม่ได้" in _stem(q):
            assert int(_answer(q)) not in reachable
            assert all(float(_choice(c)) in reachable
                       for i, c in enumerate(q.choices) if i != q.answer)
        else:
            assert float(_answer(q)) in reachable


def test_missing_exponent_makes_the_law_hold():
    for seed in SEEDS:
        q = generate("math.missing_exponent_m2", Random(seed))
        tex = [b.tex for b in q.stem if b.kind == "math"][0]
        k = int(_answer(q))
        ns = [int(x) for x in re.findall(r"\^\{(-?\d+)\}", tex)]
        if r"\cdot" in tex:
            m, n = ns
            assert k + m == n
        elif r"\left(" in tex:
            m, n = ns
            assert k * m == n
        elif r"\frac{1}" in tex:
            [m] = ns
            assert k == -m
        else:
            n, m = ns
            assert n - k == m


def test_formulas_give_back_the_given_value():
    for seed in SEEDS:
        q = generate("math.formula_context_m2", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _nums(s.replace("9C/5 + 32", "").replace("PRT/100", "").replace("²", ""))
        if "F =" in s:
            assert Fraction(9 * ans, 5) + 32 == n[-1]
        elif "คางหมู" in s:
            area, a, b = n[-3:]
            assert Fraction(a + b, 2) * ans == area
        elif "v = u + at" in s:
            u, acc, v = n[-3:]
            assert u + acc * ans == v
        elif "P = 2(w + l)" in s:
            p, length = n[-2:]
            assert 2 * (ans + length) == p
        else:
            principal, t, i = n[-3:]
            assert principal * ans * t == 100 * i


def _eval(tex: str) -> float:
    py = re.sub(r"\\frac\{(.+)\}\{(.+)\}", r"(\1)/(\2)", tex)
    py = re.sub(r"\\sqrt\{(\d+)\}", r"math.sqrt(\1)", py)
    py = re.sub(r"(\d)(math)", r"\1*\2", py).replace(r"\cdot", "*")
    return eval(py, {"math": math})


def test_exactly_one_radical_statement_is_true():
    for seed in SEEDS:
        q = generate("math.radical_true_statement_m4", Random(seed))
        truth = []
        for c in q.choices:
            lhs, rhs = _choice(c).split(" = ")
            truth.append(math.isclose(_eval(lhs), _eval(rhs)))
        assert truth.count(True) == 1 and truth[q.answer], (seed, [_choice(c) for c in q.choices])


def test_order_and_average_choices():
    for seed in SEEDS:
        q = generate("math.order_matters_m5", Random(seed))
        pool = _UNORDERED if "ไม่คำนึงถึงลำดับ" in _stem(q) else _ORDERED
        assert _answer(q) in pool
        assert sum(_choice(c) in pool for c in q.choices) == 1

        q = generate("math.choose_average_m6", Random(seed))
        s = _stem(q)
        expected = ("มัธยฐาน" if "เงินเดือน" in s
                    else "ฐานนิยม" if "นิยมมากที่สุด" in s else "ค่าเฉลี่ยเลขคณิต")
        assert _answer(q) == expected


def _surd_value(tex: str) -> float:
    m = re.fullmatch(r"(\d*)(?:\\sqrt\{(\d+)\})?", tex)
    coef, rad = m.group(1), m.group(2)
    return (int(coef) if coef else 1) * math.sqrt(int(rad) if rad else 1)


def test_special_triangles_follow_the_angle():
    for t in mh.SPECIAL_TRIANGLES:
        side = {k: _surd_value(mh._surd(*v)) for k, v in t.sides.items()}
        theta = math.radians(t.angle)
        assert math.isclose(side["opp"] / side["hyp"], math.sin(theta))
        assert math.isclose(side["adj"] / side["hyp"], math.cos(theta))
        assert side[t.given] == t.value
    for seed in SEEDS:
        q = generate("math.special_triangle_picture_m3", Random(seed))
        [img] = [b for b in q.stem if b.kind == "image"]
        t = next(x for x in mh.SPECIAL_TRIANGLES if x.asset_id == img.asset_id)
        # From the given side and the angle alone.
        theta = math.radians(t.angle)
        ratio = {"opp": math.sin(theta), "adj": math.cos(theta), "hyp": 1.0}
        expected = t.value / ratio[t.given] * ratio[t.asked]
        assert math.isclose(_surd_value(_answer(q)), expected), (seed, t)
