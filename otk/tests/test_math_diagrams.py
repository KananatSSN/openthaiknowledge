"""Math sets read off a drawing: the PNG exists, the answer comes from the
same spec the PNG was drawn from, and the alt text does not give it away."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.render.assets import is_diagram
from otk.sets._support import math_diagrams as md
from otk.sets.math.p4.lines_and_angles import angle_kind

SEEDS = range(300)
KEYS = keys_from("math_diagrams")
BY_ID = {s.asset_id: s for s in md.ALL_MATH_DIAGRAMS}


def _images(q):
    return [b for b in q.stem if b.kind == "image"]


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _stem_text(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _spec(q, i=0):
    return BY_ID[_images(q)[i].asset_id]


def test_twenty_sets_and_every_spec_has_a_png():
    assert len(KEYS) == 20
    missing = [s.asset_id for s in md.ALL_MATH_DIAGRAMS if not is_diagram(s.asset_id)]
    assert not missing
    assert len({s.asset_id for s in md.ALL_MATH_DIAGRAMS}) == len(md.ALL_MATH_DIAGRAMS)


@pytest.mark.parametrize("key", KEYS)
def test_every_question_shows_a_shipped_diagram_and_four_choices(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        imgs = _images(q)
        assert imgs and all(i.asset_id in BY_ID for i in imgs)
        assert len(q.choices) == REGISTRY[key].max_choices and len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices, (key, seed)


FIGURE_KEYS = {"math.rectangle_figure_p4", "math.quadrilateral_area_figure_p5",
               "math.triangle_area_figure_p6", "math.composite_area_figure_p6",
               "math.pythagoras_figure_m2"}


@pytest.mark.parametrize("key", KEYS)
def test_alt_text_never_states_the_answer(key):
    """Where the answer is read off the picture, the alt text is the same for
    every question, so it cannot carry the reading. A labelled figure's alt
    text states exactly the measurements drawn on it, which are the data."""
    alts = set()
    for seed in SEEDS:
        q = generate(key, Random(seed))
        for img in _images(q):
            if key in FIGURE_KEYS:
                assert img.alt == md.figure_alt(BY_ID[img.asset_id])
            else:
                alts.add(img.alt.split(": ")[-1])
    assert key in FIGURE_KEYS or len(alts) == 1, (key, alts)


def test_shape_and_solid_names():
    for seed in SEEDS:
        q = generate("math.shape_2d_picture_p1", Random(seed))
        assert _answer(q) == _spec(q).thai
        q = generate("math.solid_picture_p1", Random(seed))
        assert _answer(q) == _spec(q).thai
        q = generate("math.net_picture_m1", Random(seed))
        assert _answer(q) == _spec(q).thai


def test_clock_reading_and_duration():
    for seed in SEEDS:
        q = generate("math.clock_read_p2", Random(seed))
        c = _spec(q)
        assert _answer(q) == f"{c.h}.{c.m:02d} น."
        q = generate("math.clock_duration_p3", Random(seed))
        a, b = _spec(q, 0), _spec(q, 1)
        gap = ((b.h % 12) * 60 + b.m - (a.h % 12) * 60 - a.m) % 720
        assert int(_answer(q)) == gap


def test_fraction_picture():
    for seed in SEEDS:
        q = generate("math.fraction_picture_p3", Random(seed))
        f = _spec(q)
        n = f.d - f.n if "ไม่แรเงา" in _stem_text(q) else f.n
        assert _answer(q) == rf"\frac{{{n}}}{{{f.d}}}"


def test_angles():
    for seed in SEEDS:
        q = generate("math.protractor_read_p4", Random(seed))
        assert int(_answer(q)) == _spec(q).deg
        q = generate("math.angle_kind_picture_p4", Random(seed))
        assert _answer(q) == angle_kind(_spec(q).deg)


def test_figures():
    for seed in SEEDS:
        q = generate("math.rectangle_figure_p4", Random(seed))
        f = _spec(q)
        w, length = (f.dims[0], f.dims[0]) if f.kind == "square" else f.dims
        want = w * length if "พื้นที่" in _stem_text(q) else 2 * (w + length)
        assert int(_answer(q)) == want
        q = generate("math.quadrilateral_area_figure_p5", Random(seed))
        f = _spec(q)
        want = f.dims[0] * f.dims[1] if f.kind == "para" else Fraction((f.dims[0] + f.dims[1]) * f.dims[2], 2)
        assert Fraction(_answer(q)) == want
        q = generate("math.triangle_area_figure_p6", Random(seed))
        f = _spec(q)
        assert Fraction(_answer(q)) == Fraction(f.dims[0] * f.dims[1], 2)
        q = generate("math.composite_area_figure_p6", Random(seed))
        w, h, cw, ch = _spec(q).dims
        want = w * h - cw * ch if "พื้นที่" in _stem_text(q) else 2 * (w + h)
        assert int(_answer(q)) == want
        q = generate("math.pythagoras_figure_m2", Random(seed))
        f = _spec(q)
        a, b, c = f.dims
        assert a * a + b * b == c * c
        assert int(_answer(q)) == {"a": a, "b": b, "c": c}[f.unknown]


def test_solid_counts():
    for seed in SEEDS:
        q = generate("math.solid_counts_picture_p6", Random(seed))
        s = _spec(q)
        assert s.faces - s.edges + s.vertices == 2          # Euler, as a check on the table
        stem = _stem_text(q)
        want = s.faces if "กี่หน้า" in stem else s.edges if "กี่สัน" in stem else s.vertices
        assert int(_answer(q)) == want


def test_charts():
    for seed in SEEDS:
        q = generate("math.bar_chart_picture_p4", Random(seed))
        bc = _spec(q)
        key = dict(re.findall(r"([A-E]) = ([^\s)]+)", _stem_text(q)))
        vals = {name: bc.values["ABCDE".index(letter)] for letter, name in key.items()}
        ask = q.stem[-1].text
        named = sorted((n for n in vals if n in ask), key=ask.index)
        if "มากกว่า" in ask:
            assert int(_answer(q)) == vals[named[0]] - vals[named[1]]
        elif "ที่สุด" in ask:
            pick = (max if "มากที่สุด" in ask else min)(vals, key=vals.get)
            assert _answer(q) == pick
        else:
            assert int(_answer(q)) == vals[named[0]]
        q = generate("math.line_graph_picture_p5", Random(seed))
        v = _spec(q).values
        ask = q.stem[-1].text
        nums = [int(n) for n in re.findall(r"\d+", ask)]
        if "มากที่สุด" in ask:
            assert int(_answer(q)) == v.index(max(v)) + 1
        elif "ถึง" in ask:
            assert int(_answer(q)) == abs(v[nums[1] - 1] - v[nums[0] - 1])
        else:
            assert int(_answer(q)) == v[nums[0] - 1]


def test_number_line_and_graphs():
    for seed in SEEDS:
        q = generate("math.number_line_picture_m1", Random(seed))
        assert int(_answer(q)) == _spec(q).p
        q = generate("math.linear_graph_read_m1", Random(seed))
        fn = _spec(q)
        stem = _stem_text(q)
        if "ตัดแกน Y" in stem:
            assert _answer(q) == f"(0, {fn.c})"
        elif "ค่าของ y" in stem:
            x = int(re.search(r"x = (-?\d+)", stem).group(1))
            assert int(_answer(q)) == fn.m * x + fn.c
        else:
            y = int(re.search(r"y = (-?\d+)", stem).group(1))
            assert fn.m * int(_answer(q)) + fn.c == y
        q = generate("math.linear_function_graph_m2", Random(seed))
        fn = _spec(q)
        if "ความชัน" in _stem_text(q):
            assert int(_answer(q)) == fn.m
        else:
            m = re.fullmatch(r"y = (-?\d*)x(?: ([+-]) (\d+))?", _answer(q))
            slope = {"": 1, "-": -1}.get(m.group(1), None)
            slope = slope if slope is not None else int(m.group(1))
            c = 0 if not m.group(2) else int(m.group(3)) * (1 if m.group(2) == "+" else -1)
            assert (slope, c) == (fn.m, fn.c)
        q = generate("math.parabola_graph_m3", Random(seed))
        p = _spec(q)
        stem = _stem_text(q)
        if "จุดยอด" in stem:
            assert _answer(q) == f"({p.h}, {p.k})"
        elif "แกนสมมาตร" in stem:
            assert _answer(q) == f"x = {p.h}"
        else:
            assert int(_answer(q)) == p.k
            assert ("ต่ำสุด" in stem) == (p.a > 0)
