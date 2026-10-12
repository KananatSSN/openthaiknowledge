"""ข้อ 15 — ผลบวกของสัมประสิทธิ์ของ P(x) จาก P(x−1) + P(x+1) = x³

กำหนดให้ P(x) เป็นพหุนามโดยที่ P(x−1) + P(x+1) = x³ สำหรับทุกจำนวนจริง x
จงหาผลบวกของสัมประสิทธิ์ของ P(x)

The sum of the coefficients is P(1) — that is the whole reason the question is
asked this way. Writing P(x) = ax³ + bx² + cx + d and using

    (x−1)³ + (x+1)³ = 2x³ + 6x        (x−1)² + (x+1)² = 2x² + 2

the left-hand side is ``2a x³ + 2b x² + (6a + 2c)x + (2b + 2d)``, so

    2a = 1,   2b = 0,   6a + 2c = 0,   2b + 2d = 0

giving a = ½, b = 0, c = −3/2, d = 0 and

    P(1) = ½ + 0 − 3/2 + 0 = **−1**

The operator ``P ↦ P(x−1) + P(x+1)`` kills every odd-order cross term, which is
why the system is triangular in steps of two and never needs a matrix.

``check`` never writes down a coefficient. It treats the equation as the
recurrence ``P(k+1) = k^power − P(k−1)``, which propagates the two unknowns
α = P(1) and β = P(0) along the odd and even integers, and then imposes what
being a polynomial of degree ``power`` means — that the (power+1)-st finite
difference vanishes — at two consecutive windows. Two linear equations, two
unknowns, and α is the answer.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

#: P(x−1) + P(x+1) = x^power.
PARAMS = {"power": 3}
ANSWER = Fraction(-1)
VARIANTS = [
    {"power": 1},
    {"power": 2},
    {"power": 4},
    {"power": 5},
    {"power": 0},
    {"power": 6},
]


def solve(power=3):
    """Match coefficients from the top down; the system is triangular."""
    if power < 0:
        return None
    coefficients = [Fraction(0)] * (power + 1)
    for m in range(power, -1, -1):
        wanted = Fraction(1) if m == power else Fraction(0)
        for j in range(m + 2, power + 1, 2):
            wanted -= 2 * coefficients[j] * comb(j, m)
        coefficients[m] = wanted / 2
    return sum(coefficients)


def check(power=3):
    """Independent: the recurrence, plus "a polynomial has no (n+1)-st difference".

    ``P(k+1) = k^power − P(k−1)`` carries α = P(1) and β = P(0) up the integers,
    each value staying an affine expression ``const + p·α + q·β``. A polynomial of
    degree ``power`` has vanishing (power+1)-st finite difference, and imposing
    that at the windows starting at 0 and at 1 gives two equations. Nothing here
    ever names a coefficient of P.
    """
    if power < 0:
        return None
    order = power + 1
    values = [(Fraction(0), Fraction(0), Fraction(1)),      # P(0) = β
              (Fraction(0), Fraction(1), Fraction(0))]      # P(1) = α
    while len(values) < order + 2:
        k = len(values) - 1                                  # P(k+1) = k^p − P(k−1)
        const, alpha, beta = values[k - 1]
        values.append((Fraction(k) ** power - const, -alpha, -beta))

    def difference(start: int) -> tuple[Fraction, Fraction, Fraction]:
        out = [Fraction(0), Fraction(0), Fraction(0)]
        for i in range(order + 1):
            weight = (-1) ** (order - i) * comb(order, i)
            for slot, part in enumerate(values[start + i]):
                out[slot] += weight * part
        return tuple(out)

    (c1, a1, b1), (c2, a2, b2) = difference(0), difference(1)
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return None
    # a1·α + b1·β = −c1 and a2·α + b2·β = −c2
    return (-c1 * b2 + c2 * b1) / determinant
