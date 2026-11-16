"""Independent exact expressions, planar models, polygons and chart solvers."""
from random import Random
import re
import pytest
import sympy as s
from otk.core import REGISTRY,generate

KEYS=('math.canonical_expansion_millions_p4', 'math.rounding_statement_p4', 'math.large_addsub_sentence_p4', 'math.discount_fee_sentence_p4', 'math.product_model_statement_p4', 'math.line_notation_p4', 'math.plane_surface_model_p4', 'math.rectangle_property_statement_p4', 'math.square_summary_statement_p4', 'math.three_series_chart_summary_p4', 'math.selected_columns_row_max_p4')

def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)

def ints(text):
    return list(map(int,re.findall(r'\d+',text)))

def expr(value):
    return s.sympify(value.replace('−','-').replace('×','*').replace('÷','/'),rational=True)

@pytest.mark.parametrize('key',KEYS)
def test_independent_visible_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        assert len(choices)==len(set(choices))==REGISTRY[key].max_choices
        n=ints(stem)
        if key.endswith('canonical_expansion_millions_p4'):
            number,=n
            expected=[int(d+'0'*(len(str(number))-i-1)) for i,d in enumerate(str(number)) if d!='0']
            valid=[sorted(ints(c))==sorted(expected) for c in choices]
            assert sum(expr(c)==number for c in choices)==2
            branches.add(len(str(number)))
        elif key.endswith('rounding_statement_p4'):
            scales={'พัน':1000,'หมื่น':10000,'แสน':100000,'ล้าน':1000000}
            valid=[]
            for c in choices:
                value,name,shown=re.fullmatch(r'ปัด (\d+) ใกล้เคียงจำนวนเต็ม(\S+) ได้ (\d+)',c).groups()
                value,shown=int(value),int(shown)
                step=scales[name]
                lower=value//step*step
                expected=lower+step if value-lower>=lower+step-value else lower
                valid.append(shown==expected)
            branches.add(re.search(r'เต็ม(\S+) ได้',choices[q.answer]).group(1))
        elif key.endswith('large_addsub_sentence_p4'):
            a,b=n
            if stem.startswith('เงินเดือน'):
                expected=b-a
                branch=0
            elif stem.startswith('มีเงินฝาก'):
                expected=a-b
                branch=1
            elif stem.startswith('ขายสินค้า'):
                expected=sum([a,b])
                branch=2
            else:
                expected=a+b
                branch=3
            values=list(map(expr,choices))
            valid=[v==expected for v in values]
            assert len(set(values))==4
            branches.add(branch)
        elif key.endswith('discount_fee_sentence_p4'):
            price,discount,fee=n
            expected=price-discount+fee
            values=list(map(expr,choices))
            valid=[v==expected for v in values]
            assert len(set(values))==4
        elif key.endswith('product_model_statement_p4'):
            groups,each=n
            expected=sum([each]*groups)
            valid=[]
            for c in choices:
                left,right=c.split(' = ')
                valid.append('×' in left and expr(left)==expr(right)==expected)
        elif key.endswith('line_notation_p4'):
            a,b=re.findall(r'\b[A-Z]\b',stem)
            kind='overrightarrow' if stem.startswith('รังสี') else 'overline' if stem.startswith('ส่วนของ') else 'overleftrightarrow'
            valid=[]
            for c in choices:
                command,points=re.fullmatch(r'\\(overrightarrow|overline|overleftrightarrow)\{([A-Z]{2})\}',c).groups()
                valid.append(command==kind and (points==a+b if kind=='overrightarrow' else set(points)=={a,b}))
            branches.add(kind)
        elif key.endswith('plane_surface_model_p4'):
            ask_flat='ผิวใดเป็น' in stem
            # A flat ideal face admits one plane; the full sphere does not.
            flat=s.Matrix([[0,0,0,1],[1,0,0,1],[0,1,0,1],[1,1,0,1]]).det()==0
            curved=s.Matrix([[1,0,0,1],[0,1,0,1],[0,0,1,1],[-1,0,0,1]]).det()==0
            valid=[(curved if 'ทรงกลม' in c else flat)==ask_flat for c in choices]
            branches.add(ask_flat)
        elif key.endswith('rectangle_property_statement_p4'):
            width,length=n
            assert width!=length
            vertices=[s.Point(0,0),s.Point(length,0),s.Point(length,width),s.Point(0,width)]
            edges=[s.Segment(vertices[i],vertices[(i+1)%4]) for i in range(4)]
            diag1,diag2=s.Segment(vertices[0],vertices[2]),s.Segment(vertices[1],vertices[3])
            opposite_pairs=sum(edges[i].is_parallel(edges[i+2]) for i in range(2))
            right_angles=all(edges[i].is_perpendicular(edges[(i+1)%4]) for i in range(4))
            properties={
                'มีด้านตรงข้ามขนานกันสองคู่':opposite_pairs==2,
                'มุมภายในทุกมุมเป็นมุมฉาก':right_angles,
                'เส้นทแยงมุมมีความยาวเท่ากัน':diag1.length==diag2.length,
                'เส้นทแยงมุมแบ่งครึ่งซึ่งกันและกัน':diag1.midpoint==diag2.midpoint,
                'ด้านตรงข้ามมีความยาวเท่ากัน':all(edges[i].length==edges[i+2].length for i in range(2)),
                'มีด้านตรงข้ามขนานกันเพียงหนึ่งคู่':opposite_pairs==1,
                'มุมภายในทุกมุมเป็นมุมแหลม':all(angle<s.pi/2 for angle in s.Polygon(*vertices).angles.values()),
                'เส้นทแยงมุมตัดกันเป็นมุมฉาก':diag1.is_perpendicular(diag2),
                'ด้านประชิดทุกคู่มีความยาวเท่ากัน':len({edge.length for edge in edges})==1,
            }
            valid=[not properties[c] for c in choices]
            branches.add(choices[q.answer])
        elif key.endswith('square_summary_statement_p4'):
            side,=n
            poly=s.Polygon((0,0),(side,0),(side,side),(0,side))
            valid=[]
            for c in choices:
                value,=ints(c)
                if c.startswith('มุม'):
                    truth=value==sum(poly.angles.values())*180/s.pi
                    branch=0
                elif c.startswith('พื้นที่'):
                    truth=value==poly.area
                    branch=1
                elif c.startswith('เส้นรอบ'):
                    truth=value==poly.perimeter
                    branch=2
                else:
                    truth=value==len(poly.sides)
                    branch=3
                valid.append(not truth)
                if not truth:
                    branches.add(branch)
        elif key.endswith('three_series_chart_summary_p4'):
            rows=re.findall(r'(มกราคม|กุมภาพันธ์|มีนาคม) \| (\d+) \| (\d+) \| (\d+)',stem)
            assert len(rows)==3
            data={month:tuple(map(int,nums)) for month,*nums in rows}
            valid=[]
            for c in choices:
                if c.startswith('สมุดขายมาก'):
                    month=c.split('เดือน')[1]
                    truth=data[month][0]==max(v[0] for v in data.values())
                    branch=0
                elif c.startswith('ยางลบขายน้อย'):
                    month=c.split('เดือน')[1]
                    truth=data[month][2]==min(v[2] for v in data.values())
                    branch=1
                elif c.startswith('เดือนกุมภาพันธ์'):
                    a,b,_=data['กุมภาพันธ์']
                    truth=(a!=b) if 'ไม่เท่ากัน' in c else (a==b)
                    branch=2
                else:
                    a,b=data['มกราคม'][0],data['มีนาคม'][0]
                    truth=(a>b) if 'มากกว่า' in c else (a<b)
                    branch=3
                valid.append(not truth)
                if not truth:
                    branches.add(branch)
        else:
            rows=re.findall(r'(ป\.\d+) \| (\d+) \| (\d+) \| (\d+)',stem)
            assert len(rows)==6
            data={name:tuple(map(int,nums)) for name,*nums in rows}
            excluded={name:low+high for name,(_,low,high) in data.items()}
            expected=max(excluded,key=excluded.get)
            assert sum(data[expected])<max(map(sum,data.values()))
            assert set(choices)<=set(data)
            valid=[c==expected for c in choices]
            branches.add(expected)
        assert valid==[i==q.answer for i in range(4)],(key,seed,stem,choices)
    floors={'canonical_expansion_millions_p4':2,'rounding_statement_p4':4,'large_addsub_sentence_p4':4,
            'line_notation_p4':3,'plane_surface_model_p4':2,'rectangle_property_statement_p4':4,
            'square_summary_statement_p4':4,'three_series_chart_summary_p4':4,'selected_columns_row_max_p4':6}
    if key[5:] in floors:
        assert len(branches)==floors[key[5:]]
