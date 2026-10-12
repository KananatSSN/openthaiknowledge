"""ข้อ 10 — ค่ามากที่สุดของ (x−y)z

ให้ x, y, z เป็นจำนวนเต็มบวก โดยที่
    x + z = r·y            (โจทย์: r = 3)
    x² + y² + z² = total   (โจทย์: total = 230)
ค่ามากที่สุดของ (x−y)z เท่ากับเท่าใด

Method: squaring the first equation turns the pair (x, z) into a sum and a
product, both known once y is fixed:
    x + z = r·y ,  xz = ((r²+1)·y² − total) / 2,
so x and z are the roots of a quadratic and only y has to be searched — over the
handful of values with y² ≤ total. The objective is not symmetric in x and z, so
both orderings are scored.

``check`` is the flat triple loop over every (x, y, z) with x² + y² + z² = total.
"""

from __future__ import annotations

import math

PARAMS = {"r": 3, "total": 230}
ANSWER = 35
VARIANTS = [
    {"total": 66},
    {"r": 2, "total": 54},
    {"r": 4, "total": 306},
    {"r": 3, "total": 100},        # no solution → None
    {"r": 1, "total": 12},
]


def solutions(r=3, total=230):
    """Every (x, y, z) of positive integers meeting both conditions."""
    out = []
    for y in range(1, math.isqrt(total) + 1):
        twice = (r * r + 1) * y * y - total
        if twice < 0 or twice % 2:
            continue
        prod, summed = twice // 2, r * y
        disc = summed * summed - 4 * prod
        if disc < 0:
            continue
        root = math.isqrt(disc)
        if root * root != disc or (summed + root) % 2:
            continue
        x, z = (summed + root) // 2, (summed - root) // 2
        if x > 0 and z > 0:
            out.append((x, y, z))
            if x != z:
                out.append((z, y, x))
    return out


def solve(r=3, total=230):
    """Largest (x−y)·z, or None when the system has no positive solution."""
    found = solutions(r, total)
    return max((x - y) * z for x, y, z in found) if found else None


def check(r=3, total=230):
    """Independent: enumerate every (x, y, z) directly."""
    best = None
    limit = math.isqrt(total)
    for x in range(1, limit + 1):
        for y in range(1, limit + 1):
            for z in range(1, limit + 1):
                if x + z == r * y and x * x + y * y + z * z == total:
                    value = (x - y) * z
                    best = value if best is None else max(best, value)
    return best
