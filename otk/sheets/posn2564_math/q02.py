"""ข้อ 2 — จำนวนจริง x ≠ 0 ที่สอดคล้องกับสมการรากที่สาม

จงหาจำนวนจริง x ≠ 0 ทั้งหมดที่สอดคล้องกับสมการ
(13+x)^(2/3) + 4(13−x)^(2/3) = 5(169 − x²)^(1/3)

Substituting u = (13+x)^(1/3) and v = (13−x)^(1/3) turns the equation into a
homogeneous quadratic, because 169 − x² = (13+x)(13−x) makes the right-hand side
5uv:

    u² + 4v² = 5uv   ⟺   (u − v)(u − 4v) = 0

**u = v gives x = 0 — which is exactly what the printed ``x ≠ 0`` throws away.**
The qualifier is not decoration; without it the item has two answers. The other
branch u = 4v gives 13 + x = 64(13 − x), so x = 13·63/65 = **63/5**.

For a general coefficient m (here 4) the factorisation is (u − v)(u − mv) with
right-hand side (m+1)uv, and the surviving root is x = c(m³ − 1)/(m³ + 1).

``solve`` evaluates that. ``check`` knows nothing about the substitution: it
scans the printed function over (−c, c) and bisects every sign change, then
discards anything at x = 0.
"""

from __future__ import annotations

from fractions import Fraction

#: (c+x)^(2/3) + m(c−x)^(2/3) = (m+1)(c²−x²)^(1/3)
PARAMS = {"c": 13, "m": 4}
ANSWER = Fraction(63, 5)
TOL = 1e-7
VARIANTS = [
    {"c": 13, "m": 2},
    {"c": 7, "m": 4},
    {"c": 26, "m": 4},
    {"c": 9, "m": 3},
    {"c": 5, "m": 8},
    {"c": 13, "m": 1},      # u = v twice: only x = 0, which is excluded
]


def solve(c=13, m=4):
    """c(m³ − 1)/(m³ + 1), the root of the u = m·v branch."""
    if c <= 0 or m <= 0:
        return None
    cube = m ** 3
    if cube == 1:
        return None          # both branches collapse to x = 0
    return Fraction(c) * Fraction(cube - 1, cube + 1)


def _f(x, c, m):
    """The printed expression, left side minus right side."""
    left = (c + x) ** (2 / 3) + m * (c - x) ** (2 / 3)
    return left - (m + 1) * (c * c - x * x) ** (1 / 3)


def check(c=13, m=4):
    """Independent: scan the printed equation for sign changes and bisect.

    No substitution, no factorisation — just the function as written, sampled
    across the interval where both cube roots are of non-negative arguments. The
    ``value == 0`` case is tested before the bracketing one, since a sample that
    lands on a root exactly makes ``prev * cur < 0`` false.
    """
    if c <= 0 or m <= 0:
        return None
    steps = 4000
    roots: list[float] = []
    previous = None
    for i in range(1, steps):
        x = -c + 2 * c * i / steps
        value = _f(x, c, m)
        if value == 0.0:
            roots.append(x)
        elif previous is not None and previous[1] * value < 0:
            lo, hi = previous[0], x
            for _ in range(200):
                mid = (lo + hi) / 2
                if _f(mid, c, m) * _f(lo, c, m) <= 0:
                    hi = mid
                else:
                    lo = mid
            roots.append((lo + hi) / 2)
        previous = (x, value)

    kept = []
    for r in sorted(roots):
        if abs(r) < 1e-6:
            continue                       # the excluded x = 0
        if not kept or abs(r - kept[-1]) > 1e-6:
            kept.append(r)
    if len(kept) != 1:
        return None
    return kept[0]
