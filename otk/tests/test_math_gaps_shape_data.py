"""Primary geometry, fraction and data gap sets: each answer re-derived from
the question, each choice distinct, and each construction step the one that
really comes next."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m2.geometric_reasoning import _ANGLE_METHODS
from otk.sets.math.p6.solids import _NETS
from otk.sets.math.p5.prism import _POLY

SEEDS = range(250)
KEYS = sorted(keys_from("math_gaps_shape_data"))
_SIDES = {v: k for k, v in _POLY.items()}


def _choice(c) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in c.content)


def _stem(q) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in q.stem)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _nums(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s)]


def _frac(tex: str) -> Fraction:
    tex = tex.strip()
    m = re.fullmatch(r"(\d*)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if m:
        return int(m.group(1) or 0) + Fraction(int(m.group(2)), int(m.group(3)))
    return Fraction(int(tex))


def test_fourteen_sets_are_registered():
    assert len(KEYS) == 14


@pytest.mark.parametrize("key", KEYS)
def test_choices_are_distinct_and_full(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        texts = [_choice(c) for c in q.choices]
        assert len(texts) == len(set(texts)) == REGISTRY[key].max_choices, (seed, texts)


def test_prism_names_and_counts():
    for seed in SEEDS:
        q = generate("math.prism_name_p5", Random(seed))
        s = _stem(q)
        m = re.search(r"ฐานเป็นรูป(\S+เหลี่ยม) เรียกว่า", s)
        if m:
            assert _answer(q) == f"ปริซึม{m.group(1)}"
        else:
            n = _nums(s)[0]
            assert _answer(q) == f"รูป{_POLY[n]}"
        q = generate("math.prism_counts_p5", Random(seed))
        s = _stem(q)
        if s.startswith("ปริซึมชนิดหนึ่ง"):
            edges = _nums(s)[0]
            assert int(_answer(q)) == edges // 3 + 2
            continue
        n = _SIDES[re.match(r"ปริซึม(\S+เหลี่ยม)มี", s).group(1)]
        want = n + 2 if "หน้า" in s else 3 * n if "สัน" in s else 2 * n
        assert int(_answer(q)) == want, s


def test_nets_match_their_solids():
    solid_of = dict(_NETS)
    parts_of = {s: p for p, s in _NETS}
    for seed in SEEDS:
        q = generate("math.net_to_solid_p6", Random(seed))
        s = _stem(q)
        m = re.match(r"รูปคลี่ที่ประกอบด้วย(.+) เมื่อพับ", s)
        if m:
            assert _answer(q) == solid_of[m.group(1)]
        else:
            solid = re.match(r"รูปคลี่ของ(.+)ประกอบด้วย", s).group(1)
            assert _answer(q) == parts_of[solid]


@pytest.mark.parametrize("key", ["math.construct_rectangle_p4", "math.construct_quadrilateral_p5",
                                 "math.construct_triangle_p6"])
def test_the_next_construction_step_is_the_real_next_step(key):
    spec = REGISTRY[key]
    for seed in SEEDS:
        q = generate(key, Random(seed))
        # Regenerate the procedure the item was drawn from with the same seed.
        goal, steps, faulty = spec.procedures(Random(seed))
        shown = re.search(r"“(.+)”", _stem(q)).group(1)
        k = steps.index(shown)
        assert _answer(q) == steps[k + 1]
        assert not set(faulty) & set(steps)


def test_angle_constructions():
    method_of = {a: m for a, m in _ANGLE_METHODS}
    angle_of = {m: a for a, m in _ANGLE_METHODS}
    # Each method really makes its angle.
    assert method_of[30] and angle_of[method_of[135]] == 90 + 45
    for seed in SEEDS:
        q = generate("math.construct_angle_m2", Random(seed))
        s = _stem(q)
        m = re.match(r"“(.+)” จะได้มุม", s)
        if m:
            assert _answer(q) == f"{angle_of[m.group(1)]} องศา"
        else:
            assert _answer(q) == method_of[_nums(s)[0]]


def test_ordering_and_operations_with_mixed_numbers():
    for seed in SEEDS:
        q = generate("math.order_mixed_numbers_p6", Random(seed))
        shown = [_frac(t) for t in q.stem[-1].tex.split(r",\ ")]
        want = sorted(shown, reverse="มากไปน้อย" in _stem(q))
        assert [_frac(t) for t in _answer(q).split(r",\ ")] == want
        assert shown != want
        q = generate("math.mixed_number_ops_p6", Random(seed))
        tex = q.stem[-1].tex
        a, op1, b, op2, c = re.fullmatch(
            r"(\S+) ([+-]) (\S+) (\\times|\\div) (\S+)", tex).groups()
        a, b, c = _frac(a), _frac(b), _frac(c)
        bc = b * c if op2 == r"\times" else b / c
        assert _frac(_answer(q)) == (a + bc if op1 == "+" else a - bc), tex


def test_fraction_word_problems():
    for seed in SEEDS:
        q = generate("math.fraction_multistep_word_p6", Random(seed))
        texts = [b.text for b in q.stem if b.kind == "text"]
        fr = [_frac(b.tex) for b in q.stem if b.kind == "math"]
        s = " ".join(texts)
        if "ตัดไปทำกระเป๋า" in s:
            n = _nums(texts[1])[0]
            want = fr[0] - n * fr[1]
        elif "น้ำตาล" in s:
            sold = _nums(texts[-1])[0]
            want = fr[0] / fr[1] - sold
        else:
            share = _nums(texts[-1])[0]
            want = (fr[0] + fr[1]) / share
        assert _frac(_answer(q)) == want, s


def _table(s: str) -> dict[str, int]:
    return {r.strip(): int(v) for r, v in re.findall(r"^(.+?) \| (\d+) ", s, re.M)}


def test_making_pictographs_and_bar_charts():
    for seed in SEEDS:
        q = generate("math.pictograph_make_p3", Random(seed))
        s, table = _stem(q), _table(_stem(q))
        key = int(re.search(r"1 รูป แทน (\d+)", s).group(1))
        m = re.search(r"แถวของ(.+) ต้องมี", s)
        if m:
            assert int(_answer(q)) == table[m.group(1)] // key
        else:
            for part in _answer(q).split("   "):
                row, dots = part.split(": ")
                assert dots.count("●") * key == table[row]
        q = generate("math.bar_chart_make_p5", Random(seed))
        s, table = _stem(q), _table(_stem(q))
        m = re.search(r"1 ช่องแทน (\d+) \S+ แท่งของ(.+) ต้องยาว", s)
        if m:
            assert int(_answer(q)) == table[m.group(2)] // int(m.group(1))
        else:
            top = max(table.values())
            valid = [c for c in q.choices if 10 <= -(-top // _nums(_choice(c))[0]) <= 20]
            assert len(valid) == 1 and _choice(valid[0]) == _answer(q)


def test_line_graph_problems():
    for seed in SEEDS:
        q = generate("math.line_graph_problem_p5", Random(seed))
        s = _stem(q)
        pairs = re.findall(r"^(.+): (\d+)$", s, re.M)
        xs, ys = [p[0] for p in pairs], [int(p[1]) for p in pairs]
        if "เพิ่มขึ้นมากที่สุด" in s:
            k = max(range(len(ys) - 1), key=lambda i: ys[i + 1] - ys[i])
            assert _answer(q) == f"จาก{xs[k]}ถึง{xs[k + 1]}"
        elif "รวมทั้ง" in s:
            assert "ต้นถั่ว" not in s
            assert int(_answer(q)) == sum(ys)
        else:
            assert int(_answer(q)) == max(ys) - min(ys)
