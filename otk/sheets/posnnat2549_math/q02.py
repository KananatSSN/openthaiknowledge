"""ข้อ 2 — รัศมีวงกลมที่มีจุดศูนย์กลางบน BC และสัมผัส AB, AC (AB = 2, CA = 3, BC = 4)

The centre is the foot of the bisector from A; splitting ABC there gives
Δ = r(AB + AC)/2, and Heron gives Δ = 3√15/4, so r = 3√15/10.

``check`` places B, C on the x-axis, finds the bisector foot by the angle
bisector theorem and measures its distance to line AB.
"""

from __future__ import annotations

import math

PARAMS = {"a": 4, "b": 3, "c": 2}
ANSWER = 3 * math.sqrt(15) / 10
VARIANTS = [{"a": 7, "b": 3, "c": 9}, {"a": 5, "b": 5, "c": 6}, {"a": 13, "b": 12, "c": 5}, {"a": 3, "b": 4, "c": 5}]


def solve(a=4, b=3, c=2):
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return 2 * area / (b + c)


def check(a=4, b=3, c=2):
    x = (c * c - b * b + a * a) / (2 * a)
    apex = (x, math.sqrt(c * c - x * x))  # B = (0, 0), C = (a, 0)
    foot = (a * c / (b + c), 0.0)
    return abs(apex[0] * foot[1] - apex[1] * foot[0]) / math.hypot(*apex)
