"""ข้อ 10 — x อตรรกยะ ⇒ มี m, n ที่ 1/2555 < mx + n < 1/2012  (พิสูจน์)

Pigeonhole on the fractional parts of mx guarantees one in the window. The
solver returns the least m with the fractional part of m√d in the window,
decided exactly in integers (d = 2).

``check`` computes the fractional parts with 60-digit decimal arithmetic.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from math import isqrt

PARAMS = {"d": 2, "low_den": 2555, "high_den": 2012}
ANSWER = 6726
VARIANTS = [{"d": 3}, {"d": 7, "low_den": 1000, "high_den": 800}, {"d": 13, "low_den": 300, "high_den": 200}]


def solve(d=2, low_den=2555, high_den=2012):
    m = 1
    while True:
        k = isqrt(m * m * d)
        over_low = low_den * low_den * m * m * d > (low_den * k + 1) ** 2
        under_high = high_den * high_den * m * m * d < (high_den * k + 1) ** 2
        if over_low and under_high:
            return m
        m += 1


def check(d=2, low_den=2555, high_den=2012):
    getcontext().prec = 60
    root = Decimal(d).sqrt()
    low, high = Decimal(1) / low_den, Decimal(1) / high_den
    m = 1
    while True:
        frac = m * root - int(m * root)
        if low < frac < high:
            return m
        m += 1
