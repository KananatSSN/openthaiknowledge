"""ข้อ 5 — f((x + y + z)/3, (a + b + c)/3) = f(x, a)f(y, b)f(z, c)

For the family f(mean of m points) = k·Πf(points), required when the first
three points are not collinear: if f vanishes once it vanishes everywhere;
otherwise f(x)f(y)/f(0) depends only on x + y, so f/f(0) is a real character of
ℝ², positive on a divisible group, hence 1. So f is a constant c with
c = k·cᵐ. The source (m = 3, k = 1) gives f ≡ −1, 0, 1. The answer is the
sorted tuple of the constants.

``check`` tries every constant on a grid of quarters and every affine
f = px + qa + r with small integer coefficients against the equation at
non-collinear sample points, and returns the surviving constants (asserting no
non-constant candidate survives).
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

PARAMS = {"arity": 3, "coefficient": 1}
ANSWER = (-1.0, 0.0, 1.0)
TOL = 1e-12
VARIANTS = [{"arity": 4, "coefficient": 1}, {"arity": 3, "coefficient": 4}, {"arity": 5, "coefficient": -1}]


def solve(arity=3, coefficient=1):
    # c = 0, or c^(m − 1) = 1/k over the reals
    inverse = 1 / coefficient
    r = abs(inverse) ** (1 / (arity - 1))
    if (arity - 1) % 2:
        roots = {0.0, r if inverse > 0 else -r}
    else:
        roots = {0.0, r, -r} if inverse > 0 else {0.0}
    return tuple(sorted(roots))


def _samples(arity):
    base = [(Fraction(0), Fraction(0)), (Fraction(3), Fraction(1)), (Fraction(1), Fraction(4)),
            (Fraction(-2), Fraction(5)), (Fraction(7), Fraction(-3)), (Fraction(2), Fraction(2))]
    tuples = []
    for i in range(len(base)):
        pts = [base[(i + j) % len(base)] for j in range(arity)]
        (x1, a1), (x2, a2), (x3, a3) = pts[:3]
        if (x2 - x1) * (a3 - a1) != (x3 - x1) * (a2 - a1):
            tuples.append(pts)
    return tuples


def _ok(f, arity, coefficient):
    for pts in _samples(arity):
        mx = sum(p[0] for p in pts) / arity
        ma = sum(p[1] for p in pts) / arity
        prod = Fraction(coefficient)
        for x, a in pts:
            prod *= f(x, a)
        if f(mx, ma) != prod:
            return False
    return True


def check(arity=3, coefficient=1):
    found = []
    for c in [Fraction(v, 4) for v in range(-12, 13)]:
        if _ok(lambda x, a, c=c: c, arity, coefficient):
            found.append(c)
    for p, q, r in product(range(-2, 3), repeat=3):
        if p == q == 0:
            continue
        assert not _ok(lambda x, a, p=p, q=q, r=r: p * x + q * a + r, arity, coefficient)
    return tuple(sorted(found))
