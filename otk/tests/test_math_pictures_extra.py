"""Shapes, change, fraction bars, hundred grids and spinners: answers
re-derived from the spec each picture was drawn from."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.render.assets import is_diagram
from otk.sets._support import math_pictures_extra as mx
from otk.sets._support.math_pictures_p2 import MONEY

SEEDS = range(300)
KEYS = keys_from("math_pictures_extra")
SPECS = {s.asset_id: s for s in (*mx.BARS, *mx.GRIDS, *mx.SPINNERS, *MONEY)}
SIDES = {"mshape2d_triangle": 3, "mshape2d_square": 4, "mshape2d_rectangle": 4,
         "mshape2d_pentagon": 5, "mshape2d_hexagon": 6,
         **{p.asset_id: p.sides for p in mx.POLYGON_PICS}}


def _text(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _img(q):
    [img] = [b for b in q.stem if b.kind == "image"]
    return img


def _value(tex: str) -> Fraction:
    m = re.fullmatch(r"(\d*)(?:\\frac\{(\d+)\}\{(\d+)\})?", tex)
    whole, n, d = m.groups()
    return int(whole or 0) + (Fraction(int(n), int(d)) if n else 0)


def test_six_sets_and_every_picture_ships():
    assert len(KEYS) == 6
    assert len(set(mx.ALL_PICTURE_IDS)) == len(mx.ALL_PICTURE_IDS)
    assert [i for i in mx.ALL_PICTURE_IDS if not is_diagram(i)] == []


@pytest.mark.parametrize("key", KEYS)
def test_four_distinct_choices_and_alt_text_without_numbers(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        assert not re.search(r"\d", _img(q).alt), (key, _img(q).alt)
        choices = [_choice(c) for c in q.choices]
        assert len(choices) == REGISTRY[key].max_choices and len(set(choices)) == REGISTRY[key].max_choices, (key, seed, choices)


def test_sides_and_corners():
    shown = set()
    for seed in SEEDS:
        q = generate("math.shape_sides_picture_p2", Random(seed))
        assert int(_answer(q)) == SIDES[_img(q).asset_id]
        shown.add(_img(q).asset_id)
    # Most of the 29 drawings turn up, not the same few.
    assert len(shown) >= 25


@pytest.mark.parametrize("pic", mx.POLYGON_PICS, ids=lambda p: p.asset_id)
def test_every_polygon_is_convex_with_countable_corners(pic):
    """n distinct corners, turning the same way at each, and none flatter
    than 160° — a corner that flat reads as part of a straight side."""
    pts = pic.points
    n = len(pts)
    assert n == pic.sides and len(set(pts)) == n
    turns, angles = [], []
    for i in range(n):
        (ax, ay), (bx, by), (cx, cy) = pts[i - 1], pts[i], pts[(i + 1) % n]
        u, v = (ax - bx, ay - by), (cx - bx, cy - by)
        turns.append((bx - ax) * (cy - by) - (by - ay) * (cx - bx))
        cos = (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
        angles.append(math.degrees(math.acos(max(-1.0, min(1.0, cos)))))
    assert all(t > 0 for t in turns) or all(t < 0 for t in turns)
    assert max(angles) < 160, angles


def test_change_is_paid_minus_price():
    for seed in SEEDS:
        q = generate("math.change_picture_p3", Random(seed))
        paid = SPECS[_img(q).asset_id].total
        price = int(re.search(r"ราคา (\d+) บาท", _text(q)).group(1))
        assert int(_answer(q)) == paid - price > 0


def test_fraction_bars():
    for seed in SEEDS:
        q = generate("math.fraction_bars_p4", Random(seed))
        b = SPECS[_img(q).asset_id]
        assert _value(_answer(q)) == b.wholes + Fraction(b.part, b.d)
        form = "เศษเกิน" if "เศษเกิน" in _text(q) else "คละ"
        if form == "เศษเกิน":
            assert re.fullmatch(r"\\frac\{\d+\}\{\d+\}", _answer(q))
        assert all(_value(_choice(c)) != _value(_answer(q))
                   for i, c in enumerate(q.choices) if i != q.answer)


def test_grids():
    for seed in SEEDS:
        q = generate("math.decimal_grid_p4", Random(seed))
        g = SPECS[_img(q).asset_id]
        assert Fraction(_answer(q)) == g.wholes + Fraction(g.hundredths, 100)
        q = generate("math.percent_grid_p5", Random(seed))
        g = SPECS[_img(q).asset_id]
        shaded = g.hundredths if "ไม่ได้แรเงา" not in _text(q) else 100 - g.hundredths
        assert int(_answer(q)) == shaded


def test_spinners():
    colours = {v: k for k, v in mx.COLOURS.items()}
    for seed in SEEDS:
        q = generate("math.spinner_probability_m3", Random(seed))
        s = SPECS[_img(q).asset_id]
        c = colours[re.search(r"ช่อง(สี\S+)$", _text(q)).group(1)]
        p = Fraction(s.sectors.count(c), len(s.sectors))
        if "จะไม่ชี้ช่อง" in _text(q):
            p = 1 - p
        assert _value(_answer(q)) == p
