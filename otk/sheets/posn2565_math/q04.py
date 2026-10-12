"""ข้อ 4 — ค่าของ a + 2b + 3c

ถ้า a, b และ c เป็นจำนวนจริงซึ่งสอดคล้องกับระบบสมการ
    a + 3/b = 3,   b + 2/c = 2,   c + 1/a = 1
แล้ว a + 2b + 3c มีค่าเท่ากับเท่าใด

Walk the cycle backwards. The third equation gives c = r(a−1)/a for r = 1, the
second then gives b, and substituting into the first leaves a single equation in
a. Written out for the general constants p, q, r:

    c = r - r/a = r(a-1)/a
    b = q - q/c = q[(r-1)a - r] / (r(a-1))
    a + p/b = p  ⟹  b = p/(p-a)

so q[(r-1)a - r](p-a) = p·r·(a-1), a quadratic in a. For p = 3, q = 2, r = 1 the
(r−1) term vanishes and it collapses to a linear equation with a = −3, whence
c = 4/3, b = 1/2 and

    a + 2b + 3c = -3 + 1 + 4 = **2**.

At other constants the quadratic can have two roots, and then the question has
two answers unless both give the same combination — ``solve`` returns ``None``
in that case rather than picking one, so the generator's pool skips it.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

#: a + p/b = p, b + q/c = q, c + r/a = r; the answer is w1·a + w2·b + w3·c.
PARAMS = {"p": 3, "q": 2, "r": 1, "w1": 1, "w2": 2, "w3": 3}
ANSWER = Fraction(2)
VARIANTS = [
    {"p": 5, "q": 3, "r": 1},
    {"p": 2, "q": 4, "r": 1, "w1": 1, "w2": 1, "w3": 1},
    {"p": 3, "q": 2, "r": 2},
    {"p": 4, "q": 4, "r": 3},
    {"p": 3, "q": 2, "r": 1, "w1": 0, "w2": 0, "w3": 1},
    {"p": 0, "q": 2, "r": 1},                 # degenerate constant
]


def _roots(p, q, r):
    """Rational roots a of q[(r-1)a - r](p-a) = p·r·(a-1)."""
    # q[(r-1)a - r](p - a) = q[(r-1)pa - (r-1)a² - rp + ra]
    a2 = -q * (r - 1)
    a1 = q * ((r - 1) * p + r) - p * r
    a0 = -q * r * p + p * r
    if a2 == 0:
        if a1 == 0:
            return []
        return [Fraction(-a0, a1)]
    disc = a1 * a1 - 4 * a2 * a0
    if disc < 0:
        return []
    root = isqrt(disc)
    if root * root != disc:
        return []                              # irrational: not an exam answer
    return sorted({Fraction(-a1 + s * root, 2 * a2) for s in (1, -1)})


def solve(p=3, q=2, r=1, w1=1, w2=2, w3=3):
    """w1·a + w2·b + w3·c, when every solution of the system gives the same value."""
    if p <= 0 or q <= 0 or r <= 0:
        return None
    values = set()
    for a in _roots(p, q, r):
        if a in (0, 1, p):                     # b, c or the substitution blows up
            continue
        c = Fraction(r) * (a - 1) / a
        if c == 0:
            continue
        b = Fraction(q) - Fraction(q) / c
        if b == 0:
            continue
        values.add(w1 * a + w2 * b + w3 * c)
    if len(values) != 1:
        return None
    return next(iter(values))


def check(p=3, q=2, r=1, w1=1, w2=2, w3=3):
    """Independent: search a over the rationals and test the three equations as printed.

    No elimination and no quadratic. The first equation's residual is swept as a
    function of a, every sign change is bisected, each root is rationalised, and
    the triple is then verified against all three equations *exactly* — so a root
    that is really irrational is dropped rather than rounded into an answer.
    """
    if p <= 0 or q <= 0 or r <= 0:
        return None

    def residual(a: float):
        if a == 0:
            return None
        c = r - r / a
        if c == 0:
            return None
        b = q - q / c
        if b == 0:
            return None
        return a + p / b - p

    lo, hi = -60.0, 60.0
    steps = 240_000
    values = set()
    prev_x = lo
    prev = residual(prev_x)
    for i in range(1, steps + 1):
        x = lo + (hi - lo) * i / steps
        cur = residual(x)
        hit = cur == 0                      # the grid can land exactly on a root
        if hit or (prev is not None and cur is not None and prev * cur < 0):
            a, b_ = (x, x) if hit else (prev_x, x)
            for _ in range(0 if hit else 80):
                mid = (a + b_) / 2
                m = residual(mid)
                if m is None:
                    break
                if m * residual(a) <= 0:
                    b_ = mid
                else:
                    a = mid
            root = Fraction((a + b_) / 2).limit_denominator(10 ** 4)
            c = Fraction(r) - Fraction(r) / root if root else None
            if c:
                b = Fraction(q) - Fraction(q) / c
                if b and root + Fraction(p) / b == p and c + Fraction(r) / root == r:
                    values.add(w1 * root + w2 * b + w3 * c)
        prev, prev_x = cur, x
    if len(values) != 1:
        return None
    return next(iter(values))
