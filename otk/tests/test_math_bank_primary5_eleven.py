"""Independent rational-expression and unit solvers for the Primary 5 batch."""
from collections import Counter
from decimal import Decimal
from fractions import Fraction
from random import Random
import re
import pytest
import sympy as s
from otk.core import REGISTRY,generate

KEYS=('math.decimal_three_place_addsub_p5', 'math.decimal_bracket_calculation_p5', 'math.decimal_round_expression_p5', 'math.fraction_comparison_statement_p5', 'math.fraction_expression_extreme_p5', 'math.fraction_story_sentence_p5', 'math.fraction_discount_sentence_p5', 'math.length_equivalence_statement_p5', 'math.odd_length_equivalence_p5', 'math.length_rate_sentence_p5', 'math.khit_cost_sentence_p5')
FACTORS={'กิโลเมตร':s.Rational(1000),'เมตร':s.Rational(1),'เซนติเมตร':s.Rational(1,100),'มิลลิเมตร':s.Rational(1,1000)}

def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)

def expr(value):
    value=re.sub(r'(\d+) (\d+)/(\d+)',r'(\1+\2/\3)',value)
    return s.sympify(value.replace('×','*').replace('÷','/').replace('−','-'),rational=True)

def rational_round(value,places):
    # Locate adjacent decimals and compare distances, choosing upper on a tie.
    scale=10**places
    lower=s.floor(value*scale)
    upper=lower+1
    return s.Rational(upper if upper-value*scale<=value*scale-lower else lower,scale)

@pytest.mark.parametrize('key',KEYS)
def test_independent_visible_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        assert len(choices)==len(set(choices))==REGISTRY[key].max_choices
        if key.endswith('decimal_three_place_addsub_p5'):
            shown=stem.removeprefix('จงหาค่าของ ')
            expected=expr(shown)
            valid=[expr(c)==expected for c in choices]
            branches.add('+' in shown)
        elif key.endswith('decimal_bracket_calculation_p5'):
            shown=stem.removeprefix('จงหาค่าของ ').split(' ตอบเป็น',1)[0]
            expected=expr(shown)
            valid=[expr(c)==expected for c in choices]
            # Distinguish every bracket/operator layout from the visible expression.
            shape=re.sub(r'\d+(?:\.\d+)?','n',shown)
            branches.add(shape)
        elif key.endswith('decimal_round_expression_p5'):
            shown=stem.removeprefix('จงหาค่าของ ').split(' แล้วปัด',1)[0]
            places=int(re.search(r'ทศนิยม (\d+) ตำแหน่ง',stem).group(1))
            expected=rational_round(expr(shown),places)
            valid=[expr(c)==expected for c in choices]
            assert all(len(c.split('.')[1])==places for c in choices)
            branches.add(places)
        elif key.endswith('fraction_comparison_statement_p5'):
            valid=[]
            for c in choices:
                left,relation,right=re.fullmatch(r'(.+) ([<>=≠]) (.+)',c).groups()
                a,b=expr(left),expr(right)
                valid.append({'<':a<b,'>':a>b,'=':a==b,'≠':a!=b}[relation])
            branches.add(re.search(r' ([<>=≠]) ',choices[q.answer]).group(1))
        elif key.endswith('fraction_expression_extreme_p5'):
            values=list(map(expr,choices))
            most='มากที่สุด' in stem
            expected=(max if most else min)(values)
            valid=[v==expected for v in values]
            assert len(set(values))==4
            branches.add(most)
        elif key.endswith('fraction_story_sentence_p5'):
            values=list(map(expr,choices))
            if stem.startswith('มีเงิน'):
                whole,fraction=re.fullmatch(r'มีเงิน (\S+) บาท เก็บไว้ (\S+) ของเงินทั้งหมด เงินที่เก็บหาได้ด้วยนิพจน์ใด',stem).groups()
                expected=expr(whole)*expr(fraction)
                branch=0
            elif stem.startswith('ซื้อกุ้ง'):
                a,b=re.findall(r'(\S+) กิโลกรัม',stem)
                expected=expr(a)+expr(b)
                branch=1
            elif stem.startswith('มีน้ำส้ม'):
                a,people=re.search(r'มีน้ำส้ม (\S+) ลิตร แบ่งให้ (\S+) คน',stem).groups()
                expected=expr(a)/expr(people)
                branch=2
            else:
                a,b=re.findall(r'(\S+) กิโลกรัม',stem)
                expected=expr(a)-expr(b)
                branch=3
            valid=[v==expected for v in values]
            assert len(set(values))==4
            branches.add(branch)
        elif key.endswith('fraction_discount_sentence_p5'):
            fraction,whole=re.search(r'ราคา (\S+) ของราคาเต็ม ราคาเต็ม (\d+) บาท',stem).groups()
            expected=expr(whole)-expr(whole)*expr(fraction)
            values=list(map(expr,choices))
            valid=[v==expected for v in values]
            assert len(set(values))==4
        elif key.endswith('length_equivalence_statement_p5'):
            valid=[]
            for c in choices:
                left,right=c.split(' = ')
                a,u=left.split()
                b,v=right.split()
                valid.append(expr(a)*FACTORS[u]==expr(b)*FACTORS[v])
        elif key.endswith('odd_length_equivalence_p5'):
            values=[expr(c.split()[0])*FACTORS[c.split()[1]] for c in choices]
            freq=Counter(values)
            assert sorted(freq.values())==[1,3]
            valid=[freq[v]==1 for v in values]
            branches.add(choices[q.answer].split()[1])
        elif key.endswith('length_rate_sentence_p5'):
            distance,speed=re.search(r'ระยะทาง (\S+) กิโลเมตร ด้วยอัตราเร็วเฉลี่ย (\d+) เมตร',stem).groups()
            valid=[expr(c)*expr(speed)==expr(distance)*1000 for c in choices]
        else:
            price,kg=re.search(r'ขีดละ (\d+) บาท ซื้อ (\S+) กิโลกรัม',stem).groups()
            # One khit is 100g; reconstruct total price from 100g portions.
            valid=[expr(c)*100==expr(kg)*1000*expr(price) for c in choices]
        assert valid==[i==q.answer for i in range(4)],(key,seed,stem,choices)
        if key.endswith(('decimal_three_place_addsub_p5','decimal_bracket_calculation_p5','decimal_round_expression_p5')):
            assert len(set(map(Decimal,choices)))==4
    floors={'decimal_three_place_addsub_p5':2,'decimal_bracket_calculation_p5':8,'decimal_round_expression_p5':2,
            'fraction_comparison_statement_p5':4,'fraction_expression_extreme_p5':2,
            'fraction_story_sentence_p5':4,'odd_length_equivalence_p5':4}
    if key[5:] in floors:
        assert len(branches)==floors[key[5:]]


def test_exact_rounding_and_source_values():
    from otk.sets.math.p5.decimals import _bank_round_fraction_p5
    for value in (Fraction(13585,1000),Fraction(262025,10000),Fraction(12345,1000),Fraction(1,6),Fraction(99,40)):
        for places in (1,2):
            assert s.Rational(str(_bank_round_fraction_p5(value,places)))==rational_round(s.Rational(value),places)
    assert rational_round(expr('(99.25 ÷ 25) × 6.6'),2)==s.Rational('26.20')
    assert rational_round(expr('(1234 ÷ 16) + (45.78 × 9.75)'),1)==s.Rational('523.5')


def test_round_only_after_exact_quotient_product():
    from otk.sets.math.p5.decimals import DecimalRoundExpressionP5
    class Forced(Random):
        def __init__(self):
            super().__init__(0)
            self.values=iter((1385,3,33))
        def choice(self,values):
            return 2
        def randint(self,a,b):
            return next(self.values)
    stem,right,wrongs=DecimalRoundExpressionP5().compose(Forced())
    assert '(13.85 ÷ 3) × 3.3' in stem
    assert expr(right)==rational_round(s.Rational(1385,100)/3*s.Rational(33,10),2)==s.Rational('15.24')
    assert len(set(wrongs))>=3 and right not in wrongs
