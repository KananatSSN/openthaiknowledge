"""วันที่สอง ข้อ 6 — Σ((2a − b)/(a − b))² ≥ 5  (พิสูจน์)

With p = a/(a − b), q = b/(b − c), r = c/(c − a): (2a − b)/(a − b) = 1 + p and
(p − 1)(q − 1)(r − 1) = pqr, so pq + qr + rp = p + q + r − 1 and the sum is
(p + q + r)² + 5 ≥ 5. The solver returns S² + 5 for a given triple
(a, b, c = 1, 2, 4 gives 49/9).

``check`` adds the three squares directly.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"a": 1, "b": 2, "c": 4}
ANSWER = Fraction(49, 9)
VARIANTS = [{"a": -8, "b": 6, "c": 12}, {"a": 0, "b": 1, "c": -1}, {"a": 5, "b": 3, "c": 4}]


def solve(a=1, b=2, c=4):
    s = Fraction(a, a - b) + Fraction(b, b - c) + Fraction(c, c - a)
    return s * s + 5


def check(a=1, b=2, c=4):
    return sum(Fraction(2 * x - y, x - y) ** 2 for x, y in ((a, b), (b, c), (c, a)))
