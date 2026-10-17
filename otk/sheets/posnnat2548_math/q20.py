"""ข้อ 20 — ค่าสูงสุดของ ab^(1/2)c^(1/3)d^(1/4) เมื่อ 36a + 4b + 4c + 3d = 25

Weighted AM–GM with weights 1, 1/2, 1/3, 1/4 (W = 25/12): at the maximum each
cᵢxᵢ equals wᵢS/W, giving (a, b, c, d) = (1/3, 3/2, 1, 1) and the maximum
(1/3)√(3/2) = √6/6.

``check`` maximises numerically on the simplex of shares sᵢ = cᵢxᵢ/S by
coordinate search on the logarithm.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"coeffs": (36, 4, 4, 3), "total": 25}
ANSWER = math.sqrt(6) / 6
TOL = 1e-7
VARIANTS = [{"coeffs": (9, 37, 5, 17)}, {"total": 50}, {"coeffs": (1, 1, 1, 1), "total": 12}]

WEIGHTS = (1, Fraction(1, 2), Fraction(1, 3), Fraction(1, 4))


def solve(coeffs=(36, 4, 4, 3), total=25):
    w_total = sum(WEIGHTS)
    point = [w * total / (w_total * c) for w, c in zip(WEIGHTS, coeffs)]
    return math.prod(float(x) ** float(w) for x, w in zip(point, WEIGHTS))


def check(coeffs=(36, 4, 4, 3), total=25):
    def log_value(shares):
        return sum(float(w) * math.log(s * total / c) for w, s, c in zip(WEIGHTS, shares, coeffs))

    shares = [0.25] * 4
    step = 0.1
    best = log_value(shares)
    while step > 1e-12:
        improved = False
        for i in range(4):
            for j in range(4):
                if i != j and shares[j] > step:
                    trial = list(shares)
                    trial[i] += step
                    trial[j] -= step
                    value = log_value(trial)
                    if value > best:
                        shares, best, improved = trial, value, True
        if not improved:
            step /= 2
    return math.exp(best)
