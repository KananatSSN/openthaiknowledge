"""ข้อ 10 — xy³/(x + y) เป็นกำลังสามของจำนวนเฉพาะ

For the family x·yᵏ/(x + y) = pᵏ: x = du, y = dv with gcd(u, v) = 1 gives
dᵏuvᵏ = pᵏ(u + v), so uvᵏ | pᵏ and u + v | dᵏ; only u = 1, v = p survives,
with dᵏ = p + 1, which needs p = 2ᵏ − 1 and d = 2. The source (k = 3) gives
x = 2, y = 14 (p = 7).

``check`` tries every x, y up to 2^(k+1) + 40 and keeps the pairs whose quotient
is the k-th power of a prime.
"""

from __future__ import annotations

PARAMS = {"k": 3}
ANSWER = (2, 14)
VARIANTS = [{"k": 2}, {"k": 5}, {"k": 7}]


def solve(k=3):
    p = 2**k - 1
    assert p > 1 and all(p % d for d in range(2, int(p**0.5) + 1))
    return (2, 2 * p)


def _is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n**0.5) + 1))


def _kth_root(n, k):
    r = round(n ** (1 / k))
    for c in (r - 1, r, r + 1):
        if c > 0 and c**k == n:
            return c
    return None


def check(k=3):
    limit = 2 ** (k + 1) + 40
    found = []
    for x in range(1, limit):
        for y in range(1, limit):
            num = x * y**k
            if num % (x + y):
                continue
            p = _kth_root(num // (x + y), k)
            if p and _is_prime(p):
                found.append((x, y))
    assert len(found) == 1
    return found[0]
