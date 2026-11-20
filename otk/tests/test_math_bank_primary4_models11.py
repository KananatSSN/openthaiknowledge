"""Independent visible-content solvers for the Primary 4 timetable/models batch."""
from datetime import datetime,timedelta
from random import Random
import re

import pytest
import sympy as s

from otk.core import REGISTRY,generate

KEYS=tuple('math.'+key for key in (
    'clock_hands_from_minutes_p4','inclusive_date_weeks_p4','approximate_months_days_p4','fractional_year_weeks_p4',
    'schedule_duration_p4','departure_cutoff_p4','add_sub_sentence_p4','remaining_share_sentence_p4',
    'quotient_then_add_sentence_p4','pack_unit_price_sentence_p4','related_story_for_sentence_p4'))


def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)


def ints(value):
    return list(map(int,re.findall(r'\d+',value)))


def evaluate(expression):
    return s.sympify(expression.replace('×','*').replace('÷','/').replace('−','-'),rational=True)


def time(value):
    return datetime.strptime(value,'%H.%M')


def story_value(story):
    if story.startswith('สมุดราคา'):
        a,b,c=ints(story)
        return 2*a+(b if 'แพงกว่า' in story else -b)+(c if 'มีเงินมากกว่า' in story else -c)
    if 'ให้เพื่อนไป' in story:
        total,gift,groups=ints(story)
        return s.Rational(total-gift,groups)
    if 'แล้วแบ่งเงินทั้งหมด' in story:
        total,gift,groups=ints(story)
        return s.Rational(total+gift,groups)
    total,groups,gift=ints(story)
    return s.Rational(total,groups)+(-gift if 'แต่ละคนจ่าย' in story else gift)


@pytest.mark.parametrize('key',KEYS)
def test_independent_visible_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        assert len(set(choices))==len(choices)==REGISTRY[key].max_choices
        if key.endswith('clock_hands_from_minutes_p4'):
            hour,minute=ints(stem)
            short=int((hour%12)*30+minute/2)//30 or 12
            long=minute//5
            valid=[]
            for choice in choices:
                a,b,c=ints(choice)
                valid.append(a==short and b==short%12+1 and c==long)
            branches.add(hour)
        elif key.endswith('inclusive_date_weeks_p4'):
            start,end=ints(stem)
            span=datetime(2024,1,end)-datetime(2024,1,start)+timedelta(days=1)
            assert span.days%7==0
            valid=[int(c)*7==span.days for c in choices]
        elif key.endswith('fractional_year_weeks_p4'):
            data=ints(stem)
            assert data[0]==52
            if 'ครึ่ง' in stem:
                years=s.Rational(2*data[1]+1,2)
                branches.add(2)
            else:
                _,whole,numerator,denominator=data
                years=whole+s.Rational(numerator,denominator)
                branches.add(numerator)
            valid=[s.Rational(c,52)==years for c in choices]
        elif key.endswith('approximate_months_days_p4'):
            total,base=ints(stem)
            assert base==30
            valid=[sum([base]*m)+d==total for m,d in map(ints,choices)]
            m,d=ints(choices[q.answer])
            assert 0<=d<base
        elif key.endswith('schedule_duration_p4'):
            rows=re.findall(r'(คิดเลขเร็ว|ลูกคิด|ภาษาไทย|วาดภาพ) \| (\d{2}\.\d{2}) \| (\d{2}\.\d{2})',stem)
            assert len(rows)==4
            target=re.search(r'กิจกรรม(คิดเลขเร็ว|ลูกคิด|ภาษาไทย|วาดภาพ)ใช้เวลา',stem).group(1)
            begin,end=next((a,b) for name,a,b in rows if name==target)
            duration=(time(end)-time(begin)).total_seconds()/60
            assert duration>0
            if 'กี่ชั่วโมงกี่นาที' in stem:
                values=[60*h+m for h,m in map(ints,choices)]
                branches.add('hours')
            else:
                values=list(map(int,choices))
                branches.add('minutes')
            valid=[v==duration for v in values]
        elif key.endswith('departure_cutoff_p4'):
            rows=re.findall(r'(สาย [กขคง]) \| (\d{2}\.\d{2}) \| (\d{2}\.\d{2}) (วันเดียวกัน|วันถัดไป)',stem)
            assert len(rows)==4
            cutoff=time(re.search(r'ออกก่อน (\d{2}\.\d{2})',stem).group(1))
            eligible=[]
            for name,departure,arrival,day in rows:
                start,end=time(departure),time(arrival)
                if day=='วันถัดไป':
                    end+=timedelta(days=1)
                assert timedelta(hours=6)<=end-start<=timedelta(hours=14)
                if start<cutoff:
                    eligible.append(name)
            assert len(eligible)==1
            assert any(time(start)==cutoff for _,start,_,_ in rows)
            valid=[c==eligible[0] for c in choices]
        elif key.endswith('related_story_for_sentence_p4'):
            shown=stem.removeprefix('เรื่องใดใช้ ').removesuffix(' หาคำตอบได้')
            want=evaluate(shown)
            values=list(map(story_value,choices))
            assert len(set(values))==4
            valid=[v==want for v in values]
            branches.add('related' if choices[0].startswith('สมุดราคา') else 'sharing')
        else:
            values=list(map(evaluate,choices))
            assert len(set(values))==4,(stem,choices,values)
            if key.endswith('add_sub_sentence_p4'):
                a,b,c=ints(stem)
                if stem.startswith('มีนม'):
                    valid=[v+b+c==a for v in values]
                    branches.add('two-removals')
                else:
                    valid=[v+c==a+b for v in values]
                    branches.add('comparison-chain')
            elif key.endswith('remaining_share_sentence_p4'):
                total,broken,groups=ints(stem)
                valid=[v*groups+broken==total for v in values]
            elif key.endswith('quotient_then_add_sentence_p4'):
                price,paid,extra=ints(stem)
                valid=[(v-extra)*price==paid for v in values]
            else:
                units,per,revenue=ints(stem)
                assert units%per==0
                valid=[sum([v]*(units//per))==revenue for v in values]
        assert valid==[i==q.answer for i in range(4)],(key,seed,stem,choices)
    if key.endswith('fractional_year_weeks_p4'):
        assert branches=={1,2,3}
    if key.endswith('clock_hands_from_minutes_p4'):
        assert len(branches)==24
    if key.endswith(('schedule_duration_p4','related_story_for_sentence_p4','add_sub_sentence_p4')):
        assert len(branches)==2


def test_source_inclusive_dates_and_fractional_sharing():
    assert (datetime(2024,7,22)-datetime(2024,7,2)+timedelta(days=1)).days==21
    assert evaluate('(665230 − 200000) ÷ 4')==s.Rational(232615,2)
