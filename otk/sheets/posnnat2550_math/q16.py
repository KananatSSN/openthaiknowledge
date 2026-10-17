"""ข้อ 16 — จำนวนเต็มบวกน้อยสุดที่มีตัวหาร 24 ตัว

τ(n) = Π(eᵢ + 1): try every factorisation of d into factors ≥ 2, put the
largest exponents on the smallest primes, and take the least: 2³·3²·5 = 360.

``check`` scans n upward and counts divisors directly.
"""

from __future__ import annotations

PARAMS = {"d": 24}
ANSWER = 360
VARIANTS = [{"d": 6}, {"d": 12}, {"d": 16}, {"d": 30}]

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)


def solve(d=24):
    def patterns(rest, largest):
        if rest == 1:
            return [[]]
        out = []
        for f in range(min(rest, largest), 1, -1):
            if rest % f == 0:
                out += [[f] + tail for tail in patterns(rest // f, f)]
        return out

    best = None
    for pattern in patterns(d, d):
        value = 1
        for p, f in zip(PRIMES, pattern):
            value *= p ** (f - 1)
        best = value if best is None else min(best, value)
    return best


def check(d=24):
    n = 1
    while True:
        count = sum(2 if i * i != n else 1 for i in range(1, int(n**0.5) + 1) if n % i == 0)
        if count == d:
            return n
        n += 1
