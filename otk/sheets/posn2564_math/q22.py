"""ข้อ 22 — รัศมีของวงกลมที่มีคอร์ดตั้งฉากสองเส้น

ให้ O เป็นจุดศูนย์กลางของวงกลมวงหนึ่งซึ่งมีคอร์ด AB และ CD ตั้งฉากและตัดกันที่
จุด X ดังรูป ถ้า AB = 56 หน่วย, CD = 64 หน่วย และ OX = 28 หน่วย
แล้วรัศมีของวงกลมวงนี้ยาวกี่หน่วย

Drop a perpendicular from O to each chord. Because the chords are perpendicular
to *each other*, those two feet and O and X form a rectangle — so the distances
d₁ (to AB) and d₂ (to CD) are the legs of a right triangle with hypotenuse OX:

    OX² = d₁² + d₂²

and each distance comes from the chord it belongs to: d₁² = r² − (AB/2)²,
d₂² = r² − (CD/2)². Adding,

    28² = (r² − 28²) + (r² − 32²)   ⟹   2r² = 2592   ⟹   r = **36**

Note the coincidence that OX equals half of AB here is a red herring: the
formula never treats them as related.

``solve`` evaluates r = √((OX² + (AB/2)² + (CD/2)²)/2). ``check`` places the two
chords in coordinates for a candidate radius, measures the distance from the
centre to their crossing, and bisects on the radius until that distance is the
printed OX — so the rectangle argument is never used.
"""

from __future__ import annotations

import math

#: two perpendicular chords and the distance from the centre to their crossing.
PARAMS = {"ab": 56, "cd": 64, "ox": 28}
ANSWER = 36
TOL = 1e-7
VARIANTS = [
    {"ab": 6, "cd": 8, "ox": 5},
    {"ab": 16, "cd": 12, "ox": 10},
    {"ab": 30, "cd": 40, "ox": 25},
    {"ab": 56, "cd": 64, "ox": 40},
    {"ab": 56, "cd": 64, "ox": 100},     # X would fall outside the circle
    {"ab": 20, "cd": 20, "ox": 14},
]


def solve(ab=56, cd=64, ox=28):
    """r = √((OX² + (AB/2)² + (CD/2)²)/2)."""
    if min(ab, cd) <= 0 or ox < 0:
        return None
    half_a, half_b = ab / 2, cd / 2
    r_sq = (ox * ox + half_a * half_a + half_b * half_b) / 2
    if r_sq <= 0:
        return None
    r = math.sqrt(r_sq)
    # both chords must really fit, and X must be inside
    if r < half_a or r < half_b or ox >= r:
        return None
    return r


def _crossing(radius, ab, cd):
    """Distance from the centre to the crossing of the two chords, or None."""
    half_a, half_b = ab / 2, cd / 2
    if radius < half_a or radius < half_b:
        return None
    d1 = math.sqrt(radius * radius - half_a * half_a)    # centre to AB
    d2 = math.sqrt(radius * radius - half_b * half_b)    # centre to CD
    # AB horizontal at y = −d1, CD vertical at x = d2; they cross at (d2, −d1)
    return math.hypot(d2, d1)


def check(ab=56, cd=64, ox=28):
    """Independent: bisect the radius until the built crossing sits OX from O.

    Two chords of the given lengths are laid down perpendicular in coordinates —
    one horizontal, one vertical — and the distance from the centre to their
    intersection is measured. Growing the radius pushes that distance up
    monotonically, so a bisection finds the radius the stem describes.
    """
    if min(ab, cd) <= 0 or ox < 0:
        return None
    lo = max(ab, cd) / 2
    if _crossing(lo, ab, cd) is None:
        return None
    if _crossing(lo, ab, cd) > ox:
        return None                       # even the tightest circle is too big
    hi = lo
    for _ in range(200):
        hi *= 1.5
        got = _crossing(hi, ab, cd)
        if got is not None and got > ox:
            break
    else:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        got = _crossing(mid, ab, cd)
        if got is None:
            return None
        if got > ox:
            hi = mid
        else:
            lo = mid
    radius = (lo + hi) / 2
    if ox >= radius:
        return None
    return radius
