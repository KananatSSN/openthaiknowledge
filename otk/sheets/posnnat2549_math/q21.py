"""วันที่สอง ข้อ 3 — x − 1 หาร P(x) − Q(x)  (พิสูจน์)

At x = ω (ω³ = 1, ω ≠ 1) the right side vanishes and −ω − ω² = 1, so
2ωP(1) + Q(1) = 0, and likewise with ω²; subtracting gives P(1) = Q(1) = 0.
With P = x² + ax + u and Q = kx² + bx + v that forces a = −1 − u, b = −k − v; the
solver returns P(t) − Q(t) (u = −5, v = 9, k = 1, t = 6: 70).

``check`` finds a and b from the divisibility itself: the remainder of
2xP(x³) + Q(−x − x²) on division by 1 + x + x² is linear in (a, b), so it
computes the remainder at three points (a, b) and solves for the zero.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"u": -5, "v": 9, "k": 1, "t": 6}
ANSWER = 70
VARIANTS = [{"u": 3, "v": -2, "k": 2, "t": 5}, {"u": 0, "v": 4, "k": 3, "t": 9}, {"u": 7, "v": 1, "k": 4, "t": 2}]


def solve(u=-5, v=9, k=1, t=6):
    a, b = -1 - u, -k - v
    return (t * t + a * t + u) - (k * t * t + b * t + v)


def _poly_mul(p, q):
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return out


def _remainder(a, b, u, v, k):
    # 2x·P(x³) with P = x² + ax + u
    num = [Fraction(0)] * 8
    num[1] += 2 * u
    num[4] += 2 * a
    num[7] += 2
    # Q(y) with y = −x − x²
    y = [Fraction(0), Fraction(-1), Fraction(-1)]
    for coef, power in ((v, 0), (b, 1), (k, 2)):
        term = [Fraction(1)]
        for _ in range(power):
            term = _poly_mul(term, y)
        for i, c in enumerate(term):
            num[i] += coef * c
    den = [Fraction(1), Fraction(1), Fraction(1)]
    num = list(num)
    while len(num) >= 3:
        lead = num[-1]
        shift = len(num) - 3
        for i, c in enumerate(den):
            num[shift + i] -= lead * c
        num.pop()
    return num  # [r0, r1]


def check(u=-5, v=9, k=1, t=6):
    r00 = _remainder(0, 0, u, v, k)
    r10 = _remainder(1, 0, u, v, k)
    r01 = _remainder(0, 1, u, v, k)
    ca = [x - y for x, y in zip(r10, r00)]
    cb = [x - y for x, y in zip(r01, r00)]
    det = ca[0] * cb[1] - ca[1] * cb[0]
    a = (-r00[0] * cb[1] + r00[1] * cb[0]) / det
    b = (-ca[0] * r00[1] + ca[1] * r00[0]) / det
    return (t * t + a * t + u) - (k * t * t + b * t + v)
