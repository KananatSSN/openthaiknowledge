"""ข้อ 19 — คะแนนรวมของ 4 ทีมในรอบแบ่งกลุ่ม

4 ทีมแข่งพบกันหมด ชนะได้ 3, เสมอได้ทีมละ 1, แพ้ได้ 0 คะแนน  หลังจบการแข่งขัน
    1) มีนัดที่จบด้วยผลเสมอเพียง 1 นัด
    2) มีเพียง 1 ทีมที่ชนะได้เพียง 1 นัด
    3) มีเพียง 1 ทีมที่ได้คะแนนรวมเป็นจำนวนคี่
    4) คะแนนรวมของแต่ละทีมไม่ซ้ำกัน
ถ้าคะแนนเรียงจากมากไปน้อยเป็น a, b, c, d จงหาค่าของ 2a + 5b + 6c + 8d

Method: with only four teams there are just 3⁶ = 729 ways the six matches can
go, so this is enumeration — the work is in stating the four conditions exactly.
Note condition (2) is about teams with *exactly one win*, not at least one, and
(3) counts teams whose total is odd, not the number of odd matches.

``solve`` enumerates per-match outcomes. ``check`` enumerates the same space
through a different object — a results matrix — recomputes the four conditions
from it, and additionally asserts the surviving score vector is unique (with
several vectors the question would have no single answer) and that the total
points come to 3·decisive + 2·draws, an invariant neither search uses.
"""

from __future__ import annotations

from itertools import combinations, product

PARAMS = {"teams": 4, "win": 3, "draw": 1, "draws_total": 1, "single_win": 1,
          "odd_totals": 1, "w1": 2, "w2": 5, "w3": 6, "w4": 8}
ANSWER = 68          # the unique score vector is (a,b,c,d) = (7, 6, 4, 0)
VARIANTS = [
    {"w1": 1, "w2": 1, "w3": 1, "w4": 1},
    {"w1": 0, "w2": 0, "w3": 0, "w4": 1},
    {"draws_total": 2},
    {"win": 2},
    {"odd_totals": 2},
]


def _matches(teams: int):
    return list(combinations(range(teams), 2))


def score_vectors(teams=4, win=3, draw=1, draws_total=1, single_win=1,
                  odd_totals=1) -> set[tuple[int, ...]]:
    """Every descending score vector consistent with all four conditions."""
    pairs = _matches(teams)
    found = set()
    # 0 = home win, 1 = away win, 2 = draw
    for outcome in product((0, 1, 2), repeat=len(pairs)):
        if sum(o == 2 for o in outcome) != draws_total:
            continue
        points = [0] * teams
        wins = [0] * teams
        for (i, j), o in zip(pairs, outcome):
            if o == 2:
                points[i] += draw
                points[j] += draw
            else:
                winner = i if o == 0 else j
                points[winner] += win
                wins[winner] += 1
        if sum(w == 1 for w in wins) != single_win:
            continue
        if sum(p % 2 for p in points) != odd_totals:
            continue
        if len(set(points)) != teams:
            continue
        found.add(tuple(sorted(points, reverse=True)))
    return found


def solve(teams=4, win=3, draw=1, draws_total=1, single_win=1, odd_totals=1,
          w1=2, w2=5, w3=6, w4=8):
    """The weighted combination w1·a + w2·b + w3·c + w4·d."""
    vectors = score_vectors(teams, win, draw, draws_total, single_win,
                            odd_totals)
    if len(vectors) != 1:
        return None
    a, b, c, d = next(iter(vectors))
    return w1 * a + w2 * b + w3 * c + w4 * d


def check(teams=4, win=3, draw=1, draws_total=1, single_win=1, odd_totals=1,
          w1=2, w2=5, w3=6, w4=8):
    """Independent: rebuild from a results matrix and verify the invariants."""
    pairs = _matches(teams)
    found = set()
    for outcome in product((0, 1, 2), repeat=len(pairs)):
        table = [[None] * teams for _ in range(teams)]
        for (i, j), o in zip(pairs, outcome):
            table[i][j] = o
            table[j][i] = o if o == 2 else 1 - o
        points, wins, draws_seen = [], [], 0
        for i in range(teams):
            row = [table[i][j] for j in range(teams) if j != i]
            w = sum(1 for r in row if r == 0)
            dr = sum(1 for r in row if r == 2)
            points.append(w * win + dr * draw)
            wins.append(w)
            draws_seen += dr
        if draws_seen // 2 != draws_total:
            continue
        if sum(w == 1 for w in wins) != single_win:
            continue
        if sum(p % 2 for p in points) != odd_totals:
            continue
        if len(set(points)) != teams:
            continue
        decisive = len(pairs) - draws_total
        assert sum(points) == decisive * win + draws_total * 2 * draw, \
            "points do not reconcile with the match results"
        found.add(tuple(sorted(points, reverse=True)))
    if len(found) != 1:
        return None
    a, b, c, d = next(iter(found))
    return w1 * a + w2 * b + w3 * c + w4 * d
