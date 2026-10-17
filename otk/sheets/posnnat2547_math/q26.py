"""วันที่สอง ข้อ 5 — จำนวนเฉพาะ p ที่ p² + 2543 มีตัวหารน้อยกว่า 16 ตัว

For K ≡ 23 (mod 24) and p ≥ 5, p² ≡ 1 (mod 24), so N = p² + K is 24·m with
N ≥ 25 + K. If a prime ≥ 5 divides N, τ(N) ≥ 4·2·2 = 16; otherwise N = 2ᵃ3ᵇ
with (a + 1)(b + 1) < 16, and every such number is at most 192 < N. So only
p = 2 and p = 3 can work, and ``solve`` tests just those two: p = 2 gives
2547 = 3²·283 (6 divisors), p = 3 gives 2552 = 2³·11·29 (16 divisors).

``check`` searches every prime below 3000.
"""

from __future__ import annotations

PARAMS = {"k": 2543}
ANSWER = (2,)
VARIANTS = [{"k": 24 * 50 + 23}, {"k": 24 * 123 + 23}, {"k": 24 * 9 + 23}, {"k": 24 * 300 + 23}]


def _tau(n):
    count, f = 1, 2
    while f * f <= n:
        e = 0
        while n % f == 0:
            n //= f
            e += 1
        count *= e + 1
        f += 1
    return count * (2 if n > 1 else 1)


def solve(k=2543):
    return tuple(p for p in (2, 3) if _tau(p * p + k) < 16)


def check(k=2543):
    primes = [p for p in range(2, 3000) if all(p % f for f in range(2, int(p**0.5) + 1))]
    return tuple(p for p in primes if _tau(p * p + k) < 16)
