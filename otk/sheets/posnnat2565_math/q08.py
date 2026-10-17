"""ข้อ 8 — a₁ ที่มีลำดับตรรกยะ aₙ₊₁² − aₙ₊₁ = aₙ

For the family with bₙ = aₙ + shift: if aₙ₊₁ = u/v in lowest terms, aₙ has
denominator v², so going back through an infinite rational sequence every term
is an integer. Integer successors exist only for aₙ = t(t − 1); above 2 the
terms strictly fall, and neither 0 nor 2 has an integer predecessor above 2,
so only the constant sequences 0 and 2 survive. The answer is the starts of b:
(shift, shift + 2) (the source, shift 0: a₁ = 0 or 2).

``check`` tries every rational start with denominator ≤ 4 in [−3, 8] and keeps
those with a rational successor chain twelve steps long.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

PARAMS = {"shift": 0}
ANSWER = (0, 2)
VARIANTS = [{"shift": 1}, {"shift": -3}, {"shift": 5}]


def solve(shift=0):
    return (shift, shift + 2)


def _rational_sqrt(q):
    if q < 0:
        return None
    n, d = isqrt(q.numerator), isqrt(q.denominator)
    if n * n == q.numerator and d * d == q.denominator:
        return Fraction(n, d)
    return None


def _successors(a):
    root = _rational_sqrt(1 + 4 * a)
    if root is None:
        return []
    return sorted({(1 + root) / 2, (1 - root) / 2})


def _survives(a, depth):
    if depth == 0:
        return True
    return any(_survives(b, depth - 1) for b in _successors(a))


def check(shift=0):
    starts = sorted({Fraction(n, d) for d in range(1, 5) for n in range(-3 * d, 8 * d + 1)})
    return tuple(a + shift for a in starts if _survives(a, 12))
