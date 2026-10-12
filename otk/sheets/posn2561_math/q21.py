"""ข้อ 21 — ปริมาตรทรงกระบอกปิดที่เท่ากับพื้นที่ผิวทั้งก่อนและหลังการปรับ

ทรงกระบอกปิดอันหนึ่งมีปริมาตรเท่ากับพื้นที่ผิว หากเพิ่มความสูงขึ้น 50% และลดรัศมีลง 25%
พบว่าทรงกระบอกปิดอันใหม่ที่ได้ยังคงมีปริมาตรเท่ากับพื้นที่ผิว จงหาปริมาตรของทรงกระบอก
ปิดอันเริ่มต้น

"Volume equals surface area" for a closed cylinder is ``πr²h = 2πr² + 2πrh``,
i.e. after dividing by πr,

    rh = 2r + 2h                                        (1)

The same condition for the scaled cylinder (radius αr, height βh) is
``αβ·rh = 2αr + 2βh``. Substituting (1) into its left-hand side turns it into a
*ratio* equation with the size scaled out:

    αβ(2r + 2h) = 2αr + 2βh   ⟹   r·α(β − 1) = h·β(1 − α)

    t = r/h = β(1 − α) / (α(β − 1))

For α = 3/4 and β = 3/2 that is (3/2·1/4)/(3/4·1/2) = 1, so **r = h**. Feeding
t back into (1) with r = th gives ``h = 2(t + 1)/t`` and ``r = 2(t + 1)``, hence

    V = πr²h = 8π(t + 1)³ / t

which at t = 1 is 64π. The answer is recorded as the coefficient: **64**, i.e.
V = 64π (≈ 201.06, or 1408/7 if the cover's 22/7 is used for π).

``solve`` follows that algebra. ``check`` keeps both cylinders and never forms
the ratio: it solves (1) for h in terms of r, walks the second cylinder's own
volume-minus-surface residual until it changes sign, bisects, and returns r²h.
"""

from __future__ import annotations

from fractions import Fraction

#: the height is multiplied by height_scale, the radius by radius_scale.
PARAMS = {"height_scale": Fraction(3, 2), "radius_scale": Fraction(3, 4)}
ANSWER = 64
TOL = 1e-6
VARIANTS = [
    {"height_scale": Fraction(2), "radius_scale": Fraction(1, 2)},
    {"height_scale": Fraction(4, 3), "radius_scale": Fraction(4, 5)},
    {"height_scale": Fraction(5, 4), "radius_scale": Fraction(2, 3)},
    {"height_scale": Fraction(3), "radius_scale": Fraction(1, 4)},
    {"height_scale": Fraction(1, 2), "radius_scale": Fraction(3, 2)},
    {"height_scale": Fraction(3, 2), "radius_scale": Fraction(1)},   # no change: no t
]


def solve(height_scale=Fraction(3, 2), radius_scale=Fraction(3, 4)):
    """V/π = 8(t + 1)³/t, with t = r/h fixed by the two conditions."""
    beta, alpha = Fraction(height_scale), Fraction(radius_scale)
    denominator = alpha * (beta - 1)
    if denominator == 0:
        return None
    ratio = beta * (1 - alpha) / denominator
    if ratio <= 0:
        return None
    value = 8 * (ratio + 1) ** 3 / ratio
    return int(value) if value.denominator == 1 else value


def check(height_scale=Fraction(3, 2), radius_scale=Fraction(3, 4)):
    """Independent: keep both cylinders and bisect the second one's residual.

    Condition (1) gives ``h = 2r/(r − 2)`` for every r > 2, so the family of
    cylinders whose volume equals their surface area is one-dimensional. Walking
    r across that family and measuring ``V − S`` of the *scaled* cylinder finds
    the one that satisfies the second condition too — no ratio, no substitution.
    """
    beta, alpha = float(height_scale), float(radius_scale)

    def residual(r: float) -> float:
        h = 2 * r / (r - 2)
        radius, height = alpha * r, beta * h
        return radius * radius * height - 2 * radius * radius - 2 * radius * height

    lo = 2.0 + 1e-9
    hi = 4.0
    start = residual(lo)
    if start == 0.0:
        return None
    for _ in range(200):
        if residual(hi) * start < 0 or residual(hi) == 0.0:
            break
        hi *= 2
        if hi > 1e12:
            return None
    else:
        return None

    for _ in range(300):
        mid = (lo + hi) / 2
        value = residual(mid)
        if value == 0.0:
            lo = hi = mid
            break
        if value * start > 0:
            lo = mid
        else:
            hi = mid
    r = (lo + hi) / 2
    if r <= 2 + 1e-8:
        return None
    return r * r * (2 * r / (r - 2))
