"""Independent exact systems, integer optimization and geometric cross-products."""
from fractions import Fraction
from itertools import product
from math import pi, tan
from random import Random
import re

import pytest
import sympy as s

from otk.core import REGISTRY, generate

KEYS = ('math.system_parameter_difference_m3', 'math.mixture_mass_ratio_m3', 'math.joint_worker_time_m3',
        'math.reversed_digit_system_m3', 'math.pyramid_roof_tile_count_m3', 'math.sphere_area_from_volume_m3',
        'math.hemisphere_on_cone_area_m3', 'math.sphere_volume_from_circumference_m3', 'math.pyramid_cast_mass_m3',
        'math.cone_cup_count_m3', 'math.pyramid_surface_from_height_m3')


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def rounded(value):
    return s.floor(100 * value + s.Rational(1, 2)) / 100


@pytest.mark.parametrize('key', KEYS)
def test_independent_visible_alternatives(key):
    branches = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = content(q.stem)
        choices = [content(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        if key.endswith('system_parameter_difference_m3'):
            x, y = map(int, re.search(r'คู่อันดับ \((-?\d+), (-?\d+)\)', stem).groups())
            u, c, v, d = map(int, re.search(r'ระบบ \((\d+)\)x \+ ay = (-?\d+) และ bx \+ \((\d+)\)y = (-?\d+)', stem).groups())
            a, b = s.symbols('a b')
            sol = s.solve((s.Eq(u * x + a * y, c), s.Eq(b * x + v * y, d)), (a, b))
            expected = sol[a] - sol[b]
            valid = [s.Rational(c) == expected for c in choices]
            branches.add((x > 0, y > 0))
        elif key.endswith('mixture_mass_ratio_m3'):
            low, high = map(int, re.findall(r'ราคา (\d+) บาท', stem))
            target = int(re.search(r'ราคาเฉลี่ย (\d+) บาท', stem)[1])
            valid = []
            ratios = []
            for c in choices:
                a, b = map(int, c.split(' : '))
                assert a > 0 and b > 0
                valid.append(a * low + b * high == target * (a + b))
                ratios.append(s.Rational(a, b))
            assert len(set(ratios)) == len(ratios)
            branches.add(ratios[q.answer] > 1)
        elif key.endswith('joint_worker_time_m3'):
            first, second = map(int, re.findall(r'ใน (\d+) วัน', stem))
            adult_rate, child_rate = s.symbols('u v')
            rates = s.solve((s.Eq(adult_rate + child_rate, s.Rational(1, first)),
                             s.Eq(2 * adult_rate + child_rate, s.Rational(1, second))), (adult_rate, child_rate))
            adult = 'ผู้ใหญ่คนเดียว' in stem
            expected = 1 / rates[adult_rate if adult else child_rate]
            valid = [s.Rational(c) == expected for c in choices]
            assert len({s.Rational(c) for c in choices}) == len(choices)
            branches.add((adult, expected.q == 1))
        elif key.endswith('reversed_digit_system_m3'):
            total = int(re.search(r'เท่ากับ (\d+)', stem)[1])
            delta, direction = re.search(r'เมื่อนำ (\d+) ไป(บวก|ลบ)', stem).groups()
            delta = int(delta) * (1 if direction == 'บวก' else -1)
            feasible = [10 * a + b for a, b in product(range(1, 10), repeat=2)
                        if a + b == total and 10 * a + b + delta == 10 * b + a]
            assert len(feasible) == 1
            valid = [int(c) == feasible[0] for c in choices]
            branches.add(direction)
        elif key.endswith('pyramid_roof_tile_count_m3'):
            n, side, slant, tile = map(int, re.search(r'มุมเท่า (\d+) ด้าน ด้านฐานยาว (\d+) เมตร สูงเอียงแต่ละหน้ายาว (\d+) เมตร แผ่นวัสดุหนึ่งแผ่นครอบคลุม (\d+)', stem).groups())
            apothem = side / (2 * tan(pi / n))
            assert slant > apothem  # A right regular pyramid with these dimensions exists.
            area = sum(Fraction(side * slant, 2) for _ in range(n))
            feasible = [int(c) * tile >= area and (int(c) - 1) * tile < area for c in choices]
            valid = feasible
            branches.add((n, area % tile == 0))
        elif key.endswith('sphere_area_from_volume_m3'):
            coefficient = int(re.search(r'ปริมาตร (\d+)π', stem)[1])
            r = s.real_root(s.Rational(3 * coefficient, 4), 3)
            assert r.is_Integer
            expected = rounded(4 * s.Rational(22, 7) * r * r)
            valid = [s.Rational(c) == expected for c in choices]
        elif key.endswith('hemisphere_on_cone_area_m3'):
            height = int(re.search(r'กรวยสูง (\d+)', stem)[1])
            slant = int(re.search(r'สูงเอียง (\d+)', stem)[1])
            # The radial cross-section is a right triangle. Curved hemisphere area
            # is independently integrated as 2πr times its height r.
            radius_squared = slant ** 2 - height ** 2
            assert radius_squared > 0
            expected = rounded(2 * s.Rational(314, 100) * radius_squared)
            valid = [s.Rational(c) == expected for c in choices]
        elif key.endswith('sphere_volume_from_circumference_m3'):
            circumference = s.Rational(re.search(r'ยาว ([\d.]+) เซนติเมตร', stem)[1])
            radius = s.solve(s.Eq(2 * s.Rational(314, 100) * s.Symbol('r'), circumference))[0]
            z = s.Symbol('z')
            # Integrate circular cross-sections instead of using the sphere-volume helper.
            expected = rounded(s.integrate(s.Rational(314, 100) * (radius ** 2 - z ** 2), (z, -radius, radius)))
            valid = [s.Rational(c) == expected for c in choices]
        elif key.endswith('pyramid_cast_mass_m3'):
            width, length, height, count, density = map(int, re.search(r'กว้าง (\d+) ยาว (\d+) สูง (\d+) เซนติเมตร จำนวน (\d+) อัน วัสดุทุก 1 ลูกบาศก์เซนติเมตรมีมวล (\d+) กรัม', stem).groups())
            z = s.Symbol('z')
            volume = s.integrate(width * length * (1 - z / height) ** 2, (z, 0, height))
            expected = volume * count * density / 1000
            valid = [s.Rational(c) == expected for c in choices]
        elif key.endswith('cone_cup_count_m3'):
            r, h, litres = map(int, re.search(r'รัศมี (\d+) เซนติเมตร สูง (\d+) เซนติเมตร มีไอศกรีม (\d+) ลิตร', stem).groups())
            cup = s.Rational(22, 7) * r * r * h / 3
            total = 1000 * litres
            all_items = 'ต้องบรรจุทั้งหมด' in stem
            expected = s.ceiling(total / cup) if all_items else s.floor(total / cup)
            valid = [s.Rational(c) == expected for c in choices]
            branches.add(all_items)
        else:
            side, height = map(int, re.search(r'ด้านฐาน (\d+) เซนติเมตร สูงตั้งฉาก (\d+)', stem).groups())
            half = s.Rational(side, 2)
            # Compute each face from 3D coordinates via cross-products.
            apex = s.Matrix((0, 0, height))
            corners = [s.Matrix(p) for p in ((-half, -half, 0), (half, -half, 0), (half, half, 0), (-half, half, 0))]
            lateral = sum((corners[i] - apex).cross(corners[(i + 1) % 4] - apex).norm() / 2 for i in range(4))
            expected = side ** 2 + lateral
            valid = [s.Rational(c) == expected for c in choices]
        assert sum(valid) == 1 and valid[q.answer], (key, seed, stem, choices, valid)
    floors = {'system_parameter_difference_m3': 4, 'mixture_mass_ratio_m3': 2, 'joint_worker_time_m3': 4,
              'reversed_digit_system_m3': 2, 'pyramid_roof_tile_count_m3': 8, 'cone_cup_count_m3': 2}
    assert len(branches) >= floors.get(key.removeprefix('math.'), 0)
