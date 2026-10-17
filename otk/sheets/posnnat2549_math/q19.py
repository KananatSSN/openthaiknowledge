"""วันที่สอง ข้อ 1 — ผลคูณของจำนวนนับสามจำนวนเรียงกันไม่เป็นกำลังสองสมบูรณ์  (พิสูจน์)

n + 1 is coprime to n(n + 2) = (n + 1)² − 1, so both would have to be squares,
but n² < n(n + 2) < (n + 1)². The solver returns the least m making
m·n(n + 1)(n + 2) a square (the squarefree part, never 1); for n = 8:
720 = 2⁴·3²·5, so 5.

``check`` factors the product by trial division and multiplies the primes with
odd exponent; it also confirms the product is not a square.
"""

from __future__ import annotations

from math import isqrt

PARAMS = {"n": 8}
ANSWER = 5
VARIANTS = [{"n": 1}, {"n": 70}, {"n": 48}, {"n": 399}]


def solve(n=8):
    out = 1
    for x in (n, n + 1, n + 2):
        f = 2
        while f * f <= x:
            while x % (f * f) == 0:
                x //= f * f
            if x % f == 0:
                out *= f
                x //= f
            f += 1
        out *= x
    # merge repeated primes across the three factors
    f = 2
    while f * f <= out:
        while out % (f * f) == 0:
            out //= f * f
        f += 1
    return out


def check(n=8):
    value = n * (n + 1) * (n + 2)
    assert isqrt(value) ** 2 != value
    result, f = 1, 2
    while f * f <= value:
        e = 0
        while value % f == 0:
            value //= f
            e += 1
        if e % 2:
            result *= f
        f += 1
    return result * value
