"""ข้อ 4 — เซตของ a ที่ทำให้ 2A + B ≥ 0

กำหนดให้ a เป็นจำนวนจริงบวก และให้
    A = a - a² + a³ - a⁴ + ⋯ + (-1)^(k+1)·a^k + ⋯ - a^2024
    B = a + a² + a³ + a⁴ + ⋯ + a^k + ⋯ + a^2024
จงหาเซตของจำนวนจริงบวก a ทั้งหมดที่ทำให้ 2A + B ≥ 0

Nothing here needs the geometric-series formula. Collect the two sums term by
term: a^k gets 2(-1)^(k+1) + 1, which is 3 for odd k and -1 for even k. Pairing
each odd term with the even one after it,

    2A + B = Σ_{j=1}^{1012} a^(2j-1)·(3 - a)

and every a^(2j-1) is positive, so the whole sum takes the sign of 3 - a. The
answer is 0 < a ≤ 3 — the top exponent never enters, as long as it is even.

Returned as the threshold 3 rather than as a set, so the harness can compare it.
``check`` sums the two series directly and bisects for the sign change.
"""

from __future__ import annotations

from fractions import Fraction

#: coefficients of A and B in the combination, and the top exponent.
PARAMS = {"ca": 2, "cb": 1, "top": 2024}
ANSWER = Fraction(3)
VARIANTS = [
    {"ca": 3, "cb": 1},                   # threshold 2
    {"ca": 5, "cb": 3},                   # threshold 4
    {"ca": 2, "cb": 1, "top": 10},        # the exponent is irrelevant
    {"ca": 4, "cb": 1},
    {"ca": 7, "cb": 2},
]
TOL = 1e-6


def solve(ca=2, cb=1, top=2024):
    """The largest a with ca·A + cb·B ≥ 0, or None when every a > 0 works.

    Odd powers carry ca + cb, even powers carry cb - ca, so the pairing gives
    a^(2j-1)·[(ca + cb) + (cb - ca)·a] and the bracket decides the sign.
    """
    if top % 2:
        raise ValueError("the series must end on an even power")
    if ca <= cb:
        return None                       # bracket never turns negative
    return Fraction(ca + cb, ca - cb)


def check(ca=2, cb=1, top=2024):
    """Independent: sum both series term by term and bisect the sign change."""
    def value(a: float) -> float:
        # A short top keeps this exact enough to bisect; the maths does not
        # depend on it (see VARIANTS), and 2024 terms of a>1 overflow a float.
        n = min(top, 40)
        A = sum((-1) ** (k + 1) * a ** k for k in range(1, n + 1))
        B = sum(a ** k for k in range(1, n + 1))
        return ca * A + cb * B

    lo, hi = 1e-6, 50.0
    if value(hi) >= 0:
        return None
    if value(lo) < 0:
        return Fraction(0)
    for _ in range(200):
        mid = (lo + hi) / 2
        if value(mid) >= 0:
            lo = mid
        else:
            hi = mid
    return Fraction(lo).limit_denominator(10 ** 6)
