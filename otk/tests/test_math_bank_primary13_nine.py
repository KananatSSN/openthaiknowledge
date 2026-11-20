"""Independent sequence, canonical-digit, equation and unit checks for Primary 1/3."""
from random import Random
import re
import pytest
import sympy as s
from otk.core import REGISTRY,generate

KEYS=('math.unit_step_sequence_choice_p1', 'math.single_attribute_pattern_p1', 'math.digit_place_value_pair_p3', 'math.canonical_expansion_p3', 'math.expanded_comparison_statement_p3', 'math.order_large_sequence_p3', 'math.bracket_missing_number_p3', 'math.longer_than_reference_p3', 'math.length_estimation_error_p3')
PLACES=('หมื่น','พัน','ร้อย','สิบ','หน่วย')

def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)

def ints(value):
    return list(map(int,re.findall(r'\d+',value)))

def expression(value):
    return s.sympify(value.replace('−','-'))

@pytest.mark.parametrize('key',KEYS)
def test_independent_visible_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        assert len(choices)==len(set(choices))==REGISTRY[key].max_choices
        n=ints(stem)
        if key.endswith('unit_step_sequence_choice_p1'):
            step=1 if 'เพิ่มขึ้น' in stem else -1
            valid=[]
            for c in choices:
                row=ints(c)
                assert len(row)==4 and all(0<=v<=100 for v in row)
                valid.append(all(b-a==step for a,b in zip(row,row[1:])))
            branches.add(step)
        elif key.endswith('single_attribute_pattern_p1'):
            name=re.search(r'เปลี่ยนเฉพาะ(รูปร่าง|สี|ขนาด)',stem).group(1)
            target=('รูปร่าง','สี','ขนาด').index(name)
            valid=[]
            for c in choices:
                objects=[tuple(part.strip().split('/')) for part in c.split('→')]
                changed={i for i in range(3) if len({obj[i] for obj in objects})>1}
                valid.append(changed=={target})
            branches.add(target)
        elif key.endswith('digit_place_value_pair_p3'):
            number,digit=n
            position=str(number).index(str(digit))
            expected=(PLACES[position],digit*10**(4-position))
            valid=[]
            for c in choices:
                place,value=re.fullmatch(r'อยู่ในหลัก(\S+) มีค่า (\d+)',c).groups()
                valid.append((place,int(value))==expected)
            branches.add(('zero',digit==0))
            branches.add(('place',position))
        elif key.endswith('canonical_expansion_p3'):
            number,=n
            # Canonical decomposition: exactly one nonzero single-digit coefficient per place.
            expected=[int(d+'0'*(len(str(number))-i-1)) for i,d in enumerate(str(number)) if d!='0']
            valid=[sum(ints(c))==number and sorted(ints(c))==sorted(expected) for c in choices]
            assert sum(v==number for v in map(expression,choices))==3
            branches.add('0' in str(number))
        elif key.endswith('expanded_comparison_statement_p3'):
            valid=[]
            for c in choices:
                left,rel,right=re.fullmatch(r'(\d+) ([<>=≠]) (.+)',c).groups()
                a,b=int(left),expression(right)
                valid.append({'<':a<b,'>':a>b,'=':a==b,'≠':a!=b}[rel])
            branches.add(re.search(r' ([<>=≠]) ',choices[q.answer]).group(1))
        elif key.endswith('order_large_sequence_p3'):
            descending='มากไปน้อย' in stem
            values=n
            assert len(values)==len(set(values))==4
            valid=[]
            for c in choices:
                row=ints(c)
                assert sorted(row)==sorted(values)
                valid.append(row==sorted(values,reverse=descending))
            branches.add(descending)
        elif key.endswith('bracket_missing_number_p3'):
            equation=stem.split('ประโยค ',1)[1].replace('□','x')
            lhs,rhs=equation.split('=')
            x=s.Symbol('x')
            answer=s.solve(s.Eq(expression(lhs),expression(rhs)),x)[0]
            valid=[int(c)==answer for c in choices]
            branches.add(re.sub(r'\d+','n',equation))
        elif key.endswith('longer_than_reference_p3'):
            cm,=n
            values=[ints(c)[0] for c in choices]
            assert len(set(values))==4 and sum(v==cm*10 for v in values)==1
            valid=[s.Rational(v,10)>cm for v in values]
        else:
            estimate,m,cm=n
            expected=abs(s.Rational(estimate)-s.Rational(m)-s.Rational(cm,100))
            valid=[]
            for c in choices:
                metres,centimetres=ints(c)
                assert 0<=centimetres<100
                valid.append(s.Rational(metres)+s.Rational(centimetres,100)==expected)
            branches.add((estimate*100>m*100+cm,expected>=1))
        assert valid==[i==q.answer for i in range(4)],(key,seed,stem,choices)
    floors={'unit_step_sequence_choice_p1':2,'single_attribute_pattern_p1':3,'digit_place_value_pair_p3':7,
            'canonical_expansion_p3':2,'expanded_comparison_statement_p3':4,'order_large_sequence_p3':2,
            'bracket_missing_number_p3':3,'length_estimation_error_p3':4}
    if key[5:] in floors:
        assert len(branches)==floors[key[5:]]


def test_one_centimetre_borrow_collision():
    from otk.sets.math.p3.measurement import LengthEstimationErrorP3
    class Forced(Random):
        def randint(self,a,b):
            return 10
        def choice(self,values):
            return -1
    _,right,wrongs=LengthEstimationErrorP3().compose(Forced())
    assert right=='0 เมตร 1 เซนติเมตร'
    assert len(set(wrongs))>=3 and right not in wrongs


def test_source_ambiguities_and_bounds():
    assert 50405>50000+200+5 and 50405!=50000+200+5
    assert 80000+2000+900+10+6==80000+2000+900+16==82000+900+10+6
    x=s.Symbol('x')
    assert s.solve(s.Eq(20000+(2500-x),21300),x)==[1200]
    assert abs(1100-(1000+25))==75
