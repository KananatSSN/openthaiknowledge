"""Independent visible-content solvers for the Primary 2 / Secondary 3 batch."""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from functools import lru_cache
from math import isqrt, pi, sin
from random import Random
import re

import pytest
import sympy as s

from otk.core import REGISTRY, generate

KEYS = (
    'math.tangent_chord_angle_m3', 'math.mixed_length_statement_p2', 'math.capacity_litre_ml_comparison_p2',
    'math.system_solution_count_m3', 'math.system_basket_target_m3', 'math.two_rate_allocation_m3',
    'math.pyramid_surface_from_edge_m3', 'math.cone_volume_from_slant_m3',
    'math.hemisphere_from_sphere_area_m3', 'math.hemisphere_radius_from_volume_m3',
    'math.square_pyramid_volume_from_slant_m3', 'math.equilateral_pyramid_base_from_volume_m3',
)


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def ints(text):
    return [int(n) for n in re.findall(r'-?\d+', text)]


def rounded(value):
    value = Fraction(value)
    return (Decimal(value.numerator) / Decimal(value.denominator)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


@lru_cache(None)
def hemisphere_by_cross_sections(area_coefficient):
    radius = s.sqrt(s.Rational(area_coefficient, 4))
    z = s.Symbol('z')
    # Integrate circular cross sections through the upper hemisphere.
    return rounded(s.integrate(s.Rational(314, 100) * (radius**2 - z**2), (z, 0, radius)))


@pytest.mark.parametrize('key', KEYS)
def test_independent_visible_answers(key):
    seen = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = content(q.stem)
        choices = [content(c.content) for c in q.choices]
        answer = choices[q.answer]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        if key.endswith('tangent_chord_angle_m3'):
            angle, = ints(stem)
            # On a unit circle choose endpoints at polar angles ±angle and
            # put C at 180°. The inscribed angle is recovered by dot product.
            theta = pi * angle / 180
            from math import acos, cos
            a = (cos(theta), sin(theta))
            b = (cos(theta), -sin(theta))
            u, v = (a[0]+1,a[1]), (b[0]+1,b[1])
            norm = ((u[0]**2+u[1]**2)*(v[0]**2+v[1]**2))**0.5
            measured = acos((u[0]*v[0]+u[1]*v[1])/norm)*180/pi
            assert abs(measured-int(answer)) < 1e-8
        elif key.endswith('mixed_length_statement_p2'):
            m, cm, blue = ints(stem)
            lengths = {'ริบบิ้นสีแดง': sum([100] * m) + cm, 'ริบบิ้นสีฟ้า': blue}
            truths = []
            for choice in choices:
                left, right, gap = re.fullmatch(r'(ริบบิ้นสีแดง|ริบบิ้นสีฟ้า)ยาวกว่า(ริบบิ้นสีแดง|ริบบิ้นสีฟ้า) (\d+) เซนติเมตร', choice).groups()
                truths.append(lengths[left] - lengths[right] == int(gap) > 0)
            assert truths == [i == q.answer for i in range(4)]
        elif key.endswith('capacity_litre_ml_comparison_p2'):
            litres, ml, one, thousand = ints(stem)
            assert (one, thousand) == (1, 1000)
            red = sum([1000] * litres)
            want = 'ทั้งสองขวดจุได้เท่ากัน' if red == ml else ('ขวดสีแดงจุได้มากกว่า' if red > ml else 'ขวดสีฟ้าจุได้มากกว่า')
            assert answer == want
            seen.add(want)
        elif key.endswith('system_solution_count_m3'):
            a, b, c, d, e, f = ints(stem)
            coefficients = s.Matrix([[a,b],[d,e]])
            augmented = coefficients.row_join(s.Matrix([c,f]))
            want = 'ไม่มีคำตอบ' if coefficients.rank() != augmented.rank() else ('มีคำตอบเดียว' if coefficients.rank() == 2 else 'มีคำตอบไม่จำกัด')
            assert answer == want
            seen.add(want)
        elif key.endswith('system_basket_target_m3'):
            a,b,first,c,d,second,u,v = ints(stem)
            candidates = [(x,y) for x in range(31) for y in range(31)
                          if a*x+b*y == first and c*x+d*y == second]
            assert len(candidates) == 1
            x,y = candidates[0]
            assert int(answer) == sum([x]*u+[y]*v)
        elif key.endswith('two_rate_allocation_m3'):
            total,p,r,income = ints(stem)
            x = int(answer)
            assert 0 < x < total and p != r
            assert Fraction(x*p+(total-x)*r,100) == income
        elif key.endswith('pyramid_surface_from_edge_m3'):
            side, edge = ints(stem)
            faces = 5 if 'ฐานห้าเหลี่ยม' in stem else 4
            semiperimeter = side // 2 + edge
            squared_area = semiperimeter*(semiperimeter-side)*(semiperimeter-edge)**2
            face_area = isqrt(squared_area)
            assert face_area**2 == squared_area
            assert side / (2 * sin(pi / faces)) < edge  # real right pyramid
            want = sum([face_area] * faces) + (side**2 if faces == 4 else 0)
            assert int(answer) == want
            seen.add(faces)
        elif key.endswith('cone_volume_from_slant_m3'):
            slant, diameter = ints(stem)[:2]
            radius = s.Rational(diameter,2)
            height = s.sqrt(slant**2-radius**2)
            want = rounded(s.Rational(314,100)*radius**2*height/3)
            assert [Decimal(c)==want for c in choices] == [i==q.answer for i in range(4)]
        elif key.endswith('hemisphere_from_sphere_area_m3'):
            area = int(re.search(r'พื้นที่ผิว (\d+)π',stem)[1])
            want = hemisphere_by_cross_sections(area)
            assert [Decimal(c)==want for c in choices] == [i==q.answer for i in range(4)]
        elif key.endswith('hemisphere_radius_from_volume_m3'):
            coefficient = int(re.search(r'ปริมาตร (\d+)π',stem)[1])
            radius = int(answer)
            assert Fraction(2*radius**3,3) == coefficient
        elif key.endswith('square_pyramid_volume_from_slant_m3'):
            side, slant = ints(stem)
            heights = [h for h in range(1,200) if h*h+Fraction(side,2)**2 == slant*slant]
            assert len(heights)==1
            assert Fraction(side*side*heights[0],3) == int(answer)
        else:
            height, coefficient = map(int, re.search(r'สูง (\d+) เซนติเมตร มีปริมาตร (\d+)√3', stem).groups())
            truths = [Fraction(int(c)**2*height,12)==coefficient for c in choices]
            assert truths == [i==q.answer for i in range(4)]
    if key.endswith(('capacity_litre_ml_comparison_p2','system_solution_count_m3')):
        assert len(seen)==3
    if key.endswith('pyramid_surface_from_edge_m3'):
        assert seen=={4,5}


def test_source_solid_values_exactly():
    assert 5 * 10 * 12 // 2 == 300
    assert 36**2 + 4*36*24//2 == 3024
    assert rounded(Fraction(314,100)*6**2*8/3) == Decimal('301.44')
    assert hemisphere_by_cross_sections(64) == Decimal('133.97')
    assert Fraction(2*3**3,3)==18
    assert Fraction(6**2*4,3)==48
    assert Fraction(8**2*12,12)==64


def test_source_system_models():
    x,y=s.symbols('x y')
    assert s.solve([3*x+5*y-25,2*x+7*y-24],(x,y))=={x:5,y:2}
    assert 4*5+2*2 == 24
    assert s.solve([x+y-10000,s.Rational(7,100)*x+s.Rational(11,100)*y-940],(x,y))=={x:4000,y:6000}
