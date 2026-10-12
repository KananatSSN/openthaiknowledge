"""ข้อ 29 — ห้อง B ได้แต้มทั้งหมดกี่แต้ม

โรงเรียนแห่งหนึ่งจัดการแข่งขันฟุตบอลระหว่างห้อง A, B, C, D และ E แบบพบกันหมด
ชนะได้ 3 แต้ม เสมอได้ 1 แต้ม แพ้ได้ 0 แต้ม  จากผลการแข่งขันพบว่า
(1) A ได้ 2 แต้ม (2) B ชนะ C (3) C ได้ 4 แต้ม (4) D มีแต้มมากกว่าทุกห้อง
(5) E มีแต้มน้อยกว่าทุกห้อง (6) E เสมอกับ A  ห้อง B ได้แต้มทั้งหมดกี่แต้ม

Ten matches, three outcomes each: 3¹⁰ = 59 049 tournaments, small enough to look
at all of them. Exactly one point table survives the six clues,

    A 2   B 9   C 4   D 12   E 1

so the answer is **9**. The deduction by hand runs: A's 2 points must be two
draws, one of them with E, so E ≤ 1 and by clue 5 E = 1 and A drew C; C's 4 = a
win over E plus that draw, having lost to B and D; B and D have each beaten A, C
and E, and their head-to-head must be decisive with D winning, or D would not be
strictly top.

Both routes here are searches — this item has no closed form — but they are
written independently: ``solve`` filters a flat product of the ten results and
requires the surviving *point table* to be unique, while ``check`` is a recursive
backtracking search that prunes as it goes and rebuilds each team's points from a
results matrix. The uniqueness requirement is what makes either trustworthy: a
constraint set with two tables returns ``None`` rather than a coin flip.
"""

from __future__ import annotations

import itertools
from functools import lru_cache

TEAMS = 5
PAIRS = [(i, j) for i in range(TEAMS) for j in range(i + 1, TEAMS)]

#: A = 0, B = 1, C = 2, D = 3, E = 4. `winner` beat `loser`; `dx` drew with `dy`.
PARAMS = {"pts_a": 2, "pts_c": 4, "winner": 1, "loser": 2, "dx": 4, "dy": 0}
ANSWER = 9
VARIANTS = [
    {"pts_a": 3, "pts_c": 4},
    {"pts_a": 1, "pts_c": 6},
    {"pts_a": 2, "pts_c": 7},
    {"pts_a": 4, "pts_c": 4},
    {"pts_a": 12, "pts_c": 4},        # A cannot be top: D is
    {"pts_a": 2, "pts_c": 4, "winner": 2, "loser": 1},   # C beat B instead
]


def _points(results) -> tuple[int, ...]:
    """results[k] is 0 (first team wins), 1 (draw) or 2 (second wins)."""
    pts = [0] * TEAMS
    for (i, j), r in zip(PAIRS, results):
        if r == 0:
            pts[i] += 3
        elif r == 1:
            pts[i] += 1
            pts[j] += 1
        else:
            pts[j] += 3
    return tuple(pts)


@lru_cache(maxsize=None)
def _tables_by_ac(winner, loser, dx, dy):
    """{(A's points, C's points): the point tables D-top and E-bottom allow}."""
    wi = PAIRS.index((min(winner, loser), max(winner, loser)))
    want_w = 0 if winner < loser else 2
    di = PAIRS.index((min(dx, dy), max(dx, dy)))
    out: dict[tuple[int, int], set[tuple[int, ...]]] = {}
    for results in itertools.product((0, 1, 2), repeat=len(PAIRS)):
        if results[wi] != want_w or results[di] != 1:
            continue
        pts = _points(results)
        if any(pts[3] <= pts[k] for k in range(TEAMS) if k != 3):
            continue
        if any(pts[4] >= pts[k] for k in range(TEAMS) if k != 4):
            continue
        out.setdefault((pts[0], pts[2]), set()).add(pts)
    return out


def solve(pts_a=2, pts_c=4, winner=1, loser=2, dx=4, dy=0):
    """B's points, when the six clues leave exactly one point table."""
    if winner == loser or dx == dy or not 0 <= pts_a <= 12 or not 0 <= pts_c <= 12:
        return None
    tables = _tables_by_ac(winner, loser, dx, dy).get((pts_a, pts_c), set())
    if len(tables) != 1:
        return None
    return next(iter(tables))[1]


def check(pts_a=2, pts_c=4, winner=1, loser=2, dx=4, dy=0):
    """Independent: backtrack match by match, pruning, and rebuild the points."""
    if winner == loser or dx == dy or not 0 <= pts_a <= 12 or not 0 <= pts_c <= 12:
        return None
    grid: list[int | None] = [None] * len(PAIRS)
    wi = PAIRS.index((min(winner, loser), max(winner, loser)))
    di = PAIRS.index((min(dx, dy), max(dx, dy)))
    found: set[tuple[int, ...]] = set()

    def scores(upto: int):
        """Points so far, and how many each team may still add."""
        pts = [0] * TEAMS
        left = [0] * TEAMS
        for k, (i, j) in enumerate(PAIRS):
            r = grid[k]
            if r is None:
                left[i] += 3
                left[j] += 3
            elif r == 0:
                pts[i] += 3
            elif r == 1:
                pts[i] += 1
                pts[j] += 1
            else:
                pts[j] += 3
        return pts, left

    def walk(k: int):
        if k == len(PAIRS):
            pts, _ = scores(k)
            if pts[0] != pts_a or pts[2] != pts_c:
                return
            if any(pts[3] <= pts[t] for t in range(TEAMS) if t != 3):
                return
            if any(pts[4] >= pts[t] for t in range(TEAMS) if t != 4):
                return
            found.add(tuple(pts))
            return
        options = ((0 if winner < loser else 2,) if k == wi
                   else (1,) if k == di else (0, 1, 2))
        for r in options:
            grid[k] = r
            pts, left = scores(k)
            # A and C have fixed totals: prune once they cannot be reached.
            if pts[0] <= pts_a <= pts[0] + left[0] and \
               pts[2] <= pts_c <= pts[2] + left[2]:
                walk(k + 1)
            grid[k] = None

    walk(0)
    if len(found) != 1:
        return None
    return next(iter(found))[1]
