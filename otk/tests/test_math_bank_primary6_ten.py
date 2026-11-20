"""Independent rational models, capacity bounds and exposed-edge counts."""
from fractions import Fraction
from itertools import product
from random import Random
import re

import pytest
import sympy as s

from otk.core import REGISTRY, generate

KEYS = ('math.mixed_remaining_model_p6', 'math.two_fraction_purchases_model_p6',
        'math.fraction_order_statement_p6', 'math.decimal_operation_model_p6',
        'math.decimal_division_story_p6', 'math.ribbon_sale_model_p6', 'math.decimal_bag_count_p6',
        'math.multiple_cube_volume_p6', 'math.cuboid_capacity_extreme_p6', 'math.square_grid_perimeter_p6')


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def mixed(label):
    parts = label.strip().split()
    return sum(map(Fraction, parts))


def expr(label):
    return s.sympify(label.replace('−', '-').replace('×', '*').replace('÷', '/'), rational=True, locals={k: s.Symbol(k) for k in 'LNEP'})


@pytest.mark.parametrize('key', KEYS)
def test_independent_visible_choices(key):
    branches = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = content(q.stem)
        choices = [content(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        if key.endswith('mixed_remaining_model_p6'):
            amounts = [mixed(v) for v in re.findall(r'([\d/ ]+) เมตร', stem)]
            assert len(amounts) == 3
            total, a, b = amounts
            # Inverse conservation: the requested amount plus both known uses equals the total.
            valid = [expr(c) + s.Rational(a) + s.Rational(b) == s.Rational(total) for c in choices]
            assert len({expr(c) for c in choices}) == len(choices)
            branches.add('ต้องการผ้า' in stem)
        elif key.endswith('two_fraction_purchases_model_p6'):
            weights = [mixed(v) for v in re.findall(r'([\d/ ]+) กิโลกรัม', stem)]
            prices = list(map(int, re.findall(r'กิโลกรัมละ (\d+) บาท', stem)))
            assert len(weights) == len(prices) == 2
            # Price per fractional kilogram is computed by whole-number numerator costs / denominator.
            expected = sum(s.Rational(w.numerator * p, w.denominator) for w, p in zip(weights, prices))
            valid = [expr(c) == expected for c in choices]
            assert len({expr(c) for c in choices}) == len(choices)
        elif key.endswith('fraction_order_statement_p6'):
            asc = 'จากน้อยไปมาก' in stem
            valid = []
            for c in choices:
                values = [mixed(x) for x in c.split(' , ')]
                assert len(values) == len(set(values)) == 3
                # Cross-products check each adjacent rational pair, rather than sorting generator values.
                signs = [a.numerator * b.denominator < b.numerator * a.denominator for a, b in zip(values, values[1:])]
                valid.append(all(signs) if asc else not any(signs))
            branches.add(asc)
        elif key.endswith('decimal_operation_model_p6'):
            numbers = [s.Rational(x) for x in re.findall(r'\d+(?:\.\d+)?', stem)]
            assert len(numbers) == 2
            a, b = numbers
            if 'ดอกเบี้ย' in stem:
                expected, mode = a + b, '+'
            elif 'ริบบิ้น' in stem:
                expected, mode = a - b, '-'
            elif 'ราคากิโลกรัมละ' in stem:
                expected, mode = a * b, '*'
            else:
                # Stem lists mass then payment; preserve semantic roles independently of choice order.
                expected, mode = b / a, '/'
            valid = [expr(c) == expected for c in choices]
            assert len({expr(c) for c in choices}) == len(choices)
            branches.add(mode)
        elif key.endswith('decimal_division_story_p6'):
            valid = []
            for c in choices:
                # Identify what is unknown from the story: per-person or per-item amount.
                division = 'ได้คนละ' in c or 'ของราคาชิ้นละกี่บาท' in c
                valid.append(division)
            branches.add('แบ่งให้' in choices[q.answer])
        elif key.endswith('ribbon_sale_model_p6'):
            length, count, each, price = [s.Rational(v) for v in re.findall(r'[LNEP]=([\d.]+)', stem)]
            assert length == count * each
            per_piece = 'บาทต่อเส้น' in stem
            amount = count if per_piece else length
            symbols = {s.Symbol(k): v for k, v in zip(('L', 'N', 'E', 'P'), (length, count, each, price))}
            values = [expr(c).subs(symbols) for c in choices]
            valid = [v / price == amount for v in values]
            assert len(set(values)) == len(values)
            branches.add(per_piece)
        elif key.endswith('decimal_bag_count_p6'):
            total, bag = map(s.Rational, re.findall(r'([\d.]+) กิโลกรัม', stem))
            all_items = 'ต้องบรรจุทั้งหมด' in stem
            feasible = [n for n in range(100) if n * bag >= total] if all_items else [n for n in range(100) if n * bag <= total]
            answer = (min if all_items else max)(feasible)
            valid = [s.Rational(c) == answer for c in choices]
            assert total % bag != 0
            branches.add((all_items, bag))
        elif key.endswith('multiple_cube_volume_p6'):
            side, count = map(int, re.findall(r'\d+', stem))
            answer = count * sum(1 for _ in product(range(side), repeat=3))
            valid = [int(c) == answer for c in choices]
        elif key.endswith('cuboid_capacity_extreme_p6'):
            rows = re.findall(r'(ถัง[กขคง]): กว้าง (\d+) ยาว (\d+) สูง ([\d.]+) เมตร', stem)
            assert len(rows) == 4
            volumes = {name: s.Rational(w) * s.Rational(length) * s.Rational(h) for name, w, length, h in rows}
            assert len(set(volumes.values())) == 4
            maximum = 'มากที่สุด' in stem
            answer = (max if maximum else min)(volumes, key=volumes.get)
            valid = [c == answer for c in choices]
            assert set(choices) == set(volumes)
            branches.add((maximum, answer))
        else:
            unit = int(re.search(r'ด้านละ (\d+) หน่วย', stem)[1])
            nth = int(re.findall(r'รูปที่ (\d+)', stem)[-1])
            # Count edges of actual unit cells that have no neighbouring tile.
            cells = set(product(range(nth), repeat=2))
            exposed = sum((x + dx, y + dy) not in cells for x, y in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            answer = exposed * unit
            valid = [int(c) == answer for c in choices]
            branches.add(unit)
        assert sum(valid) == 1 and valid[q.answer], (key, seed, stem, choices, valid)
    floors = {'mixed_remaining_model_p6': 2, 'fraction_order_statement_p6': 2, 'decimal_operation_model_p6': 4,
              'decimal_division_story_p6': 2, 'ribbon_sale_model_p6': 2, 'decimal_bag_count_p6': 12,
              'cuboid_capacity_extreme_p6': 8, 'square_grid_perimeter_p6': 4}
    assert len(branches) >= floors.get(key.removeprefix('math.'), 0)
