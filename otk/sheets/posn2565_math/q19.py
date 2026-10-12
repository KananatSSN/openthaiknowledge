"""ข้อ 19 — ค่าของ y − x

กำหนดให้ x, y เป็นจำนวนจริงซึ่งสอดคล้องกับสมการ
    x³ − y³ + 9x² + 12y² + 34x − 55y + 140 = 0
จงหาค่าของ y − x

Both halves are the *same* increasing cubic in disguise. Completing them,

    x³ + 9x² + 34x = (x+3)³ + 7(x+3) - 48
    y³ - 12y² + 55y = (y-4)³ + 7(y-4) + 92

and the loose constants −48 − 92 + 140 cancel exactly, so the equation is

    u³ + 7u = v³ + 7v,      u = x + 3,  v = y - 4.

t ↦ t³ + 7t is strictly increasing, hence injective, so u = v and

    y - x = 3 + 4 = **7**

for every solution — there are infinitely many (x, y) pairs and they all give the
same difference, which is why the question can ask for it.

In general the printed equation is the expansion of (x+p)³ + k(x+p) =
(y−q)³ + k(y−q), giving y − x = p + q; ``solve`` needs k ≥ 0 so the cubic really
is injective.
"""

from __future__ import annotations

from fractions import Fraction

#: (x+p)³ + k(x+p) = (y-q)³ + k(y-q)
PARAMS = {"p": 3, "q": 4, "k": 7}
ANSWER = 7
VARIANTS = [
    {"p": 1, "q": 1, "k": 2},
    {"p": 5, "q": 2, "k": 1},
    {"p": 0, "q": 6, "k": 12},
    {"p": 2, "q": 3, "k": 0},          # a plain cube: still injective
    {"p": 2, "q": 3, "k": -9},         # not monotone: u = v can fail
]


def coefficients(p=3, q=4, k=7):
    """The printed coefficients (x², y², x, y, constant) of the expansion."""
    return (3 * p, 3 * q, 3 * p * p + k, -(3 * q * q + k),
            p ** 3 + k * p + q ** 3 + k * q)


def solve(p=3, q=4, k=7):
    """y - x = p + q, because t³ + kt is injective for k ≥ 0."""
    if k < 0:
        return None
    return p + q


def check(p=3, q=4, k=7):
    """Independent: solve the printed equation for y at several x and subtract.

    The coefficients are expanded first, then for each x the cubic in y is solved
    by bisection on the equation *as printed*. No completion of cubes happens
    here — if the difference were not constant, these would disagree.
    """
    if k < 0:
        return None
    cx2, cy2, cx, cy, const = coefficients(p, q, k)

    def lhs(x: float, y: float) -> float:
        return (x ** 3 - y ** 3 + cx2 * x * x + cy2 * y * y
                + cx * x + cy * y + const)

    diffs = set()
    for x in (-7.0, -2.5, 0.0, 1.0, 4.5, 11.0):
        lo, hi = -1e4, 1e4
        if lhs(x, lo) * lhs(x, hi) > 0:
            return None
        for _ in range(200):
            mid = (lo + hi) / 2
            if lhs(x, lo) * lhs(x, mid) <= 0:
                hi = mid
            else:
                lo = mid
        y = (lo + hi) / 2
        assert abs(lhs(x, y)) < 1e-6 * max(1.0, abs(x) ** 3)
        diffs.add(Fraction(y - x).limit_denominator(10 ** 4))
    if len(diffs) != 1:
        return None
    value = next(iter(diffs))
    return int(value) if value.denominator == 1 else value
