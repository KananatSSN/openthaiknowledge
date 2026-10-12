"""ข้อ 9 — เซตของ a ที่สมการมีคำตอบเป็นจำนวนจริงบวกอย่างน้อย 1 คำตอบ

จงหาเซตของจำนวนจริง a ทั้งหมดที่ทำให้สมการ  x² + 2(a+2)x + a + 14 = 0
มีคำตอบเป็นจำนวนจริงบวกอย่างน้อย 1 คำตอบ

Three cases, and the middle one is the trap:

* product a+14 < 0 — roots have opposite signs, one is positive. Always counts.
* product = 0 — a root at 0 and the other at -2(a+2) = 24 > 0. Counts.
* product > 0 — both roots share a sign, so they must both be positive: sum
  -2(a+2) > 0 needs a < -2, and the discriminant (a+5)(a-2) ≥ 0 needs a ≤ -5.

Together the three give exactly a ≤ -5. Note a ≥ 2 also has real roots, but both
are negative, so the discriminant alone is not the answer — that is the mistake
the item is built to catch.

Returned as the boundary -5. ``check`` scans a densely and actually solves the
quadratic each time.
"""

from __future__ import annotations

from fractions import Fraction

#: x² + 2(a + shift)x + (a + konst) = 0
PARAMS = {"shift": 2, "konst": 14}
ANSWER = Fraction(-5)
VARIANTS = [
    {"shift": 1, "konst": 6},
    {"shift": 3, "konst": 8},
    {"shift": 0, "konst": 5},
    {"shift": 2, "konst": 20},
    {"shift": 4, "konst": 30},
]
TOL = 1e-6


def _roots(a: float, shift: int, konst: int):
    b, c = 2 * (a + shift), a + konst
    disc = b * b - 4 * c
    if disc < 0:
        return []
    r = disc ** 0.5
    return [(-b + r) / 2, (-b - r) / 2]


def solve(shift=2, konst=14):
    """The largest a admitting a positive root — the set is (-∞, that].

    The discriminant is a² + (2·shift - 1)a + shift² - konst; its larger root is
    where "both roots real and both positive" starts to fail, and everything at
    or below it works.
    """
    b1 = 2 * shift - 1
    c1 = shift * shift - konst
    disc = b1 * b1 - 4 * c1
    if disc < 0:
        return None
    root = (-b1 - disc ** 0.5) / 2               # the smaller discriminant root
    return Fraction(root).limit_denominator(10 ** 6)


def check(shift=2, konst=14):
    """Independent: scan a and solve the quadratic, looking for a positive root."""
    def ok(a: float) -> bool:
        return any(r > 0 for r in _roots(a, shift, konst))

    lo, hi = -10 ** 4, 10 ** 4
    if not ok(lo):
        return None
    for _ in range(200):                          # bisect the boundary
        mid = (lo + hi) / 2
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return Fraction(lo).limit_denominator(10 ** 6)
