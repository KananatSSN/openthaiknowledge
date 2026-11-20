"""Independent visible-content solvers for the Primary 6 text-layer batch."""
from random import Random
import re
import pytest
import sympy as s
from otk.core import REGISTRY, generate

KEYS=('math.non_equivalent_ratio_p6', 'math.principal_interest_ratio_p6', 'math.calendar_percent_sentence_p6', 'math.gcd_lcm_product_model_p6', 'math.quadratic_product_pattern_p6', 'math.axial_cylinder_section_p6', 'math.box_volume_sentence_p6', 'math.cube_litres_sentence_p6', 'math.box_dimension_sentence_p6', 'math.mixed_box_cost_sentence_p6')

def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)

def ints(value):
    return list(map(int,re.findall(r'\d+',value)))

def expression(value):
    return s.sympify(value.replace('×','*').replace('÷','/').replace('−','-'))

@pytest.mark.parametrize('key',KEYS)
def test_independent_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        assert len(choices)==len(set(choices))==REGISTRY[key].max_choices
        n=ints(stem)
        if key.endswith('non_equivalent_ratio_p6'):
            a,b=n
            valid=[(lambda x,y:x*b!=y*a)(*ints(c)) for c in choices]
        elif key.endswith('principal_interest_ratio_p6'):
            percent,=n
            valid=[(lambda x,y:10000*y==100*percent*x)(*ints(c)) for c in choices]
        elif key.endswith('axial_cylinder_section_p6'):
            radius,height=n
            polygon=s.Polygon((0,0),(2*radius,0),(2*radius,height),(0,height))
            valid=[c.startswith('สี่เหลี่ยมผืนผ้า') and ints(c)==[polygon.area] for c in choices]
        else:
            values=[expression(c) for c in choices]
            assert len(set(values))==4
            if key.endswith('calendar_percent_sentence_p6'):
                days,worked=n
                valid=[v*days==worked*100 for v in values]
            elif key.endswith('gcd_lcm_product_model_p6'):
                a,b,c=n
                gcd_mode='เชือก' in stem
                branches.add(gcd_mode)
                expected=s.igcd(a,b,c) if gcd_mode else s.ilcm(a,b,c)
                valid=[v==expected for v in values]
            elif key.endswith('quadratic_product_pattern_p6'):
                step,increment,*terms=n
                assert increment==step
                x=s.Symbol('x',positive=True)
                root=s.solve(s.Eq(x*(x+step),terms[-1]),x)[0]
                valid=[v==(root+step)*(root+2*step) for v in values]
            elif key.endswith('box_volume_sentence_p6'):
                a,b,c=n
                valid=[v==s.prod([a,b,c]) for v in values]
            elif key.endswith('cube_litres_sentence_p6'):
                side,=n
                valid=[v*1000==(side*100)**3 for v in values]
            elif key.endswith('box_dimension_sentence_p6'):
                volume,length,other=n
                mixed='ลูกบาศก์เซนติเมตร' in stem
                branches.add(mixed)
                valid=[v*length*other*(100 if mixed else 1)==volume for v in values]
            else:
                width,length,thick,price=n
                valid=[v*10000==width*length*thick*price for v in values]
        assert valid==[i==q.answer for i in range(4)],(key,seed,stem,choices)
    if key.endswith(('gcd_lcm_product_model_p6','box_dimension_sentence_p6')):
        assert branches=={False,True}


def test_box_distractor_coincidence():
    from otk.sets.math.p6.volume_and_surface_area import BoxVolumeSentenceP6
    class Forced(Random):
        def sample(self,population,k):
            return [6,10,4]
    _,right,wrongs=BoxVolumeSentenceP6().compose(Forced())
    assert len(set(map(expression,wrongs)))>=3
    assert expression(right) not in map(expression,wrongs)


def test_source_exact_units():
    assert s.Rational(84000,500*120)==s.Rational(7,5)
    assert s.Rational(120,100)*2*s.Rational(300,100)*500==3600
    assert s.Rational(235*100,120)==s.Rational(1175,6)
    assert s.Rational(8700*100,85)==s.Rational(174000,17)
