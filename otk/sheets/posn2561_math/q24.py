"""ข้อ 24 — ค่า r² จากเส้นตัดวงกลมสองเส้นที่ทำมุมกัน

จากรูป วงกลมมีรัศมี r หน่วย AB = 8 หน่วย, CD = 5 หน่วย, BP = 6 หน่วย และ ∠APD = 60°
จงหาค่าของ r²

**Read off the figure:** both lines from P are *secants*, each meeting the circle
twice, with B nearer P than A on one and C nearer P than D on the other.

The power of the point does the first half. PA = PB + AB = 6 + 8 = 14, so

    power = PB · PA = 84 = PC · PD = PC(PC + 5)  ⟹  PC = 7, PD = 12

The second half is where the 60° enters. The foot of the perpendicular from the
centre to a chord is its midpoint, so the centre's projections onto the two rays
are at ``(6 + 14)/2 = 10`` and ``(7 + 12)/2 = 9.5``. Putting P at the origin with
one ray along the x-axis and the other at θ,

    O·u₁ = 10  ⟹  Oₓ = 10        O·u₂ = 9.5  ⟹  10cos60° + O_y sin60° = 9.5

so O_y = 4.5/(√3/2) = 3√3 and PO² = 100 + 27 = 127. Finally the power is also
``PO² − r²``:

    r² = 127 − 84 = **43**

(Sanity: the half-chords then come out as √(43 − 27) = 4 and √(43 − 36.75) = 2.5,
which are half of 8 and half of 5.)

``solve`` follows that. ``check`` has never heard of the power of a point: it
puts B and A on one ray, slides C along the other, takes the circle through the
three points each time, and bisects on the position of C until the *fourth*
point D lands on that circle at the printed distance. Then it reports the
circle's own radius.
"""

from __future__ import annotations

from fractions import Fraction
from math import cos, hypot, radians, sin

#: PB = bp, BA = ab along one secant; CD = cd along the other; ∠APD = angle.
PARAMS = {"ab": 8, "cd": 5, "bp": 6, "angle": 60}
ANSWER = 43
TOL = 1e-6
VARIANTS = [
    {"ab": 6, "cd": 4, "bp": 4, "angle": 45},
    {"ab": 8, "cd": 5, "bp": 6, "angle": 90},
    {"ab": 10, "cd": 3, "bp": 2, "angle": 30},
    {"ab": 5, "cd": 5, "bp": 5, "angle": 60},
    {"ab": 8, "cd": 5, "bp": 6, "angle": 20},
    {"ab": 8, "cd": 5, "bp": 6, "angle": 0},      # the two secants coincide
]


def _snap(value: float):
    if abs(value - round(value)) < 1e-7:
        return int(round(value))
    close = Fraction(value).limit_denominator(64)
    return close if abs(float(close) - value) < 1e-9 else value


def solve(ab=8, cd=5, bp=6, angle=60):
    """Power of the point for the second secant, then the two chord midpoints."""
    if ab <= 0 or cd < 0 or bp <= 0 or not 0 < angle < 180:
        return None
    power = bp * (bp + ab)
    near = (-cd + (cd * cd + 4 * power) ** 0.5) / 2        # PC
    far = near + cd                                        # PD
    theta = radians(angle)
    foot_one = (bp + bp + ab) / 2
    foot_two = (near + far) / 2
    height = (foot_two - foot_one * cos(theta)) / sin(theta)
    return _snap(foot_one * foot_one + height * height - power)


def check(ab=8, cd=5, bp=6, angle=60):
    """Independent: fit the circle through three of the points and slide the fourth.

    B and A sit on the x-axis at distances bp and bp + ab. C is placed at
    distance s along the second ray and the circle through A, B, C is
    constructed from its perpendicular bisectors; the residual is how far D — at
    distance s + cd along the same ray — misses that circle. Bisecting on s
    finds the configuration the sheet drew, and the answer is the fitted
    circle's radius, measured back to all four points.
    """
    if ab <= 0 or cd < 0 or bp <= 0 or not 0 < angle < 180:
        return None
    theta = radians(angle)
    direction = (cos(theta), sin(theta))
    b_pt = (float(bp), 0.0)
    a_pt = (float(bp + ab), 0.0)
    midline = (bp + bp + ab) / 2            # the centre's x, from chord AB

    def centre(s: float):
        c_pt = (s * direction[0], s * direction[1])
        # |O − B| = |O − C| with O = (midline, y) — linear in y
        denominator = 2 * (c_pt[1] - b_pt[1])
        if abs(denominator) < 1e-12:
            return None
        numerator = (c_pt[0] ** 2 + c_pt[1] ** 2 - b_pt[0] ** 2 - b_pt[1] ** 2
                     - 2 * midline * (c_pt[0] - b_pt[0]))
        return midline, numerator / denominator

    def residual(s: float) -> float | None:
        origin = centre(s)
        if origin is None:
            return None
        d_pt = ((s + cd) * direction[0], (s + cd) * direction[1])
        return (hypot(d_pt[0] - origin[0], d_pt[1] - origin[1])
                - hypot(b_pt[0] - origin[0], b_pt[1] - origin[1]))

    lo, hi, previous = None, None, None
    steps = 4000
    span = 4 * (bp + ab) + 4 * cd + 4
    for i in range(1, steps + 1):
        s = span * i / steps
        value = residual(s)
        if value is None:
            previous = None
            continue
        if value == 0.0:
            lo = hi = s
            break
        if previous is not None and previous[1] * value < 0:
            lo, hi = previous[0], s
            break
        previous = (s, value)
    if lo is None:
        return None

    for _ in range(200):
        if lo == hi:
            break
        mid = (lo + hi) / 2
        value = residual(mid)
        if value is None:
            return None
        if value == 0.0:
            lo = hi = mid
            break
        if residual(lo) * value <= 0:
            hi = mid
        else:
            lo = mid
    s = (lo + hi) / 2

    origin = centre(s)
    if origin is None:
        return None
    points = [a_pt, b_pt, (s * direction[0], s * direction[1]),
              ((s + cd) * direction[0], (s + cd) * direction[1])]
    radii = [hypot(p[0] - origin[0], p[1] - origin[1]) for p in points]
    if max(radii) - min(radii) > 1e-6 * max(1.0, max(radii)):
        return None
    return _snap(sum(r * r for r in radii) / 4)
