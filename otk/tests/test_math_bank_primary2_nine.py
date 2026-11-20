"""Validate every displayed choice using calendar dates and normalized measurements."""
import calendar
from fractions import Fraction
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.month_ordinal_p2', 'math.month_pair_days_p2', 'math.half_metre_p2',
        'math.unit_quantity_p2', 'math.calibrated_volume_tools_p2', 'math.repeating_colour_pair_p2',
        'math.weighing_tool_precision_p2', 'math.weight_threshold_p2', 'math.weight_extreme_p2')
MONTHS = 'มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def grams(label):
    if label.endswith('กิโลกรัมครึ่ง'):
        return 1000 * (Fraction(int(re.search(r'\d+', label)[0])) + Fraction(1, 2))
    parts = re.findall(r'(\d+) (กิโลกรัม|กรัม|ขีด)', label)
    assert parts, label
    return sum(int(n) * {'กิโลกรัม': 1000, 'กรัม': 1, 'ขีด': 100}[unit] for n, unit in parts)


@pytest.mark.parametrize('key', KEYS)
def test_visible_answers_independently(key):
    branches = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = content(q.stem)
        choices = [content(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        if key.endswith('month_ordinal_p2'):
            if 'มีชื่อว่า' in stem:
                i = int(re.search(r'\d+', stem)[0]) - 1
                valid = [c == MONTHS[i] for c in choices]
                branches.add('name')
            else:
                month = next(m for m in MONTHS if 'เดือน' + m in stem)
                valid = [int(c) == MONTHS.index(month) + 1 for c in choices]
                branches.add('ordinal')
        elif key.endswith('month_pair_days_p2'):
            year, a, b = map(int, re.findall(r'\d+', stem))
            total = sum(calendar.monthrange(year, m)[1] for m in (a, b))
            valid = [int(c) == total for c in choices]
            branches.add((calendar.isleap(year), 2 in (a, b)))
        elif key.endswith('half_metre_p2'):
            whole = int(re.search(r'\d+', stem)[0])
            expected = (whole + Fraction(1, 2)) * 100
            mixed = 'เขียนเป็นเมตร' in stem
            actual = []
            for c in choices:
                nums = list(map(int, re.findall(r'\d+', c)))
                actual.append(nums[0] * 100 + nums[1] if mixed else nums[0])
            valid = [a == expected for a in actual]
            branches.add(mixed)
        elif key.endswith('repeating_colour_pair_p2'):
            shown = stem.split(': ', 1)[1].split(' เติมสี')[0].split(' · ')
            holes = [i for i, x in enumerate(shown) if x == '□']
            assert len(shown) == 10 and len(holes) == 2
            valid = []
            for c in choices:
                candidate = shown[:]
                colours = c.split(' และ ')
                assert len(colours) == 2
                for i, colour in zip(holes, colours):
                    candidate[i] = colour
                valid.append(all(candidate[i] == candidate[i % 4] for i in range(len(candidate))))
            # Enumerate all possible two-colour assignments, independent of stored answer.
            palette = set(shown) - {'□'}
            possibilities = []
            for x in palette:
                for y in palette:
                    row = shown[:]
                    row[holes[0]], row[holes[1]] = x, y
                    if all(row[i] == row[i % 4] for i in range(len(row))):
                        possibilities.append((x, y))
            assert len(possibilities) == 1
            pattern = tuple(shown[i] for i in (0, 2, 3))
            branches.add(tuple(v == shown[0] for v in pattern))
            branches.add(('same', possibilities[0][0] == possibilities[0][1]))
        elif key.endswith('unit_quantity_p2'):
            unit = stem.split('เป็นหน่วย')[0]
            # Match dimensional families, not objects or the physical state of contents.
            expected = ('ปริมาตร' if unit in ('ลิตร', 'มิลลิลิตร') else
                        'ความยาว' if unit in ('เมตร', 'เซนติเมตร') else
                        'น้ำหนัก' if unit in ('กรัม', 'กิโลกรัม') else 'เวลา')
            valid = [c == expected for c in choices]
            branches.add(unit)
        elif key.endswith('calibrated_volume_tools_p2'):
            valid = []
            for c in choices:
                tools = c.split(' · ')
                assert len(tools) == 3
                # Every tool must carry a volume unit, rather than a length/mass scale
                # or a vessel whose capacity has not been specified.
                good = all('ลิตร' in t and 'ไม่ระบุ' not in t for t in tools)
                valid.append(good)
                if not good:
                    branches.add('capacity' if 'ไม่ระบุ' in c else 'mass' if 'กรัม' in c else 'length')
        elif key.endswith('weighing_tool_precision_p2'):
            mass, required = map(int, re.findall(r'\d+', stem)[:2])
            rows = re.findall(r'(เครื่องชั่ง[กขคง]) ชั่งได้ไม่เกิน (\d+) กรัม ขีดแบ่ง (\d+) กรัม', stem)
            assert len(rows) == 4
            # Feasible tools must satisfy both independent inequalities.
            feasible = {label for label, cap, step in rows if mass <= int(cap) and int(step) <= required}
            assert len(feasible) == 1
            valid = [c in feasible for c in choices]
            branches.add((required, next(iter(feasible))))
        elif key.endswith('weight_threshold_p2'):
            threshold = int(re.findall(r'\d+', stem)[-1])
            more = 'หนักกว่า' in stem
            vals = [grams(c) for c in choices]
            valid = [v > threshold if more else v < threshold for v in vals]
            assert sum(v == threshold for v in vals) == 2
            branches.add(more)
        else:
            vals = [grams(c) for c in choices]
            assert len(set(vals)) == len(vals)
            maximum = 'หนักที่สุด' in stem
            expected = (max if maximum else min)(vals)
            valid = [v == expected for v in vals]
            branches.add(maximum)
        assert sum(valid) == 1, (key, seed, stem, choices, valid)
        assert valid[q.answer], (key, seed, stem, choices)
    floors = {'month_ordinal_p2': 2, 'month_pair_days_p2': 4, 'half_metre_p2': 2,
              'unit_quantity_p2': 8, 'repeating_colour_pair_p2': 4, 'calibrated_volume_tools_p2': 3,
              'weighing_tool_precision_p2': 12, 'weight_threshold_p2': 2, 'weight_extreme_p2': 2}
    assert len(branches) >= floors[key.removeprefix('math.')]
