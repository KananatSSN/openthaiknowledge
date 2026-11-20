"""Solve the new arithmetic forms from visible content by integer enumeration."""
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.equal_sums_missing_p1', 'math.match_sum_expression_p1',
        'math.missing_minuend_p1', 'math.match_difference_expression_p1')


def text_of(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def arithmetic(expression):
    """Count signed unit tokens; no generator solver or Python evaluation."""
    total = 0
    for token in re.findall(r'[+−-]?\s*\d+', expression):
        token = token.replace(' ', '').replace('−', '-')
        value = int(token)
        total += sum(1 for _ in range(abs(value))) * (-1 if value < 0 else 1)
    return total


@pytest.mark.parametrize('key', KEYS)
def test_visible_answers_independently(key):
    forms = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        choices = [text_of(c.content) for c in q.choices]
        assert len(set(choices)) == len(choices) == REGISTRY[key].max_choices
        if key.endswith(('equal_sums_missing_p1', 'missing_minuend_p1')):
            equation, = [b.tex for b in q.stem if b.kind == 'math']
            assert r'\\square' not in equation  # one TeX command, no line break
            assert equation.count(r'\square') == 1
            left, right = equation.split('=')
            candidates = []
            for n in range(101):
                left_value = arithmetic(left.replace(r'\square', str(n)))
                right_value = arithmetic(right.replace(r'\square', str(n)))
                if left_value == right_value:
                    candidates.append(n)
            assert candidates == [int(choices[q.answer])]
            forms.add((r'\square' in left, left.strip().startswith(r'\square') or right.strip().startswith(r'\square')))
            if key.endswith('equal_sums_missing_p1'):
                # These draws go beyond swapping the two full-side addends.
                full_side = right if r'\square' in left else left
                visible = [int(n) for n in re.findall(r'\d+', full_side)]
                assert int(choices[q.answer]) not in visible
        else:
            stem = text_of(q.stem)
            target = stem.split('เท่ากับ ')[1]
            total = arithmetic(target)
            if len(re.findall(r'\d+', target)) == 2:
                assert target not in choices
                if key.endswith('match_sum_expression_p1'):
                    assert sorted(re.findall(r'\d+', target)) != sorted(re.findall(r'\d+', choices[q.answer]))
            truths = [arithmetic(c) == total for c in choices]
            assert truths == [i == q.answer for i in range(len(choices))]
            forms.add(len(re.findall(r'\d+', target)))
            for choice in choices:
                assert all(0 <= int(n) <= 100 for n in re.findall(r'\d+', choice))
    if key.endswith('equal_sums_missing_p1'):
        assert len(forms) == 4
    else:
        assert len(forms) == 2


def test_printed_equations_by_substitution():
    assert 32 + 68 == 41 + 59
    assert 36 + 53 == 12 + 77
    assert 82 - 44 == 38 and 15 == 42 - 27
    assert 54 + 45 == 41 + 58
    assert 71 - 9 == 66 - 4
    assert 85 - 58 - 13 == 14
