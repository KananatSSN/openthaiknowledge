"""ป.2 enrichment: answers re-derived from what the learner is shown."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.kit import story as _story

SEEDS = range(300)
NEW = keys_from("math_p2")
ENRICHED = ["math.two_step_word_problem", "math.pictograph", "math.convert_length_p2",
            "math.convert_weight_p2"]


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


def test_the_module_registers_twenty_four_sets():
    assert len(NEW) == 24
    assert all(REGISTRY[k].level_for() == "ป.2" for k in NEW)


@pytest.mark.parametrize("key", NEW + ENRICHED)
def test_four_distinct_choices(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        assert len(q.choices) == REGISTRY[key].max_choices, (key, seed, _stem(q))
        assert len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices


def test_compare_sign_reads_both_sides():
    for seed in SEEDS:
        q = generate("math.compare_sign", Random(seed))
        left, right = q.stem[0].text.split(":", 1)[1].split("___")
        a, b = _eval(left), _eval(right)
        assert _answer(q) == ("<" if a < b else ">" if a > b else "=")


def test_number_reading_round_trips():
    back = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")
    for seed in SEEDS:
        q = generate("math.number_reading_p2", Random(seed))
        stem, ans = _stem(q), _answer(q)
        if "อ่านว่า" in stem:
            assert ans == _story.thai_words(int(q.stem[1].tex))
        elif "“" in stem:
            words = re.search(r"“(.+)”", stem).group(1)
            assert _story.thai_words(int(ans)) == words
        elif "ตัวเลขไทย" in stem:
            assert ans.translate(back) == q.stem[1].tex
        else:
            assert ans == stem.split()[0].translate(back)


def test_expanded_form_adds_up():
    for seed in SEEDS:
        q = generate("math.expanded_form_p2", Random(seed))
        shown = q.stem[1].tex
        if "+" in shown:
            assert _eval(shown) == int(_answer(q))
            assert all(_choice(c) == _answer(q) or int(_choice(c)) != _eval(shown)
                       for c in q.choices)
        else:
            values = [_eval(_choice(c)) for c in q.choices]
            assert values[q.answer] == int(shown)
            assert values.count(int(shown)) == 1


def test_order_numbers_is_sorted():
    for seed in SEEDS:
        q = generate("math.order_numbers_p2", Random(seed))
        nums = [int(x) for x in _answer(q).split(r",\ ")]
        asc = "น้อยไปมาก" in q.stem[0].text
        assert nums == sorted(nums, reverse=not asc)
        assert sorted(nums) == sorted(int(x) for x in q.stem[1].tex.split(r",\ "))


@pytest.mark.parametrize("key", ["math.missing_addsub_p2", "math.multiplication_properties_p2",
                                 "math.multiply_divide_relation_p2"])
def test_box_value_makes_the_sentence_true_and_no_other_choice_does(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        tex = q.stem[-1].tex.split(r"\Rightarrow")[-1].replace(r"\quad", "")
        if "=" not in tex:           # a bare product: n × 0, n × 1
            assert _eval(tex) == int(_answer(q))
            continue
        for i, c in enumerate(q.choices):
            left, right = tex.replace(r"\square", _choice(c)).split("=")
            assert (_eval(left) == _eval(right)) == (i == q.answer), (tex, _choice(c))


@pytest.mark.parametrize("key", ["math.multiply_1x2_p2", "math.division_facts_p2",
                                 "math.mixed_ops_p2"])
def test_expression_evaluates_to_its_answer(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        assert _eval(q.stem[-1].tex) == int(_answer(q))


def test_remainder_division():
    for seed in SEEDS:
        q = generate("math.division_remainder_p2", Random(seed))
        a, b = map(int, q.stem[-1].tex.split(r" \div "))
        want = a // b if "ผลหาร" in q.stem[0].text else a % b
        assert int(_answer(q)) == want and a % b


def test_multiplication_story_is_a_product():
    for seed in SEEDS:
        q = generate("math.multiplication_word_problem_p2", Random(seed))
        nums = _numbers(_stem(q))
        ans = int(_answer(q))
        if len(nums) == 2:
            assert ans == nums[0] * nums[1], _stem(q)
        else:                         # legs or wheels: one number, a known count each
            assert ans // nums[0] in (2, 3, 4, 6, 8) and ans % nums[0] == 0, _stem(q)


def test_division_story_is_a_quotient():
    for seed in SEEDS:
        q = generate("math.division_word_problem_p2", Random(seed))
        nums = _numbers(_stem(q))
        ans = int(_answer(q))
        if len(nums) == 2:
            assert ans == max(nums) // min(nums) and max(nums) % min(nums) == 0, _stem(q)
        else:
            assert nums[0] % ans == 0 and nums[0] // ans in (2, 4, 6, 8), _stem(q)


def test_mixed_sentence_has_exactly_one_choice_with_the_right_value():
    for seed in SEEDS:
        sentence = generate("math.mixed_ops_sentence_p2", Random(seed))
        word = generate("math.mixed_ops_word_problem_p2", Random(seed))
        # Both sets draw the same story from the same seed.
        assert sentence.stem[0].text == word.stem[0].text
        values = [_eval(_choice(c).split("=")[0]) for c in sentence.choices]
        right = values[sentence.answer]
        assert right == int(_answer(word))
        assert values.count(right) == 1


def test_two_step_add_sub_combines_three_numbers_once_each_way():
    for seed in SEEDS:
        q = generate("math.two_step_add_sub_p2", Random(seed))
        nums = _numbers(_stem(q))
        if len(nums) == 2:            # one amount, and how many more the other has
            a, gap = nums
            assert int(_answer(q)) == 2 * a + gap, _stem(q)
            continue
        a, b, c = nums
        assert int(_answer(q)) in (a + b - c, a - b + c, c - a - b), _stem(q)


def test_two_step_times_then_add():
    for seed in SEEDS:
        q = generate("math.two_step_word_problem", Random(seed))
        a, b, c = _numbers(_stem(q))
        assert int(_answer(q)) == a * b + c, _stem(q)


@pytest.mark.parametrize("key, steps", [("math.number_pattern_p2", (2, 5, 10, 100))])
def test_number_pattern_is_arithmetic(key, steps):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        terms = [int(_answer(q)) if t.strip() == r"\square" else int(t)
                 for t in q.stem[-1].tex.split(r",\ ")]
        diffs = {b - a for a, b in zip(terms, terms[1:])}
        assert len(diffs) == 1 and abs(diffs.pop()) in steps
        assert all(0 <= t <= 1000 for t in terms)


def test_repeating_pattern_has_period_three():
    for seed in SEEDS:
        q = generate("math.repeating_pattern_p2", Random(seed))
        row = [_answer(q) if s == "___" else s for s in q.stem[-1].text.split()]
        assert all(row[i] == row[i % 3] for i in range(len(row))), row


def test_time_notation():
    for seed in SEEDS:
        q = generate("math.time_notation_p2", Random(seed))
        stem, ans = q.stem[0].text, _answer(q)
        if "เขียนแบบใด" in stem:
            h, m = _numbers(stem)
            assert ans == f"{h}.{m:02d} น."
        elif "อ่านว่า" in stem:
            h, m = _numbers(stem)
            assert ans == f"{h} นาฬิกา {m} นาที"
        else:
            h, _, mark = _numbers(stem)
            assert ans == f"{h}.{5 * mark:02d} น."


def test_hours_and_minutes():
    for seed in SEEDS:
        q = generate("math.hours_minutes_p2", Random(seed))
        stem, ans = q.stem[0].text, int(_answer(q))
        nums = _numbers(stem)
        if "ชั่วโมงกับอีก" in stem:
            assert nums[0] == 60 * nums[1] + ans
        elif "ชั่วโมง" in stem:
            assert ans == 60 * nums[0] + nums[1]
        else:
            assert ans == nums[0] + nums[1]


def test_length_and_weight_stories():
    for seed in SEEDS:
        q = generate("math.length_word_problem_p2", Random(seed))
        n, ans = _numbers(_stem(q)), int(_answer(q))
        if "รวมกัน" in _stem(q):
            assert ans == 100 * (n[0] + n[2]) + n[1] + n[3]
        elif "สูงกว่า" in _stem(q):
            assert ans == 100 * n[0] + n[1] - n[2]
        elif "ไกลกว่า" in _stem(q):
            assert ans == 100 * n[0] + n[1] + n[2]
        elif "ต่อริบบิ้น" in _stem(q):
            assert ans == n[0] * n[1]
        else:
            assert ans == 100 * n[0] - n[1]
        q = generate("math.weight_word_problem_p2", Random(seed))
        n, ans, stem = _numbers(_stem(q)), int(_answer(q)), _stem(q)
        if "กิโลกรัม" in stem and "กรัม เท่ากับ" in stem:
            assert ans == 1000 * n[0] + n[1]
        elif "เท่ากับกี่กรัม" in stem:
            assert ans == 100 * n[0]
        elif "รวมหนัก" in stem:
            assert ans == 100 * (n[0] + n[1])
        else:
            assert ans == 1000 * n[0] - n[1]


def _chart(q):
    lines = q.stem[0].text.split("\n")
    key = _numbers(lines[-2])[-1]
    rows = {ln.split(":")[0]: ln.count("●") * key for ln in lines if ":" in ln}
    return rows, key, lines[-1]


def test_pictograph_values_are_symbols_times_key():
    for seed in SEEDS:
        q = generate("math.pictograph", Random(seed))
        rows, key, ask = _chart(q)
        asked = [r for r in rows if r in ask]
        assert len(asked) == 1 and rows[asked[0]] == int(_answer(q))
        q = generate("math.pictograph_compare_p2", Random(seed))
        rows, key, ask = _chart(q)
        x, y = [rows[r] for r in sorted((r for r in rows if r in ask), key=ask.index)]
        want = x - y if "มากกว่า" in ask else x + y
        assert int(_answer(q)) == want
        q = generate("math.pictograph_symbols_p2", Random(seed))
        rows, key, ask = _chart(q)
        row = [r for r in rows if f"แถวของ{r}" in ask][0]
        extra = _numbers(ask)[0]
        assert int(_answer(q)) == (rows[row] + extra) // key


def test_conversions_p2():
    for seed in SEEDS:
        q = generate("math.convert_length_p2", Random(seed))
        n = _numbers(_stem(q))
        assert int(_answer(q)) == 100 * n[0] + (n[1] if len(n) > 1 else 0)
        q = generate("math.convert_weight_p2", Random(seed))
        n = _numbers(_stem(q))
        assert int(_answer(q)) == 10 * n[0] + (n[1] if len(n) > 1 else 0)
