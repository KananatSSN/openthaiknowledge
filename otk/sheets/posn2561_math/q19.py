"""ข้อ 19 — ความยาวรอบรูปสามเหลี่ยมจากส่วนสูงที่แบ่งเป็นรูปคล้าย

กำหนดสามเหลี่ยม ABC มีฐานยาว 20 เซนติเมตร หากลากเส้นจากจุดยอดมาตั้งฉากกับฐาน จะพบว่า
เส้นนี้มีความยาว 8 เซนติเมตร, เส้นนี้ไม่แบ่งครึ่งมุมยอด, และเส้นนี้แบ่งสามเหลี่ยมออกเป็น
สามเหลี่ยมสองรูปที่คล้ายกัน จงหาความยาวรอบรูปสามเหลี่ยม ABC นี้

The altitude splits the base into p and q with p + q = 20. Two *right* triangles
with a common leg h are similar in only two ways: leg-for-leg (p = q — which is
the isosceles case, and that is precisely the reading the third bullet rules out
by saying the line does **not** bisect the apex angle), or crosswise:

    p/h = h/q   ⟹   pq = h²

That one word is the question. pq = 64 with p + q = 20 gives p, q = 4, 16, hence
sides √(16 + 64) = 4√5 and √(256 + 64) = 8√5 — and incidentally a right angle at
the apex, since 80 + 320 = 400 = 20².

The perimeter comes out without ever naming p and q. Because ``h² = pq``,

    AB² = p² + h² = p² + pq = p(p + q) = p·base

so ``AB + AC = √base·(√p + √q)`` and ``(√p + √q)² = p + q + 2√(pq) = base + 2h``:

    perimeter = base + √(base(base + 2h)) = 20 + √720 = 20 + 12√5 ≈ 46.8328

``solve`` returns that closed form. ``check`` bisects ``p(base − p) − h²`` for p,
confirms the two right triangles really are similar by comparing their leg
ratios, and then adds up three measured distances.
"""

from __future__ import annotations

from math import hypot, sqrt

#: base and the altitude dropped to it.
PARAMS = {"base": 20, "height": 8}
ANSWER = 46.83281572999748
TOL = 1e-7
VARIANTS = [
    {"base": 10, "height": 3},
    {"base": 25, "height": 12},
    {"base": 13, "height": 6},
    {"base": 100, "height": 7},
    {"base": 20, "height": 10},      # p = q: the altitude bisects, so no answer
    {"base": 20, "height": 12},      # pq = h² has no real split at all
]


def solve(base=20, height=8):
    """perimeter = base + √(base(base + 2h)), from pq = h²."""
    if base <= 0 or height <= 0:
        return None
    if base * base <= 4 * height * height:
        # p = q (the excluded bisecting case) or no real split at all
        return None
    return base + sqrt(base * (base + 2 * height))


def check(base=20, height=8):
    """Independent: find the foot numerically, then measure the three sides.

    ``p(base − p) − h²`` is bisected on (0, base/2); the exact-hit branch is
    written first because a grid landing on the root is the standard way this
    kind of search silently misses it. The similarity the question asserts is
    then confirmed as ``p/h = h/q`` before any length is added up.
    """
    if base <= 0 or height <= 0:
        return None
    if base * base <= 4 * height * height:
        return None

    def residual(p: float) -> float:
        return p * (base - p) - height * height

    lo, hi = 0.0, base / 2
    if residual(lo) > 0 or residual(hi) < 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        value = residual(mid)
        if value == 0.0:
            lo = hi = mid
            break
        if value < 0:
            lo = mid
        else:
            hi = mid
    p = (lo + hi) / 2
    q = base - p
    if p <= 0 or abs(p - q) < 1e-9:
        return None
    if abs(p / height - height / q) > 1e-7:
        return None
    return base + hypot(p, height) + hypot(q, height)
