"""ข้อ 12 — ลำดับการใส่ถุงเท้าและรองเท้า 4 เท้า

2k distinct actions, and on each foot exactly half the orders put the sock
first: (2k)!/2^k = 8!/16 = 2520.

``check`` enumerates every order of the 2k actions.
"""

from __future__ import annotations

from itertools import permutations
from math import factorial

PARAMS = {"feet": 4}
ANSWER = 2520
VARIANTS = [{"feet": 1}, {"feet": 2}, {"feet": 3}]


def solve(feet=4):
    return factorial(2 * feet) // 2**feet


def check(feet=4):
    actions = [(f, kind) for f in range(feet) for kind in (0, 1)]
    return sum(all(p.index((f, 0)) < p.index((f, 1)) for f in range(feet)) for p in permutations(actions))
