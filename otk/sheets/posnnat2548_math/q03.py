"""ข้อ 3 — AB/BC ในสามเหลี่ยมหน้าจั่วที่มุมฐานเป็นสองเท่าของมุมยอด

5x = 180° gives the apex 36°. The bisector of a base angle cuts off a similar
triangle, so AB/BC = φ = (1 + √5)/2, and φⁿ = (Lₙ + Fₙ√5)/2 for the powers the
generator also asks (source: n = 1).

``check`` uses the sine rule on the 36°–72°–72° triangle.
"""

from __future__ import annotations

import math

PARAMS = {"n": 1}
ANSWER = (1 + math.sqrt(5)) / 2
VARIANTS = [{"n": 2}, {"n": 3}, {"n": 7}, {"n": 9}]


def solve(n=1):
    lucas, fib = (2, 1), (0, 1)
    for _ in range(n):
        lucas, fib = (lucas[1], lucas[0] + lucas[1]), (fib[1], fib[0] + fib[1])
    return (lucas[0] + fib[0] * math.sqrt(5)) / 2


def check(n=1):
    return (math.sin(math.radians(72)) / math.sin(math.radians(36))) ** n
