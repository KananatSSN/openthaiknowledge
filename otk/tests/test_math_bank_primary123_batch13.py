"""Solve visible statements, clocks, coin groups, ledgers and models independently."""
from collections import Counter
from datetime import datetime
from decimal import Decimal
from random import Random
import re

import pytest
import sympy as s

from otk.core import REGISTRY, generate

KEYS = tuple('math.' + k for k in (
    'expanded_form_judgement_p1', 'place_value_statement_p1', 'length_order_names_p1',
    'colloquial_clock_p2', 'clock_hands_from_hour_p2', 'clock_period_to_24h_p2',
    'calendar_event_month_p2', 'daily_schedule_activity_p2', 'pattern_changing_attribute_p2',
    'money_purse_comparison_p3', 'money_odd_purse_p3', 'satang_ledger_query_p3',
    'purchase_sentence_models_p3'))
MONTHS = 'มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def ints(value):
    return list(map(int, re.findall(r'\d+', value)))


def coin_value(label):
    denomination, count, quarter, quarters = ints(label)
    assert quarter == 25
    return sum([Decimal(denomination)] * count + [Decimal('.25')] * quarters)


@pytest.mark.parametrize('key', KEYS)
def test_independent_visible_answers(key):
    seen = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = content(q.stem)
        choices = [content(c.content) for c in q.choices]
        answer = choices[q.answer]
        assert len(set(choices)) == len(choices) == REGISTRY[key].max_choices
        if key.endswith('expanded_form_judgement_p1'):
            canonical = []
            for choice in choices:
                n, a, b = ints(choice)
                assert s.Eq(n, a + b)
                canonical.append(str(n).zfill(2) == str(a // 10) + str(b) and a % 10 == 0 and b < 10)
            assert canonical == [i != q.answer for i in range(4)]
        elif key.endswith('place_value_statement_p1'):
            truths = []
            for choice in choices:
                digit, n, value = ints(choice)
                place = 10 if 'หลักสิบ' in choice else 1
                truths.append(int(str(n)[-2 if place == 10 else -1]) == digit and value == digit * place)
            assert truths == [i == q.answer for i in range(4)]
        elif key.endswith('length_order_names_p1'):
            lengths = dict((name, int(length)) for name, length in re.findall(r'(สี\S+?)ยาว (\d+) เซนติเมตร', stem))
            assert len(lengths) == 4
            values = [lengths[name] for name in answer.split(' → ')]
            assert values == sorted(lengths.values(), reverse='ยาวไปสั้น' in stem)
            seen.add('ยาวไปสั้น' in stem)
        elif key.endswith('colloquial_clock_p2'):
            hour, minute = ints(stem)
            # Decode every answer back to 24h rather than calling the authoring formatter.
            truths = []
            for choice in choices:
                nums = ints(choice)
                h = nums[0]
                h += 12 if 'บ่าย' in choice else 18 if 'ทุ่ม' in choice else 0
                m = nums[1] if len(nums) > 1 else 0
                truths.append((h, m) == (hour, minute))
            assert truths == [i == q.answer for i in range(4)]
            seen.add('ตี' if hour < 6 else 'โมง' if hour < 12 else 'ทุ่ม')
        elif key.endswith('clock_hands_from_hour_p2'):
            h, m = ints(stem)
            minute_angle = 6 * m
            hour_angle = 30 * h % 360
            truths = [(a % 12 * 30 == hour_angle and b % 12 * 30 == minute_angle)
                      for a, b in map(ints, choices)]
            assert truths == [i == q.answer for i in range(4)]
            seen.add(h)
        elif key.endswith('clock_period_to_24h_p2'):
            numbers = ints(stem)
            h = numbers[0]
            mark = numbers[-2]  # last numeral is 24 in the question.
            m = mark % 12 * 5
            hour = h + (12 if 'หลังเที่ยงวัน' in stem else 0)
            want = datetime(2000, 1, 1, hour, m).strftime('%H.%M น.')
            assert answer == want
            seen.add(hour >= 12)
        elif key.endswith('calendar_event_month_p2'):
            target = re.search(r'กิจกรรม(\S+)อยู่ในเดือนใด', stem).group(1)
            date = re.search(re.escape(target) + r' (\d+)/(\d+)', stem)
            day, month = map(int, date.groups())
            assert datetime(2000, month, day).month == MONTHS.index(answer) + 1
            seen.add(target)
        elif key.endswith('daily_schedule_activity_p2'):
            data, question = stem.split(' ตามตาราง')
            hour, minute = ints(question)
            entries = re.findall(r'(\d+)\.00 น\. (\S+)', data)
            want = next(activity for h, activity in entries if int(h) == hour)
            assert minute == 0 and answer == want
            seen.add(answer)
        elif key.endswith('pattern_changing_attribute_p2'):
            data = stem.split('แบบรูป: ')[1].split(' ลักษณะใด')[0]
            rows = [part.split() for part in data.split(' → ')]
            varied = [name for i, name in enumerate(('ขนาด', 'สี', 'รูปร่าง'))
                      if len({row[i] for row in rows}) > 1]
            assert varied == [answer]
            assert rows[:3] == rows[3:]
            seen.add(answer)
        elif key.endswith('money_purse_comparison_p3'):
            totals = {}
            for name, note, count, baht, whole, satang, small in re.findall(
                    r'(\S+): ธนบัตร (\d+) บาท (\d+) ฉบับ เหรียญ (\d+) บาท (\d+) เหรียญ เหรียญ (\d+) สตางค์ (\d+) เหรียญ', stem):
                totals[name] = sum([Decimal(note)] * int(count) + [Decimal(baht)] * int(whole)
                                   + [Decimal(satang) / 100] * int(small))
            assert len(totals) == len(set(totals.values())) == 4
            if 'มีเงินรวมกี่บาท' in stem:
                target = re.search(r' (\S+)มีเงินรวมกี่บาท', stem).group(1)
                assert Decimal(answer.removesuffix(' บาท')) == totals[target]
                seen.add('total')
            else:
                want = sorted(totals, key=totals.get, reverse='มากที่สุด' in stem)[0]
                assert answer == want
                seen.add('most' if 'มากที่สุด' in stem else 'least')
        elif key.endswith('money_odd_purse_p3'):
            amounts = list(map(coin_value, choices))
            frequencies = Counter(amounts)
            assert sorted(frequencies.values()) == [1, 3]
            assert frequencies[amounts[q.answer]] == 1
        elif key.endswith('satang_ledger_query_p3'):
            rows = re.findall(r'(\d) \| ([^|]+) \| (รับ|จ่าย) \| (\d+\.\d{2})', stem)
            assert len(rows) == 8
            incoming, outgoing, day2, mother, father = [], [], [], [], []
            balance = Decimal(0)
            for day, name, kind, amount in rows:
                value = Decimal(amount)
                (incoming if kind == 'รับ' else outgoing).append(value)
                balance += value if kind == 'รับ' else -value
                assert balance >= 0
                if kind == 'จ่าย' and day == '2':
                    day2.append(value)
                if name == 'แม่ให้เงิน':
                    mother.append(value)
                if name == 'พ่อให้เงิน':
                    father.append(value)
            if 'วันที่ 2 มีรายจ่ายรวม' in stem:
                want, mode = sum(day2), 'day2'
            elif 'เงินคงเหลือ' in stem:
                want, mode = balance, 'balance'
            elif 'ต่างกัน' in stem:
                want, mode = abs(sum(mother) - sum(father)), 'parents'
            else:
                want, mode = sum(incoming), 'income'
            assert [Decimal(c.removesuffix(' บาท')) == want for c in choices] == [i == q.answer for i in range(4)]
            seen.add(mode)
        else:
            data = ints(stem)
            if stem.startswith('ซื้อสมุด'):
                a, b, c, d = data
                want = sum([b] * a + [d] * c)
                seen.add('two-products')
            else:
                total, paid, months = data
                remaining = total - paid
                want = s.Rational(remaining, months)
                assert want * months + paid == total
                seen.add('instalments')
            values = [s.sympify(c.split('=')[0].replace(r'\times', '*').replace(r'\div', '/'), rational=True)
                      for c in choices]
            assert [v == want for v in values] == [i == q.answer for i in range(4)]
    floors = {'length_order_names_p1': 2, 'colloquial_clock_p2': 3, 'clock_hands_from_hour_p2': 24,
              'clock_period_to_24h_p2': 2, 'calendar_event_month_p2': 4, 'daily_schedule_activity_p2': 4, 'pattern_changing_attribute_p2': 3,
              'money_purse_comparison_p3': 3, 'satang_ledger_query_p3': 4, 'purchase_sentence_models_p3': 2}
    if key[5:] in floors:
        assert len(seen) == floors[key[5:]]
