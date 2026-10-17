"""วันที่สอง ข้อ 4 — 4 กลุ่ม กลุ่มละ 7 คน ต้องมีสี่คนเพศเดียวกันจากสองกลุ่มสองเลขที่  (พิสูจน์)

Case count: two groups with the same majority gender share at most one seat of
it; three such groups are impossible (two 4-sets cover all 7 seats, leaving the
third at most 2), and two-and-two forces the boy-majority groups to have at
least 5 boys, whose sets then share 3 seats. The solver counts the
same-gender (group pair, seat pair) choices for a layout with girls in the
first seats: girls (4, 4, 3, 3) in groups of 7 give 42.

``check`` enumerates every 4-student subset of the actual students.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"girls": (4, 4, 3, 3), "seats": 7}
ANSWER = 42
VARIANTS = [{"girls": (1, 4, 1, 7), "seats": 8}, {"girls": (0, 2, 5), "seats": 5}, {"girls": (3, 3, 3, 3)}]


def solve(girls=(4, 4, 3, 3), seats=7):
    count = 0
    for r, s in combinations(range(len(girls)), 2):
        for i, j in combinations(range(1, seats + 1), 2):
            n = (i <= girls[r]) + (j <= girls[r]) + (i <= girls[s]) + (j <= girls[s])
            count += n in (0, 4)
    return count


def check(girls=(4, 4, 3, 3), seats=7):
    students = [(r, s, s <= girls[r]) for r in range(len(girls)) for s in range(1, seats + 1)]
    return sum(1 for four in combinations(students, 4)
               if len({x[0] for x in four}) == 2 and len({x[1] for x in four}) == 2 and len({x[2] for x in four}) == 1)
