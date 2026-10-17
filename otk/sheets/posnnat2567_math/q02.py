"""ข้อ 2 — (m⁵ + n)/(m² + n²) และ (m + n⁵)/(m² + n²) เป็นจำนวนเต็ม

Modulo D = m² + n², m² ≡ −n², so m⁵ + n ≡ n(1 + mn³) and m + n⁵ ≡ m(1 + nm³);
both vanishing forces gcd(m, n) = 1 and then D | 1 + mn³ and D | 1 + nm³, which
only m = n = 1 survives. The solver returns the two remainders (3, 7: the
reduced forms).

``check`` divides the fifth powers out directly and, once, searches m, n ≤ 60
for pairs with both remainders zero, asserting only (1, 1) appears.
"""

from __future__ import annotations

PARAMS = {"m": 3, "n": 7}
ANSWER = (18, 48)
VARIANTS = [{"m": 2, "n": 5}, {"m": 11, "n": 4}, {"m": 1, "n": 1}]


def solve(m=3, n=7):
    d = m * m + n * n
    return (n * (1 + m * n**3) % d, m * (1 + n * m**3) % d)


def check(m=3, n=7):
    hits = [(x, y) for x in range(1, 61) for y in range(1, 61)
            if (x**5 + y) % (x * x + y * y) == 0 and (x + y**5) % (x * x + y * y) == 0]
    assert hits == [(1, 1)]
    d = m * m + n * n
    return ((m**5 + n) % d, (m + n**5) % d)
