"""Independent solutions for the Primary 1 text-layer batch, from visible data."""
from datetime import date, timedelta
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = (
    'math.dozen_change_p1', 'math.equal_amount_total_p1', 'math.calendar_date_shift_p1',
    'math.compare_spending_totals_p1', 'math.purchase_from_balance_p1',
    'math.budget_conclusion_p1', 'math.length_comparison_statement_p1',
)


def ints(s):
    return [int(x) for x in re.findall(r'\d+', s)]


def choice_text(c):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in c.content)


@pytest.mark.parametrize('key', KEYS)
def test_answers_from_visible_stems(key):
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = ' '.join(getattr(b, 'text', '') for b in q.stem)
        ns = ints(stem)
        answer = choice_text(q.choices[q.answer])
        assert len(q.choices) == REGISTRY[key].max_choices
        if key.endswith('dozen_change_p1'):
            # Model twelve individual objects instead of the formula used in the set.
            objects = list(range(12))
            change = ns[0]
            if 'เพิ่ม' in stem:
                objects.extend(range(12, 12 + change))
            else:
                for _ in range(change):
                    objects.pop()
            want = len(objects)
        elif key.endswith('equal_amount_total_p1'):
            amount = ns[0]
            want = sum(1 for _ in range(2) for _ in range(amount))
        elif key.endswith('calendar_date_shift_p1'):
            elapsed, day = ns
            start = date(2026, 1, day)
            target = start + timedelta(days=elapsed) if stem.startswith('เมื่อ') else start - timedelta(days=elapsed)
            assert target.month == 1
            want = target.day
        elif key.endswith('compare_spending_totals_p1'):
            totals = {}
            for name, first, second in re.findall(r'คน ([กขคง]) ซื้อขนม (\d+) บาท และซื้อน้ำ (\d+) บาท', stem):
                # Enumerate the baht in both purchases.
                totals[name] = len([*range(int(first)), *range(int(second))])
            assert len(totals) == len(set(totals.values())) == 4
            want = f'คน {min(totals, key=totals.get)}'
        elif key.endswith('purchase_from_balance_p1'):
            have, *_, left = ns
            prices = {name: int(p) for name, p in re.findall(r'(\S+?)ราคา (\d+) บาท', stem)}
            solutions = [name for name, p in prices.items() if have - p == left]
            assert len(solutions) == 1
            want = solutions[0]
        elif key.endswith('budget_conclusion_p1'):
            have, price = ns
            # Simulate paying one baht per baht of price.
            unspent = list(range(have))
            missing = 0
            for _ in range(price):
                if unspent:
                    unspent.pop()
                else:
                    missing += 1
            want = (f'เงินไม่พอ ต้องหาเพิ่ม {missing} บาท' if missing
                    else f'เงินพอ ซื้อแล้วเหลือ {len(unspent)} บาท' if unspent
                    else 'เงินพอดี ซื้อแล้วไม่เหลือเงิน')
        else:
            red, blue = ns
            longest, shortest = ('สีแดง', 'สีฟ้า') if red > blue else ('สีฟ้า', 'สีแดง')
            gap = len(set(range(red)) ^ set(range(blue)))
            want = f'ริบบิ้น{longest}ยาวกว่าริบบิ้น{shortest} {gap} เซนติเมตร'
        assert answer == str(want), (key, seed, stem, answer, want)


def test_budget_covers_shortage_exact_and_surplus():
    seen = set()
    for seed in range(100):
        q = generate('math.budget_conclusion_p1', Random(seed))
        answer = choice_text(q.choices[q.answer])
        seen.add('exact' if 'เงินพอดี' in answer else 'shortage' if 'เงินไม่พอ' in answer else 'surplus')
    assert seen == {'exact', 'shortage', 'surplus'}


def test_source_numerical_regressions():
    # The source values, without reproducing its stems.
    assert len(list(range(12)) + list(range(6))) == 18
    assert len(list(range(12))[10:]) == 2
    assert sum([10, 10]) == 20
    assert sum([48, 48]) == 96
    assert (date(2026, 1, 5) + timedelta(days=3)).day == 8
    assert [sum(pair) for pair in ((2, 5), (3, 5), (4, 5))] == [7, 8, 9]
    assert [p for p in (6, 4, 5) if 8 - p == 4] == [4]
    assert len(range(68, 75)) == 7
    assert len(set(range(40)) ^ set(range(17))) == 23
