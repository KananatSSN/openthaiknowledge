"""ข้อ 26 — ค่าของ x + y

ให้ x และ y เป็นจำนวนจริงบวกซึ่งสอดคล้องกับระบบสมการ
    x√y + y√x = √2
    x√x + y√y = 13√2
แล้ว x + y มีค่าเท่ากับเท่าใด

Substituting u = √x and v = √y turns both lines into symmetric functions:

    x√y + y√x = u²v + uv² = uv(u + v)
    x√x + y√y = u³ + v³ = (u + v)³ − 3uv(u + v)

so with s = u + v and P = uv the system is just ``Ps = √2`` and
``s³ − 3Ps = 13√2``. The second gives ``s³ = 13√2 + 3√2 = 16√2 = 2^{9/2}``,
hence ``s = 2^{3/2} = 2√2``, then ``P = √2 / (2√2) = 1/2`` and

    x + y = u² + v² = s² − 2P = 8 − 1 = **7**.

(u and v are real and positive: s² − 4P = 6 > 0.)

Generally, with ``x√y + y√x = a√2`` and ``x√x + y√y = b√2``, ``s³ = (b + 3a)√2``,
so ``s`` is rational-times-√2 exactly when ``b + 3a = 2t³``, giving ``s = t√2``,
``P = a/t`` and ``x + y = 2t² − 2a/t``. The sheet is t = 2, a = 1.

``solve`` uses that closed form. ``check`` never introduces u and v: it solves
the printed system numerically for (x, y) by a two-dimensional bisection and adds
the two numbers it finds.
"""

from __future__ import annotations

from fractions import Fraction
from math import sqrt

#: x√y + y√x = a√2 and x√x + y√y = b√2.
PARAMS = {"a": 1, "b": 13}
ANSWER = Fraction(7)
TOL = 1e-7
VARIANTS = [
    {"a": 2, "b": 10},
    {"a": 3, "b": 7},
    {"a": 1, "b": 51},          # t = 3: x + y = 52/3
    {"a": 6, "b": 36},
    {"a": 1, "b": 1},           # b + 3a = 4 is not 2t³
    {"a": 5, "b": 1},           # no positive pair at all
]


def shape(a=1, b=13):
    """(t, s = t√2, P) when the system has a nice closed form, else None."""
    if a <= 0 or b <= 0:
        return None
    total = b + 3 * a                      # s³ = total·√2
    if total % 2:
        return None
    cube = total // 2
    t = round(cube ** (1 / 3))
    for cand in (t - 1, t, t + 1):
        if cand > 0 and cand ** 3 == cube:
            t = cand
            break
    else:
        return None
    return t, Fraction(a, t)


def solve(a=1, b=13):
    """x + y = s² − 2uv, with s and uv read off the two symmetric equations."""
    got = shape(a, b)
    if got is None:
        return None
    t, p = got
    if 2 * t * t - 4 * p < 0:               # u and v would not be real
        return None
    return 2 * t * t - 2 * p


def check(a=1, b=13):
    """Independent: solve the printed system for (x, y) numerically and add them.

    No substitution is made. For each candidate x the first equation is solved
    for y by bisection (its left side is increasing in y), the residual of the
    *second* equation is tracked as x sweeps, and a sign change is bisected to
    the pair. The two roots x ≤ y are mirror images, so both are checked to give
    the same sum.
    """
    if a <= 0 or b <= 0:
        return None
    r2 = sqrt(2.0)
    first, second = a * r2, b * r2

    def y_of(x: float):
        """y > 0 with x√y + y√x = a√2, or None if the curve does not reach it."""
        lo, hi = 0.0, 1e6
        if x <= 0:
            return None
        if x * sqrt(hi) + hi * sqrt(x) < first:
            return None
        for _ in range(200):
            mid = (lo + hi) / 2
            if x * sqrt(mid) + mid * sqrt(x) < first:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    def residual(x: float):
        y = y_of(x)
        if y is None:
            return None
        return x * sqrt(x) + y * sqrt(y) - second

    sums = []
    lo, hi, steps = 1e-9, 400.0, 40_000
    prev = residual(lo)
    for i in range(1, steps + 1):
        x = lo + (hi - lo) * i / steps
        cur = residual(x)
        if cur is None or prev is None:
            prev = cur
            continue
        if prev * cur <= 0:
            left, right = x - (hi - lo) / steps, x
            for _ in range(200):
                mid = (left + right) / 2
                fl, fm = residual(left), residual(mid)
                if fl is None or fm is None:
                    break
                if fl * fm <= 0:
                    right = mid
                else:
                    left = mid
            root = (left + right) / 2
            partner = y_of(root)
            if partner is not None:
                sums.append(root + partner)
        prev = cur

    if not sums:
        return None
    if max(sums) - min(sums) > 1e-6:
        return None
    got = sum(sums) / len(sums)
    snapped = Fraction(got).limit_denominator(10 ** 4)
    return snapped if abs(float(snapped) - got) < 1e-7 else got
