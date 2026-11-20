"""Re-solve the new Primary 1 sets independently from their visible content."""
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.multi_dozen_total_p1', 'math.story_matches_sentence_p1',
        'math.equivalent_number_forms_p1', 'math.compare_sums_p1')
DIGITS = ('ศูนย์', 'หนึ่ง', 'สอง', 'สาม', 'สี่', 'ห้า', 'หก', 'เจ็ด', 'แปด', 'เก้า')


def words(n):
    if n < 10:
        return DIGITS[n]
    tens, ones = divmod(n, 10)
    head = 'สิบ' if tens == 1 else 'ยี่สิบ' if tens == 2 else DIGITS[tens] + 'สิบ'
    return head + ('' if ones == 0 else 'เอ็ด' if ones == 1 else DIGITS[ones])


READ_WORD = {words(n): n for n in range(100)}
TO_ARABIC = str.maketrans('๐๑๒๓๔๕๖๗๘๙', '0123456789')


def ints(s):
    return [int(n) for n in re.findall(r'\d+', s)]


def text_of(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


@pytest.mark.parametrize('key', KEYS)
def test_independent_answers(key):
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = text_of(q.stem)
        choices = [text_of(c.content) for c in q.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(set(choices)) == len(choices)
        if key.endswith('multi_dozen_total_p1'):
            dozens, loose = ints(stem)
            want = sum(1 for _ in range(dozens) for _ in range(12)) + loose
            assert choices[q.answer] == str(want)
        elif key.endswith('story_matches_sentence_p1'):
            a, b = ints(stem)
            adding = '+' in stem
            truths = []
            for choice in choices:
                first, change = ints(choice)
                same_operation = ('เพิ่ม' in choice) == adding
                truths.append(first == a and change == b and same_operation)
                # Check the represented arithmetic by counting objects too.
                pool = list(range(first))
                if 'เพิ่ม' in choice:
                    pool.extend(range(first, first + change))
                else:
                    for _ in range(change):
                        pool.pop()
                if truths[-1]:
                    assert len(pool) == (a + b if adding else a - b)
            assert truths == [i == q.answer for i in range(len(choices))]
        elif key.endswith('equivalent_number_forms_p1'):
            truths = []
            for choice in choices:
                arabic, thai, word = choice.split(', ')
                values = (int(arabic), int(thai.translate(TO_ARABIC)), READ_WORD[word])
                truths.append(len(set(values)) == 1)
            assert truths == [i == q.answer for i in range(len(choices))]
        else:
            a, b, c, d = ints(stem)
            left = len([*range(a), *range(b)])
            right = len([*range(c), *range(d)])
            truths = []
            for choice in choices:
                if choice.startswith('ทั้งสอง'):
                    value = ints(choice)[0]
                    truths.append(left == right == value)
                else:
                    truths.append(left < right if 'น้อยกว่า' in choice else left > right if 'มากกว่า' in choice else left == right)
            assert truths == [i == q.answer for i in range(len(choices))]


def test_number_forms_exercise_zero_and_irregular_words():
    seen = set()
    for seed in range(1000):
        q = generate('math.equivalent_number_forms_p1', Random(seed))
        seen.add(int(text_of(q.choices[q.answer].content).split(', ')[0]))
    assert {0, 1, 10, 11, 20, 21, 99} <= seen


def test_sum_comparison_includes_all_three_relations():
    seen = set()
    for seed in range(300):
        q = generate('math.compare_sums_p1', Random(seed))
        seen.add(text_of(q.choices[q.answer].content))
    assert len(seen) == 3


def test_source_values():
    assert sum([12, 12, 7]) == 31
    assert sum([3, 4]) < sum([3, 5])
    assert int('๗'.translate(TO_ARABIC)) == READ_WORD['เจ็ด'] == 7
