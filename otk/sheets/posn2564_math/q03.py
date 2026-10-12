"""ข้อ 3 — ค่าของ m + k + a จากเส้นตรงสองเส้นและพาราโบลา

กำหนดให้ a, m, k เป็นจำนวนจริง ถ้าเส้นตรง y = x − 2a ผ่านจุด (2m, a) ที่อยู่ใน
จตุภาคที่ 3 และเส้นตรง y = 3x − 2k ตัดกับพาราโบลา y = −2x² + x − m + k + 6
ที่จุด (a, 2) จงหาค่าของ m + k + a

Three printed facts, three unknowns — but they resolve in a fixed order:

* (2m, a) on y = x − 2a gives a = 2m − 2a, so **m = 3a/2**;
* (a, py) on y = 3x − 2k gives **k = (3a − py)/2**;
* (a, py) on the parabola, after substituting both, collapses to

      2a² − a + (3·py/2 − const) = 0

The two roots at the sheet's constants are a = 3/2 and a = −1, and **จตุภาคที่ 3
is what picks the second**: the point is (2m, a) = (3a, a), which is in the third
quadrant exactly when a < 0. Then m + k + a = 4a − py/2 = **−5**.

``solve`` takes the negative root of that quadratic in exact arithmetic and
refuses any parameters that leave zero or two of them negative. ``check`` never
forms the quadratic: it sweeps a numerically and keeps the values at which all
three printed conditions hold simultaneously.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: the parabola is y = −2x² + x − m + k + const, and it meets the second line at
#: (a, py).
PARAMS = {"py": 2, "const": 6}
ANSWER = -5
TOL = 1e-7
VARIANTS = [
    {"py": 2, "const": 8},
    {"py": 4, "const": 9},
    {"py": 1, "const": 5},
    {"py": 6, "const": 12},
    {"py": 3, "const": 7},
    {"py": 2, "const": 1},      # both roots positive: no third-quadrant point
]


def _roots(py, const):
    """Roots of 2a² − a + (3·py/2 − const) = 0, exact when the disc is square."""
    tail = Fraction(3 * py, 2) - const
    disc = Fraction(1) - 8 * tail
    if disc < 0:
        return []
    num, den = disc.numerator, disc.denominator
    rn, rd = math.isqrt(num), math.isqrt(den)
    if rn * rn == num and rd * rd == den:
        root = Fraction(rn, rd)
    else:
        root = math.sqrt(float(disc))     # irrational: the answer is a float
    return [(1 + root) / 4, (1 - root) / 4]


def solve(py=2, const=6):
    """4a − py/2, at the unique root with a < 0."""
    roots = _roots(py, const)
    negative = [a for a in roots if a < 0]
    if len(negative) != 1:
        return None                       # จตุภาคที่ 3 must pick exactly one
    a = negative[0]
    value = 4 * a - Fraction(py, 2)
    if isinstance(value, Fraction):
        return int(value) if value.denominator == 1 else value
    return value


def check(py=2, const=6):
    """Independent: sweep a and keep the values where every printed fact holds.

    For each candidate a the two lines *define* m and k — the first from
    (2m, a) lying on y = x − 2a, the second from (a, py) lying on y = 3x − 2k —
    and the parabola condition is then simply evaluated, not solved. The third
    quadrant is tested on the point itself rather than as a sign rule on a.
    """
    def residual(a):
        m = 3 * a / 2
        k = (3 * a - py) / 2
        return py - (-2 * a * a + a - m + k + const)

    found: list[float] = []
    previous = None
    steps = 20000
    for i in range(steps + 1):
        a = -50.0 + 100.0 * i / steps
        value = residual(a)
        if value == 0.0:
            found.append(a)
        elif previous is not None and previous[1] * value < 0:
            lo, hi = previous[0], a
            for _ in range(200):
                mid = (lo + hi) / 2
                if residual(mid) * residual(lo) <= 0:
                    hi = mid
                else:
                    lo = mid
            found.append((lo + hi) / 2)
        previous = (a, value)

    admissible = []
    for a in found:
        m = 3 * a / 2
        if 2 * m < 0 and a < 0:           # the point (2m, a) is in quadrant 3
            if not admissible or abs(a - admissible[-1]) > 1e-9:
                admissible.append(a)
    if len(admissible) != 1:
        return None
    a = admissible[0]
    return 4 * a - py / 2
