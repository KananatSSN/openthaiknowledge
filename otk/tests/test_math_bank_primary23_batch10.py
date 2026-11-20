"""Independent equation, schedule and exact-unit solvers for the Primary 2/3 batch."""
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from random import Random
import re

import pytest
import sympy as s

from otk.core import REGISTRY,generate

KEYS=tuple('math.'+key for key in (
    'match_three_digit_sum_p2','balance_three_digit_sums_p2',
    'match_three_digit_difference_p2','balance_three_digit_differences_p2',
    'activity_time_lookup_p3','weight_comparison_statement_p3','weight_estimation_error_p3',
    'capacity_comparison_statement_p3','capacity_estimation_error_p3','share_decimal_litres_p3'))


def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)


def ints(value):
    return list(map(int,re.findall(r'\d+',value)))


def weight(label):
    if 'กิโลกรัม' in label:
        kg,grams=ints(label)
        return sum([1000]*kg)+grams
    grams,=ints(label)
    return grams


@pytest.mark.parametrize('key',KEYS)
def test_independent_visible_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        assert len(choices)==len(set(choices))==REGISTRY[key].max_choices
        if key.endswith(('match_three_digit_sum_p2','match_three_digit_difference_p2')):
            target,=ints(stem)
            values=[s.sympify(c.replace('−','-')) for c in choices]
            valid=[value==target for value in values]
            assert len(set(values))==4
            assert all(100<=n<=999 for c in choices for n in ints(c))
        elif key.endswith('balance_three_digit_sums_p2'):
            a,b,c=ints(stem)
            x=s.Symbol('x')
            answer=s.solve(s.Eq(a+b,x+c),x)[0]
            valid=[int(choice)==answer for choice in choices]
            assert 100<=a<=999 and 100<=b<=999 and a+b<=1000
        elif key.endswith('balance_three_digit_differences_p2'):
            a,b,c=ints(stem)
            x=s.Symbol('x')
            answer=s.solve(s.Eq(a-b,c-x),x)[0]
            valid=[int(choice)==answer for choice in choices]
            assert all(100<=n<=999 for n in (a,b,c))
        elif key.endswith('activity_time_lookup_p3'):
            rows=re.findall(r'(ตื่นนอน|ช่วยงานบ้าน|ดูโทรทัศน์|ทำการบ้าน|เข้านอน) \| (\d{2}\.\d{2}) น\.',stem)
            assert len(rows)==len(set(t for _,t in rows))==5
            target=re.search(r'เริ่มกิจกรรม(\S+)เวลาใด',stem).group(1)
            shown=next(t for activity,t in rows if activity==target)
            expected=datetime.strptime(shown,'%H.%M').strftime('%H.%M น.')
            valid=[choice==expected for choice in choices]
            branches.add(target)
        elif key.endswith('weight_comparison_statement_p3'):
            kg,khit,second=ints(stem)
            masses={'เป็ด':sum([1000]*kg+[100]*khit),'ปลา':second}
            valid=[]
            for choice in choices:
                large,small,gap=re.fullmatch(r'(เป็ด|ปลา)หนักกว่า(เป็ด|ปลา) (\d+) กรัม',choice).groups()
                valid.append(masses[large]-masses[small]==int(gap)>0)
            branches.add(masses['เป็ด']>masses['ปลา'])
        elif key.endswith('weight_estimation_error_p3'):
            kg,khit,actual_kg,actual_g=ints(stem)
            estimate=Fraction(kg)+Fraction(khit,10)
            actual=Fraction(actual_kg)+Fraction(actual_g,1000)
            error=abs(estimate-actual)*1000
            valid=[weight(choice)==error for choice in choices]
            answer=choices[q.answer]
            if 'กิโลกรัม' in answer:
                _,g=ints(answer)
                assert 0<=g<1000
            branches.add((estimate>actual,'กิโลกรัม' in answer))
        elif key.endswith('capacity_comparison_statement_p3'):
            a,b=map(Decimal,re.findall(r'(\d+\.\d+) ลิตร',stem))
            capacities={'ถังน้ำ':a,'กระป๋อง':b}
            valid=[]
            for choice in choices:
                large,small,gap=re.fullmatch(r'(ถังน้ำ|กระป๋อง)จุได้มากกว่า(ถังน้ำ|กระป๋อง) (\d+\.\d+) ลิตร',choice).groups()
                valid.append(capacities[large]-capacities[small]==Decimal(gap)>0)
            branches.add(a>b)
        elif key.endswith('capacity_estimation_error_p3'):
            a,b=map(Decimal,re.findall(r'(\d+\.\d+) ลิตร',stem))
            error=abs(a-b)*1000
            valid=[int(choice)==error for choice in choices]
            branches.add(a>b)
        else:
            amount=Decimal(re.search(r'(\d+\.\d+) ลิตร',stem).group(1))
            cups=int(re.search(r'แก้ว (\d+) ใบ',stem).group(1))
            valid=[sum([Decimal(choice)]*cups)==amount*1000 for choice in choices]
            branches.add(amount==int(amount))
        assert valid==[i==q.answer for i in range(4)],(key,seed,stem,choices)
    floors={'activity_time_lookup_p3':5,'weight_comparison_statement_p3':2,
            'weight_estimation_error_p3':4,'capacity_comparison_statement_p3':2,
            'capacity_estimation_error_p3':2,'share_decimal_litres_p3':2}
    if key[5:] in floors:
        assert len(branches)==floors[key[5:]]


def test_source_mixed_unit_values():
    assert abs(Fraction(56)-Fraction(48300,1000))*1000==7700
    assert abs(Fraction(25,10)-Fraction(18,10))*1000==700
    assert abs(Decimal('3')-Decimal('2.8'))*1000==200
    assert Decimal('1.25')*1000/5==250
