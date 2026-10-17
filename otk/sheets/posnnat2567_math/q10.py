"""ข้อ 10 — ค่าสูงสุดของ abcd(a + b)(b + c)(c + d)(d + a) เมื่อ Σ∛ = 4

For the family ∛a + ∛b + ∛c + ∛d = 4s the product is homogeneous of degree 24 in
the cube roots, so the maximum is s²⁴ times the source's. Setting opposite cube
roots equal and optimising the remaining pair gives 4¹⁴/5¹⁰ ≈ 27.49, larger
than the symmetric point's 16. The solver returns 4¹⁴s²⁴/5¹⁰.

``check`` writes a = x³ (and so on) with x + y + z + w = 4s, scans a coarse grid
of the simplex, then refines the best point by a shrinking pattern search, and
returns the largest value found.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"scale": 1}
ANSWER = Fraction(268435456, 9765625)
VARIANTS = [{"scale": 2}, {"scale": 3}, {"scale": Fraction(1, 2)}]
TOL = 1e-8


def solve(scale=1):
    return Fraction(4**14, 5**10) * Fraction(scale) ** 24


def _value(x, y, z, w):
    a, b, c, d = x**3, y**3, z**3, w**3
    return a * b * c * d * (a + b) * (b + c) * (c + d) * (d + a)


def check(scale=1):
    s = float(scale)
    total = 4 * s
    steps = 24
    best, point = -1.0, None
    for i in range(1, steps):
        for j in range(1, steps - i):
            for k in range(1, steps - i - j):
                x, y, z = total * i / steps, total * j / steps, total * k / steps
                w = total - x - y - z
                v = _value(x, y, z, w)
                if v > best:
                    best, point = v, [x, y, z]
    step = total / steps
    while step > 1e-13 * s:
        improved = False
        for idx in range(3):
            for sign in (1, -1):
                trial = list(point)
                trial[idx] += sign * step
                w = total - sum(trial)
                if min(trial) > 0 and w > 0:
                    v = _value(*trial, w)
                    if v > best:
                        best, point, improved = v, trial, True
        if not improved:
            step /= 2
    return best
