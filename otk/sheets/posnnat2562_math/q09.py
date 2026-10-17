"""ข้อ 9 — รูปทับแก้วมีจำนวนเหลี่ยมได้มากสุดเท่าใด (รูป 2019 เหลี่ยม)

A triangle has its vertices on some regular n-gon iff each angle is a multiple
of π/n (inscribed angles). So every corner of the dissected polygon is at most
(n − 1)π/n, and (m − 2)π ≤ m(n − 1)π/n gives m ≤ 2n. For odd n the regular
2n-gon fanned from its centre uses triangles with angles π/n and (n − 1)π/2n
twice, which are allowed. The answer is 2n (2019: 4038).

``check`` finds the largest m with (m − 2)·n ≤ m·(n − 1) by counting up, then
builds the fan of the regular m-gon and confirms each triangle's angles, in units
of π/n, are positive integers.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"n": 2019}
ANSWER = 4038
VARIANTS = [{"n": 3}, {"n": 5}, {"n": 7}, {"n": 101}]


def solve(n=2019):
    assert n % 2 == 1 and n >= 3
    return 2 * n


def check(n=2019):
    m = 3
    while (m + 1 - 2) * n <= (m + 1) * (n - 1):
        m += 1
    # fan of the regular m-gon from its centre: apex 2π/m, base angles (π − 2π/m)/2
    apex = Fraction(2, m) * n  # in units of π/n
    base = (1 - Fraction(2, m)) / 2 * n
    assert apex.denominator == 1 and base.denominator == 1 and apex > 0 and base > 0
    assert apex + 2 * base == n
    return m
