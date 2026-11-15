"""Independent visible-content checks for the Primary 1 reasoning paper."""
from collections import deque
from itertools import combinations, permutations, product
from math import gcd
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = tuple('math.'+key for key in (
    'block_rotation_p1','ordered_sharing_p1','grid_relative_position_p1','pair_absence_p1',
    'balance_ball_swaps_p1','overlap_circle_sums_p1','race_constraints_p1',
    'seven_segment_removal_p1','grid_path_check_p1','digit_clues_p1',
    'knockout_matches_p1','reverse_double_balance_p1'))


def content(blocks):
    return ' '.join(getattr(b,'text',getattr(b,'tex','')) for b in blocks)


def ints(value):
    return list(map(int,re.findall(r'\d+',value)))


def min_swaps(n,a,b):
    # Breadth-first search of legal swaps, retaining both inventories.
    queue=deque([(a,b,0)])
    seen={(a,b)}
    while queue:
        x,y,steps=queue.popleft()
        if n+x == n+y:
            return steps
        for dx in (-1,1):
            # +1: A sends a 1 and receives a 2; -1 reverses these values.
            if dx==1 and not (x<n and y>0):
                continue
            if dx==-1 and not (x>0 and y<n):
                continue
            state=(x+dx,y-dx)
            if state not in seen:
                seen.add(state)
                queue.append((*state,steps+1))
    raise AssertionError('No balancing sequence')


@pytest.mark.parametrize('key',KEYS)
def test_independent_visible_answers(key):
    branches=set()
    for seed in range(300):
        q=generate(key,Random(seed))
        stem=content(q.stem)
        choices=[content(c.content) for c in q.choices]
        answer=choices[q.answer]
        assert len(choices)==len(set(choices))==REGISTRY[key].max_choices
        if key.endswith('block_rotation_p1'):
            n,step=ints(stem)
            want=n//gcd(n,step)
            assert int(answer)==want
            assert all((k*step)%n for k in range(1,want))
        elif key.endswith('ordered_sharing_p1'):
            total,people,minimum=ints(stem)
            assert (people,minimum)==(3,1)
            ways={tuple(sorted(parts)) for parts in combinations(range(1,total),3) if sum(parts)==total}
            assert int(answer)==len(ways)
        elif key.endswith('grid_relative_position_p1'):
            rows,cols=ints(stem)
            front_more='ด้านหน้ามีมาก' in stem
            left_more='ด้านซ้ายมีมาก' in stem
            grid=[list(range(start,start+cols)) for start in range(1,rows*cols+1,cols)]
            valid=[]
            for r,line in enumerate(grid):
                for c,label in enumerate(line):
                    front=len(grid[:r])
                    back=len(grid[r+1:])
                    left=len(line[:c])
                    right=len(line[c+1:])
                    if not min(front,back,left,right):
                        continue
                    if (front>back if front_more else front<back) and (left>right if left_more else left<right):
                        valid.append(label)
            assert valid==[int(answer)]
            branches.add((rows,cols,front_more,left_more))
        elif key.endswith('pair_absence_p1'):
            total,unmatched=ints(stem)
            possibles=[(boys,girls) for boys in range(total) for girls in range(total)
                       if boys+girls==total and boys==girls]
            assert len(possibles)==1
            _,girls=possibles[0]
            assert int(answer)+unmatched==girls
        elif key.endswith('balance_ball_swaps_p1'):
            one,a,two,b,one2,c,two2,d=ints(stem)
            assert (one,two,one2,two2)==(1,2,1,2)
            assert a+b==c+d
            assert int(answer)==min_swaps(a+b,b,d)
        elif key.endswith('overlap_circle_sums_p1'):
            left,right,total=ints(stem)
            triples=[(a,b,c) for a in range(total+1) for b in range(total+1) for c in range(total+1)
                     if a+left==b+left+right==c+right==total]
            assert len(triples)==1 and sum(triples[0])==int(answer)
        elif key.endswith('race_constraints_p1'):
            a,b,c,d,a_again=re.search(r'ไม่มีอันดับร่วม ([A-D]) ไม่ได้อันดับแรก ([A-D]) เข้าเส้นชัยก่อน ([A-D]) และ ([A-D]) เข้าเส้นชัยหลัง ([A-D])',stem).groups()
            assert a==a_again
            ranks=[order for order in permutations('ABCD')
                   if order[0]!=a and order.index(b)<order.index(c) and order.index(a)<order.index(d)]
            assert [tuple(label.split(' → ')) in ranks for label in choices]==[i==q.answer for i in range(4)]
            assert len(ranks)>1  # The task selects an option, not a globally unique ranking.
        elif key.endswith('seven_segment_removal_p1'):
            segments=('abcdef','bc','abdeg','abcdg','bcfg','acdfg','acdefg','abc','abcdefg','abcdfg')
            removed=int(re.search(r'หยิบออก (\d+) ก้าน',stem).group(1))
            all_segments=set(segments[8])
            possible=[str(d) for d,parts in enumerate(segments) if len(all_segments-set(parts))==removed]
            assert answer.split(', ')==possible
            branches.add(removed)
        elif key.endswith('grid_path_check_p1'):
            right,up=ints(stem)
            reaches=[(p.count('→'),p.count('↑'))==(right,up) for p in choices]
            assert reaches==[i!=q.answer for i in range(4)]
        elif key.endswith('digit_clues_p1'):
            data=ints(stem)
            if 'สามหลัก' in stem:
                dh,dt,total=data
                possible=[]
                for digits in product(range(10),repeat=3):
                    h,t,u=digits
                    if h and h-u==dh and t-u==dt and sum(digits)==total:
                        possible.append(100*h+10*t+u)
                assert possible==[int(answer)]
                branches.add('three')
            else:
                total,=data
                possibles=[n for n in range(10,100) if sum(map(int,str(n)))==total]
                most='มากที่สุด' in stem
                assert int(answer)==sorted(possibles,reverse=most)[0]
                branches.add('max' if most else 'min')
        elif key.endswith('knockout_matches_p1'):
            players,=ints(stem)
            matches=0
            while players>1:
                matches+=players//2
                players=(players+1)//2
            assert int(answer)==matches
        else:
            first,last,final=ints(stem)
            valid=[n for n in range(201) if n>=first and 2*(n-first)-last==final]
            assert valid==[int(answer)]
    if key.endswith('seven_segment_removal_p1'):
        assert branches==set(range(1,6))
    if key.endswith('digit_clues_p1'):
        assert branches=={'three','max','min'}

    if key.endswith('grid_relative_position_p1'):
        assert len(branches)==16
