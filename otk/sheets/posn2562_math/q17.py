"""ข้อ 17 — ปริมาตรของกล่องแรก

มีกล่องทรงสี่เหลี่ยมมุมฉากที่ฐานเป็นรูปสี่เหลี่ยมจัตุรัสสองกล่อง กล่องแรกมีพื้นที่ผิว
ทั้งหกด้านรวมกันเท่ากับ 2 เท่าของปริมาตร กล่องที่สองมีความสูงเป็นครึ่งหนึ่งและมี
ความยาวฐานเป็นสองเท่าของกล่องแรก และมีพื้นที่ผิวทั้งหกด้านของกล่องนี้รวมกันเท่ากับ
3 เท่าของปริมาตร จงหาปริมาตรของกล่องแรก

With base side s and height h, a square-based box has surface ``2s² + 4sh`` and
volume ``s²h``. The two conditions, each divided through by s, are linear in the
pair (s, h):

    box 1:  2s + 4h = k₁·s·h                        (k₁ = 2)
    box 2:  2·f·s + 4·g·h = k₂·f·g·s·h              (f = 2, g = ½, k₂ = 3)

Solving the first for s and substituting eliminates s altogether:

    h = 2(f − g) / (g(f·k₂ − k₁)) = 2(1.5)/(0.5·4) = **3/2**

and then ``s = 4h/(k₁h − 2) = 6/1 =`` **6**, so the first box is 6 × 6 × 3/2 and

    volume = 36 · 3/2 = **54**

(Checking: surface 2·36 + 4·6·1.5 = 108 = 2·54 ✓; the second box is 12 × 12 × ¾
with volume 108 and surface 2·144 + 4·12·0.75 = 324 = 3·108 ✓.)

``solve`` uses that elimination with exact fractions. ``check`` searches the two
printed conditions numerically — bisecting h until the residual of the second
condition vanishes — and rebuilds both boxes to verify the ratios before
reporting a volume.
"""

from __future__ import annotations

from fractions import Fraction

#: surface = k1·volume for box 1; box 2 scales the base by f and the height by g
#: and satisfies surface = k2·volume.
PARAMS = {"k1": 2, "k2": 3, "f": Fraction(2), "g": Fraction(1, 2)}
ANSWER = 54
TOL = 1e-6
VARIANTS = [
    {"k1": 1, "k2": 2, "f": Fraction(2), "g": Fraction(1, 2)},
    {"k1": 2, "k2": 3, "f": Fraction(3), "g": Fraction(1, 3)},
    {"k1": 3, "k2": 4, "f": Fraction(2), "g": Fraction(1, 2)},
    {"k1": 2, "k2": 5, "f": Fraction(2), "g": Fraction(1, 4)},
    {"k1": 2, "k2": 2, "f": Fraction(2), "g": Fraction(1, 2)},   # equal ratios
    {"k1": 2, "k2": 3, "f": Fraction(1), "g": Fraction(1)},      # the same box twice
]


def dimensions(k1=2, k2=3, f=Fraction(2), g=Fraction(1, 2)):
    """(s, h) of the first box, exactly — or None when no positive box fits."""
    k1, k2, f, g = Fraction(k1), Fraction(k2), Fraction(f), Fraction(g)
    if f <= 0 or g <= 0 or k1 <= 0 or k2 <= 0:
        return None
    denom = g * (f * k2 - k1)
    if denom == 0:
        return None
    h = 2 * (f - g) / denom
    if h <= 0 or k1 * h - 2 == 0:
        return None
    s = 4 * h / (k1 * h - 2)
    if s <= 0:
        return None
    return s, h


def solve(k1=2, k2=3, f=Fraction(2), g=Fraction(1, 2)):
    """Volume s²h of the first box."""
    got = dimensions(k1, k2, f, g)
    if got is None:
        return None
    s, h = got
    volume = s * s * h
    return int(volume) if volume.denominator == 1 else volume


def check(k1=2, k2=3, f=Fraction(2), g=Fraction(1, 2)):
    """Independent: bisect on the height until both printed conditions hold.

    For a trial height, the first condition alone fixes the base side; the second
    box is then built from it by the printed scalings and the shortfall in *its*
    condition is measured. That residual is bracketed and bisected, and both
    surface-to-volume ratios are verified on the boxes that come out before any
    volume is reported.
    """
    k1f, k2f, ff, gf = float(k1), float(k2), float(f), float(g)
    if ff <= 0 or gf <= 0 or k1f <= 0 or k2f <= 0:
        return None

    def side(h: float):
        """Base side forced by box 1's condition at this height, if positive."""
        denom = k1f * h - 2
        if abs(denom) < 1e-12:
            return None
        s = 4 * h / denom
        return s if s > 0 else None

    def residual(h: float):
        s = side(h)
        if s is None:
            return None
        big_s, big_h = ff * s, gf * h
        surface = 2 * big_s * big_s + 4 * big_s * big_h
        volume = big_s * big_s * big_h
        return surface - k2f * volume

    lo, hi, steps = 1e-6, 400.0, 400_000
    found = []
    prev, prev_h = residual(lo), lo
    for i in range(1, steps + 1):
        h = lo + (hi - lo) * i / steps
        cur = residual(h)
        if cur is not None and prev is not None and prev * cur < 0:
            left, right = prev_h, h
            for _ in range(200):
                mid = (left + right) / 2
                fl, fm = residual(left), residual(mid)
                if fl is None or fm is None:
                    break
                if fl * fm <= 0:
                    right = mid
                else:
                    left = mid
            found.append((left + right) / 2)
        prev, prev_h = cur, h

    volumes = []
    for h in found:
        s = side(h)
        if s is None:
            continue
        if abs(2 * s * s + 4 * s * h - k1f * s * s * h) > 1e-5 * max(1.0, s * s * h):
            continue
        volumes.append(s * s * h)
    if not volumes:
        return None
    if max(volumes) - min(volumes) > 1e-5 * max(volumes):
        return None
    got = sum(volumes) / len(volumes)
    return round(got) if abs(got - round(got)) < 1e-6 else got
