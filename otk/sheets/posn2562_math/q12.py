"""ข้อ 12 — เศษจากการหาร ((2^2562 · 3^2019)^2020)^2563 ด้วย 10

จงหาเศษจากการหาร ((2^2562 · 3^2019)^2020)^2563 ด้วย 10

The two nested exponents multiply through, so the number is

    2^(2562·2020·2563) · 3^(2019·2020·2563)   (mod 10)

and both last digits cycle with period 4: ``2, 4, 8, 6`` and ``3, 9, 7, 1``. Only
the exponents *modulo 4* matter, and both contain the factor **2020 ≡ 0 (mod 4)**
— so both exponents are ≡ 0, landing on the last entry of each cycle:

    2^(4k) ends in 6,   3^(4k) ends in 1,   6 · 1 = 6

so the remainder is **6**. Neither 2562 nor 2019 nor 2563 is ever needed; the
2020 in the middle settles it alone.

Note that ``2^0 = 1`` would end in 1, not 6 — the cycle argument needs the
exponent to be positive, which it is.

``solve`` reduces each exponent modulo the cycle length and multiplies.
``check`` never mentions cycles: it hands the whole thing to modular
exponentiation, which squares its way down from a ten-digit exponent.
"""

from __future__ import annotations

from math import prod

#: (base, exponent) pairs inside, the exponents applied outside, and the modulus.
PARAMS = {"bases": ((2, 2562), (3, 2019)), "outer": (2020, 2563), "mod": 10}
ANSWER = 6
VARIANTS = [
    {"bases": ((2, 2562), (3, 2019)), "outer": (2021, 2563), "mod": 10},
    {"bases": ((2, 1), (3, 1)), "outer": (1,), "mod": 10},
    {"bases": ((7, 13), (3, 5)), "outer": (11, 9), "mod": 10},
    {"bases": ((2, 2562), (3, 2019)), "outer": (2020, 2563), "mod": 100},
    {"bases": ((5, 4), (2, 3)), "outer": (7,), "mod": 10},
    {"bases": ((2, 0),), "outer": (5,), "mod": 10},          # the number is 1
]


def _cycle(base: int, mod: int) -> tuple[int, int]:
    """(offset, period) of base^k mod mod — where the powers start repeating."""
    seen: dict[int, int] = {}
    value, k = 1 % mod, 0
    while value not in seen:
        seen[value] = k
        value = value * base % mod
        k += 1
    return seen[value], k - seen[value]


def solve(bases=((2, 2562), (3, 2019)), outer=(2020, 2563), mod=10):
    """The remainder, by reducing each exponent modulo its own cycle length."""
    if mod <= 1 or not bases:
        return None
    multiplier = prod(outer) if outer else 1
    if multiplier < 0:
        return None
    result = 1
    for base, inner in bases:
        exponent = inner * multiplier
        offset, period = _cycle(base % mod, mod)
        if exponent < offset:
            reduced = exponent
        else:
            reduced = offset + (exponent - offset) % period
        result = result * pow(base, reduced, mod) % mod
    return result


def check(bases=((2, 2562), (3, 2019)), outer=(2020, 2563), mod=10):
    """Independent: raise the whole product with modular exponentiation.

    The exponents are multiplied out into a single ten-digit number and handed to
    three-argument ``pow``, which square-and-multiplies its way down. No cycle is
    computed and no periodicity is assumed — the only shared idea is that the
    modulus can be applied as you go.
    """
    if mod <= 1 or not bases:
        return None
    multiplier = 1
    for factor in outer:
        multiplier *= factor
    if multiplier < 0:
        return None
    result = 1
    for base, inner in bases:
        result = result * pow(base, inner * multiplier, mod) % mod
    return result
