"""ข้อ 7 — จำนวนเสาไฟน้อยสุดบนแถบ |x − y| ≤ 1

The diagonal points (i, i) each need a lamp within distance 1 (radius 1.01 reaches
only distance 0 and 1), and no lamp is within 1 of two of them; so n + 1 lamps
are needed, and lamps on the diagonal suffice. The solver returns n + 1.

``check`` finds the smallest dominating set of the strip's points (neighbours
at distance 1) by trying every set of each size in turn.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"n": 4}
ANSWER = 5
VARIANTS = [{"n": 1}, {"n": 2}, {"n": 5}, {"n": 6}]


def solve(n=4):
    return n + 1


def check(n=4):
    pts = [(x, y) for x in range(n + 1) for y in range(n + 1) if abs(x - y) <= 1]
    reach = {p: frozenset(q for q in pts if (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 <= 1.01**2)
             for p in pts}
    everything = frozenset(pts)
    for size in range(1, len(pts) + 1):
        for lamps in combinations(pts, size):
            if frozenset().union(*(reach[p] for p in lamps)) == everything:
                return size
    raise AssertionError
