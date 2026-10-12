"""ม.4–ม.6 sets read off a drawing: the PNG exists, the answer comes from the
spec the PNG was drawn from, and the alt text is the same for every item."""

from __future__ import annotations

from otk.tests._origins import keys_from

from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.render.assets import is_diagram
from otk.sets._support import math_diagrams_hi as hi
from otk.sets.math.m6.regression import _TREND_R, _TREND_TEXT

SEEDS = range(300)
KEYS = keys_from("math_diagrams_hi")
BY_ID = {s.asset_id: s for s in hi.ALL_HI_DIAGRAMS}


def _images(q):
    return [b for b in q.stem if b.kind == "image"]


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _each(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        yield q, BY_ID[_images(q)[0].asset_id]


def test_five_sets_and_every_spec_has_a_png():
    assert len(KEYS) == 5
    missing = [s.asset_id for s in hi.ALL_HI_DIAGRAMS if not is_diagram(s.asset_id)]
    assert not missing
    assert len(BY_ID) == len(hi.ALL_HI_DIAGRAMS)


@pytest.mark.parametrize("key", KEYS)
def test_shipped_diagram_constant_alt_and_four_choices(key):
    alts = set()
    for seed in SEEDS:
        q = generate(key, Random(seed))
        imgs = _images(q)
        assert len(imgs) == 1 and imgs[0].asset_id in BY_ID
        alts.add(imgs[0].alt)
        assert len(q.choices) == REGISTRY[key].max_choices and len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices, (key, seed)
    assert len(alts) == 1


def test_venn_answers():
    for q, v in _each("math.venn_picture_m4"):
        A, B = v.a_only + v.both, v.b_only + v.both
        U = A + v.b_only + v.neither
        want = {r"n(A \cup B)": A + v.b_only, r"n(A \cap B)": v.both, r"n(A - B)": v.a_only,
                r"n(B')": U - B, r"n(A' \cap B')": v.neither, r"n(A)": A}[q.stem[1].tex]
        assert _answer(q) == str(want)


def test_sine_answers():
    for q, g in _each("math.sine_graph_picture_m5"):
        s = _stem(q)
        if "แอมพลิจูด" in s:
            assert _answer(q) == str(abs(g.a))
        elif "คาบ" in s:
            assert _answer(q) == str(360 // g.b)
        else:
            assert f"\\{g.fn}" in _answer(q)


def test_box_plot_answers():
    for q, b in _each("math.box_plot_picture_m6"):
        s = _stem(q)
        want = ("25" if "ร้อยละ" in s else str(b.med) if "มัธยฐาน" in s
                else str(b.q3 - b.q1) if "ระหว่างควอร์ไทล์" in s
                else str(b.hi - b.lo) if "พิสัย" in s else str(b.q3))
        assert _answer(q) == want


def test_scatter_answers():
    for q, s in _each("math.scatter_plot_picture_m6"):
        assert _answer(q) in (_TREND_TEXT[s.trend], _TREND_R[s.trend])


def _below(z: int) -> Fraction:
    """Percent of the standard normal below z, by the 68–95–99.7 rule."""
    band = {1: Fraction(34), 2: Fraction(27, 2), 3: Fraction(47, 20)}
    if abs(z) >= 9:
        return Fraction(0) if z < 0 else Fraction(100)
    half = sum(band[k] for k in range(1, abs(z) + 1))
    return 50 + half if z >= 0 else 50 - half


def test_normal_areas_follow_the_rule():
    for (lo, hi_), area in hi.NORMAL_AREAS.items():
        assert area == _below(hi_) - _below(lo), (lo, hi_)


def test_normal_answers():
    for q, n in _each("math.normal_curve_picture_m6"):
        assert Fraction(_answer(q)) == hi.NORMAL_AREAS[(n.lo, n.hi)]
