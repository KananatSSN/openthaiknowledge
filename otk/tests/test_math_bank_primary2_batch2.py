"""Independent answers from visible Primary 2 division and chart questions."""
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.unit_price_p2', 'math.quotient_remainder_story_p2', 'math.least_remainder_p2',
        'math.days_to_weeks_p2', 'math.remaining_two_step_p2', 'math.grouped_sales_p2',
        'math.two_purchase_total_p2', 'math.pictograph_selected_total_p2', 'math.pictograph_matching_rows_p2')


def ints(s):
    return [int(n) for n in re.findall(r'\d+', s)]


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def divide_by_counting(total, group):
    count = 0
    while total >= group:
        total -= group
        count += 1
    return count, total


def read_chart(stem):
    scale = int(re.search(r'กำหนดให้ ● แทนขนม (\d+) ชิ้น', stem)[1])
    return {line.split(':')[0]: sum(1 for c in line if c == '●' for _ in range(scale))
            for line in stem.splitlines() if ':' in line}, scale


@pytest.mark.parametrize('key', KEYS)
def test_visible_answers_independently(key):
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = content(q.stem)
        choices = [content(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        answer = choices[q.answer]
        ns = ints(stem)
        if key.endswith('unit_price_p2'):
            count, total = (6, ns[0]) if 'ครึ่งโหล' in stem else ns
            solutions = [price for price in range(1, 1000) if sum([price] * count) == total]
            assert len(solutions) == 1
            want = solutions[0]
        elif key.endswith('quotient_remainder_story_p2'):
            total, people = ns
            quotient, remainder = divide_by_counting(total, people)
            assert ints(answer) == [quotient, remainder]
            truths = []
            for choice in choices:
                quotient, remainder = ints(choice)
                truths.append(quotient * people + remainder == total and 0 <= remainder < people)
            assert truths == [i == q.answer for i in range(len(choices))]
            continue
        elif key.endswith('least_remainder_p2'):
            total = ns[0]
            remainders = [divide_by_counting(total, ints(c)[0])[1] for c in choices]
            assert remainders.count(min(remainders)) == 1
            assert remainders[q.answer] == min(remainders)
            continue
        elif key.endswith('days_to_weeks_p2'):
            solutions = [weeks for weeks in range(1, 13) if sum(1 for _ in range(weeks) for _ in range(7)) == ns[0]]
            assert len(solutions) == 1
            want = solutions[0]
        elif key.endswith('remaining_two_step_p2'):
            total, removed, factor = ns
            objects = list(range(total))[removed:]
            if 'แบ่งให้' in stem:
                piles = [0] * factor
                for i, _ in enumerate(objects):
                    piles[i % factor] += 1
                assert len(set(piles)) == 1
                want = piles[0]
            else:
                want = sum(factor for _ in objects)
        elif key.endswith('grouped_sales_p2'):
            if 'กล่องละ' in stem:
                total, per_box, price = ns
                boxes = [list(range(total))[i:i + per_box] for i in range(0, total, per_box)]
                assert all(len(box) == per_box for box in boxes)
                want = sum(price for _ in boxes)
            else:
                items, price, people = ns
                piles = [0] * people
                for i in range(sum([price] * items)):
                    piles[i % people] += 1
                assert len(set(piles)) == 1
                want = piles[0]
        elif key.endswith('two_purchase_total_p2'):
            books, book_price, pencils, pencil_price = ns
            want = sum([book_price] * books + [pencil_price] * pencils)
        elif key.endswith('pictograph_selected_total_p2'):
            chart, _ = read_chart(stem)
            days = re.findall(r'วัน(?:จันทร์|อังคาร|พุธ|พฤหัสบดี|ศุกร์)', stem.splitlines()[-1])
            assert len(set(days)) == 3
            want = sum(chart[day] for day in days)
        else:
            chart, _ = read_chart(stem)
            target = ints(stem.splitlines()[-1])[0]
            matching = {day for day, amount in chart.items() if amount == target}
            assert len(matching) == 2
            truths = [set(choice.split(' และ ')) == matching for choice in choices]
            assert truths == [i == q.answer for i in range(len(choices))]
            continue
        assert answer == str(want), (key, seed, stem, answer, want)


def test_both_compound_story_variants_are_exercised():
    for key, marker in (('math.remaining_two_step_p2', 'แบ่งให้'), ('math.grouped_sales_p2', 'กล่องละ'),
                        ('math.unit_price_p2', 'ครึ่งโหล')):
        seen = {marker in content(generate(key, Random(seed)).stem) for seed in range(50)}
        assert seen == {True, False}


def test_least_remainder_skips_a_total_with_too_few_distinct_remainders():
    from otk.sets.math.p2.division import LeastRemainderP2

    class Rng:
        def __init__(self):
            self.totals = iter((60, 58))

        def randint(self, lo, hi):
            return next(self.totals)

        def sample(self, values, k):
            return list(values)[:k]

        def choice(self, values):
            return values[0]

    stem, right, wrongs = LeastRemainderP2().compose(Rng())
    assert ints(stem)[0] == 58
    assert len(set([right, *wrongs])) == 4


def test_source_regressions():
    assert sum([7] * 7) == 49
    assert sum([5] * 6) == 30
    assert divide_by_counting(45, 6) == (7, 3)
    assert divide_by_counting(100, 9) == (11, 1)
    assert [divide_by_counting(58, d)[1] for d in (5, 6, 7)] == [3, 4, 2]
    assert divide_by_counting(60 - 25, 5) == (7, 0)
    assert sum([35] * (27 - 18)) == 315
    assert divide_by_counting(sum([45] * 6), 3) == (90, 0)
    assert sum([89] * divide_by_counting(42, 6)[0]) == 623
    assert sum([24] * 5 + [49] * 3) == 267
    assert sum([5, 4, 5, 6, 8]) * 10 == 280
    assert sum([6, 5, 4]) * 5 == 75
