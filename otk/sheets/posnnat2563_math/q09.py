"""ข้อ 9 — จำนวนช่องที่ไม่ถูกไถน้อยสุดด้วยรถไถ k คันบนตาราง n × n

Each northeast route meets each anti-diagonal in one square, so k routes cover
at most k squares of each anti-diagonal; summing min(k, length) over the 2n − 1
anti-diagonals leaves at least (n − k)² uncovered, and routes hugging nested
staircases achieve it. The solver returns (n − k)².

``check`` lists every up/right route and tries every multiset of k of them,
returning the fewest squares left unploughed.
"""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement

PARAMS = {"n": 4, "k": 2}
ANSWER = 4
VARIANTS = [{"n": 3, "k": 1}, {"n": 5, "k": 2}, {"n": 5, "k": 3}, {"n": 4, "k": 3}]


def solve(n=4, k=2):
    return (n - k) ** 2


def _routes(n):
    routes = []
    for ups in combinations(range(2 * n - 2), n - 1):
        r = c = 0
        cells = {(0, 0)}
        for step in range(2 * n - 2):
            if step in ups:
                r += 1
            else:
                c += 1
            cells.add((r, c))
        routes.append(frozenset(cells))
    return routes


def check(n=4, k=2):
    routes = _routes(n)
    best = n * n
    for choice in combinations_with_replacement(routes, k):
        best = min(best, n * n - len(frozenset().union(*choice)))
    return best
