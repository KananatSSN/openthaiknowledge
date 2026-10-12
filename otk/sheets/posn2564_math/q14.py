"""ข้อ 14 — ผลรวมของ n สองหลักที่ nᵏ ลงท้ายเหมือน n เสมอ

จงหาผลรวมของจำนวนเต็มบวก n ทั้งหมด โดยที่ 10 ≤ n ≤ 99 และ nᵏ มีเลขสองหลักสุดท้าย
เหมือนกับ n สำหรับทุกๆ จำนวนเต็มบวก k

"For **every** k" sounds like infinitely many conditions, but k = 2 implies all
the rest: if n² ≡ n then multiplying by n repeatedly keeps it. So the condition
is n² ≡ n (mod 100), i.e. n(n − 1) ≡ 0 — the **automorphic** numbers.

Since 100 = 4·25 and consecutive integers are coprime, the Chinese remainder
theorem splits it: n ≡ 0 or 1 mod 4, and n ≡ 0 or 1 mod 25, four combinations
giving n ≡ 0, 1, 25, 76. Only 25 and 76 are two-digit, so the sum is **101**.

``solve`` builds those idempotents with CRT from the modulus's prime-power
factorisation — no search at all. ``check`` tests each n in the range directly,
raising it to many powers and comparing the last digits, which is the printed
condition rather than the reduction of it.
"""

from __future__ import annotations

from itertools import product

#: nᵏ ≡ n (mod `mod`) for all k, with lo ≤ n ≤ hi.
PARAMS = {"mod": 100, "lo": 10, "hi": 99}
ANSWER = 101
VARIANTS = [
    {"mod": 100, "lo": 1, "hi": 99},
    {"mod": 1000, "lo": 100, "hi": 999},
    {"mod": 10, "lo": 1, "hi": 9},
    {"mod": 16, "lo": 2, "hi": 15},
    {"mod": 100, "lo": 30, "hi": 99},
    {"mod": 1001, "lo": 10, "hi": 999},
]


def _factor(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def solve(mod=100, lo=10, hi=99):
    """Sum the idempotents of ℤ/mod that fall in the range.

    n² ≡ n (mod pᵃ) forces n ≡ 0 or 1 modulo each prime power, so the solutions
    are exactly the CRT combinations of those choices — 2^ω(mod) of them.
    """
    if mod < 2 or lo > hi:
        return None
    powers = [p ** e for p, e in _factor(mod).items()]
    total = 0
    for choice in product((0, 1), repeat=len(powers)):
        # CRT: build n with n ≡ choice[i] (mod powers[i])
        n, modulus = 0, 1
        for want, pk in zip(choice, powers):
            while n % pk != want:
                n += modulus
            modulus *= pk
        n %= mod
        if lo <= n <= hi:
            total += n
    return total


def check(mod=100, lo=10, hi=99):
    """Independent: test the printed condition on every n in the range."""
    if mod < 2 or lo > hi:
        return None
    if hi - lo > 200_000:
        return None
    total = 0
    for n in range(lo, hi + 1):
        if all(pow(n, k, mod) == n % mod for k in range(1, 60)):
            total += n
    return total
