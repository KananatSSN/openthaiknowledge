"""ข้อ 2 — f : ℕ → ℕ ที่ f(2m + 2n) = f(m)f(n)

f(m)f(n) depends only on m + n, so f(1)f(n) = f(2)f(n − 1) and f is geometric:
f(n) = f(1)r^(n−1); then f(2m + 2n) = f(m)f(n) forces r = 1 and f ≡ 1. The
solver returns f(k) for a geometric f (the source's f(1) = 1, r = 1: f(10) = 1).

``check`` builds the values from f(n) = f(2)f(n − 1)/f(1) one step at a time and
confirms f(2m + 2n) = f(m)f(n) on a range when r = 1.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"first": 1, "ratio": 1, "k": 10}
ANSWER = 1
VARIANTS = [{"first": 3, "ratio": 2, "k": 5}, {"first": 2, "ratio": 5, "k": 3}, {"k": 1}]


def solve(first=1, ratio=1, k=10):
    return first * ratio ** (k - 1)


def check(first=1, ratio=1, k=10):
    values = [None, Fraction(first), Fraction(first * ratio)]
    while len(values) <= max(k, 30):
        values.append(values[2] * values[-1] / values[1])
    if first == 1 and ratio == 1:
        assert all(values[2 * m + 2 * n] == values[m] * values[n] for m in range(1, 7) for n in range(1, 7))
    return values[k]
