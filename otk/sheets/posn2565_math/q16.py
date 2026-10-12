"""ข้อ 16 — ผลบวกของคำตอบทั้งหมดของสมการ

จงหาผลบวกของคำตอบทั้งหมดของสมการ  (x² − x − 1)^(2x² − 11x + 15) = 1

A power equals 1 in exactly three ways, and all three contribute here:

* **exponent zero, base non-zero** — 2x² − 11x + 15 = 0 gives x = 5/2 and x = 3,
  and the base is 11/4 and 5 there, both non-zero;
* **base one** — x² − x − 1 = 1 gives x = 2 and x = −1, and any exponent will do;
* **base minus one with an even integer exponent** — x² − x − 1 = −1 gives x = 0
  and x = 1, but the exponent is 15 at x = 0 (odd, so the value is −1) and 6 at
  x = 1 (even ✓). Only x = 1 survives.

    5/2 + 3 + 2 + (−1) + 1 = **15/2**

Missing the third case entirely, or keeping both of its roots, are the two ways
this item is got wrong — the generator offers both sums as distractors.

``solve`` works with exact rationals and returns ``None`` if any of the three
quadratics has irrational roots, since "the sum of all solutions" is then not a
number the sheet's format can ask for.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

#: base x² + bx + c and exponent px² + qx + r.
PARAMS = {"b": -1, "c": -1, "p": 2, "q": -11, "r": 15}
ANSWER = Fraction(15, 2)
VARIANTS = [
    {"b": -1, "c": -1, "p": 1, "q": -5, "r": 6},
    {"b": -3, "c": 1, "p": 2, "q": -11, "r": 15},
    {"b": 0, "c": -2, "p": 1, "q": -3, "r": 2},
    {"b": -1, "c": -3, "p": 2, "q": -11, "r": 15},
    {"b": -1, "c": -1, "p": 1, "q": -1, "r": -1},    # irrational roots
]


def _roots(a, bb, cc):
    """Rational roots of a·x² + bb·x + cc, or None if any is irrational."""
    if a == 0:
        return [] if bb == 0 else [Fraction(-cc, bb)]
    disc = bb * bb - 4 * a * cc
    if disc < 0:
        return []
    root = isqrt(disc)
    if root * root != disc:
        return None
    return sorted({Fraction(-bb + s * root, 2 * a) for s in (1, -1)})


def solve(b=-1, c=-1, p=2, q=-11, r=15):
    """Sum of every x with (x² + bx + c)^(px² + qx + r) = 1."""
    def base(x):
        return x * x + b * x + c

    def expo(x):
        return p * x * x + q * x + r

    hits = set()
    for coeffs, keep in (
            ((p, q, r), lambda x: base(x) != 0),                 # exponent 0
            ((1, b, c - 1), lambda x: True),                      # base 1
            ((1, b, c + 1), lambda x: expo(x).denominator == 1
                                      and expo(x) % 2 == 0)):     # base -1
        found = _roots(*coeffs)
        if found is None:
            return None
        hits.update(x for x in found if keep(x))
    return sum(hits, Fraction(0))


def check(b=-1, c=-1, p=2, q=-11, r=15):
    """Independent: gather candidates numerically, then test the equation itself.

    Roots of the three defining quadratics are found by bisection rather than by
    the quadratic formula, a dense sweep looks for anything they might have
    missed, and every candidate is kept only if evaluating the *original* power
    really gives 1 — so the case analysis above is validated rather than assumed.
    """
    for quad in ((p, q, r), (1, b, c - 1), (1, b, c + 1)):
        if _roots(*quad) is None:
            return None

    def value(x: float):
        """(x²+bx+c)^(px²+qx+r) as a real number, or None where it is undefined."""
        bs = x * x + b * x + c
        ex = p * x * x + q * x + r
        if bs > 0:
            return bs ** ex
        if abs(bs) < 1e-12:
            return None if abs(ex) < 1e-12 else 0.0
        return bs ** round(ex) if abs(ex - round(ex)) < 1e-9 else None

    candidates: set[Fraction] = set()
    lo, hi, steps = -60.0, 60.0, 240_000
    for quad in ((p, q, r), (1, b, c - 1), (1, b, c + 1)):
        def f(x, quad=quad):
            return quad[0] * x * x + quad[1] * x + quad[2]
        prev = f(lo)
        for i in range(1, steps + 1):
            x = lo + (hi - lo) * i / steps
            cur = f(x)
            if cur == 0:
                candidates.add(Fraction(x).limit_denominator(10 ** 4))
            elif prev * cur < 0:
                a_, b_ = x - (hi - lo) / steps, x
                for _ in range(80):
                    mid = (a_ + b_) / 2
                    if f(a_) * f(mid) <= 0:
                        b_ = mid
                    else:
                        a_ = mid
                candidates.add(Fraction((a_ + b_) / 2).limit_denominator(10 ** 4))
            prev = cur

    hits = set()
    for cand in candidates:
        got = value(float(cand))
        if got is not None and abs(got - 1.0) < 1e-6:
            hits.add(cand)
    return sum(hits, Fraction(0))
