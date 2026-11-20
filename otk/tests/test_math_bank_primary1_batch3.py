"""Independently solve visible measurement questions, including boundary ticks."""
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.measuring_tool_p1', 'math.weight_difference_pairs_p1', 'math.scale_kg_khit_p1')


def text_of(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def ints(s):
    return [int(n) for n in re.findall(r'\d+', s)]


@pytest.mark.parametrize('key', KEYS)
def test_independent_answers(key):
    seen = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = text_of(q.stem)
        choices = [text_of(c.content) for c in q.choices]
        assert len(set(choices)) == len(choices) == REGISTRY[key].max_choices
        if key.endswith('measuring_tool_p1'):
            length, = ints(stem)
            candidates = []
            for i, choice in enumerate(choices):
                limits = ints(choice)
                if not limits or limits[0] < length:
                    continue
                if ('โค้งแนบ' in stem) == ('อ่อน' in choice):
                    candidates.append((limits[0], i))
            want = min(candidates)[1]
            assert q.answer == want
            seen.add(choices[want])
        elif key.endswith('weight_difference_pairs_p1'):
            # Convert both masses into grams, rather than using a khit gap.
            gaps = []
            for label in choices:
                kg, khit = ints(label)
                grams = [1000 * kg, 100 * khit]
                gaps.append(max(grams) - min(grams))
            assert gaps.count(max(gaps)) == 1
            assert q.answer == gaps.index(max(gaps))
        else:
            ten, one, start, end, ticks = ints(stem)
            assert ten == 10 and one == 1 and end == start + 1
            # Walk the small tick marks, then divide into groups of ten.
            marks = list(range(start * 10, end * 10 + 1))
            kg, khit = divmod(marks[ticks], 10)
            assert choices[q.answer] == f'{kg} กิโลกรัม {khit} ขีด'
            seen.add(ticks)
    if key.endswith('measuring_tool_p1'):
        assert len(seen) == 3
    elif key.endswith('scale_kg_khit_p1'):
        assert seen == set(range(1, 10))


def test_source_weight_differences_by_grams():
    # Original Q11: 2kg/5khit, 15khit/1kg, 2kg/10khit.
    grams = [(2000, 500), (1500, 1000), (2000, 1000)]
    assert [max(pair) - min(pair) for pair in grams] == [1500, 500, 1000]


def test_every_scale_parameter_has_distinct_normalized_choices():
    from otk.sets.math.p1.measurement import ScaleKgKhitP1

    class Parameters:
        def __init__(self, kg, tick):
            self.values = iter((kg, tick))

        def randint(self, low, high):
            value = next(self.values)
            assert low <= value <= high
            return value

    for kg in range(1, 6):
        for tick in range(1, 10):
            _, correct, wrong = ScaleKgKhitP1().compose(Parameters(kg, tick))
            assert correct not in wrong and len(set(wrong)) == len(wrong) >= 3
            for reading in [correct, *wrong]:
                _, khit = ints(reading)
                assert 0 <= khit < 10
