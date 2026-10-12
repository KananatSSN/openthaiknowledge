"""ข้อ 28 — ค่ามากที่สุดที่เป็นไปได้ของ x + y (คำตอบเป็นจำนวนตรรกยะ)

กำหนดให้ x, y เป็นจำนวน**ตรรกยะ**ที่สอดคล้องกับสมการ
    x² + 8xy − 11y² − 16x + 8y + 16 = 0
จงหาค่ามากที่สุดที่เป็นไปได้ของ x + y

The word ตรรกยะ is the whole question — over the reals the curve is a hyperbola
and ``x + y`` is unbounded. Read it as a quadratic in x:

    x² + (8y − 16)x + (−11y² + 8y + 16) = 0

whose discriminant is

    (8y − 16)² − 4(−11y² + 8y + 16) = 108y² − 288y + 192 = **12(3y − 4)²**

— a perfect square trinomial times 12. For x to be rational that value must be a
rational square, and since 12 is not, the only way is ``3y − 4 = 0``. Then

    y = 4/3,  x = −(8·4/3 − 16)/2 = 8/3,  x + y = **4**

and there is exactly one rational point on the whole curve, so "the maximum" is
that single value.

In general, for ``x² + Bxy + Cy² + Dx + Ey + F = 0`` the discriminant in y is
``(B² − 4C)y² + (2BD − 4E)y + (D² − 4F)``. The item works precisely when that is
``k(py − q)²`` with k a non-square; when its leading coefficient *is* a rational
square there are infinitely many rational points and no maximum, which is what
``solve`` returns None for.

``check`` knows none of this: it sweeps rational y with small denominators, tests
whether the discriminant is a rational square, solves for x, verifies the printed
equation exactly, and keeps the largest sum it finds.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

#: x² + Bxy + Cy² + Dx + Ey + F = 0.
PARAMS = {"b": 8, "c": -11, "d": -16, "e": 8, "f": 16}
ANSWER = Fraction(4)
VARIANTS = [
    {"b": 6, "c": 3, "d": 6, "e": -6, "f": -15},
    {"b": 6, "c": -2, "d": -4, "e": -12, "f": 4},
    {"b": 0, "c": -8, "d": 10, "e": 16, "f": 17},
    {"b": 8, "c": 6, "d": 14, "e": 56, "f": 49},
    {"b": 0, "c": -3, "d": 0, "e": 0, "f": 0},        # only the origin is rational
    {"b": 0, "c": -1, "d": 0, "e": 0, "f": -4},       # leading term 4: a square
    {"b": 8, "c": -11, "d": -16, "e": 8, "f": 15},    # no longer a square trinomial
]


def _rational_sqrt(value: Fraction):
    """√value as a Fraction when it is one, else None."""
    if value < 0:
        return None
    n, d = value.numerator, value.denominator
    rn, rd = isqrt(n), isqrt(d)
    return Fraction(rn, rd) if rn * rn == n and rd * rd == d else None


def discriminant(b=8, c=-11, d=-16, e=8, f=16):
    """(A₂, A₁, A₀): the discriminant of the x-quadratic, as a quadratic in y."""
    return b * b - 4 * c, 2 * b * d - 4 * e, d * d - 4 * f


def solve(b=8, c=-11, d=-16, e=8, f=16):
    """The only rational x + y, when the discriminant is (non-square)·(linear)²."""
    a2, a1, a0 = discriminant(b, c, d, e, f)
    if a2 <= 0:
        return None
    if a1 * a1 != 4 * a2 * a0:            # not a perfect square trinomial in y
        return None
    if _rational_sqrt(Fraction(a2)) is not None:
        return None                       # a square: infinitely many points
    y = Fraction(-a1, 2 * a2)             # the single root of the trinomial
    x = -(Fraction(b) * y + d) / 2
    if x * x + b * x * y + c * y * y + d * x + e * y + f != 0:
        return None
    return x + y


def check(b=8, c=-11, d=-16, e=8, f=16, span=200, denom=40):
    """Independent: sweep rational y and keep every point that really is rational.

    For each y = n/m the discriminant is computed as a Fraction and tested for
    being a rational square; when it is, both roots x are formed, substituted
    back into the printed equation, and the sums collected. If more than the one
    expected point turns up — or if a whole family does — the search reports
    None rather than a maximum over its own window.
    """
    best, seen = None, 0
    for m in range(1, denom + 1):
        for n in range(-span, span + 1):
            y = Fraction(n, m)
            if y.denominator != m:                  # already met in lowest terms
                continue
            disc = (b * y + d) ** 2 - 4 * (c * y * y + e * y + f)
            root = _rational_sqrt(disc)
            if root is None:
                continue
            for sign in (1, -1):
                x = (-(b * y + d) + sign * root) / 2
                if x * x + b * x * y + c * y * y + d * x + e * y + f != 0:
                    continue
                seen += 1
                best = x + y if best is None else max(best, x + y)
    if best is None:
        return None
    if seen > 2:            # the two signs of a double root are the same point
        return None         # a genuine family: no maximum to report
    return best
