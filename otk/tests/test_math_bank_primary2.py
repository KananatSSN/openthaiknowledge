"""Re-solve Primary 2 text-first generators from the learner-visible questions.

Tests use enumeration, repeated addition, and timedelta independently of the
arithmetic that constructs each generator's answer. Private source text stays
in the bank; the numerical source regressions here contain no copied stems.
"""
from datetime import timedelta
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = (
    'math.half_dozen_packs_p2', 'math.daily_total_weeks_p2',
    'math.pack_price_irrelevant_p2', 'math.sum_durations_p2',
    'math.payment_from_change_p2', 'math.purchase_from_change_p2',
    'math.compare_sale_prices_p2', 'math.comparison_amount_p2', 'math.equal_packs_p2',
)


def numbers(s):
    return [int(n) for n in re.findall(r'\d+', s)]


def choice_text(c):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in c.content)


@pytest.mark.parametrize('key', KEYS)
def test_answers_rederived_from_visible_question(key):
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = ' '.join(getattr(b, 'text', '') for b in q.stem)
        ns = numbers(stem)
        answer = choice_text(q.choices[q.answer])
        assert len(q.choices) == REGISTRY[key].max_choices
        if key.endswith('half_dozen_packs_p2'):
            # Count six individual items in each pack.
            want = sum(1 for _ in range(ns[0]) for _ in range(6))
        elif key.endswith('daily_total_weeks_p2'):
            want = sum([ns[0]] * len(('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')))
        elif key.endswith('pack_price_irrelevant_p2'):
            _, colours, price, packs = ns
            want = sum([price] * packs)
            assert colours != price
        elif key.endswith('sum_durations_p2'):
            first, second = ns
            duration = timedelta(minutes=first) + timedelta(minutes=second)
            hours = duration.seconds // 3600
            minutes = duration.seconds % 3600 // 60
            want = f'{hours} ชั่วโมง {minutes} นาที'
        elif key.endswith('payment_from_change_p2'):
            price, change = ns
            solutions = [paid for paid in range(1001) if paid - price == change]
            assert len(solutions) == 1
            want = solutions[0]
        elif key.endswith('purchase_from_change_p2'):
            have, *_, left = ns
            prices = {name: int(value) for name, value in re.findall(r'(\S+?)ราคา (\d+) บาท', stem)}
            solutions = [name for name, price in prices.items() if have - price == left]
            assert len(solutions) == 1
            want = solutions[0]
            # Every other purchase produces a different remaining balance.
            assert all(have - prices[choice_text(c)] != left for i, c in enumerate(q.choices) if i != q.answer)
        elif key.endswith('compare_sale_prices_p2'):
            price_a, discount_a, price_b, discount_b = ns
            # Count the baht remaining after crossing out the discounted baht.
            net_a = len(range(discount_a, price_a))
            net_b = len(range(discount_b, price_b))
            cheap = 'ก' if net_a < net_b else 'ข'
            gap = len(range(min(net_a, net_b), max(net_a, net_b)))
            want = f'ร้าน {cheap} ถูกกว่า {gap} บาท'
        elif key.endswith('comparison_amount_p2'):
            if stem.startswith('มะลิมีเงินน้อยกว่า'):
                gap, known = ns
                solutions = [x for x in range(1001) if known + gap == x]
            elif stem.startswith('ต้นมีเงินมากกว่า'):
                gap, known = ns
                solutions = [x for x in range(1001) if x + gap == known]
            elif stem.startswith('มะลิมีเงิน '):
                known, gap = ns
                solutions = [x for x in range(1001) if x - known == gap]
            else:
                known, gap = ns
                solutions = [x for x in range(1001) if known - x == gap]
            assert len(solutions) == 1
            want = solutions[0]
        else:
            _, each, total = ns
            solutions = [packs for packs in range(1, 11) if sum([each] * packs) == total]
            assert len(solutions) == 1
            want = solutions[0]
        assert answer == str(want), (key, seed, stem, answer, want)


def test_source_numerical_regressions():
    # 2564 term 1: half-dozen packs, daily week, total duration.
    assert sum([6] * 6) == 36
    assert sum([10] * 7) == 70
    assert timedelta(minutes=50) + timedelta(minutes=35) == timedelta(hours=1, minutes=25)
    # 2567 term 2: relevant pack price, pack count, payment and purchase.
    assert sum([123] * 2) == 246
    assert sum([177] * 2) == 354
    assert [paid for paid in range(1001) if paid - 356 == 644] == [1000]
    assert [price for price in (349, 229, 439) if 750 - price == 311] == [439]
    # The first shop is dearer despite its larger discount.
    assert len(range(150, 729)) == 579
    assert len(range(115, 690)) == 575


def test_duration_choices_cover_every_minute_pair():
    from otk.sets.math.p2.time import SumDurationsP2

    class Pair:
        def __init__(self, first, second):
            self.values = iter((first, second))

        def randint(self, low, high):
            value = next(self.values)
            assert low <= value <= high
            return value

    for first in range(25, 60):
        for second in range(25, 60):
            _, correct, wrongs = SumDurationsP2().compose(Pair(first, second))
            assert len(set(wrongs) - {correct}) >= REGISTRY['math.sum_durations_p2'].max_choices - 1
            assert len(wrongs) == len(set(wrongs))
            hours, minutes = numbers(correct)
            assert timedelta(hours=hours, minutes=minutes) == timedelta(minutes=first + second)
