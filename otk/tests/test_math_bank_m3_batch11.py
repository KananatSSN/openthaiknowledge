"""Independent symbolic, enumeration and geometry checks for the M3 text batch."""
from fractions import Fraction
from random import Random
import ast
import re
import pytest
import sympy as s
from otk.core import REGISTRY,generate

KEYS=('math.inequality_representation_m3', 'math.age_constraint_m3', 'math.rectangle_area_bound_m3', 'math.factor_cube_identity_m3', 'math.factor_fourth_power_m3', 'math.quadratic_standard_form_m3', 'math.quadratic_dimension_m3', 'math.quadratic_past_age_m3', 'math.quadratic_number_relation_m3', 'math.quadratic_root_relation_m3', 'math.perpendicular_travel_m3')

def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)

def ints(text):
    return list(map(int,re.findall(r'-?\d+',text.replace('−','-'))))

def expr(text):
    return s.sympify(text.replace('×','*').replace('÷','/').replace('−','-').replace('²','**2').replace('³','**3').replace('⁴','**4'))

def polynomial(equation):
    left,right=equation.split('=')
    return s.expand(expr(left)-expr(right))

@pytest.mark.parametrize('key',KEYS)
def test_independent_visible_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        assert len(choices)==len(set(choices))==REGISTRY[key].max_choices
        n=ints(stem)
        x=s.Symbol('x')
        if key.endswith('inequality_representation_m3') and 'เส้นจำนวน' in stem:
            bound,=n
            closed='จุดทึบ' in stem
            right='ทางขวา' in stem
            probes=[s.Rational(bound)-s.Rational(1,2),s.Rational(bound),s.Rational(bound)+s.Rational(1,2)]
            expected=[(v>=bound if closed else v>bound) if right else (v<=bound if closed else v<bound) for v in probes]
            valid=[]
            for c in choices:
                relation=c.split()[1]
                relations={'<':lambda v:v<bound,'≤':lambda v:v<=bound,'>':lambda v:v>bound,'≥':lambda v:v>=bound}
                valid.append([relations[relation](v) for v in probes]==expected)
            branches.add(('ray',closed,right))
        elif key.endswith('inequality_representation_m3'):
            extra,divisor,cap=n
            probes={Fraction(divisor*cap-extra)+delta for delta in (-1,0,1)}
            probes|={Fraction(divisor*(cap-extra))+delta for delta in (-1,0,1)}
            is_le='≤' in stem
            expected=[(v+extra)/divisor<=cap if is_le else (v+extra)/divisor>=cap for v in probes]
            valid=[]
            for choice in choices:
                grouped='ผลบวก' in choice
                a,b,c=ints(choice)
                inc,d=(a,b) if grouped else (b,a)
                le='ไม่เกิน' in choice
                actual=[]
                for v in probes:
                    value=(v+inc)/d if grouped else v/d+inc
                    actual.append(value<=c if le else value>=c)
                valid.append(actual==expected)
            branches.add(('word',is_le))
        elif key.endswith('age_constraint_m3'):
            first='แม่' in stem
            branches.add(first)
            if first:
                m,t,cap=n
                feasible=[age for age in range(1,cap) if age*m+t+age+t<=cap]
                valid=[int(c)==max(feasible) for c in choices]
            else:
                g1,g2,cap=n
                feasible=[young+g2+g1 for young in range(1,cap) if young+(young+g2)+(young+g2+g1)>cap]
                valid=[int(c)==min(feasible) for c in choices]
        elif key.endswith('rectangle_area_bound_m3'):
            m,e,p=n
            width=s.solve(s.Eq(2*(x+m*x+e),p),x)[0]
            # Approach the excluded endpoint from above; derivative proves monotonicity.
            area=x*(m*x+e)
            assert s.diff(area,x).subs(x,width)>0
            limit=s.limit(area,x,width,dir='+')
            valid=[int(c)==limit for c in choices]
        elif key.endswith(('factor_cube_identity_m3','factor_fourth_power_m3')):
            shown=stem.removeprefix('แยกตัวประกอบ ')
            target=s.Poly(expr(shown),*sorted(expr(shown).free_symbols,key=str))
            polys=[s.Poly(expr(c),*target.gens) for c in choices]
            assert len(set(map(str,polys)))==4
            valid=[p==target for p in polys]
            if key.endswith('factor_cube_identity_m3'):
                branches.add(('y' in stem,'³ +' in stem))
        elif key.endswith('quadratic_standard_form_m3'):
            coeff='สัมประสิทธิ์' in stem
            branches.add(coeff)
            if coeff:
                eq=stem.split('สมการ ',1)[1].split(' ย้าย',1)[0]
                expected=tuple(s.Poly(polynomial(eq),x).all_coeffs())
                valid=[ast.literal_eval(c)==expected for c in choices]
            else:
                valid=[s.Poly(polynomial(c),x).degree()==2 for c in choices]
        elif key.endswith('quadratic_dimension_m3'):
            triangle='สามเหลี่ยม' in stem
            branches.add(triangle)
            if triangle:
                area,gap=n
                expected=s.solve(s.Eq(x*(x-gap)/2,area),x)
                valid=[int(c)>gap and int(c) in expected for c in choices]
            else:
                m,e,area=n
                valid=[s.Rational(c)*(s.Rational(c)-e)/m==area and int(c)>e for c in choices]
        elif key.endswith('quadratic_past_age_m3'):
            future,ago,again=n
            assert ago==again
            # Enumerate actual ages and reconstruct both times.
            feasible=[age for age in range(ago+1,300) if age+future==(age-ago)**2]
            assert len(feasible)==1
            valid=[int(c)==feasible[0] for c in choices]
        elif key.endswith('quadratic_number_relation_m3'):
            even='จำนวนเต็มคู่' in stem
            branches.add(even)
            if even:
                a,b=n
                valid=[]
                for c in choices:
                    small,large=ints(c)
                    valid.append(small>0 and small%2==0 and large-small==2 and a*(small+large)==b*small*large)
            else:
                gap,total=n
                valid=[int(c)>gap and int(c)**2+(int(c)-gap)**2==total for c in choices]
        elif key.endswith('quadratic_root_relation_m3'):
            known='รากหนึ่ง' in stem
            branches.add(known)
            if known:
                a,constant,zero,root=n
                assert zero==0
                coefficient=s.solve(s.Eq(a*root**2+x*root+constant,0),x)[0]
                roots=s.solve(a*x*x+coefficient*x+constant,x)
                expected=sum(roots)
            else:
                shift,p,constant=n
                roots=s.solve(s.Eq((x+shift)**2,p*x+constant),x)
                assert len(roots)==2 and all(r.is_real for r in roots)
                expected=s.prod(roots).simplify()
            valid=[int(c)==expected for c in choices]
            assert len(set(map(int,choices)))==4
        else:
            gap,distance=n
            valid=[int(c)>gap and int(c)**2+(int(c)-gap)**2==distance**2 for c in choices]
        assert valid==[i==q.answer for i in range(4)],(key,seed,stem,choices)
    expected_counts={'inequality_representation_m3':6,'age_constraint_m3':2,'factor_cube_identity_m3':4,
                     'quadratic_standard_form_m3':2,'quadratic_dimension_m3':2,
                     'quadratic_number_relation_m3':2,'quadratic_root_relation_m3':2}
    if key[5:] in expected_counts:
        assert len(branches)==expected_counts[key[5:]]


def test_source_corrections_and_geometry():
    x=s.Symbol('x',real=True)
    assert s.expand((x+10)*(x*x+2*x+28))==s.expand((x+4)**3+216)
    assert [n for n in range(1,20) if 0<36-4*n<2*n]==[7,8]
    assert s.Rational(-6)+s.Rational(-12,3*(-6))==s.Rational(-16,3)
    assert 80*80+60*60==100*100


def test_forced_age_and_root_distractor_collisions():
    from otk.sets.math.m3.quadratic import QuadraticPastAgeM3,QuadraticRootRelationM3
    class ForcedAge(Random):
        def __init__(self):
            super().__init__(0)
            self.values=iter((4,6))
        def randint(self,a,b):
            return next(self.values)
    _,right,wrongs=QuadraticPastAgeM3().compose(ForcedAge())
    assert len(set(wrongs))>=3 and right not in wrongs
    class ForcedRoots(Random):
        def __init__(self):
            super().__init__(0)
            self.values=iter((2,2,6))
        def choice(self,values):
            return True
        def randint(self,a,b):
            return next(self.values)
    _,right,wrongs=QuadraticRootRelationM3().compose(ForcedRoots())
    assert len(set(wrongs))>=3 and right not in wrongs


def test_known_root_distractor_collision():
    from otk.sets.math.m3.quadratic import QuadraticRootRelationM3
    class Forced(Random):
        def __init__(self):
            super().__init__(0)
            self.values=iter((3,3,6))
        def choice(self,values):
            return False
        def randint(self,a,b):
            return next(self.values)
    _,right,wrongs=QuadraticRootRelationM3().compose(Forced())
    assert len(set(wrongs))>=3 and right not in wrongs
