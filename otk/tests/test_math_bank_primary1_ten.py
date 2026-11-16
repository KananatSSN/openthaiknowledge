"""Independent enumeration, integer optimization and conservation for Primary1 puzzles."""
from fractions import Fraction
from itertools import permutations, product
from random import Random
import re

import pytest

from otk.core import REGISTRY, generate

KEYS = ('math.post_interval_distance_p1', 'math.rank_both_ends_p1', 'math.possible_nth_weekday_p1',
        'math.equal_pieces_size_rank_p1', 'math.minimum_coins_p1', 'math.latin_missing_sum_p1',
        'math.minimum_bags_p1', 'math.distinct_fruit_assignment_p1', 'math.equalize_piles_p1',
        'math.digit_inequality_count_p1')


def content(blocks):
    return ' '.join(getattr(b, 'text', getattr(b, 'tex', '')) for b in blocks)


def coin_bfs(amount, coins):
    reached = {0}
    for count in range(amount + 1):
        if amount in reached:
            return count
        reached = {x + c for x in reached for c in coins if x + c <= amount}
    raise AssertionError('unreachable')


def latin_completion(grid):
    def fill():
        empty = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
        if not empty:
            return [row[:] for row in grid]
        def possible(r, c):
            return set(range(1, 5)) - set(grid[r]) - {grid[j][c] for j in range(4)}
        r, c = min(empty, key=lambda pos: len(possible(*pos)))
        for n in possible(r, c):
            grid[r][c] = n
            solved = fill()
            if solved:
                return solved
        grid[r][c] = 0
        return None
    return fill()


@pytest.mark.parametrize('key', KEYS)
def test_independent_visible_alternatives(key):
    branches = set()
    for seed in range(300):
        q = generate(key, Random(seed))
        stem = content(q.stem)
        choices = [content(c.content) for c in q.choices]
        assert len(choices) == len(set(choices)) == REGISTRY[key].max_choices
        if key.endswith('post_interval_distance_p1'):
            gap, first, last = map(int, re.search(r'ห่าง (\d+) เมตร เสาต้นที่ (\d+) ถึงต้นที่ (\d+)', stem).groups())
            positions = [0]
            for _ in range(last):
                positions.append(positions[-1] + gap)
            answer = positions[last] - positions[first]
            branches.add(first == 1)
        elif key.endswith('rank_both_ends_p1'):
            left, right = map(int, re.findall(r'\d+', stem))
            possibilities = [n for n in range(left, 30)
                             if len(list(range(n))[left - 1:]) == right]
            assert len(possibilities) == 1
            answer = possibilities[0]
        elif key.endswith('possible_nth_weekday_p1'):
            nth = int(re.search(r'ครั้งที่ (\d+)', stem)[1])
            possible = set()
            for first_weekday in range(7):
                dates = [d for d in range(1, 29) if (first_weekday + d - 1) % 7 == 0]
                possible.add(dates[nth - 1])
            valid = [int(c) in possible for c in choices]
            branches.add(nth)
        elif key.endswith('equal_pieces_size_rank_p1'):
            rows = re.findall(r'(เอ|บี|ซี|ดี)แบ่ง (\d+) ชิ้น', stem)
            rank = int(re.search(r'อันดับที่ (\d+)', stem)[1])
            large = 'ใหญ่เป็นอันดับ' in stem
            order = sorted(rows, key=lambda t: Fraction(1, int(t[1])), reverse=large)
            answer = order[rank - 1][0]
            assert all(c in dict(rows) for c in choices)
            branches.add((rank, large))
        elif key.endswith('minimum_coins_p1'):
            section = stem.split('ชนิดราคา ')[1].split(' บาท')[0]
            coins = list(map(int, re.findall(r'\d+', section)))
            amount = int(re.search(r'ให้ได้ (\d+) บาท', stem)[1])
            answer = coin_bfs(amount, coins)
            branches.add(tuple(coins))
        elif key.endswith('latin_missing_sum_p1'):
            data = stem.split('): ')[1].split(' ผลรวม')[0]
            rows = [row.split() for row in data.split(' / ')]
            assert len(rows) == 4 and all(len(row) == 4 for row in rows)
            grid = [[0 if x == '□' else int(x) for x in row] for row in rows]
            holes = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
            solved = latin_completion(grid)
            assert solved
            assert all(set(row) == set(range(1, 5)) for row in solved)
            assert all({solved[r][c] for r in range(4)} == set(range(1, 5)) for c in range(4))
            answer = sum(solved[r][c] for r, c in holes)
            branches.add(len(holes))
        elif key.endswith('minimum_bags_p1'):
            capacity, total = map(int, re.findall(r'\d+', stem))
            feasible = [n for n in range(total + 1) if capacity * n >= total]
            answer = min(feasible)
            branches.add(total % capacity == 0)
        elif key.endswith('distinct_fruit_assignment_p1'):
            people = stem.split(' เลือกผลไม้')[0].split(', ')
            fruits = ('ส้ม', 'มะม่วง', 'องุ่น', 'เงาะ')
            clauses = re.findall(r'(เอ|บี|ซี|ดี)ไม่เลือก([^·]+)', stem)
            forbidden = {p: {f for f in fruits if f in clause} for p, clause in clauses}
            assignments = [dict(zip(people, p)) for p in permutations(fruits)]
            feasible = [p for p in assignments if all(p[name] not in bans for name, bans in forbidden.items())]
            assert len(feasible) == 1
            target = re.search(r'(เอ|บี|ซี|ดี)เลือกผลไม้ชนิดใด', stem)[1]
            answer = feasible[0][target]
            assert set(choices) == set(fruits)
            branches.add((target, answer))
        elif key.endswith('equalize_piles_p1'):
            counts = list(map(int, re.search(r'มีจำนวน ([\d, ]+) ชิ้น', stem)[1].split(', ')))
            total = sum(counts)
            assert total % 4 == 0
            target = total // 4
            deficits = [target - x for x in counts if x < target]
            surpluses = [x - target for x in counts if x > target]
            assert len(deficits) == len(surpluses) == 2
            # Exhaust all 2x2 integral transport plans. Every moved item is counted once.
            plans = [sum(v) for v in product(range(9), repeat=4)
                     if v[0] + v[1] == surpluses[0] and v[2] + v[3] == surpluses[1]
                     and v[0] + v[2] == deficits[0] and v[1] + v[3] == deficits[1]]
            assert plans
            answer = min(plans)
        else:
            a, sign, b = re.search(r'(\d+) − □ ([><≥≤]) (\d+)', stem).groups()
            a, b = int(a), int(b)
            # Directly construct the solution set by inverse inequality intervals,
            # including 0 as a digit and both possible boundary inclusions.
            possible = {d for d in range(10) if
                        (d < a - b if sign == '>' else d <= a - b if sign == '≥' else
                         d > a - b if sign == '<' else d >= a - b)}
            answer = len(possible)
            branches.add((sign, 0 in possible))
        if not key.endswith('possible_nth_weekday_p1'):
            valid = [c == answer if isinstance(answer, str) else int(c) == answer for c in choices]
        assert sum(valid) == 1 and valid[q.answer], (key, seed, stem, choices, valid)
    floors = {'post_interval_distance_p1': 2, 'possible_nth_weekday_p1': 4,
              'equal_pieces_size_rank_p1': 4, 'minimum_coins_p1': 7,
              'latin_missing_sum_p1': 5, 'minimum_bags_p1': 2,
              'distinct_fruit_assignment_p1': 16, 'digit_inequality_count_p1': 4}
    assert len(branches) >= floors.get(key.removeprefix('math.'), 0)
