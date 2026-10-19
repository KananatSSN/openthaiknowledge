"""ข้อ 1 — |S| มากสุดเมื่อผลบวกของสองสมาชิกต่างกันเป็นกำลังสอง และ 2009, 2087 ∈ S

A third member c needs c + a = u² and c + b = v², so (v − u)(v + u) = b − a
with factors of equal parity; 2087 − 2009 = 78 ≡ 2 (mod 4) admits none, so
|S| = 2. ``solve`` factors b − a and runs a clique search on the candidates.

``check`` scans u directly (c = u² − a for u up to a bound), keeps c with c + b
a square, and runs its own clique search.
"""

from __future__ import annotations

from itertools import combinations
from math import isqrt

PARAMS = {"a": 2009, "b": 2087}
ANSWER = 2
VARIANTS = [{"a": 10, "b": 390}, {"a": 6, "b": 30}, {"a": 50, "b": 239}, {"a": 33, "b": 192}]


def _square(v):
    return v >= 0 and isqrt(v) ** 2 == v


def _clique(pool):
    for size in range(len(pool), 0, -1):
        for group in combinations(pool, size):
            if all(_square(x + y) for x, y in combinations(group, 2)):
                return size
    return 0


def solve(a=2009, b=2087):
    diff, found = b - a, set()
    for d1 in range(1, isqrt(diff) + 1):
        if diff % d1 == 0 and (d1 + diff // d1) % 2 == 0:
            u = (diff // d1 - d1) // 2
            c = u * u - a
            if c > 0 and c not in (a, b):
                found.add(c)
    return 2 + _clique(sorted(found))


def check(a=2009, b=2087):
    found = set()
    for u in range(1, (b - a) + isqrt(a) + 2):
        c = u * u - a
        if c > 0 and c not in (a, b) and _square(c + b):
            found.add(c)
    return 2 + _clique(sorted(found))
