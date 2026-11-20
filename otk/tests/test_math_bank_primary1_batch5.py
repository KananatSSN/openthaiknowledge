"""Re-solve every visible option for closest weights and false comparisons."""
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.closest_weight_pair_p1', 'math.false_sum_comparison_p1')


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


@pytest.mark.parametrize('key', KEYS)
def test_independent_visible_answers(key):
    seen = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        choices = [content(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        if key.endswith('closest_weight_pair_p1'):
            gaps = []
            for choice in choices:
                kg, khit = [int(n) for n in re.findall(r'\d+', choice)]
                # Compare in grams, independently of the generator's khit solver.
                a, b = sum([1000] * kg), sum([100] * khit)
                gaps.append(max(a, b) - min(a, b))
            assert len(set(gaps)) == len(gaps)
            assert q.answer == gaps.index(min(gaps))
            assert q.answer != gaps.index(max(gaps))
            seen.add(gaps[q.answer])
        else:
            truths = []
            for choice in choices:
                a, b, sign, right = re.fullmatch(r'(\d+) \+ (\d+) ([=<>≠]) (\d+)', choice).groups()
                total = len([*range(int(a)), *range(int(b))])
                right = int(right)
                verdict = {'=': total == right, '<': total < right,
                           '>': total > right, '≠': total != right}[sign]
                truths.append(verdict)
            assert truths == [i != q.answer for i in range(len(choices))]
            seen.add(re.search(r'[=<>≠]', choices[q.answer])[0])
    assert len(seen) >= (3 if key.endswith('closest_weight_pair_p1') else 4)


def test_source_closest_pair_by_grams():
    # 6kg vs7khit; 13khit vs2kg; 5khit vs4kg.
    gaps = [abs(6000-700), abs(1300-2000), abs(500-4000)]
    assert gaps == [5300, 700, 3500] and gaps.index(min(gaps)) == 1


def test_source_negative_instruction_and_inequality():
    assert [98 == 90+8, 54 > 50+2, 48 < 40+6] == [True, True, False]
    assert [50+8 == 80+5, 49 != 40+5, 30+1 > 37] == [False, True, False]
