"""ข้อ 26 — ค่าของ a + b เมื่อ a มากที่สุดและ b น้อยที่สุดในเซต X

กำหนดให้ X = { |x−3| + |x−5| + |x−8| : −3 ≤ x ≤ 10 }  ถ้า a เป็นสมาชิกในเซต X
ที่มีค่ามากที่สุด และ b เป็นสมาชิกในเซต X ที่มีค่าน้อยที่สุด แล้วค่าของ a + b
เท่ากับเท่าใด

f(x) = Σ|x − pᵢ| is convex and piecewise linear, so on a closed interval

* its **minimum** is at the median of the points, pushed to the nearer end of the
  interval if the median falls outside it;
* its **maximum** is at one of the two endpoints — never inside.

For the points 3, 5, 8 the median is 5, giving 2 + 0 + 3 = 5, and the endpoints
give f(−3) = 6 + 8 + 11 = 25 and f(10) = 7 + 5 + 2 = 14. So a = 25, b = 5 and

    a + b = **30**.

The trap is answering with 5 + 14: the maximum is at the *far* endpoint, and which
end that is depends on where the points sit, not on which end is larger.
"""

from __future__ import annotations

from fractions import Fraction

#: the three points inside the absolute values, and the interval for x.
PARAMS = {"points": (3, 5, 8), "lo": -3, "hi": 10}
ANSWER = 30
VARIANTS = [
    {"points": (1, 2, 6), "lo": 0, "hi": 10},
    {"points": (3, 5, 8), "lo": 4, "hi": 6},       # median inside, tight interval
    {"points": (3, 5, 8), "lo": 6, "hi": 20},      # median outside: min at lo
    {"points": (-4, 0, 9), "lo": -10, "hi": 10},
    {"points": (2, 2, 2), "lo": -5, "hi": 5},      # all three coincide
    {"points": (3, 5, 8), "lo": 7, "hi": 2},       # empty interval
]


def _f(x, points) -> Fraction:
    return sum((abs(Fraction(x) - p) for p in points), Fraction(0))


def solve(points=(3, 5, 8), lo=-3, hi=10):
    """max + min of a convex piecewise-linear sum of distances on [lo, hi]."""
    if lo > hi:
        return None
    median = sorted(points)[len(points) // 2]
    best = _f(min(max(median, lo), hi), points)         # clamped to the interval
    worst = max(_f(lo, points), _f(hi, points))
    total = worst + best
    return int(total) if total.denominator == 1 else total


def check(points=(3, 5, 8), lo=-3, hi=10):
    """Independent: scan the interval on a fine rational grid and take both ends.

    Nothing here knows the function is convex or where its median is. The grid
    step divides 1, and every breakpoint is an integer, so the extremes are hit
    exactly rather than approached.
    """
    if lo > hi:
        return None
    step = Fraction(1, 8)
    values = []
    x = Fraction(lo)
    while x <= hi:
        values.append(_f(x, points))
        x += step
    values.append(_f(hi, points))
    total = max(values) + min(values)
    return int(total) if total.denominator == 1 else total
