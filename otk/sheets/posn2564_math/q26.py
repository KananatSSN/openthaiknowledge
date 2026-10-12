"""ข้อ 26 — ค่า t ทั้งหมดที่อสมการเป็นจริงสำหรับทุกจำนวนจริง x

จงหาจำนวนจริง t ทั้งหมดที่ทำให้อสมการ  −2 < (2x² + tx − 3)/(x² + x + 2) < 3
เป็นจริงสำหรับทุกจำนวนจริง x

**The denominator is positive for every x** — its discriminant is 1 − 8 < 0 — so
each side of the inequality may be multiplied out without flipping, and each
becomes "this quadratic is positive everywhere", i.e. a discriminant condition:

    left:   2x² + tx − 3 > −2(x² + x + 2)  ⟺  4x² + (t+2)x + 1 > 0
            ⟺ (t+2)² < 16  ⟺  −6 < t < 2
    right:  2x² + tx − 3 <  3(x² + x + 2)  ⟺  x² + (3−t)x + 9 > 0
            ⟺ (3−t)² < 36  ⟺  −3 < t < 9

Both must hold, so **−3 < t < 2**. Note the strict inequalities matter at the
ends: at t = 2 the left quadratic touches zero, and equality is not allowed.

Checking the denominator first is the whole trick — if it could change sign, none
of this would follow.

``solve`` returns the interval from those two discriminants. ``check`` never
forms a discriminant: it evaluates the printed fraction on a dense grid of x for
a candidate t, refines the largest and smallest values by a local search (the
true extremes fall between grid points), and bisects on t to find the two
endpoints where the "for all x" property is lost.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: lo < (a·x² + t·x + c)/(x² + px + q) < hi, for all real x.
PARAMS = {"lo": -2, "hi": 3, "a": 2, "c": -3, "p": 1, "q": 2}
ANSWER = (Fraction(-3), Fraction(2))
TOL = 1e-5
VARIANTS = [
    {"lo": -2, "hi": 4},
    {"lo": -1, "hi": 3},
    {"lo": -3, "hi": 3},
    {"lo": -2, "hi": 3, "c": -1},
    {"lo": -2, "hi": 3, "p": 0, "q": 1},
    {"lo": 3, "hi": -2},          # empty band
]


def _bounds(lo, hi, a, c, p, q):
    """The two open t-intervals, as (low, high) pairs of floats."""
    out = []
    # (a − lo)x² + (t − lo·p)x + (c − lo·q) > 0 for all x
    for bound, sign in ((lo, 1), (hi, -1)):
        head = sign * (a - bound)
        tail = sign * (c - bound * q)
        shift = sign * (-bound * p)
        if head <= 0:
            return None               # not positive definite for any t
        # (t·sign + shift)² < 4·head·tail
        if tail <= 0:
            return None
        span = math.sqrt(4 * head * tail)
        centre = -shift
        out.append(((centre - span) * sign, (centre + span) * sign))
    lows = [min(pair) for pair in out]
    highs = [max(pair) for pair in out]
    return max(lows), min(highs)


def solve(lo=-2, hi=3, a=2, c=-3, p=1, q=2):
    """Intersect the two discriminant conditions."""
    if hi <= lo:
        return None
    if p * p - 4 * q >= 0:
        return None                   # the denominator changes sign
    got = _bounds(lo, hi, a, c, p, q)
    if got is None:
        return None
    low, high = got
    if high <= low:
        return None
    exact = []
    for value in (low, high):
        near = Fraction(value).limit_denominator(1000)
        exact.append(near if abs(float(near) - value) < 1e-9 else value)
    return tuple(exact)


def _refine(f, x, width=0.01, best=max):
    """Golden-section search for the extreme of ``f`` near ``x``.

    The grid only brackets an extreme; the true one sits between samples, and a
    grid point next to it misses its value by enough to move a bisected endpoint
    by ~1e-4. Refining locally is what a finer grid would cost 100× to approach.
    """
    sign = 1 if best is max else -1
    left, right = x - width, x + width
    ratio = (math.sqrt(5) - 1) / 2
    for _ in range(80):
        m1 = right - ratio * (right - left)
        m2 = left + ratio * (right - left)
        if sign * f(m1) > sign * f(m2):
            right = m2
        else:
            left = m1
    return f((left + right) / 2)


def _holds(t, lo, hi, a, c, p, q):
    """Is the printed inequality true for every x? Sampled, then refined."""
    def value(x):
        return (a * x * x + t * x + c) / (x * x + p * x + q)

    xs = [i / 100.0 for i in range(-6000, 6001)]
    if any(x * x + p * x + q <= 0 for x in xs):
        return False
    values = [value(x) for x in xs]
    top = _refine(value, xs[max(range(len(xs)), key=lambda i: values[i])], best=max)
    bottom = _refine(value, xs[min(range(len(xs)), key=lambda i: values[i])], best=min)
    return lo < bottom and top < hi


def check(lo=-2, hi=3, a=2, c=-3, p=1, q=2):
    """Independent: bisect on t for the two ends of the region where it holds.

    The inequality is *evaluated*, never rearranged — for a given t the fraction
    is sampled across a wide range of x and the "for all x" claim either survives
    or it does not. Bisecting that boolean on each side gives the endpoints.
    """
    if hi <= lo:
        return None
    if p * p - 4 * q >= 0:
        return None
    inside = None
    for i in range(-2000, 2001):
        t = i / 100.0
        if _holds(t, lo, hi, a, c, p, q):
            inside = t
            break
    if inside is None:
        return None

    ends = []
    for direction in (-1, 1):
        good, bad = inside, inside
        for _ in range(200):
            bad += direction * 0.5
            if not _holds(bad, lo, hi, a, c, p, q):
                break
        else:
            return None
        for _ in range(60):
            mid = (good + bad) / 2
            if _holds(mid, lo, hi, a, c, p, q):
                good = mid
            else:
                bad = mid
        ends.append((good + bad) / 2)
    return tuple(sorted(ends))
