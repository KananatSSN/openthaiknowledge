"""ป.2–ป.3 picture sets: every picture ships, and every answer is re-derived
here from the spec the picture was drawn from."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.render.assets import is_diagram
from otk.sets._support import math_pictures_p2 as mp2

SEEDS = range(300)
KEYS = keys_from("math_pictures_p2")
SPECS = {s.asset_id: s for s in (*mp2.ARRAYS, *mp2.GROUPS, *mp2.MONEY, *mp2.BLOCKS,
                                 *mp2.SHADED, *mp2.GROWING)}


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
    assert len(SPECS) == len(mp2.ALL_PICTURE_IDS)
    assert [i for i in SPECS if not is_diagram(i)] == []


@pytest.mark.parametrize("key", KEYS)
def test_four_distinct_choices_and_alt_text_without_numbers(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        _, img = _spec(q)
        assert not re.search(r"\d", img.alt), (key, img.alt)
        choices = [_choice(c) for c in q.choices]
        assert len(choices) == REGISTRY[key].max_choices and len(set(choices)) == REGISTRY[key].max_choices, (key, seed, choices)


def _sentence(s: str) -> tuple[int, str, int, int]:
    a, op, b, c = re.fullmatch(r"(\d+) (\\times|\\div|\+|-) (\d+) = (\d+)", s).groups()
    return int(a), op, int(b), int(c)


def test_multiplication_reads_rows_or_plates():
    for seed in SEEDS:
        q = generate("math.multiplication_picture_p2", Random(seed))
        spec, _ = _spec(q)
        n, each = (spec.rows, spec.cols) if isinstance(spec, mp2.Array) else (spec.groups, spec.size)
        if "ประโยคสัญลักษณ์" in _text(q):
            assert _sentence(_answer(q)) == (n, r"\times", each, n * each)
        else:
            assert int(_answer(q)) == n * each


def test_division_reads_the_plates():
    for seed in SEEDS:
        q = generate("math.division_picture_p2", Random(seed))
        g, _ = _spec(q)
        stem = _text(q)
        total = g.groups * g.size
        if "ประโยคสัญลักษณ์" in stem:
            assert _sentence(_answer(q)) == (total, r"\div", g.groups, g.size)
        elif stem.endswith("ได้กี่จาน"):
            assert f"จานละ {g.size} " in stem and int(_answer(q)) == g.groups
        else:
            assert f"ใส่จาน {g.groups} ใบ" in stem and int(_answer(q)) == g.size
        if "ประโยคสัญลักษณ์" not in stem:
            assert f" {total} " in stem


def test_money_adds_every_piece():
    for m in mp2.MONEY:
        assert m.total <= 1000 and len(m.pieces) >= 2
        assert all(v in mp2.COINS + mp2.NOTES for v, _ in m.pieces)
    for seed in SEEDS:
        q = generate("math.money_picture_p2", Random(seed))
        m, _ = _spec(q)
        assert int(_answer(q)) == sum(v * n for v, n in m.pieces)


def test_blocks_read_hundreds_tens_ones():
    assert any(b.tens == 0 for b in mp2.BLOCKS)
    for seed in SEEDS:
        q = generate("math.base_ten_blocks_p2", Random(seed))
        b, _ = _spec(q)
        if "รูปกระจาย" in _text(q):
            parts = [int(p) for p in _answer(q).split(" + ")]
            assert sum(parts) == 100 * b.hundreds + 10 * b.tens + b.ones
            assert all(p in (100 * b.hundreds, 10 * b.tens, b.ones) for p in parts)
        else:
            assert int(_answer(q)) == 100 * b.hundreds + 10 * b.tens + b.ones


def test_fraction_of_a_group_counts_the_asked_colour():
    for seed in SEEDS:
        q = generate("math.fraction_of_group_p3", Random(seed))
        s, _ = _spec(q)
        k = s.k if "สีแดง" in _text(q) else s.n - s.k
        assert _answer(q) == rf"\frac{{{k}}}{{{s.n}}}"


def test_growing_pattern_adds_one_column_each_figure():
    for seed in SEEDS:
        q = generate("math.growing_pattern_picture_p3", Random(seed))
        g, _ = _spec(q)
        stem = _text(q)
        if "เพิ่มขึ้นจากรูปก่อน" in stem:
            assert int(_answer(q)) == g.count(2) - g.count(1) == g.rows
        else:
            n = int(re.search(r"รูปที่ (\d+)", stem).group(1))
            # Figure 1 has start columns, and each figure adds one column of rows.
            assert int(_answer(q)) == g.rows * g.start + g.rows * (n - 1)
