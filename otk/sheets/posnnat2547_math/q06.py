"""ข้อ 6 — เศษจากการหาร f(x⁷) ด้วย f(x) = x⁶ + ⋯ + x + 1

f(x) divides xⁿ − 1 (n = 7), so x^(mk) ≡ x^(mk mod n). With g = gcd(m, n) each
multiple of g below n appears g times: the remainder is g(1 + x^g + ⋯ + x^(n−g)),
which is 0 when g = 1 and the constant n when g = n. The answer is the
remainder's coefficient tuple (constant term first): (7,).

``check`` does polynomial long division of f(x^m) by f(x).
"""

from __future__ import annotations

from math import gcd

PARAMS = {"n": 7, "m": 7}
ANSWER = (7,)
VARIANTS = [{"n": 7, "m": 3}, {"n": 6, "m": 4}, {"n": 8, "m": 12}, {"n": 5, "m": 15}]


def _trim(coeffs):
    coeffs = list(coeffs)
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return tuple(coeffs)


def solve(n=7, m=7):
    g = gcd(m, n)
    if g == 1:
        return (0,)
    if g == n:
        return (n,)
    out = [0] * n
    for j in range(n // g):
        out[j * g] = g
    return _trim(out)


def check(n=7, m=7):
    num = [0] * ((n - 1) * m + 1)
    for k in range(n):
        num[k * m] += 1
    den = [1] * n  # monic, degree n − 1
    while len(num) >= len(den):
        lead = num[-1]
        shift = len(num) - len(den)
        for i, c in enumerate(den):
            num[shift + i] -= lead * c
        num.pop()
    return _trim(num) if num else (0,)
