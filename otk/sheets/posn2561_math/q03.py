"""ข้อ 3 — จำนวนนับที่น้อยที่สุดที่มีตัวประกอบ 60 จำนวน

จงหาจำนวนนับที่น้อยที่สุดที่มีตัวประกอบทั้งหมด 60 จำนวน และเป็นตัวประกอบเฉพาะที่
แตกต่างกันเพียงสามจำนวน

For ``n = p^a q^b r^c`` the divisor count is ``(a+1)(b+1)(c+1)``, so the exponent
pattern must be one of the ways to write 60 as a product of three factors, each
at least 2:

    60 = 2·2·15 = 2·3·10 = 2·5·6 = 3·4·5

The primes should be 2, 3, 5 — the three smallest — and the **larger exponents
belong on the smaller primes**, since swapping a bigger exponent onto a bigger
prime can only increase the product. That gives four candidates:

    2¹⁴·3·5    = 245760
    2⁹·3²·5    = 23040
    2⁵·3⁴·5    = 12960
    2⁴·3³·5²   = **10800**

and the last one wins: ``(4+1)(3+1)(2+1) = 60`` divisors, three distinct primes.
The nearly-balanced split beats the lopsided ones, which is the opposite of what
"make the exponent large" instinct suggests.

``solve`` enumerates the factorisations and pairs the sorted exponents with the
sorted primes. ``check`` does not sort: it tries **every permutation** of the
exponents against the primes, so the descending-order argument is verified rather
than assumed, and for small targets it also scans the integers directly.
"""

from __future__ import annotations

from itertools import permutations

#: how many divisors, over how many distinct primes.
PARAMS = {"divisors": 60, "primes": 3}
ANSWER = 10800
VARIANTS = [
    {"divisors": 12, "primes": 3},
    {"divisors": 60, "primes": 2},
    {"divisors": 36, "primes": 3},
    {"divisors": 24, "primes": 2},
    {"divisors": 30, "primes": 4},        # 30 needs a factor 1: impossible
    {"divisors": 1, "primes": 3},
]
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23)


def _splits(total: int, parts: int):
    """Every non-increasing tuple of ``parts`` factors ≥ 2 with that product."""
    if parts == 1:
        if total >= 2:
            yield (total,)
        return
    factor = 2
    while factor ** parts <= total:
        if total % factor == 0:
            for rest in _splits(total // factor, parts - 1):
                if rest[0] >= factor:
                    yield (factor,) + rest
        factor += 1


def solve(divisors=60, primes=3):
    """Smallest n with that many divisors over exactly that many primes."""
    if divisors < 2 or primes < 1 or primes > len(SMALL_PRIMES):
        return None
    best = None
    for split in _splits(divisors, primes):
        exponents = sorted((f - 1 for f in split), reverse=True)
        value = 1
        for prime, exponent in zip(SMALL_PRIMES, exponents):
            value *= prime ** exponent
        best = value if best is None else min(best, value)
    return best


def check(divisors=60, primes=3):
    """Independent: try every prime-to-exponent matching, and scan when small.

    The exponents are paired with the primes in all ``primes!`` orders rather
    than sorted into place, so the "big exponent on the small prime" step is
    tested. When the winner is small enough the integers up to it are also swept
    directly, counting divisors by trial division.
    """
    if divisors < 2 or primes < 1 or primes > len(SMALL_PRIMES):
        return None
    best = None
    for split in _splits(divisors, primes):
        for order in permutations(f - 1 for f in split):
            value = 1
            for prime, exponent in zip(SMALL_PRIMES, order):
                value *= prime ** exponent
            best = value if best is None else min(best, value)
    if best is None:
        return None

    if best <= 3 * 10 ** 5:
        def profile(n: int):
            count, distinct, rest, factor = 1, 0, n, 2
            while factor * factor <= rest:
                power = 0
                while rest % factor == 0:
                    rest //= factor
                    power += 1
                if power:
                    count *= power + 1
                    distinct += 1
                factor += 1
            if rest > 1:
                count *= 2
                distinct += 1
            return count, distinct

        for n in range(2, best):
            if profile(n) == (divisors, primes):
                return n            # a smaller one would mean the argument fails
    return best
