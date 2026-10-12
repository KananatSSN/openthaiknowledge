"""ข้อ 22 — ค่าของ ∠A + ∠C

กำหนดให้ ΔABC เป็นรูปสามเหลี่ยม ซึ่ง ∠B = 2∠C และ BC = 2AB จงหา ∠A + ∠C

Write γ for ∠C, so ∠B = 2γ and ∠A = 180° − 3γ. The side condition goes through
the law of sines — BC is opposite A and AB is opposite C — so ``BC = 2·AB``
means ``sin A = 2 sin C``:

    sin(180° − 3γ) = 2 sin γ   ⟹   sin 3γ = 2 sin γ

and the triple-angle identity ``sin 3γ = 3 sin γ − 4 sin³γ`` turns that into

    3s − 4s³ = 2s   ⟹   s(1 − 4s²) = 0   ⟹   sin γ = ½

(γ = 0 is not a triangle, and γ = 150° would make ∠B = 300°). So γ = 30°,
∠B = 60°, ∠A = 90° — a 30-60-90 triangle, where the side opposite 30° really is
half the hypotenuse — and

    ∠A + ∠C = 180° − ∠B = **120°**

Note the answer is just ``180° − k·γ``: only ∠B has to be pinned down.

``solve`` finds γ from ``sin((k+1)γ) = m sin γ`` by bisection and reports
180° − kγ. ``check`` builds the triangle instead: it places B at the origin with
the two given sides at the given angle and measures ∠C off the coordinates,
keeping the configuration only when the measured angle really is γ.
"""

from __future__ import annotations

from math import atan2, cos, degrees, hypot, radians, sin

#: ∠B = k·∠C and BC = m·AB.
PARAMS = {"k": 2, "m": 2}
ANSWER = 120.0
TOL = 1e-6
#: below this the triangle has collapsed to a segment.
MIN_ANGLE = 1e-3
VARIANTS = [
    {"k": 2, "m": 1.5},
    {"k": 3, "m": 2},
    {"k": 2, "m": 1},          # equilateral-ish: ∠A = ∠C
    {"k": 4, "m": 2},
    {"k": 1, "m": 2},          # sin 2γ = 2 sin γ needs cos γ = 1
    {"k": 2, "m": 3},          # sin 3γ = 3 sin γ has no root either
]


def _residual(gamma_deg: float, k: float, m: float) -> float:
    """sin((k+1)γ) − m·sin γ, the law-of-sines condition."""
    return sin(radians((k + 1) * gamma_deg)) - m * sin(radians(gamma_deg))


def solve(k=2, m=2):
    """∠A + ∠C = 180° − k·γ, with γ the angle the side ratio forces."""
    if k <= 0 or m <= 0:
        return None
    top = 180 / (k + 1)
    lo, hi, steps = 1e-9, top - 1e-9, 200_000
    roots = []
    prev, prev_x = _residual(lo, k, m), lo
    for i in range(1, steps + 1):
        x = lo + (hi - lo) * i / steps
        cur = _residual(x, k, m)
        if cur == 0.0:
            roots.append(x)
        elif prev * cur < 0:
            left, right = prev_x, x
            for _ in range(200):
                mid = (left + right) / 2
                if _residual(left, k, m) * _residual(mid, k, m) <= 0:
                    right = mid
                else:
                    left = mid
            roots.append((left + right) / 2)
        prev, prev_x = cur, x
    # γ → 0 makes every configuration degenerate to a segment, which both
    # routes would otherwise report as a solution.
    kept = [g for g in roots if MIN_ANGLE < g < top - MIN_ANGLE]
    if len(kept) != 1:
        return None
    return 180 - k * kept[0]


def check(k=2, m=2):
    """Independent: build the triangle from the two given sides and measure it.

    B sits at the origin with A at distance 1 and C at distance m, separated by
    the angle ∠B = kγ; the angle at C is then measured from the coordinates with
    ``atan2`` and compared with γ. Sweeping γ and bisecting that mismatch finds
    the triangle — the law of sines is never used, and neither is the
    triple-angle identity.
    """
    if k <= 0 or m <= 0:
        return None

    def mismatch(gamma_deg: float) -> float:
        b = (0.0, 0.0)
        a = (1.0, 0.0)
        angle_b = radians(k * gamma_deg)
        c = (m * cos(angle_b), m * sin(angle_b))
        ca = (a[0] - c[0], a[1] - c[1])
        cb = (b[0] - c[0], b[1] - c[1])
        if hypot(*ca) < 1e-12 or hypot(*cb) < 1e-12:
            return 1e9
        measured = abs(degrees(atan2(ca[1], ca[0]) - atan2(cb[1], cb[0])))
        measured = min(measured % 360, 360 - measured % 360)
        return measured - gamma_deg

    top = 180 / (k + 1)
    lo, hi, steps = 1e-9, top - 1e-9, 200_000
    roots = []
    prev, prev_x = mismatch(lo), lo
    for i in range(1, steps + 1):
        x = lo + (hi - lo) * i / steps
        cur = mismatch(x)
        if cur == 0.0:
            roots.append(x)
        elif prev * cur < 0:
            left, right = prev_x, x
            for _ in range(200):
                mid = (left + right) / 2
                if mismatch(left) * mismatch(mid) <= 0:
                    right = mid
                else:
                    left = mid
            roots.append((left + right) / 2)
        prev, prev_x = cur, x

    kept = []
    for gamma in roots:
        if not MIN_ANGLE < gamma < top - MIN_ANGLE:
            continue
        if abs(mismatch(gamma)) > 1e-7:
            continue
        kept.append(180 - k * gamma)
    if not kept:
        return None
    if max(kept) - min(kept) > 1e-6:
        return None
    return sum(kept) / len(kept)
