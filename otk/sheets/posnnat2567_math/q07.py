"""ข้อ 7 — จำนวนผลเฉลย (z₁, …, zₘ) ที่ Σ zₖ⁷ = n

z³ − 2z² + 2z − 1 = (z − 1)(z² − z + 1), roots 1 and ω, ω̄ with ω = e^(iπ/3), and
ω⁷ = ω. With a ones and b, c of ω, ω̄: the sum is real only if b = c, then
a + b = n and a + 2b = m, so b = m − n, a = 2n − m and the count is
m!/((m − n)!²(2n − m)!) (5, 3: 30).

``check`` runs over all 3ᵐ tuples of the roots numerically and counts those
whose seventh-power sum is n.
"""

from __future__ import annotations

from cmath import exp, pi
from itertools import product
from math import factorial

PARAMS = {"m": 5, "n": 3}
ANSWER = 30
VARIANTS = [{"m": 4, "n": 2}, {"m": 6, "n": 4}, {"m": 7, "n": 4}, {"m": 3, "n": 3}]


def solve(m=5, n=3):
    return factorial(m) // (factorial(m - n) ** 2 * factorial(2 * n - m))


def check(m=5, n=3):
    roots = [1, exp(1j * pi / 3), exp(-1j * pi / 3)]
    for z in roots:
        assert abs(z**3 - 2 * z * z + 2 * z - 1) < 1e-12
    return sum(1 for tup in product(roots, repeat=m) if abs(sum(z**7 for z in tup) - n) < 1e-9)
