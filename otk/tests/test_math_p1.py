"""ป.1 enrichment: answers re-derived from what the learner is shown.

Each check reads the stem the way a learner would — the numbers in the story,
the symbols in a row, the sentence in a choice — and recomputes the answer
without the generator's own arithmetic.
"""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.kit import story as _story

SEEDS = range(300)
NEW = keys_from("math_p1")


def _stem(q) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in q.stem)


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _numbers(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s)]


def test_the_module_registers_twenty_sets():
    assert len(NEW) == 20
    assert all(REGISTRY[k].level_for() == "ป.1" for k in NEW)


@pytest.mark.parametrize("n, words", [
    (0, "ศูนย์"), (1, "หนึ่ง"), (10, "สิบ"), (11, "สิบเอ็ด"), (20, "ยี่สิบ"),
    (21, "ยี่สิบเอ็ด"), (25, "ยี่สิบห้า"), (100, "หนึ่งร้อย"), (101, "หนึ่งร้อยเอ็ด"),
    (111, "หนึ่งร้อยสิบเอ็ด"), (1005, "หนึ่งพันห้า"), (2019, "สองพันสิบเก้า"),
    (10000, "หนึ่งหมื่น"), (1_000_001, "หนึ่งล้านเอ็ด"), (21_000_000, "ยี่สิบเอ็ดล้าน"),
])
def test_thai_words(n, words):
    assert _story.thai_words(n) == words


@pytest.mark.parametrize("key", NEW + ["math.add_word_problem", "math.sub_word_problem"])
def test_four_distinct_choices_and_numbers_within_one_hundred(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        assert len(q.choices) == REGISTRY[key].max_choices, (key, seed)
        assert len({_choice(c) for c in q.choices}) == REGISTRY[key].max_choices
        stem = _stem(q)
        assert all(n <= 100 for n in _numbers(stem)), (key, stem)
        assert all(n <= 200 for n in _numbers(_answer(q)))


@pytest.mark.parametrize("key, op", [
    ("math.add_word_problem", lambda a, b: a + b),
    ("math.sub_word_problem", lambda a, b: a - b),
])
def test_one_step_stories_combine_their_two_numbers(key, op):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        a, b = _numbers(_stem(q))
        assert int(_answer(q)) == op(a, b), _stem(q)


@pytest.mark.parametrize("key", ["math.compare_word_problem",
                                 "math.missing_part_word_problem"])
def test_comparison_and_missing_part_are_a_sum_or_a_difference(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        a, b = _numbers(_stem(q))
        ans = int(_answer(q))
        assert ans in (a + b, abs(a - b)), _stem(q)
        # The other operation is always on offer — it is the mistake.
        wrong = a + b if ans == abs(a - b) else abs(a - b)
        assert str(wrong) in {_choice(c) for c in q.choices} or wrong == 0


def _solve_sentence(tex: str) -> int | None:
    """The whole number the box stands for, found by trying them all."""
    left, right = tex.split("=")
    for v in range(0, 201):
        expr_l = left.replace(r"\square", str(v))
        expr_r = right.replace(r"\square", str(v))
        if eval(expr_l) == eval(expr_r):
            return v
    return None


def test_number_sentence_has_exactly_one_matching_sentence():
    for seed in SEEDS:
        q = generate("math.word_problem_number_sentence", Random(seed))
        values = [_solve_sentence(_choice(c)) for c in q.choices]
        story = q.stem[0].text
        a, b = _numbers(story)[:2]
        right = values[q.answer]
        assert right in (a + b, abs(a - b)), story
        assert values.count(right) == 1, (story, [_choice(c) for c in q.choices])


def test_mixed_expression_evaluates_to_its_answer():
    for seed in SEEDS:
        q = generate("math.add_sub_mixed", Random(seed))
        assert eval(q.stem[-1].tex) == int(_answer(q))


def test_mixed_missing_box_makes_the_sentence_true_and_nothing_else_does():
    for seed in SEEDS:
        q = generate("math.add_sub_mixed_missing", Random(seed))
        tex = q.stem[-1].tex
        for i, c in enumerate(q.choices):
            left, right = tex.replace(r"\square", _choice(c)).split("=")
            assert (eval(left) == eval(right)) == (i == q.answer), (tex, _choice(c))


def test_mixed_story_is_one_up_and_one_down():
    for seed in SEEDS:
        q = generate("math.add_sub_mixed_word_problem", Random(seed))
        a, b, c = _numbers(_stem(q))
        assert int(_answer(q)) in (a + b - c, a - b + c), _stem(q)


def test_number_pattern_is_arithmetic_by_one_or_ten():
    for seed in SEEDS:
        q = generate("math.number_pattern_p1", Random(seed))
        terms = [int(_answer(q)) if t.strip() == r"\square" else int(t)
                 for t in q.stem[-1].tex.split(r",\ ")]
        steps = {b - a for a, b in zip(terms, terms[1:])}
        assert len(steps) == 1 and abs(steps.pop()) in (1, 10), terms


def test_pattern_rule_names_the_step():
    for seed in SEEDS:
        q = generate("math.pattern_rule_p1", Random(seed))
        terms = [int(t) for t in q.stem[-1].tex.split(r",\ ")]
        step = terms[1] - terms[0]
        word, size = _answer(q).split("ทีละ")
        assert int(size) == abs(step)
        assert ("เพิ่มขึ้น" in word) == (step > 0)


def test_repeating_pattern_answer_completes_a_period_two_row():
    for seed in SEEDS:
        q = generate("math.repeating_pattern_p1", Random(seed))
        row = q.stem[-1].text.split()
        row = [_answer(q) if s == "___" else s for s in row]
        assert all(row[i] == row[i % 2] for i in range(len(row))), row


def test_pictograph_read_counts_the_symbols_in_the_asked_row():
    for seed in SEEDS:
        q = generate("math.pictograph_read_p1", Random(seed))
        lines = q.stem[0].text.split("\n")
        rows = {ln.split(":")[0]: ln.count("●") for ln in lines if ":" in ln}
        asked = [r for r in rows if r in lines[-1]]
        assert len(asked) == 1, lines[-1]
        assert rows[asked[0]] == int(_answer(q))


def test_pictograph_most_picks_the_longest_or_shortest_row():
    for seed in SEEDS:
        q = generate("math.pictograph_most_p1", Random(seed))
        rows = {ln.split(":")[0]: ln.count("●")
                for ln in q.stem[0].text.split("\n") if ":" in ln}
        pick = (max if "มากที่สุด" in q.stem[1].text else min)(rows, key=rows.get)
        assert _answer(q) == pick


def test_true_comparison_has_exactly_one_true_sentence():
    ops = {"<": int.__lt__, ">": int.__gt__, "=": int.__eq__, r"\neq": int.__ne__}
    for seed in SEEDS:
        q = generate("math.true_comparison_p1", Random(seed))
        truth = []
        for c in q.choices:
            a, op, b = _choice(c).split()
            truth.append(ops[op](int(a), int(b)))
        assert truth.count(True) == 1 and truth[q.answer]


def test_number_words_round_trip():
    for seed in SEEDS:
        q = generate("math.number_words_p1", Random(seed))
        if q.stem[0].text.startswith("จำนวนนี้"):
            assert _answer(q) == _story.thai_words(int(q.stem[1].tex))
        else:
            words = re.search(r"“(.+)”", q.stem[0].text).group(1)
            assert _story.thai_words(int(_answer(q))) == words


def test_thai_numerals_round_trip():
    back = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")
    for seed in SEEDS:
        q = generate("math.thai_numerals_p1", Random(seed))
        assert _answer(q).translate(back) == q.stem[1].text.translate(back)


def test_who_has_most_reads_the_amounts():
    for seed in SEEDS:
        q = generate("math.compare_who_most_p1", Random(seed))
        stem = q.stem[0].text
        amounts = dict(re.findall(r"(\S+?)มี(?:\S*?) (\d+) ", stem))
        amounts = {k.split()[-1]: int(v) for k, v in amounts.items()}
        pick = (max if "มากที่สุด" in stem else min)(amounts, key=amounts.get)
        assert _answer(q) == pick, (stem, amounts)


def test_subtraction_within_twenty_crosses_ten():
    for seed in SEEDS:
        q = generate("math.subtract_within_20_p1", Random(seed))
        a, b = _numbers(_stem(q))
        assert 11 <= a <= 18 and b <= 9 and b > a % 10
        assert _answer(q) == str(a - b)
        assert len({_choice(c) for c in q.choices}) == REGISTRY["math.subtract_within_20_p1"].max_choices
