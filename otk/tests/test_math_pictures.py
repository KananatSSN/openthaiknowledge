"""ป.1 picture sets: every picture ships, and every answer is re-derived here
from the spec the picture was drawn from, not from the generator's arithmetic."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from random import Random

import pytest

from otk.core import generate
from otk.core.render.assets import is_diagram
from otk.sets._support import math_pictures as mp

SEEDS = range(300)
KEYS = keys_from("math_pictures")
SPECS = {s.asset_id: s for s in (*mp.ALL_SCENES, *mp.TWO_ROWS, *mp.JOINED, *mp.CROSSED,
                                 *mp.HIDDEN, *mp.BUNDLES)}
THAI = {k.thai: k for k in mp.KINDS}


def _text(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _spec(q):
    [img] = [b for b in q.stem if b.kind == "image"]
    return SPECS[img.asset_id], img


def _asked_kind(stem: str) -> mp.Kind:
    # The longest name wins: "ลูกบอล" is not "ลูกโป่ง", "ดอกไม้" is not "ดาว".
    return THAI[max((name for name in THAI if name in stem), key=len)]


def test_nine_sets_and_every_picture_ships():
    assert len(KEYS) == 9
    assert len(SPECS) == len(mp.ALL_PICTURE_IDS)
    assert [i for i in SPECS if not is_diagram(i)] == []


@pytest.mark.parametrize("key", KEYS)
def test_questions_show_a_picture_whose_alt_text_hides_the_answer(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        _, img = _spec(q)
        assert not re.search(r"\d", img.alt), (key, img.alt)
        choices = [_choice(c) for c in q.choices]
        assert len(choices) >= 3 and len(set(choices)) == len(choices), (key, seed)


def test_counting_answers_recount_the_picture():
    for key in ("math.count_objects_p1", "math.count_objects_20_p1", "math.count_kind_p1"):
        zeros = 0
        for seed in SEEDS:
            q = generate(key, Random(seed))
            scene, _ = _spec(q)
            kind = _asked_kind(_text(q))
            expected = sum(1 for k, _, _ in scene.items if k == kind.key)
            zeros += expected == 0
            assert _answer(q) == str(expected), (key, seed)
            assert kind.unit in _text(q)
        assert (zeros > 0) == (key == "math.count_kind_p1")


def test_count_ranges_follow_the_curriculum_ramp():
    assert {len(s.items) for s in mp.SMALL_COUNTS} == set(range(1, 11))
    assert {len(s.items) for s in mp.LARGE_COUNTS} == set(range(11, 21))
    assert max(len(s.items) for s in mp.MIXED) <= 12


def test_ordinal_answers_read_the_line():
    for seed in SEEDS:
        q = generate("math.ordinal_position_p1", Random(seed))
        line, _ = _spec(q)
        names = [mp.BY_KEY[k].thai for k, _, _ in line.items]
        stem = _text(q)
        from_left = "ทางซ้าย" in stem
        if stem.startswith("สิ่งของลำดับ"):
            words = {w: n for n, w in {1: "หนึ่ง", 2: "สอง", 3: "สาม", 4: "สี่", 5: "ห้า",
                                       6: "หก", 7: "เจ็ด"}.items()}
            pos = words[re.search(r"ลำดับที่(\S+?)นับ", stem).group(1)]
            order = names if from_left else names[::-1]
            assert _answer(q) == order[pos - 1], seed
        else:
            kind = _asked_kind(stem)
            index = names.index(kind.thai)
            assert int(_answer(q)) == (index + 1 if from_left else len(names) - index), seed


def test_bundles_are_tens_and_ones():
    for seed in SEEDS:
        q = generate("math.count_bundles_p1", Random(seed))
        b, _ = _spec(q)
        if "กี่สิบ" in _text(q):
            assert _answer(q) == f"{b.tens} สิบ {b.ones} หน่วย"
        else:
            assert _answer(q) == str(10 * b.tens + b.ones)


def test_group_comparison():
    for seed in SEEDS:
        q = generate("math.compare_groups_p1", Random(seed))
        r, _ = _spec(q)
        counts = {mp.BY_KEY[r.top].thai: r.top_n, mp.BY_KEY[r.bottom].thai: r.bottom_n}
        if _text(q) == "จากภาพ ข้อใดถูกต้อง":
            names = "|".join(counts)
            for i, c in enumerate(q.choices):
                m = re.fullmatch(rf"({names})(มากกว่า|น้อยกว่า|กับ)({names})(มีจำนวนเท่ากัน)?",
                                 _choice(c))
                a, rel, b = counts[m.group(1)], m.group(2), counts[m.group(3)]
                holds = {"มากกว่า": a > b, "น้อยกว่า": a < b, "กับ": a == b}[rel]
                assert holds == (i == q.answer), (seed, _choice(c))
        else:
            assert int(_answer(q)) == abs(r.top_n - r.bottom_n)


def _sentence(answer: str) -> tuple[int, str, int, int]:
    a, op, b, c = re.fullmatch(r"(\d+) ([+-]) (\d+) = (\d+)", answer).groups()
    return int(a), op, int(b), int(c)


def test_joining_and_taking_away():
    for seed in SEEDS:
        q = generate("math.add_pictures_p1", Random(seed))
        j, _ = _spec(q)
        if "ประโยคสัญลักษณ์" in _text(q):
            assert _sentence(_answer(q)) == (j.a, "+", j.b, j.a + j.b)
        else:
            assert int(_answer(q)) == j.a + j.b

        q = generate("math.subtract_pictures_p1", Random(seed))
        c, _ = _spec(q)
        left = c.total - c.gone
        if "ประโยคสัญลักษณ์" in _text(q):
            assert _sentence(_answer(q)) == (c.total, "-", c.gone, left)
            wrong = [_sentence(_choice(x)) for i, x in enumerate(q.choices) if i != q.answer]
            assert (c.total, "-", c.gone, left) not in wrong
        else:
            assert int(_answer(q)) == left


def test_hidden_part():
    for seed in SEEDS:
        q = generate("math.part_whole_p1", Random(seed))
        h, _ = _spec(q)
        assert f"ทั้งหมด {h.total} " in _text(q)
        assert int(_answer(q)) == h.inside
