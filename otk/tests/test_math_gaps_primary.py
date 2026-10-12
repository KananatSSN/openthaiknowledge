"""The primary gap sets: every answer is re-derived from the numbers in the
question, independently of the generator, and every choice is distinct."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from decimal import Decimal
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.p3.measurement import _ESTIMATES, _TOOLS

SEEDS = range(250)
KEYS = sorted(keys_from("math_gaps_primary"))


def _stem(q) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in q.stem)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", "") or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _int(s: str) -> int:
    return int(s.replace("{,}", "").replace(",", ""))


def _nums(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace("{,}", "").replace(",", ""))]


def test_fifteen_sets_are_registered():
    assert len(KEYS) == 15


@pytest.mark.parametrize("key", KEYS)
def test_choices_are_distinct_and_the_answer_is_one_of_them(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        texts = [_choice(c) for c in q.choices]
        assert len(texts) == len(set(texts)) == REGISTRY[key].max_choices, (seed, texts)


def test_capacity_litres():
    for seed in SEEDS:
        q = generate("math.capacity_litre_p2", Random(seed))
        s, n = _stem(q), _nums(_stem(q))
        if "มากกว่า" in s:
            want = n[0] - n[1]
        elif "เทน้ำจาก" in s:
            want = n[0] * n[1]
        elif "ตักกี่ครั้ง" in s:
            want = n[0] // n[1]
            assert n[0] % n[1] == 0
        else:
            want = n[0] - n[1] + n[2]
        assert _int(_answer(q)) == want, s


def test_estimates_and_tools_name_the_right_unit_and_tool():
    unit_of = {thing: f"ประมาณ {amount} {unit}" for thing, amount, unit, _ in _ESTIMATES}
    tool_of = {what: tool for what, tool, _ in _TOOLS}
    for seed in SEEDS:
        q = generate("math.estimate_measure_p3", Random(seed))
        thing = re.search(r"เมื่อคาดคะเน (.+)น่าจะเป็นเท่าใด", _stem(q)).group(1)
        assert _answer(q) == unit_of[thing]
        q = generate("math.measuring_tool_p3", Random(seed))
        what = re.search(r"ต้องการวัด(.+) ควรใช้", _stem(q)).group(1)
        assert _answer(q) == tool_of[what]


def test_tonnes():
    for seed in SEEDS:
        q = generate("math.metric_ton_p3", Random(seed))
        s, n = _stem(q), _nums(_stem(q))
        if s.endswith("เมตริกตัน เท่ากับกี่กิโลกรัม"):
            want = n[0] * 1000
        elif "เท่ากับกี่กิโลกรัม" in s:
            want = n[0] * 1000 + n[1]
        elif "รถบรรทุก" in s:
            want = n[0] * 1000 - n[1]
        else:
            total = n[0] * n[1]
            want = abs(total - 1000)
            assert ("มากกว่า" in s) == (total > 1000)
        assert _int(_answer(q)) == want, s


@pytest.mark.parametrize("grade", ["p3", "p4"])
def test_large_addition_and_subtraction(grade):
    for seed in SEEDS:
        q = generate(f"math.add_sub_large_{grade}", Random(seed))
        a, b = _nums(q.stem[-1].tex)
        want = a + b if "+" in q.stem[-1].tex else a - b
        assert _int(_answer(q)) == want
        q = generate(f"math.missing_addsub_large_{grade}", Random(seed))
        tex = q.stem[-1].tex.replace("{,}", "")
        box = _int(_answer(q))
        lhs, rhs = tex.split("=")
        assert eval(lhs.replace(r"\square", str(box))) == int(rhs), tex
        q = generate(f"math.addsub_word_large_{grade}", Random(seed))
        s, n = _stem(q), _nums(_stem(q))
        if "ทั้งหมดกี่คน" in s:
            want = n[0] + n[1]
        elif "ส่งไปขาย" in s or "แพงกว่า" in s:
            want = n[0] - n[1]
        else:
            want = n[0] + n[1] - n[2]
        assert _int(_answer(q)) == want, s
        if grade == "p3":
            assert max(_nums(s) or [0]) <= 100_000
        else:
            assert max(_nums(s)) > 100_000


def _frac(tex: str) -> Fraction:
    m = re.fullmatch(r"(\d*)\\frac\{(\d+)\}\{(\d+)\}", tex.strip())
    if m:
        return int(m.group(1) or 0) + Fraction(int(m.group(2)), int(m.group(3)))
    return Fraction(int(tex))


def test_fraction_comparison_picks_the_extreme_of_the_four_shown():
    for seed in SEEDS:
        q = generate("math.compare_fractions_multiple_p4", Random(seed))
        shown = [_frac(t) for t in q.stem[-1].tex.split(r",\ ")]
        dens = sorted({f.denominator for f in shown if f.denominator > 1})
        assert all(d2 % d1 == 0 for d1 in dens for d2 in dens if d2 >= d1), shown
        want = max(shown) if "มากที่สุด" in _stem(q) else min(shown)
        assert _frac(_answer(q)) == want
        assert {_frac(_choice(c)) for c in q.choices} == set(shown)


_STORY_FOR = {
    r"\d+ \\times \d+ \+ \d+": "และมีสมุดอยู่แล้ว",
    r"\d+ \\times \d+ - \d+": "แจกเพื่อนไป",
    r"\d+ \\times \(\d+ \+ \d+\)": "นักเรียนหญิง",
    r"\(\d+ \+ \d+\) \\times \d+": "แลกลูกอม",
}


def test_the_story_matches_the_number_sentence():
    for seed in SEEDS:
        q = generate("math.story_for_sentence_p4", Random(seed))
        tex = q.stem[-1].tex
        cue = next(c for pat, c in _STORY_FOR.items() if re.fullmatch(pat + r" = \\square", tex))
        assert cue in _answer(q)
        # The same three numbers appear in the story, in the same order.
        assert _nums(_answer(q)) == _nums(tex)


def test_units_written_as_decimals():
    per = {"เมตร": 100, "กิโลเมตร": 1000, "เซนติเมตร": 10, "กิโลกรัม": 1000, "เมตริกตัน": 1000}
    for key in ("math.length_decimal_p5", "math.weight_decimal_p5"):
        for seed in SEEDS:
            q = generate(key, Random(seed))
            whole, big, part, _small = re.match(r"(\d+) (\S+) (\d+) (\S+) เท่ากับ", _stem(q)).groups()
            want = Decimal(whole) + Decimal(part) / per[big]
            assert Decimal(_answer(q)) == want, _stem(q)


def test_decimal_word_problems():
    for seed in SEEDS:
        q = generate("math.measure_decimal_word_p5", Random(seed))
        s, n = _stem(q), _nums(_stem(q))
        if "ผ้าผืนแรก" in s:
            want = Decimal(n[0] + n[1]) / 100
        elif "เนย" in s:
            want = Decimal(n[0] * n[1]) / 1000
        elif "เดินมาแล้ว" in s:
            want = Decimal(n[0] * 1000 + n[1] - n[2]) / 1000
        else:
            want = Decimal(n[2] * (n[0] * 1000 + n[1])) / 1000
        assert Decimal(_answer(q)) == want, s
