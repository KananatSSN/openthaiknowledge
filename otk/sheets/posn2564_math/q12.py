"""ข้อ 12 — ค่าของ a + 2/a เมื่อ (a³ + 8/a³)² = 9,025

กำหนดให้ a เป็นจำนวนจริงบวกที่สอดคล้องกับ (a³ + 8/a³)² = 9,025
จงหาค่าของ a + 2/a

Since a > 0, the inner bracket is positive and √9025 = 95, so a³ + 8/a³ = 95.
Cubing the wanted quantity t = a + 2/a produces exactly that bracket plus a
multiple of t itself:

    t³ = a³ + 3·a²·(2/a) + 3·a·(2/a)² + 8/a³ = (a³ + 8/a³) + 6t

so t³ − 6t − 95 = 0, whose only real root is **t = 5**. (It factors as
(t − 5)(t² + 5t + 19), and the quadratic has negative discriminant.)

In general, with 2 replaced by c the identity is t³ − 3c·t − s = 0 where
s = a³ + c³/a³ — the cube of a sum in disguise, never a substitution.

``solve`` finds the real root of that cubic in closed form. ``check`` goes back
to the printed equation: it solves a³ + c³/a³ = s for a itself by bisection and
evaluates a + c/a numerically, so the identity is never used.
"""

from __future__ import annotations

import math

#: (a³ + c³/a³)² = sq, with a > 0.
PARAMS = {"sq": 9025, "c": 2}
ANSWER = 5
TOL = 1e-7
VARIANTS = [
    {"sq": 2704, "c": 1},
    {"sq": 9025, "c": 1},
    {"sq": 1024, "c": 2},
    {"sq": 40000, "c": 3},
    {"sq": 400, "c": 1},
    {"sq": 0, "c": 2},          # a³ + 8/a³ = 0 is impossible for a > 0
]


def solve(sq=9025, c=2):
    """The real root of t³ − 3c·t − √sq = 0."""
    if sq <= 0 or c <= 0:
        return None
    s = math.sqrt(sq)
    if s < 2 * math.sqrt(c ** 3):
        return None            # AM–GM: a³ + c³/a³ cannot go below 2√(c³)
    # depressed cubic t³ + pt + q with p = −3c, q = −s
    p, q = -3.0 * c, -s
    disc = (q / 2) ** 2 + (p / 3) ** 3
    if disc < 0:
        return None            # three real roots: not the shape this item has
    root = math.cbrt(-q / 2 + math.sqrt(disc)) + math.cbrt(-q / 2 - math.sqrt(disc))
    return root


def check(sq=9025, c=2):
    """Independent: solve for a itself, then evaluate a + c/a.

    a³ + c³/a³ is decreasing on (0, √c] and increasing after, so the branch with
    a ≥ √c is bisected directly on the printed equation. The cube-of-a-sum
    identity plays no part.
    """
    if sq <= 0 or c <= 0:
        return None
    s = math.sqrt(sq)

    def f(a):
        return a ** 3 + c ** 3 / a ** 3 - s

    base = math.sqrt(c)
    if f(base) > 0:
        return None            # below the AM–GM floor: no such a
    lo, hi = base, base
    for _ in range(400):
        hi *= 1.05
        if f(hi) > 0:
            break
    else:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        if f(mid) * f(lo) <= 0:
            hi = mid
        else:
            lo = mid
    a = (lo + hi) / 2
    return a + c / a
