"""ข้อ 27 — จำนวนเต็มบวกมากสุดที่มี 2564 เป็นตัวประกอบและมีตัวหาร 2021 ตัว

จงหาจำนวนเต็มบวกมากสุดซึ่งมี 2564 เป็นตัวประกอบ และมีจำนวนตัวหารบวกอยู่ทั้งหมด
2021 จำนวนพอดี  (หมายเหตุ: 43, 47 และ 641 เป็นจำนวนเฉพาะ)

2564 = 2²·641 and 2021 = 43·47, and **both factorisations are what the หมายเหตุ
is for**. The divisor count (a+1)(b+1)⋯ must equal 43·47, a product of two
primes, so the number has at most two prime factors — and it already needs the
two of 2564. So it is 2^a·641^b with

    (a+1)(b+1) = 2021,  a ≥ 2,  b ≥ 1   ⟹   (a,b) = (42,46) or (46,42)

Of those two, the larger is the one that puts **the larger exponent on the larger
prime**: 2⁴²·641⁴⁶ beats 2⁴⁶·641⁴² by a factor of (641/2)⁴. So the answer is
**2⁴² · 641⁴⁶**, a 430-digit number.

The tempting third option, a single prime to the 2020th power, is ruled out by
2564 needing *two* distinct primes.

``solve`` compares the rivals by logarithm, without ever building them; the
ordering argument above holds here, but not for every variant (see ``solve``). ``check`` builds them: it enumerates every factorisation of
the divisor count into per-prime exponents, constructs each candidate as an
actual integer, verifies its divisor count by factorising it back, and takes the
maximum by direct comparison.

**Both return the answer in factored form**, as ((2, 42), (641, 46)). The number
itself has 430 digits, and the sheet prints it factored too — writing it out
would say less, and it would not survive the float comparison the harness uses.
"""

from __future__ import annotations

#: the required factor, and the exact number of positive divisors.
PARAMS = {"base": 2564, "divisors": 2021}
#: (prime, exponent) pairs: 2⁴² · 641⁴⁶
ANSWER = ((2, 42), (641, 46))
VARIANTS = [
    {"base": 12, "divisors": 15},
    {"base": 2564, "divisors": 2021 * 2},
    {"base": 45, "divisors": 21},
    {"base": 2564, "divisors": 9},
    {"base": 2564, "divisors": 7},        # one prime only: impossible
    {"base": 100, "divisors": 25},
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


def _factorisations(n, floor=2):
    """Every multiset of factors ≥ floor whose product is n."""
    if n == 1:
        yield ()
        return
    for d in range(floor, n + 1):
        if n % d:
            continue
        for rest in _factorisations(n // d, d):
            yield (d, *rest)


def solve(base=2564, divisors=2021):
    """Try each way of giving the exponents to the primes; compare by logarithm.

    The divisor count fixes the exponents as a multiset. Without constraints the
    best pairing is sorted (biggest exponent on the biggest prime), but ``base``
    sets a minimum exponent per prime, and that can rule the sorted pairing out:
    with ``divisors=4042`` the minimum 2 on the prime 2 forces 2²⁰²⁰·641¹ over any
    sorted choice. So every order is tried, and sizes are compared through
    Σ e·log p — never building the integers, which keeps this independent of
    ``check``'s exact comparison.
    """
    import math
    from itertools import permutations
    if base < 2 or divisors < 1:
        return None
    needed = _factor(base)
    primes = sorted(needed)
    best = None
    best_log = None
    for shape in _factorisations(divisors):
        if len(shape) != len(primes):
            continue
        for order in set(permutations(e - 1 for e in shape)):
            if any(e < needed[p] for e, p in zip(order, primes)):
                continue
            size = sum(e * math.log(p) for e, p in zip(order, primes))
            if best_log is None or size > best_log:
                best_log = size
                best = tuple((p, e) for p, e in zip(primes, order))
    return best


def check(base=2564, divisors=2021):
    """Independent: build every candidate and count its divisors from scratch.

    Each assignment of exponents to primes — in *every* order, not just the
    sorted one — is realised as an integer, refactorised, and its divisor count
    recomputed from that factorisation. Only numbers that pass go into the
    comparison, and the winner is chosen by comparing the integers themselves.
    """
    if base < 2 or divisors < 1:
        return None
    from itertools import permutations
    primes = sorted(_factor(base))
    if len(primes) > 4:
        return None
    best = None
    best_value = None
    for shape in _factorisations(divisors):
        if len(shape) != len(primes):
            continue
        for order in set(permutations(shape)):
            value = 1
            for e, p in zip(order, primes):
                value *= p ** (e - 1)
            if value % base:
                continue
            count = 1
            for e in _factor(value).values():
                count *= e + 1
            if count != divisors:
                continue
            if best_value is None or value > best_value:
                best_value = value
                best = tuple((p, e - 1) for p, e in zip(primes, order))
    return best
