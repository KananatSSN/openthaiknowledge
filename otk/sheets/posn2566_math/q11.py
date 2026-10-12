"""ข้อ 11 — ผลบวกรัศมีของวงกลมสองวงที่สัมผัสกันในรูปสี่เหลี่ยมผืนผ้า

ให้ ABCD เป็นรูปสี่เหลี่ยมผืนผ้าที่มีด้าน AB ยาว 9 หน่วย และด้าน BC ยาว 8 หน่วย
T₁ เป็นวงกลมที่มีจุดศูนย์กลาง O₁ รัศมี r₁ สัมผัสกับด้าน AD และด้าน CD
T₂ เป็นวงกลมที่มีจุดศูนย์กลาง O₂ รัศมี r₂ สัมผัสกับด้าน AB และด้าน BC และสัมผัสกับ T₁
จงหาค่าของ r₁ + r₂

Each circle is pinned into its own corner by its two tangencies: with
A = (0,0), B = (w,0), C = (w,h), D = (0,h),

    O₁ = (r₁, h − r₁)        O₂ = (w − r₂, r₂)

and the two touch externally, so |O₁O₂| = r₁ + r₂. Writing s = r₁ + r₂ the
cross-terms cancel and **only the sum appears**:

    (w − s)² + (s − h)² = s²   ⟹   s² − 2(w + h)s + (w² + h²) = 0

    s = (w + h) ± √(2wh)

For 9 by 8 that is 17 ± 12, so s = 5 or s = 29 — and 29 is far larger than the
rectangle, so **r₁ + r₂ = 5**.

The individual radii are *not* determined: only their sum is, which is exactly
what the question asks for. Discarding the second root is the other half of the
item.

``solve`` takes the smaller root. ``check`` never forms that quadratic: it picks
several r₁, bisects the tangency condition for the matching r₂, and reports the
sum only when the different starting radii agree — which also demonstrates that
the sum, and not each radius, is what the configuration fixes.
"""

from __future__ import annotations

from fractions import Fraction
from math import hypot, isqrt

#: rectangle w × h; T₁ in the D corner, T₂ in the B corner.
PARAMS = {"width": 9, "height": 8}
ANSWER = 5
TOL = 1e-7
VARIANTS = [
    {"width": 8, "height": 9},
    {"width": 4, "height": 2},
    {"width": 10, "height": 5},
    {"width": 6, "height": 6},
    {"width": 12, "height": 6},
    {"width": 3, "height": 7},
]


def solve(width=9, height=8):
    """s = (w + h) − √(2wh); the other root is bigger than the rectangle."""
    if width <= 0 or height <= 0:
        return None
    inner = 2 * width * height
    root = isqrt(inner)
    if root * root == inner:
        value = Fraction(width + height - root)
        if value <= 0:
            return None
        return int(value) if value.denominator == 1 else value
    value = width + height - inner ** 0.5
    return value if value > 0 else None


def check(width=9, height=8):
    """Independent: fix r₁, bisect for r₂, and confirm the sum does not move.

    For a chosen r₁ the second circle must satisfy
    ``|O₁O₂| − (r₁ + r₂) = 0``; that residual is bisected in r₂. Several r₁ are
    tried, and a value is returned only when every one gives the same sum — the
    quadratic in s is never written down.
    """
    if width <= 0 or height <= 0:
        return None
    sums = []
    for share in (0.3, 0.45, 0.6):
        guess = solve(width, height)
        if guess is None:
            return None
        r1 = float(guess) * share

        def residual(r2: float, r1=r1) -> float:
            o1 = (r1, height - r1)
            o2 = (width - r2, r2)
            return hypot(o1[0] - o2[0], o1[1] - o2[1]) - (r1 + r2)

        lo, hi = 1e-9, min(width, height)
        if residual(lo) * residual(hi) > 0:
            return None
        for _ in range(300):
            mid = (lo + hi) / 2
            value = residual(mid)
            if value == 0.0:
                lo = hi = mid
                break
            if residual(lo) * value <= 0:
                hi = mid
            else:
                lo = mid
        sums.append(r1 + (lo + hi) / 2)
    if max(sums) - min(sums) > 1e-7 * max(1.0, max(sums)):
        return None
    return sum(sums) / len(sums)
