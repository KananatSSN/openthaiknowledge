"""วันที่สอง ข้อ 5 — ค่าเฉลี่ยจำนวนการจับมือ (ชาย m หญิง n)

Each of the m + n − 1 neighbouring pairs is same-sex with probability
(C(m, 2) + C(n, 2))/C(m + n, 2); by linearity the mean is
(m(m − 1) + n(n − 1))/(m + n). For m = 3, n = 4: 18/7.

``check`` lists every distinct line-up and averages the handshakes.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations

PARAMS = {"m": 3, "n": 4}
ANSWER = Fraction(18, 7)
VARIANTS = [{"m": 1, "n": 1}, {"m": 5, "n": 2}, {"m": 4, "n": 4}]


def solve(m=3, n=4):
    return Fraction(m * (m - 1) + n * (n - 1), m + n)


def check(m=3, n=4):
    rows = set(permutations("B" * m + "G" * n))
    total = sum(sum(1 for u, v in zip(r, r[1:]) if u == v) for r in rows)
    return Fraction(total, len(rows))
