"""ข้อ 14 — ห.ร.ม. ของ 5²⁵⁴⁷ − 1 กับ 5²⁰⁰⁴ − 1

a^m − 1 ≡ a^(m−n) − 1 (mod a^n − 1), so the exponents run the Euclidean
algorithm: the gcd is a^gcd(m, n) − 1 = 5³ − 1 = 124.

``check`` takes the gcd of the two integers themselves.
"""

from __future__ import annotations

from math import gcd

PARAMS = {"a": 5, "m": 2547, "n": 2004}
ANSWER = 124
VARIANTS = [{"a": 2, "m": 12, "n": 18}, {"a": 3, "m": 35, "n": 21}, {"a": 7, "m": 64, "n": 40}, {"m": 2550}]


def solve(a=5, m=2547, n=2004):
    return a ** gcd(m, n) - 1


def check(a=5, m=2547, n=2004):
    return gcd(a**m - 1, a**n - 1)
