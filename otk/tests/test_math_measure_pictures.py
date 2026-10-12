"""Instruments and icon pictographs: every picture ships, and every answer is
re-derived here from the spec the picture was drawn from."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.render.assets import is_diagram
from otk.sets._support import math_measure_pictures as mm
from otk.sets._support.math_pictures import KINDS

SEEDS = range(300)
KEYS = keys_from("math_measure_pictures")
SPECS = {s.asset_id: s for s in (*mm.RULERS, *mm.PICTOGRAPHS_P1, *mm.PICTOGRAPHS_P2,
                                 *mm.SCALES, *mm.JUGS, *mm.CUBES)}
THAI = {k.thai: k.key for k in KINDS}


def _text(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _spec(q):
    [img] = [b for b in q.stem if b.kind == "image"]
    return SPECS[img.asset_id], img


def test_six_sets_and_every_picture_ships():
    assert len(KEYS) == 6
    assert len(SPECS) == len(mm.ALL_PICTURE_IDS)
    assert [i for i in SPECS if not is_diagram(i)] == []


@pytest.mark.parametrize("key", KEYS)
def test_four_distinct_choices_and_alt_text_without_numbers(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        _, img = _spec(q)
        assert not re.search(r"\d", img.alt), (key, img.alt)
        choices = [_choice(c) for c in q.choices]
        assert len(choices) == REGISTRY[key].max_choices and len(set(choices)) == REGISTRY[key].max_choices, (key, seed, choices)


def test_ruler_reads_end_minus_start():
    assert any(r.start for r in mm.RULERS) and all(r.start + r.length <= 15 for r in mm.RULERS)
    for seed in SEEDS:
        q = generate("math.ruler_picture_p1", Random(seed))
        r, _ = _spec(q)
        assert int(_answer(q)) == (r.start + r.length) - r.start


def _named_kind(text: str) -> str:
    return THAI[max((n for n in THAI if n in text), key=len)]


@pytest.mark.parametrize("key", ["math.pictograph_picture_p1", "math.pictograph_key_picture_p2"])
def test_pictographs(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        p, _ = _spec(q)
        per = int(m.group(1)) if (m := re.search(r"1 รูป แทน (\d+)", _text(q))) else 1
        assert per == p.key
        values = {k: n * per for k, n in p.rows}
        assert len(set(values.values())) == len(values)
        stem = _text(q)
        if "มากที่สุด" in stem or "น้อยที่สุด" in stem:
            pick = max if "มากที่สุด" in stem else min
            assert THAI[_answer(q)] == pick(values, key=values.get)
        elif "มากกว่า" in stem:
            a, b = re.search(r"จากแผนภูมิ (\S+)มากกว่า(\S+)อยู่เท่าใด", stem).groups()
            assert int(_answer(q)) == values[_named_kind(a)] - values[_named_kind(b)]
        else:
            assert int(_answer(q)) == values[_named_kind(stem.split("มี")[-1])]


def test_scale_reads_kilograms_and_khit():
    for seed in SEEDS:
        q = generate("math.scale_picture_p2", Random(seed))
        s, _ = _spec(q)
        kg = re.search(r"(\d+) กิโลกรัม", _answer(q))
        khit = re.search(r"(\d+) ขีด", _answer(q))
        total = (int(kg.group(1)) if kg else 0) * 10 + (int(khit.group(1)) if khit else 0)
        assert total == 10 * s.kg + s.khit and s.kg < s.top


def test_jug_reads_the_level():
    assert all(j.level % j.step == 0 and 0 < j.level < j.top for j in mm.JUGS)
    for seed in SEEDS:
        q = generate("math.jug_picture_p3", Random(seed))
        j, _ = _spec(q)
        assert int(_answer(q)) == j.level


def test_cubes_multiply_out():
    for seed in SEEDS:
        q = generate("math.unit_cubes_p5", Random(seed))
        c, _ = _spec(q)
        assert int(_answer(q)) == c.w * c.d * c.h
