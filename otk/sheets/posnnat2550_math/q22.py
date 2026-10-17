"""วันที่สอง ข้อ 4 — จำนวนเฉพาะ p ที่ (2^(p−1) − 1)/p เป็นกำลังสองสมบูรณ์

For odd p, (2ʰ − 1)(2ʰ + 1) = p·k² with coprime factors (h = (p − 1)/2):
2ʰ + 1 = y² only for h = 3 (p = 7), and 2ʰ − 1 = y² only for h = 1 (p = 3).
The solver searches the primes below a bound for any base a (the proof covers
a = 2): (3, 7).

``check`` uses a different square test (binary search for the root) and a
different prime list (a sieve).
"""

from __future__ import annotations

from math import isqrt

PARAMS = {"a": 2, "bound": 60}
ANSWER = (3, 7)
VARIANTS = [{"a": 3}, {"a": 7}, {"a": 26}, {"a": 2, "bound": 200}]


def solve(a=2, bound=60):
    primes = [p for p in range(2, bound) if all(p % f for f in range(2, isqrt(p) + 1))]
    out = []
    for p in primes:
        if a % p:
            q = (a ** (p - 1) - 1) // p
            if isqrt(q) ** 2 == q:
                out.append(p)
    return tuple(out)


def check(a=2, bound=60):
    sieve = [True] * bound
    sieve[0:2] = [False, False]
    for i in range(2, bound):
        if sieve[i]:
            for j in range(i * i, bound, i):
                sieve[j] = False

    def is_square(q):
        lo, hi = 0, q + 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if mid * mid <= q:
                lo = mid
            else:
                hi = mid
        return lo * lo == q

    return tuple(p for p in range(bound) if sieve[p] and a % p and is_square((a ** (p - 1) - 1) // p))
