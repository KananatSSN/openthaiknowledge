"""Primary 5 bank additions, independently checked from learner-visible data."""
from fractions import Fraction as F
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.quadrilateral_repetition_p5', 'math.related_quad_dimensions_p5',
        'math.parallelogram_land_area_p5', 'math.square_area_from_perimeter_p5',
        'math.percent_pass_table_p5', 'math.monthly_savings_bonus_p5',
        'math.percent_share_difference_p5', 'math.percent_remainder_share_p5',
        'math.fractional_unit_price_p5', 'math.proportional_reward_difference_p5')


def text_of(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def numbers(s):
    return [F(n) for n in re.findall(r'\d+(?:\.\d+)?', s)]


def numeric(s):
    return F(s.replace('{,}', '').replace(',', ''))


def polygon_area(points):
    loop = points + points[:1]
    return abs(sum(x * v - y * u for (x, y), (u, v) in zip(loop, loop[1:]))) / 2


def sheared_area(base, height):
    return polygon_area([(0, 0), (base, 0), (base + 1, height), (1, height)])


@pytest.mark.parametrize('key', KEYS)
def test_answers_from_visible_data(key):
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = text_of(q.stem)
        choices = [text_of(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        ns = numbers(stem)
        if key.endswith('percent_pass_table_p5'):
            full, percent = ns[:2]
            scores = {name: int(score) for name, score in re.findall(r'([กขคงจ]): (\d+) คะแนน', stem)}
            assert len(scores) == 5
            wanted = {name for name, score in scores.items() if F(score, full) >= percent / 100}
            at_boundary = {name for name, score in scores.items() if 100 * score == percent * full}
            assert at_boundary and at_boundary <= wanted
            assert [set(c.split(' และ ')) == wanted for c in choices] == [i == q.answer for i in range(len(choices))]
            continue
        if key.endswith('fractional_unit_price_p5'):
            quantity, cost, wanted = ns
            assert [numeric(c) * quantity == cost * wanted for c in choices] == [i == q.answer for i in range(len(choices))]
            denominator = (cost / quantity).denominator
            for factor in (2, 5):
                while denominator % factor == 0:
                    denominator //= factor
            assert denominator != 1  # Unit price genuinely cannot terminate as a decimal.
            continue
        if key.endswith('percent_remainder_share_p5'):
            total, percent, groups = ns
            truths = [numeric(c) * groups * 100 + total * percent == 100 * total for c in choices]
            assert truths == [i == q.answer for i in range(len(choices))]
            continue
        if key.endswith('proportional_reward_difference_p5'):
            points, prizes, other_points = ns
            truths = [(prizes - numeric(c)) * points == prizes * other_points for c in choices]
            assert truths == [i == q.answer for i in range(len(choices))]
            continue
        answer = numeric(choices[q.answer])
        if key.endswith('quadrilateral_repetition_p5'):
            if stem.startswith('สนาม'):
                side, laps = ns
                wanted = sum([side] * (4 * int(laps)))
            elif stem.startswith('ที่ดิน'):
                a, b, layers = ns
                wanted = sum([a, b, a, b] * int(layers))
            else:
                base, height, tiles = ns
                wanted = sum([sheared_area(base, height)] * int(tiles))
        elif key.endswith('related_quad_dimensions_p5'):
            if 'ขนมเปียกปูน' in stem:
                base, numerator, denominator = ns
                height = base * numerator / denominator
                wanted = sheared_area(base, height)
            else:
                width, multiple = ns
                wanted = sum([width, width * multiple, width, width * multiple])
        elif key.endswith('parallelogram_land_area_p5'):
            base, height, one_rai, square_wa_per_rai = ns
            assert one_rai == 1
            assert answer * square_wa_per_rai == sheared_area(base, height)
            continue
        elif key.endswith('square_area_from_perimeter_p5'):
            perimeter, = ns
            solutions = [F(t, 10) for t in range(1, 1001) if sum([F(t, 10)] * 4) == perimeter]
            assert len(solutions) == 1
            side = solutions[0]
            wanted = polygon_area([(0, 0), (side, 0), (side, side), (0, side)])
        elif key.endswith('monthly_savings_bonus_p5'):
            monthly, months, percent = ns
            assert months == 12
            # Distributivity: give each equal contribution the stated final bonus,
            # then sum, rather than following the set's accumulated-balance formula.
            wanted = sum([monthly + monthly * percent / 100] * int(months))
        else:
            total, first, second = ns
            a = sum(100 * (i + 1) <= total * first for i in range(int(total)))
            b = sum(100 * (i + 1) <= total * second for i in range(int(total)))
            wanted = len(set(range(a)) ^ set(range(b)))
        assert answer == wanted, (key, seed, stem, answer, wanted)


def test_repetition_and_related_dimension_variants_all_exercised():
    repetition = set()
    related = set()
    for seed in range(100):
        stem = text_of(generate('math.quadrilateral_repetition_p5', Random(seed)).stem)
        repetition.add('laps' if stem.startswith('สนาม') else 'fence' if stem.startswith('ที่ดิน') else 'area')
        related.add('ขนมเปียกปูน' in text_of(generate('math.related_quad_dimensions_p5', Random(seed)).stem))
    assert repetition == {'laps', 'fence', 'area'}
    assert related == {True, False}


def test_source_regressions_and_early_rounding_trap():
    assert sum([F('34.7')] * 36) == F('1249.2')
    assert sum([F(19), F('25.5')] * 6) == 267
    assert sheared_area(80, 40) == 400 * 8
    assert polygon_area([(0, 0), (15, 0), (15, 15), (0, 15)]) == 225
    assert F(45, 50) >= F(90, 100)
    assert not F(44, 50) >= F(90, 100)
    assert sum([F(120) * F('1.045')] * 12) == F('1504.8')
    assert 140 * (F(45, 100) - F(25, 100)) == 28
    assert F(11200) * 20 + 320000 * F(30, 100) == 320000
    assert F('28.75') * 120 == 230 * 15
    assert F('1.92') * 15 != F('28.75')
    assert (12 - 3) * 200 == 12 * 150
