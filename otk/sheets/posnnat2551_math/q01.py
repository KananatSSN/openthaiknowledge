"""ข้อ 1 — cos∠CAE เมื่อ ∠BAC = 90°, ∠ABC = 60° และ BE : EC = 3 : 2

With A at the origin, AB = 1 on the x-axis and AC = tan B on the y-axis,
E = (q, p·tan B)/(p + q) for BE : EC = p : q, so
cos∠CAE = p·tan B/√(q² + p² tan² B) = 3√3/√31.

``check`` builds the triangle with B at 60° from side lengths, places E on BC
and measures the angle with a dot product.
"""

from __future__ import annotations

import math

PARAMS = {"angle_b": 60, "p": 3, "q": 2}
ANSWER = 3 * math.sqrt(3) / math.sqrt(31)
VARIANTS = [{"angle_b": 45, "p": 1, "q": 4}, {"angle_b": 30, "p": 2, "q": 5}, {"p": 1, "q": 1}]


def solve(angle_b=60, p=3, q=2):
    tan_b = math.tan(math.radians(angle_b))
    return p * tan_b / math.sqrt(q * q + p * p * tan_b * tan_b)


def check(angle_b=60, p=3, q=2):
    bc = 7.0
    ab = bc * math.cos(math.radians(angle_b))
    ac = bc * math.sin(math.radians(angle_b))
    b, c = (ab, 0.0), (0.0, ac)  # A at the origin
    e = ((q * b[0] + p * c[0]) / (p + q), (q * b[1] + p * c[1]) / (p + q))
    return (c[0] * e[0] + c[1] * e[1]) / (math.hypot(*c) * math.hypot(*e))
