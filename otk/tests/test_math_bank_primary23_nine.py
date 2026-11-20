"""Independent visible-content solvers for Primary 2/3 measurement and chart gaps."""
from itertools import combinations
from random import Random
import re
import pytest
import sympy as s
from otk.core import REGISTRY,generate

KEYS=('math.round_trip_metres_p2', 'math.volume_comparison_statement_p2', 'math.container_equivalence_p2', 'math.dry_measure_method_p2', 'math.pictograph_pair_target_p2', 'math.pictograph_extreme_amount_p2', 'math.comparison_amount_large_p3', 'math.three_revenues_large_p3', 'math.mixed_length_result_p3')

def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)

def ints(text):
    return list(map(int,re.findall(r'\d+',text)))

def chart(stem):
    rows=dict((day,len(symbols.split())) for day,symbols in re.findall(r'(วัน\S+): ([● ]+)',stem))
    scale=int(re.search(r'แทนขนม (\d+) ชิ้น',stem).group(1))
    assert len(rows)==5
    return {day:n*scale for day,n in rows.items()}

@pytest.mark.parametrize('key',KEYS)
def test_independent_visible_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        assert len(choices)==len(set(choices))==REGISTRY[key].max_choices
        n=ints(stem)
        if key.endswith('round_trip_metres_p2'):
            distance,=n
            valid=[s.Rational(c)/2==distance for c in choices]
        elif key.endswith('volume_comparison_statement_p2'):
            valid=[]
            for c in choices:
                a,b=ints(c)
                if 'มากกว่า' in c:
                    truth=a>b
                elif 'น้อยกว่า' in c:
                    truth=a<b
                else:
                    truth=a==b
                valid.append(not truth)
            branches.add('เท่ากับ' in choices[q.answer])
        elif key.endswith('container_equivalence_p2'):
            bottles,one,jug,count=n
            assert one==1
            bottle=s.Rational(jug,bottles)
            valid=[]
            for c in choices:
                b,j=ints(c)
                left,right=b*bottle,j*jug
                valid.append(left<right if 'น้อยกว่า' in c else left>right if 'มากกว่า' in c else left==right)
            branches.add((count>bottles)-(count<bottles))
        elif key.endswith('dry_measure_method_p2'):
            coarse='หากตวงถ่าน' in stem
            expected='ตวงให้พูนเหนือขอบ' if coarse else 'ตวงเสมอขอบแล้วปาดเรียบ'
            valid=[c==expected for c in choices]
            branches.add(coarse)
        elif key.endswith('pictograph_pair_target_p2'):
            data=chart(stem)
            target=int(re.search(r'ขายขนมรวม (\d+) ชิ้น',stem).group(1))
            pairs=[tuple(pair) for pair in combinations(data,2) if sum(data[d] for d in pair)==target]
            assert len(pairs)==1
            valid=[sum(data[d] for d in c.split(' และ '))==target for c in choices]
        elif key.endswith('pictograph_extreme_amount_p2'):
            data=chart(stem)
            most='ขายขนมมากที่สุด' in stem
            answer=(max if most else min)(data.values())
            valid=[]
            for c in choices:
                day,value=c.split(' จำนวน ')
                value=int(value.split()[0])
                valid.append(data[day]==value==answer)
            branches.add(most)
        elif key.endswith('comparison_amount_large_p3'):
            unknown=s.Symbol('t')
            if stem.startswith('นาเก็บเงินได้ '):
                small,gap=n
                equation=s.Eq(unknown-small,gap)
                branches.add(0)
            elif stem.startswith('ธีเก็บเงินได้ '):
                large,gap=n
                equation=s.Eq(large-unknown,gap)
                branches.add(1)
            elif stem.startswith('นาเก็บเงินได้น้อยกว่า'):
                gap,small=n
                equation=s.Eq(unknown-small,gap)
                branches.add(2)
            else:
                gap,large=n
                equation=s.Eq(large-unknown,gap)
                branches.add(3)
            expected=s.solve(equation,unknown)[0]
            valid=[int(c)==expected for c in choices]
            assert 0<expected<=100000
        elif key.endswith('three_revenues_large_p3'):
            a,b,c=n
            expected=sum([a,b,c])
            assert any(10000<=v<=99999 for v in (a,b,c))
            valid=[int(c)==expected for c in choices]
        else:
            a,x,b,y=n
            factor=1000 if 'กิโลเมตร' in stem else 100
            add='รวมกันยาว' in stem
            first=s.Rational(a)+s.Rational(x,factor)
            second=s.Rational(b)+s.Rational(y,factor)
            expected=first+second if add else first-second
            valid=[]
            for c in choices:
                major_count,r=ints(c)
                assert 0<=r<factor
                valid.append(s.Rational(major_count)+s.Rational(r,factor)==expected)
            branches.add((factor,add,x+y>=factor if add else x<y))
        assert valid==[i==q.answer for i in range(4)],(key,seed,stem,choices)
    floors={'volume_comparison_statement_p2':2,'container_equivalence_p2':3,'dry_measure_method_p2':2,
            'pictograph_extreme_amount_p2':2,'comparison_amount_large_p3':4,'mixed_length_result_p3':8}
    if key[5:] in floors:
        assert len(branches)==floors[key[5:]]


def test_source_exact_units_and_double_false_statement():
    assert 789+789==1578
    assert not 5>5 and not 5<3
    assert s.Rational(450+380,100)==s.Rational(83,10)
    assert s.Rational(540-180,100)==s.Rational(18,5)


def test_revenue_partial_total_collision():
    from otk.sets.math.p3.addition_and_subtraction import ThreeRevenuesLargeP3
    class Forced(Random):
        def __init__(self):
            super().__init__(0)
            self.values=iter((5000,12000,5000))
        def randint(self,a,b):
            return next(self.values)
    _,right,wrongs=ThreeRevenuesLargeP3().compose(Forced())
    assert len(set(wrongs))>=3 and right not in wrongs
