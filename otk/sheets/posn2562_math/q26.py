"""ข้อ 26 — รากที่มีค่ามากที่สุดของสมการที่สอง

กำหนดให้ p เป็นจำนวนจริง และ r₁, r₂ เป็นรากทั้งสองของสมการ x² − 17x − 632 = p
แล้วรากที่มีค่ามากที่สุดของสมการ (x − r₁)(x − r₂) + p + 2 = 0 มีค่าเท่าใด

p never has to be known — it cancels. Since r₁ and r₂ are the roots of
``x² − 17x − (632 + p) = 0``, that quadratic *is* its own factorisation:

    (x − r₁)(x − r₂) = x² − 17x − 632 − p

so the second equation reads

    x² − 17x − 632 − p + p + 2 = 0   ⟹   x² − 17x − 630 = 0

The p's cancel exactly, and the discriminant is a perfect square:
``289 + 2520 = 2809 = 53²``, giving roots ``(17 ± 53)/2`` = 35 and −18. The
larger is **35**.

The shift of +2 is the only thing the second equation adds to the first — a
generated version keeps the structure by shifting the constant term by any
amount, and the answer stays rational exactly when ``b² − 4(c + shift)`` is a
perfect square.

``solve`` uses that cancellation. ``check`` refuses to: it picks several
different values of p, solves the first quadratic numerically for r₁ and r₂,
builds the second equation from those numbers, finds its largest root by
bisection, and only reports a value if every p gives the same one.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt, sqrt

#: x² + b·x + c = p defines the roots; the second equation adds ``shift``.
PARAMS = {"b": -17, "c": -632, "shift": 2}
ANSWER = 35
VARIANTS = [
    {"b": -17, "c": -632, "shift": 0},
    {"b": -10, "c": -100, "shift": 4},
    {"b": 6, "c": -40, "shift": -15},
    {"b": -3, "c": 0, "shift": -4},
    {"b": -17, "c": -632, "shift": 3},        # discriminant is no longer square
    {"b": 2, "c": 5, "shift": 0},             # no real root at all
]


def solve(b=-17, c=-632, shift=2):
    """Largest root of x² + bx + (c + shift) = 0 — p cancels out."""
    constant = c + shift
    disc = b * b - 4 * constant
    if disc < 0:
        return None
    root = isqrt(disc)
    if root * root != disc:
        return None                      # the sheet's format wants an exact value
    value = Fraction(-b + root, 2)
    return int(value) if value.denominator == 1 else value


def check(b=-17, c=-632, shift=2, probes=(0.0, 1.0, -7.5, 100.0, -63.25)):
    """Independent: build the second equation from real roots, for several p.

    For each probe value of p the first quadratic is solved numerically to get
    r₁ and r₂, the product ``(x − r₁)(x − r₂) + p + shift`` is evaluated as
    written, and its largest root is found by bisection on a bracket. The claim
    that the answer does not depend on p is tested, not assumed.
    """
    if b * b - 4 * (c + shift) < 0:
        return None
    answers = []
    for p in probes:
        disc = b * b - 4 * (c - p)
        if disc < 0:
            continue
        r1 = (-b - sqrt(disc)) / 2
        r2 = (-b + sqrt(disc)) / 2

        def second(x: float, r1=r1, r2=r2, p=p) -> float:
            return (x - r1) * (x - r2) + p + shift

        lo, hi = max(r1, r2), max(r1, r2) + 1.0
        guard = 0
        while second(hi) <= 0 and guard < 200:
            hi += max(1.0, abs(hi))
            guard += 1
        if second(lo) > 0 or second(hi) < 0:
            continue
        for _ in range(300):
            mid = (lo + hi) / 2
            if second(mid) <= 0:
                lo = mid
            else:
                hi = mid
        answers.append((lo + hi) / 2)
    if not answers:
        return None
    if max(answers) - min(answers) > 1e-6:
        return None
    got = sum(answers) / len(answers)
    snapped = Fraction(got).limit_denominator(4)
    if abs(float(snapped) - got) > 1e-6:
        return None
    return int(snapped) if snapped.denominator == 1 else snapped
