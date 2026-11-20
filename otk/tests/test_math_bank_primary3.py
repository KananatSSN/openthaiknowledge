"""Independently reconstruct new money/story answers from visible content."""
from decimal import Decimal
from fractions import Fraction
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.half_then_daily_budget_p3', 'math.resale_profit_unit_price_p3',
        'math.unit_price_from_balance_p3', 'math.buy_several_satang_p3')


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def ints(s):
    return [int(n) for n in re.findall(r'\d+', s)]


@pytest.mark.parametrize('key', KEYS)
def test_independent_visible_answers(key):
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = content(q.stem)
        choices = [content(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        answer = choices[q.answer]
        values = ints(stem)
        if key.endswith('half_then_daily_budget_p3'):
            start, days = values
            daily = int(answer)
            # Inverse check: reconstruct all spending and the identical gift.
            spent = sum([daily] * days)
            assert spent + spent == start
        elif key.endswith('resale_profit_unit_price_p3'):
            count, cost, profit = values
            candidates = [price for price in range(1, 1000)
                          if sum([price] * count) - cost == profit]
            assert candidates == [int(answer)]
        elif key.endswith('unit_price_from_balance_p3'):
            start, count, left = values
            spent = sum([int(answer)] * count)
            assert spent + left == start
            assert Fraction(start - left, count).denominator == 1
        else:
            count, baht, satang = values
            # Decimal currency addition, independent of integer-satang product.
            unit = Decimal(baht) + Decimal(satang) / 100
            total = sum([unit] * count, Decimal(0))
            a, b = ints(answer)
            assert Decimal(a) + Decimal(b) / 100 == total
            assert all(0 <= ints(choice)[1] < 100 for choice in choices)


def test_money_carry_to_whole_baht_is_present():
    seen = set()
    for seed in range(300):
        q = generate('math.buy_several_satang_p3', Random(seed))
        seen.add(ints(content(q.choices[q.answer].content))[1])
    assert seen == {0, 25, 50, 75}


def test_source_inverse_and_exact_money_values():
    assert 450 * 7 * 2 == 6300
    assert Decimal('425.25') * 3 == Decimal('1275.75')
    assert 889 * 3 - 2167 == 500
    assert 240 * 7 + 2320 == 4000
    assert 2862 // 9 * 12 == 3816
    assert 970 + 650 + 380 == 1000 * 2
    assert 40 * 4 == 20 * 8


def test_profit_inputs_can_have_remainders_before_combining():
    seen = False
    for seed in range(300):
        q = generate('math.resale_profit_unit_price_p3', Random(seed))
        count, cost, profit = ints(content(q.stem))
        if cost % count and profit % count:
            answer = int(content(q.choices[q.answer].content))
            assert cost // count + profit // count == answer - 1
            assert Fraction(cost, count) + Fraction(profit, count) == answer
            seen = True
    assert seen
