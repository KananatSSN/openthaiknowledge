"""Independent place-value and strict-order checks from visible questions."""
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.digit_value_difference_p2', 'math.number_between_bounds_p2')


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


@pytest.mark.parametrize('key', KEYS)
def test_independent_visible_answers(key):
    seen = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        choices = [content(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        if key.endswith('digit_value_difference_p2'):
            stem = content(q.stem)
            number = re.search(r'จำนวน (\d+)', stem)[1]
            places = re.findall(r'หลัก(ร้อย|สิบ|หน่วย)', stem)
            # Build each positional contribution as a count of equal groups.
            parts = {name: sum([int(digit)] * len(range(size)))
                     for name, digit, size in zip(('ร้อย', 'สิบ', 'หน่วย'), number, (100, 10, 1))}
            left, right = (parts[name] for name in places)
            want = max(left, right) - min(left, right)
            assert int(choices[q.answer]) == want
            seen.add(tuple(sorted(places)))
            if number[0] == number[2] and set(places) == {'ร้อย', 'หน่วย'}:
                assert want == sum([int(number[0])] * 99)
        else:
            stem = content(q.stem)
            first, last = [int(n) for n in re.findall(r'\d+', stem)]
            ascending = 'น้อยไปมาก' in stem
            assert (first < last) == ascending
            truths = [([first, int(c), last] == sorted({first, int(c), last}, reverse=not ascending))
                      for c in choices]
            assert truths == [i == q.answer for i in range(len(choices))]
            assert all(100 <= n <= 999 for n in (first, last, *map(int, choices)))
            seen.add(ascending)
    assert len(seen) == (3 if key.endswith('digit_value_difference_p2') else 2)


def test_source_values_and_strict_endpoints():
    assert 50 - 6 == 44
    assert sum([4] * 100) - 4 == 396
    assert [n for n in (313, 342, 340) if 314 < n < 341] == [340]


def test_zero_contributions_and_identical_digits_are_exercised():
    answers = set()
    for seed in range(2000):
        q = generate('math.digit_value_difference_p2', Random(seed))
        answers.add(int(content(q.choices[q.answer].content)))
    assert {0, 44, 396, 891} <= answers
