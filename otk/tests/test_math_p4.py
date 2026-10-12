"""ป.4 enrichment: answers re-derived from what the learner is shown."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from decimal import Decimal
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.kit import story as _story

SEEDS = range(300)
NEW = keys_from("math_p4")
ENRICHED = ["math.bar_chart_diff", "math.rectangle_area_perimeter"]


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _numbers(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace(",", ""))]


def _eval(tex: str) -> float:
    return eval(tex.replace(r"\times", "*").replace(r"\div", "/"))


def _int(tex: str) -> int:
    return int(tex.replace("{,}", ""))


def _frac(tex: str) -> Fraction:
    """3, \\frac{3}{4} or 2\\frac{3}{4} as a Fraction."""
    m = re.fullmatch(r"(\d*)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if not m:
        return Fraction(int(tex))
    whole, n, d = m.groups()
    return int(whole or 0) + Fraction(int(n), int(d))


def test_the_module_registers_twenty_four_sets():
    assert len(NEW) == 24
    assert all(REGISTRY[k].level_for() == "ป.4" for k in NEW)


@pytest.mark.parametrize("key", NEW + ENRICHED)
def test_four_distinct_choices(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        assert len(q.choices) == REGISTRY[key].max_choices, (key, seed, _stem(q))
        assert len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices


def test_large_number_reading():
    for seed in SEEDS:
        q = generate("math.number_reading_p4", Random(seed))
        if "อ่านว่า" in _stem(q):
            assert _answer(q) == _story.thai_words(int(q.stem[1].tex))


def test_place_value_of_millions():
    places = ("หน่วย", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน")
    for seed in SEEDS:
        q = generate("math.place_value_millions_p4", Random(seed))
        n, digit = _numbers(_stem(q))
        pos = len(str(n)) - 1 - str(n).index(str(digit))
        if "หลักใด" in _stem(q):
            assert _answer(q) == f"หลัก{places[pos]}"
        else:
            assert _int(_answer(q)) == digit * 10 ** pos


def test_compare_large_numbers():
    for seed in SEEDS:
        q = generate("math.compare_large_numbers_p4", Random(seed))
        values = [_int(_choice(c)) for c in q.choices]
        want = max(values) if "มากที่สุด" in _stem(q) else min(values)
        assert _int(_answer(q)) == want


def test_estimate_rounds_each_price_first():
    for seed in SEEDS:
        q = generate("math.estimate_word_problem_p4", Random(seed))
        a, b = _numbers(_stem(q))[:2]
        r = lambda n: (n + 500) // 1000 * 1000
        assert int(_answer(q)) == r(a) + r(b)


def test_fraction_kinds():
    for seed in SEEDS:
        q = generate("math.fraction_kinds_p4", Random(seed))
        kinds = []
        for c in q.choices:
            t = _choice(c)
            m = re.fullmatch(r"(\d*)\\frac\{(\d+)\}\{(\d+)\}", t)
            whole, n, d = m.groups()
            kinds.append("คละ" if whole else "แท้" if int(n) < int(d) else "เกิน")
        want = {"ข้อใดเป็นเศษส่วนแท้": "แท้", "ข้อใดเป็นเศษส่วนเกิน": "เกิน",
                "ข้อใดเป็นจำนวนคละ": "คละ"}[q.stem[0].text]
        assert kinds[q.answer] == want and kinds.count(want) == 1, [_choice(c) for c in q.choices]


def test_improper_mixed_keeps_the_value():
    for seed in SEEDS:
        q = generate("math.improper_mixed_p4", Random(seed))
        shown = _frac(q.stem[1].tex)
        values = [_frac(_choice(c)) for c in q.choices]
        assert values[q.answer] == shown and values.count(shown) == 1


@pytest.mark.parametrize("key", ["math.fraction_addsub_multiple_p4"])
def test_fraction_arithmetic(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        left, op, right = re.fullmatch(r"(.+?) ([+-]) (.+)", q.stem[1].tex).groups()
        want = _frac(left) + _frac(right) if op == "+" else _frac(left) - _frac(right)
        values = [_frac(_choice(c)) for c in q.choices]
        assert values[q.answer] == want and values.count(want) == 1


def test_fraction_story():
    for seed in SEEDS:
        q = generate("math.fraction_word_problem_p4", Random(seed))
        a, b = [_frac(blk.tex) for blk in q.stem if getattr(blk, "tex", None)]
        want = a - b if "เหลือ" in _stem(q) or "ยังไม่ได้" in _stem(q) else a + b
        values = [_frac(_choice(c)) for c in q.choices]
        assert values[q.answer] == want and values.count(want) == 1


def test_decimal_reading():
    from otk.sets.math.p4.decimals import dec_words
    for seed in SEEDS:
        q = generate("math.decimal_reading_p4", Random(seed))
        if "อ่านว่า" in _stem(q):
            assert _answer(q) == dec_words(q.stem[1].tex)
        elif "รูปกระจาย" in _stem(q):
            values = [Decimal(str(round(_eval(_choice(c)), 6))) for c in q.choices]
            assert values[q.answer] == Decimal(q.stem[1].tex)
            assert values.count(Decimal(q.stem[1].tex)) == 1
        else:
            words = re.search(r"“(.+)”", _stem(q)).group(1)
            assert dec_words(_answer(q)) == words


def test_decimal_compare_and_arithmetic():
    for seed in SEEDS:
        q = generate("math.decimal_compare_p4", Random(seed))
        values = [Decimal(_choice(c)) for c in q.choices]
        want = max(values) if "มากที่สุด" in _stem(q) else min(values)
        assert Decimal(_answer(q)) == want
        q = generate("math.decimal_addsub_p4", Random(seed))
        a, op, b = q.stem[-1].tex.split()
        want = Decimal(a) + Decimal(b) if op == "+" else Decimal(a) - Decimal(b)
        assert Decimal(_answer(q)) == want


def test_decimal_story():
    for seed in SEEDS:
        q = generate("math.decimal_word_problem_p4", Random(seed))
        nums = [Decimal(x) for x in re.findall(r"\d+(?:\.\d+)?", _stem(q))]
        s = _stem(q)
        want = (nums[0] - nums[1]) if ("เหลือ" in s) else nums[0] + nums[1]
        assert Decimal(_answer(q)) == want, s


def test_mixed_story_sentence_and_value():
    for seed in SEEDS:
        q = generate("math.two_step_sentence_p4", Random(seed))
        values = [_eval(_choice(c).split("=")[0]) for c in q.choices]
        assert values.count(values[q.answer]) == 1
        w = generate("math.two_step_word_problem_p4", Random(seed))
        assert int(_answer(w)) == values[q.answer]


def test_mixed_ops_multiply_first():
    for seed in SEEDS:
        q = generate("math.mixed_ops_p4", Random(seed))
        assert _eval(q.stem[-1].tex) == int(_answer(q))


def test_time_units():
    rates = {("นาที", "วินาที"): 60, ("ชั่วโมง", "นาที"): 60, ("วัน", "ชั่วโมง"): 24,
             ("สัปดาห์", "วัน"): 7, ("ปี", "เดือน"): 12}
    for seed in SEEDS:
        q = generate("math.time_units_p4", Random(seed))
        s = _stem(q)
        (big, small), k = next((u, k) for u, k in rates.items() if f" {u[0]} " in f" {s} "
                               and f" {u[1]}" in s)
        n = _numbers(s)
        if "กับอีก" in s:
            assert n[0] == n[1] * k + int(_answer(q))
        else:
            assert int(_answer(q)) == n[0] * k + n[1]


def test_calendar_and_travel():
    from otk.sets.math.p4.time import _MONTHS
    days = dict(_MONTHS)
    for seed in SEEDS:
        q = generate("math.calendar_word_problem_p4", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _numbers(s)
        if "พ.ศ." in s:
            assert ans == n[1] - n[0]
        elif "สัปดาห์" in s:
            assert ans == 7 * n[0] + n[1]
        else:
            month = re.search(r"วันที่ \d+ (\S+) อีก", s).group(1)
            assert ans == days[month] - n[0] + n[1]
        q = generate("math.travel_time_p4", Random(seed))
        (h1, m1), (h2, m2) = [(int(a), int(b)) for a, b in re.findall(r"(\d+)\.(\d+) น\.", _stem(q))]
        span = (24 * 60 - (60 * h1 + m1)) + 60 * h2 + m2
        h, m = divmod(span, 60)
        assert _answer(q) == f"{h} ชั่วโมง" + (f" {m} นาที" if m else "")


def test_angles():
    for seed in SEEDS:
        q = generate("math.clock_angle_p4", Random(seed))
        h = _numbers(_stem(q))[0] % 12        # 15.00 น. reads as 3 o'clock
        assert int(_answer(q)) == 30 * min(h, 12 - h)
        q = generate("math.angles_around_point_p4", Random(seed))
        a, b = _numbers(_stem(q))[-2:]
        whole = 180 if "เส้นตรง" in _stem(q) else 360
        assert int(_answer(q)) == whole - a - b


def test_rectangles():
    for seed in SEEDS:
        q = generate("math.rectangle_missing_side_p4", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _numbers(s)
        if "จัตุรัส" in s:
            assert 4 * ans == n[0]
        elif "พื้นที่" in s:
            assert ans * n[1] == n[0]
        else:
            assert 2 * (ans + n[1]) == n[0]
        q = generate("math.rectangle_word_problem_p4", Random(seed))
        s, ans = _stem(q), int(_answer(q))
        n = _numbers(s)
        if "รั้ว" in s:
            assert ans == 2 * (n[0] + n[1]) * n[2]
        elif "แผ่นยาง" in s:
            assert ans == (n[0] // n[2]) * (n[1] // n[2])
        elif "ตัดรูปสี่เหลี่ยมจัตุรัส" in s:
            assert ans == n[0] * n[1] - n[2] * n[2]
        elif "ริบบิ้น" in s:
            assert ans == n[0] - 2 * (n[1] + n[2])
        elif "ยาวรอบรูป" in s:
            assert ans == (n[0] // 4) ** 2 and n[0] % 4 == 0
        else:
            assert ans == n[0] * n[0] * n[1]


def _bars(q):
    lines = q.stem[0].text.split("\n")
    scale = _numbers(lines[-1] if "■ แทน" in lines[-1] else lines[-2])[-1]
    return {ln.split(":")[0]: ln.count("■") * scale for ln in lines if ":" in ln}


def test_bar_charts():
    for seed in SEEDS:
        q = generate("math.bar_chart_read_p4", Random(seed))
        rows = _bars(q)
        ask = q.stem[0].text.split("\n")[-1]
        asked = [r for r in rows if r in ask]
        assert rows[asked[0]] == int(_answer(q))
        q = generate("math.bar_chart_diff", Random(seed))
        rows = _bars(q)
        assert int(_answer(q)) == max(rows.values()) - min(rows.values())
