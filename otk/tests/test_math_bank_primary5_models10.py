"""Check every offered calculation by an independent inverse relation."""
from decimal import Decimal
from fractions import Fraction
from random import Random
import re

import pytest
import sympy as s

from otk.core import REGISTRY,generate

KEYS=tuple('math.'+key for key in (
    'proportion_sentence_p5','fraction_decimal_to_percent_p5','percent_expression_comparison_p5',
    'percent_part_sentence_p5','percent_remainder_sentence_p5','profit_sale_sentence_p5',
    'profit_rate_sentence_p5','original_from_discount_sentence_p5','cost_from_loss_sentence_p5',
    'double_bar_summary_p5'))


def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)


def ints(value):
    return list(map(int,re.findall(r'\d+',value)))


def evaluate(expression):
    return s.sympify(expression.replace('×','*').replace('÷','/').replace('−','-'),rational=True)


@pytest.mark.parametrize('key',KEYS)
def test_independent_visible_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        assert len(choices)==len(set(choices))==REGISTRY[key].max_choices
        if key.endswith('fraction_decimal_to_percent_p5'):
            if stem.startswith('เศษส่วน'):
                a,b=ints(stem)
                original=Fraction(a,b)
                branches.add('fraction')
            else:
                original=Fraction(re.search(r'0\.\d+',stem).group())
                branches.add('decimal')
            valid=[Fraction(Decimal(c.removesuffix('%')))/100==original for c in choices]
        elif key.endswith('percent_expression_comparison_p5'):
            amounts=[Fraction(p*n,100) for p,n in map(ints,choices)]
            want=(max if 'มากที่สุด' in stem else min)(amounts)
            valid=[value==want for value in amounts]
            assert len(set(amounts))==4
            branches.add('มากที่สุด' in stem)
        elif key.endswith('double_bar_summary_p5'):
            data=re.findall(r'(เทนนิส|ปิงปอง|ว่ายน้ำ|ฟุตบอล) \| (\d+) \| (\d+)',stem)
            assert len(data)==4
            boys={name:int(a) for name,a,b in data}
            girls={name:int(b) for name,a,b in data}
            if 'รวมมากที่สุด' in stem:
                totals={name:boys[name]+girls[name] for name in boys}
                assert len(set(totals.values()))==4
                want=sorted(totals,key=totals.get)[-1]
                valid=[c==want for c in choices]
                branches.add('maximum')
            else:
                female='ผู้สมัครหญิง' in stem
                selected=girls if female else boys
                # Visit each category in a different order, then count individual people.
                want=len([1 for name in sorted(selected) for _ in range(selected[name])])
                valid=[int(c)==want for c in choices]
                branches.add('female' if female else 'male')
        else:
            values=[evaluate(c) for c in choices]
            assert len(set(values))==4, (stem,choices,values)
            data=ints(stem)
            if key.endswith('proportion_sentence_p5'):
                n,total,target=data
                if stem.startswith('สมุด'):
                    valid=[value*n==total*target for value in values]
                    branches.add('price')
                else:
                    valid=[value*total==target*n for value in values]
                    branches.add('workers')
            elif key.endswith('percent_part_sentence_p5'):
                if stem.startswith('ร้อยละ'):
                    percent,total=data
                    branches.add('quantity')
                else:
                    total,percent=data
                    branches.add('discount')
                valid=[value*100==total*percent for value in values]
            elif key.endswith('percent_remainder_sentence_p5'):
                whole,known=data
                if stem.startswith('ผลไม้'):
                    valid=[value*whole/100+known==whole for value in values]
                    branches.add('percent')
                else:
                    valid=[value+whole*s.Rational(known,100)==whole for value in values]
                    branches.add('amount')
            elif key.endswith('profit_sale_sentence_p5'):
                cost,percent=data
                valid=[(value-cost)*100==percent*cost for value in values]
            elif key.endswith('profit_rate_sentence_p5'):
                cost,sale=data
                valid=[cost*(1+value/100)==sale for value in values]
            elif key.endswith('original_from_discount_sentence_p5'):
                discount,percent=data
                valid=[value*percent/100==discount for value in values]
            else:
                sale,loss=data
                valid=[value*(1-s.Rational(loss,100))==sale for value in values]
        assert valid==[i==q.answer for i in range(4)],(key,seed,stem,choices)
    floors={'proportion_sentence_p5':2,'fraction_decimal_to_percent_p5':2,
            'percent_expression_comparison_p5':2,'percent_part_sentence_p5':2,
            'percent_remainder_sentence_p5':2,'double_bar_summary_p5':3}
    if key[5:] in floors:
        assert len(branches)==floors[key[5:]]


def test_source_loss_model_preserves_noninteger_cost():
    # The source's answer is an expression. No currency rounding is requested.
    cost=s.Rational(3540000,89)
    assert cost*s.Rational(89,100)==35400
    assert evaluate('(100 ÷ (100 − 11)) × 35400')==cost
    assert cost.q==89



def test_chart_equal_series_totals_and_constant_selected_counts():
    class EqualTotals(Random):
        def __init__(self):
            super().__init__(0)
            self.counts=iter((20,20,20,20,17,19,21,23))

        def randint(self,a,b):
            value=next(self.counts)
            assert a<=value<=b
            return value

        def choice(self,seq):
            return False  # Sum the male series, rather than choose a category.

    stem,answer,wrongs=REGISTRY['math.double_bar_summary_p5'].compose(EqualTotals())
    assert 'ผู้สมัครชายทั้งหมด' in stem and answer=='80'
    assert len(set(wrongs))>=REGISTRY['math.double_bar_summary_p5'].max_choices-1
    assert set(wrongs)=={'160','20','40'}
    assert answer not in wrongs
