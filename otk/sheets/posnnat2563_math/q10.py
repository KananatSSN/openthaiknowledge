"""ข้อ 10 — พหุนาม P ที่ P(n) | n! + 2 ทุกจำนวนเต็มบวก n

For the family P(n) | n! + K for all n ≥ s: a prime p | P(m) divides P(m + jp),
so p | (m + jp)! + K for all large j, forcing p | K; so P's values have bounded
prime support and bounded size, and P is constant. A constant d works iff
d | n! + K for every n ≥ s, i.e. d | gcd(s!, K). The source (s = 1, K = 2)
gives gcd(1, 2) = 1: P = ±1. The answer is the sorted tuple of the constants.

``check`` takes the gcd of n! + K over n = s..s + 40 directly and lists ±d.
"""

from __future__ import annotations

from math import factorial, gcd

PARAMS = {"start": 1, "offset": 2}
ANSWER = (-1, 1)
VARIANTS = [{"start": 3, "offset": 2}, {"start": 4, "offset": 12}, {"start": 5, "offset": 30}]


def solve(start=1, offset=2):
    g = gcd(factorial(start), offset)
    divisors = [d for d in range(1, g + 1) if g % d == 0]
    return tuple(sorted([-d for d in divisors] + divisors))


def check(start=1, offset=2):
    g = 0
    for n in range(start, start + 41):
        g = gcd(g, factorial(n) + offset)
    return tuple(sorted(s * d for d in range(1, g + 1) if g % d == 0 for s in (1, -1)))
