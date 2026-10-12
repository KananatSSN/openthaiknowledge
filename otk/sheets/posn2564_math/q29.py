"""ข้อ 29 — จำนวนสมาชิกของเซต A ของเศษส่วนอย่างต่ำที่มี ab = 30!

ให้ A เป็นเซตของจำนวนตรรกยะ r = a/b ทั้งหมด ที่อยู่ระหว่าง 0 และ 1 โดย a, b
เป็นจำนวนเต็มบวก ซึ่ง ห.ร.ม. ของ a และ b เท่ากับ 1 และ ab = 30·29·28⋯3·2·1
จงหาจำนวนสมาชิกของ A

Coprimality is a very strong condition here: if a prime p divides the product
ab = 30!, then **all** of its copies must go to the same side, since a and b share
no factor. So a coprime factorisation is just a choice, for each *distinct* prime
of 30!, of which side it lands on — and the multiplicities never matter at all.

There are 10 primes at most 30 (2, 3, 5, 7, 11, 13, 17, 19, 23, 29), giving 2¹⁰
ordered factorisations; the condition 0 < r < 1 keeps exactly half of them, since
a ≠ b always (30! is not a square — 29 appears once). So |A| = 2⁹ = **512**.

``solve`` counts the primes and returns 2^(ω−1) — it never builds 30!. ``check``
does build it, then walks all 2^ω subsets, forms the actual a and b as big
integers, and verifies gcd(a,b) = 1, a·b = 30! and a < b for each one it counts.
"""

from __future__ import annotations

from math import gcd

#: ab = n! with a/b in lowest terms and 0 < a/b < 1.
PARAMS = {"n": 30}
ANSWER = 512
VARIANTS = [
    {"n": 10},
    {"n": 20},
    {"n": 4},
    {"n": 2},
    {"n": 50},
    {"n": 1},          # 1! = 1 has no prime at all: a = b = 1, and r = 1
]


def _primes_upto(n):
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            for multiple in range(p * p, n + 1, p):
                sieve[multiple] = False
    return [p for p in range(2, n + 1) if sieve[p]]


def solve(n=30):
    """2^(ω−1), where ω is the number of distinct primes at most n."""
    if n < 1:
        return None
    omega = len(_primes_upto(n))
    if omega == 0:
        return 0               # 1! = 1 gives only a/b = 1, which is excluded
    return 2 ** (omega - 1)


def check(n=30):
    """Independent: build every coprime split of n! and count the ones below 1.

    The factorial is formed as an integer and each subset of its primes is
    assembled into an actual numerator with the full multiplicity; every counted
    pair is verified against all three printed conditions — coprime, product
    equal to n!, and strictly between 0 and 1.
    """
    if n < 1:
        return None
    if n > 200:
        return None
    primes = _primes_upto(n)
    if len(primes) > 20:
        return None

    factorial = 1
    for k in range(2, n + 1):
        factorial *= k

    powers = []
    for p in primes:
        power, k = 1, p
        while k <= n:
            power *= p ** (n // k)
            k *= p
        powers.append(power)

    count = 0
    for mask in range(1 << len(primes)):
        a = 1
        for i, power in enumerate(powers):
            if mask >> i & 1:
                a *= power
        b, rest = divmod(factorial, a)
        if rest or gcd(a, b) != 1 or a * b != factorial:
            continue
        if 0 < a < b:
            count += 1
    return count
