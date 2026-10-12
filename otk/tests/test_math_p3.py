"""ป.3 enrichment: answers re-derived from what the learner is shown."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.kit import story as _story

SEEDS = range(300)
NEW = keys_from("math_p3")
ENRICHED = ["math.make_change", "math.table_sum"]


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _numbers(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s)]


def _eval(tex: str) -> float:
    return eval(tex.replace(r"\times", "*").replace(r"\div", "/"))


def _frac(tex: str) -> Fraction:
    n, d = re.fullmatch(r"\\frac\{(\d+)\}\{(\d+)\}", tex).groups()
    return Fraction(int(n), int(d))


def _clock(s: str) -> int:
    """'9.05 น.' -> minutes after midnight."""
    h, m = re.search(r"(\d+)\.(\d+) น\.", s).groups()
    return 60 * int(h) + int(m)


def test_the_module_registers_twenty_five_sets():
    # 24, and the three-digit multiplication step added by the content audit.
    assert len(NEW) == 25
    assert all(REGISTRY[k].level_for() == "ป.3" for k in NEW)


@pytest.mark.parametrize("key", NEW + ENRICHED)
def test_four_distinct_choices(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        assert len(q.choices) == REGISTRY[key].max_choices, (key, seed, _stem(q))
        assert len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices


def test_number_reading_to_one_hundred_thousand():
    for seed in SEEDS:
        q = generate("math.number_reading_p3", Random(seed))
        stem, ans = _stem(q), _answer(q)
        if "อ่านว่า" in stem:
            assert ans == _story.thai_words(int(q.stem[1].tex))
        elif "“" in stem:
            assert _story.thai_words(int(ans)) == re.search(r"“(.+)”", stem).group(1)


def test_order_numbers_picks_the_extreme():
    for seed in SEEDS:
        q = generate("math.order_numbers_p3", Random(seed))
        values = [int(_choice(c)) for c in q.choices]
        want = max(values) if "มากที่สุด" in q.stem[0].text else min(values)
        assert int(_answer(q)) == want


@pytest.mark.parametrize("key", ["math.multiply_4x1_p3", "math.mixed_ops_p3"])
def test_expression_evaluates_to_its_answer(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        assert _eval(q.stem[-1].tex) == int(_answer(q))


def test_multiplication_story_is_the_product_of_its_numbers():
    for seed in SEEDS:
        q = generate("math.multiplication_word_problem_p3", Random(seed))
        a, b = _numbers(_stem(q))
        assert int(_answer(q)) == a * b


def test_division_story_rounds_the_right_way():
    for seed in SEEDS:
        q = generate("math.division_word_problem_p3", Random(seed))
        stem, ans = _stem(q), int(_answer(q))
        total, per = _numbers(stem)
        if "อย่างน้อย" in stem:
            assert ans == -(-total // per)
        elif "เหลือ" in stem:
            assert ans == total % per
        else:
            assert ans == total // per


def test_two_step_sentence_matches_the_story_value():
    for seed in SEEDS:
        q = generate("math.two_step_sentence_p3", Random(seed))
        values = [_eval(_choice(c).split("=")[0]) for c in q.choices]
        assert values.count(values[q.answer]) == 1
        assert values[q.answer] >= 0 and values[q.answer] == int(values[q.answer])


def test_two_step_word_problem_is_never_negative():
    for seed in SEEDS:
        q = generate("math.two_step_word_problem_p3", Random(seed))
        assert int(_answer(q)) >= 0, _stem(q)


@pytest.mark.parametrize("key, steps", [("math.number_pattern_p3", (3, 4, 6, 7, 8, 9, 25, 50))])
def test_number_pattern_is_arithmetic(key, steps):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        terms = [int(_answer(q)) if t.strip() == r"\square" else int(t)
                 for t in q.stem[-1].tex.split(r",\ ")]
        diffs = {b - a for a, b in zip(terms, terms[1:])}
        assert len(diffs) == 1 and abs(diffs.pop()) in steps


def test_pattern_rule_names_the_step():
    for seed in SEEDS:
        q = generate("math.pattern_rule_p3", Random(seed))
        terms = [int(t) for t in q.stem[-1].tex.split(r",\ ")]
        word, size = _answer(q).split("ทีละ")
        assert int(size) == abs(terms[1] - terms[0])
        assert ("เพิ่มขึ้น" in word) == (terms[1] > terms[0])


def test_growing_pattern_continues_the_step():
    for seed in SEEDS:
        q = generate("math.growing_pattern_p3", Random(seed))
        _, t1, _, t2, _, t3, k = _numbers(_stem(q))
        assert t2 - t1 == t3 - t2
        assert int(_answer(q)) == t1 + (t2 - t1) * (k - 1)


def test_baht_and_satang():
    for seed in SEEDS:
        q = generate("math.baht_satang_p3", Random(seed))
        stem, ans = _stem(q), _answer(q)
        n = _numbers(stem)
        if "เท่ากับกี่สตางค์" in stem:
            assert int(ans) == 100 * n[0] + n[1]
        elif "แบบมีจุด" in stem:
            assert ans == f"{n[0]}.{n[1]:02d} บาท"
        elif "ห้าสิบ" in stem:
            assert int(ans) * 2 == n[0]
        else:
            assert int(ans) * 4 == n[0]


def test_income_expense_record_adds_up():
    for seed in SEEDS:
        q = generate("math.income_expense_record_p3", Random(seed))
        lines = q.stem[0].text.split("\n")
        income = sum(_numbers(ln)[-1] for ln in lines if "รายรับ " in ln)
        expense = sum(_numbers(ln)[-1] for ln in lines if "รายจ่าย " in ln)
        ask, ans = lines[-1], int(_answer(q))
        want = (income - expense if "คงเหลือ" in ask else expense if "รายจ่าย" in ask
                else income)
        assert ans == want, q.stem[0].text
        assert income - expense >= 0


def test_24_hour_clock_is_consistent_with_spoken_time():
    from otk.sets.math.p3.time import spoken as say
    for seed in SEEDS:
        q = generate("math.clock_24h_p3", Random(seed))
        stem, ans = _stem(q), _answer(q)
        if "ตรงกับเวลาใด" in stem:
            words = re.search(r"“(.+)”", stem).group(1)
            minutes = _clock(ans)
            assert say(minutes // 60, minutes % 60 == 30) == words
        else:
            minutes = _clock(stem)
            assert ans == say(minutes // 60, minutes % 60 == 30)


def test_spoken_hours_are_all_different():
    from otk.sets.math.p3.time import spoken as say
    # Half hours are asked for every hour but 0, 12 (no half) and 6, 18,
    # which speech does not tell apart.
    said = [say(h, half) for h in range(24) for half in (False, True)
            if not (half and h in (0, 6, 12, 18))]
    assert len(said) == len(set(said))


def test_duration():
    from otk.sets.math.p3.time import spoken as say
    for seed in SEEDS:
        q = generate("math.duration_p3", Random(seed))
        stem, ans = _stem(q), int(_answer(q))
        if "ชั่วโมง" in stem:
            hours = [h for h in range(24) for w in [say(h)] if f"เวลา {w} " in stem + " "]
            assert len(hours) == 2 and ans == hours[1] - hours[0], stem
        else:
            start, end = (60 * int(h) + int(m) for h, m in re.findall(r"(\d+)\.(\d+) น\.", stem))
            assert ans == end - start


def test_time_word_problem():
    for seed in SEEDS:
        q = generate("math.time_word_problem_p3", Random(seed))
        stem = _stem(q)
        given = _clock(stem)
        span = int(re.search(r"(\d+) นาที", stem).group(1))
        want = given + span if "เสร็จ" in stem else given - span
        assert _clock(_answer(q)) == want


def test_length_weight_capacity_stories():
    for seed in SEEDS:
        q = generate("math.length_word_problem_p3", Random(seed))
        s, n, ans = _stem(q), _numbers(_stem(q)), int(_answer(q))
        if "มิลลิเมตร" in s:
            assert ans == 10 * n[0] + n[1]
        elif "ตัดเป็นเส้น" in s:
            assert ans == 100 * n[0] // n[1]
        elif "เดินไป" in s:
            assert ans == n[0] + 1000 * n[1] + n[2]
        else:
            assert ans == 1000 * n[0] + n[1]
        q = generate("math.weight_word_problem_p3", Random(seed))
        s, n, ans = _stem(q), _numbers(_stem(q)), int(_answer(q))
        if "รวมหนัก" in s:
            assert ans == 1000 * (n[0] + n[2]) + n[1] + n[3]
        elif "เหลือ" in s:
            assert ans == 1000 * n[0] - n[1]
        elif "กล่องละ" in s:
            assert ans == n[0] * n[1]
        else:
            assert ans == 1000 * n[0] + n[1] - n[2]
        q = generate("math.capacity_word_problem_p3", Random(seed))
        s, n, ans = _stem(q), _numbers(_stem(q)), int(_answer(q))
        if "เท่ากับกี่มิลลิลิตร" in s:
            assert ans == 1000 * n[0] + n[1]
        elif "ใบละ" in s:
            assert ans == n[0] * n[1]
        elif "เหลือน้ำ" in s:
            assert ans == 1000 * n[0] - (1000 * n[1] + n[2] if len(n) == 3 else n[1])
        else:
            total = 1000 * n[0] + (n[1] if len(n) == 3 else 0)
            assert ans == total // n[-1] and total % n[-1] == 0


def test_kitchen_measures_use_the_given_rate():
    for seed in SEEDS:
        q = generate("math.kitchen_measures_p3", Random(seed))
        one, rate, n = _numbers(_stem(q))
        assert one == 1 and int(_answer(q)) == rate * n


def test_compare_fractions_picks_the_extreme_value():
    for seed in SEEDS:
        q = generate("math.compare_fractions_p3", Random(seed))
        values = [_frac(_choice(c)) for c in q.choices]
        want = max(values) if "มากที่สุด" in q.stem[0].text else min(values)
        assert values[q.answer] == want and values.count(want) == 1


def test_fraction_story_answer_and_no_equal_wrong_value():
    for seed in SEEDS:
        q = generate("math.fraction_word_problem_p3", Random(seed))
        given = [_frac(b.tex) for b in q.stem if getattr(b, "tex", None)]
        s = _stem(q)
        a, b = given
        want = (a + b if "ทั้งหมด" in s else a - b if "เหลือเชือก" in s else 1 - a - b)
        values = [_frac(_choice(c)) for c in q.choices]
        assert values[q.answer] == want, s
        assert values.count(want) == 1


def test_tables():
    for seed in SEEDS:
        q = generate("math.table_read_p3", Random(seed))
        lines = q.stem[0].text.split("\n")
        rows = {ln.split(" | ")[0]: int(ln.split(" | ")[1]) for ln in lines[2:-1]}
        ask, ans = lines[-1], int(_answer(q))
        named = sorted((r for r in rows if r in ask), key=ask.index)
        if "มากกว่า" in ask:
            assert ans == rows[named[0]] - rows[named[1]], ask
        elif "รวมกัน" in ask:
            assert ans == rows[named[0]] + rows[named[1]], ask
        else:
            assert ans == rows[named[0]], ask
        q = generate("math.table_most_p3", Random(seed))
        lines = q.stem[0].text.split("\n")
        rows = {ln.split(" | ")[0]: int(ln.split(" | ")[1]) for ln in lines[2:]}
        pick = (max if "มากที่สุด" in q.stem[1].text else min)(rows, key=rows.get)
        assert _answer(q) == pick
        q = generate("math.table_sum", Random(seed))
        lines = q.stem[0].text.split("\n")
        assert int(_answer(q)) == sum(int(ln.split(" | ")[1]) for ln in lines[2:-1])


def test_make_change():
    for seed in SEEDS:
        q = generate("math.make_change", Random(seed))
        n = _numbers(_stem(q))
        ans = int(_answer(q))
        if len(n) == 3:
            assert ans == n[2] - n[0] - n[1]
        else:
            assert ans == max(n) - min(n)
