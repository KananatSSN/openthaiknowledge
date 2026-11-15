"""Independent visible-content checks for the eleven-set digestion batch."""
import calendar
from decimal import Decimal
from fractions import Fraction
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = (
    'math.age_year_month_difference_p4', 'math.monthly_reading_duration_p4',
    'math.average_task_duration_p4', 'math.repeated_seconds_duration_p4',
    'math.reserve_half_remaining_p4', 'math.organizer_shared_cost_p4',
    'math.reserve_fraction_daily_budget_p5', 'math.equal_pieces_cm_to_mm_p5',
    'math.two_cuts_metres_to_cm_p5', 'math.mixed_weight_remaining_kg_p5',
    'math.price_per_khit_from_grams_p5',
)
MONTHS = ('มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
          'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม')


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def ints(s):
    return [int(n) for n in re.findall(r'\d+', s)]


def decimals(s):
    return [Decimal(n) for n in re.findall(r'\d+(?:\.\d+)?', s)]


@pytest.mark.parametrize('key', KEYS)
def test_independent_visible_answers(key):
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = content(q.stem)
        choices = [content(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        answer = choices[q.answer]
        if key.endswith('age_year_month_difference_p4'):
            ay, am, by, bm = ints(stem)
            elapsed = 0
            year, month = by, bm
            while (year, month) < (ay, am):
                month += 1
                if month == 12:
                    year, month = year + 1, 0
                elapsed += 1
            y, m = ints(answer)
            assert sum([12] * y) + m == elapsed
            assert 0 <= m < 12
        elif key.endswith('monthly_reading_duration_p4'):
            name = next(m for m in MONTHS if f'เดือน{m}ของ' in stem)
            days = calendar.monthrange(2025, MONTHS.index(name) + 1)[1]
            per, = ints(stem)
            h, m = ints(answer)
            assert sum([per] * days) == sum([60] * h) + m
            assert 0 <= m < 60
        elif key.endswith('average_task_duration_p4'):
            count, h, m = ints(stem)
            assert sum([int(answer)] * count) == sum([60] * h) + m
        elif key.endswith('repeated_seconds_duration_p4'):
            count, seconds = ints(stem)
            m, s = ints(answer)
            assert sum([seconds] * count) == sum([60] * m) + s
            assert 0 <= s < 60
        elif key.endswith('reserve_half_remaining_p4'):
            total, sold = ints(stem)
            assert sum([int(answer), int(answer), sold]) == total
        elif key.endswith('organizer_shared_cost_p4'):
            friends, room, food = ints(stem)
            attendees = len(['กานดา', *range(friends)])
            assert sum([int(answer)] * attendees) == room + food
            assert int(answer) * friends != room + food
        elif key.endswith('reserve_fraction_daily_budget_p5'):
            total, k, d, days = ints(stem)
            reserved = Fraction(total * k, d)
            assert sum([int(answer)] * days) + reserved == total
        elif key.endswith('equal_pieces_cm_to_mm_p5'):
            cm, count = decimals(stem)
            assert Decimal(answer) * count == cm * 10
        elif key.endswith('two_cuts_metres_to_cm_p5'):
            total, first, second = decimals(stem)
            assert Decimal(answer) / 100 + first + second == total
        elif key.endswith('mixed_weight_remaining_kg_p5'):
            first, second, removed = decimals(stem)
            assert (Decimal(answer) + removed) * 1000 == first + second
        else:
            per, grams, one, hundred = ints(stem)
            assert (one, hundred) == (1, 100)
            assert int(answer) * 100 == grams * per


def test_source_key_error_includes_organizer():
    total = 28750 + 49250
    assert Fraction(total, 25) == 3120
    assert Fraction(total, 24) == 3250  # printed key forgets the organizer


def test_source_exact_unit_conversions():
    assert Decimal('86.4') * 10 / 4 == 216
    assert (Decimal('5.28') - Decimal('1.82') - Decimal('1.73')) * 100 == 173
    assert (Decimal(3225) + 1784) / 1000 - Decimal('1.67') == Decimal('3.339')
    assert 6800 // 100 * 31 == 2108
    assert Fraction(3000) * (1 - Fraction(1, 5)) / 20 == 120


def test_months_and_borrowing_cases_are_exercised():
    months = set()
    borrowing = False
    for seed in range(300):
        q = generate('math.monthly_reading_duration_p4', Random(seed))
        stem = content(q.stem)
        months.add(next(m for m in MONTHS if f'เดือน{m}ของ' in stem))
        q = generate('math.age_year_month_difference_p4', Random(seed))
        _, am, _, bm = ints(content(q.stem))
        borrowing |= am < bm
    assert months == set(MONTHS) and borrowing
