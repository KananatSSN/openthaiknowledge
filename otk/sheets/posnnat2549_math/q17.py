"""ข้อ 17 — จำนวนวิธีต่อตัว 6 คน (A บน B, C; B บน D, E; C บน E, F)

Lighter people stand higher, so the count is the number of linear extensions
of the poset A < B, A < C, B < D, B < E, C < E, C < F. ``solve`` counts them by
a dynamic programme over the set already placed: 16.

``check`` tries all permutations.
"""

from __future__ import annotations

from itertools import permutations

PARAMS = {"top": 1, "rows": 3}
ANSWER = 16
VARIANTS = [{"rows": 2}, {"top": 2, "rows": 2}, {"top": 2, "rows": 3}, {"top": 3, "rows": 2}]


def _pyramid(top, rows):
    index, starts = 0, []
    for i in range(rows):
        starts.append(index)
        index += top + i
    pairs = [(starts[i] + j, starts[i + 1] + j + d) for i in range(rows - 1) for j in range(top + i) for d in (0, 1)]
    return index, pairs


def solve(top=1, rows=3):
    size, pairs = _pyramid(top, rows)
    need = [0] * size
    for upper, lower in pairs:
        need[lower] |= 1 << upper
    ways = [0] * (1 << size)
    ways[0] = 1
    for mask in range(1 << size):
        if ways[mask]:
            for v in range(size):
                if not mask >> v & 1 and need[v] & mask == need[v]:
                    ways[mask | 1 << v] += ways[mask]
    return ways[-1]


def check(top=1, rows=3):
    size, pairs = _pyramid(top, rows)
    return sum(all(p.index(u) < p.index(v) for u, v in pairs) for p in permutations(range(size)))
