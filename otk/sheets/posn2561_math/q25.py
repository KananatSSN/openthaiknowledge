"""ข้อ 25 — ความน่าจะเป็นที่ฝนไม่ตกสองวันติดกันจากลูกโซ่มาร์คอฟ

ในการพยากรณ์อากาศช่วงฤดูฝนของเมืองหนึ่ง พบว่า หากในวันหนึ่งฝนตกแล้ว ความน่าจะเป็นที่
ฝนไม่ตกในวันถัดไปเป็น 5/6 และหากในวันหนึ่งฝนไม่ตกแล้ว ความน่าจะเป็นที่ฝนไม่ตกในวันถัดไป
เป็น 1/2 ถ้าในสัปดาห์นี้ฝนไม่ตกในวันอังคาร จงหาความน่าจะเป็นที่ในสัปดาห์นี้ฝนไม่ตกทั้งใน
วันพฤหัสบดีและวันศุกร์

Tuesday → Thursday is two steps and Thursday → Friday is one more, and the chain
forgets everything but the previous day, so the answer factorises:

    P(Thu dry ∧ Fri dry | Tue dry) = P(Thu dry | Tue dry) · P(Fri dry | Thu dry)

Write p = P(dry | dry yesterday) and q = P(dry | rain yesterday). Then
``f₀ = 1`` and ``f_{n+1} = p·f_n + q(1 − f_n) = q + (p − q)f_n``, whose fixed
point is π = q/(1 − p + q), so

    f_n = π + (1 − π)(p − q)ⁿ

With p = 1/2, q = 5/6: π = (5/6)/(4/3) = 5/8 and p − q = −1/3, so
f₂ = 5/8 + (3/8)(1/9) = 2/3. Multiplying by p:

    2/3 × 1/2 = **1/3**

The trap is reading the two printed fractions as ``P(rain)`` — both are stated
as the probability that it does **not** rain.

``solve`` uses that closed form in exact fractions. ``check`` writes out every
day-by-day weather sequence from Tuesday to Friday, multiplies the transition
probabilities along each one, and adds up the paths that end dry on both of the
two named days.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

#: gap = days from the known dry day to the first day asked about.
PARAMS = {"dry_after_rain": Fraction(5, 6), "dry_after_dry": Fraction(1, 2),
          "gap": 2}
ANSWER = Fraction(1, 3)
VARIANTS = [
    {"gap": 1},
    {"gap": 3},
    {"dry_after_rain": Fraction(1, 3), "dry_after_dry": Fraction(3, 4)},
    {"dry_after_rain": Fraction(1, 2), "dry_after_dry": Fraction(1, 2), "gap": 4},
    {"dry_after_rain": Fraction(1), "dry_after_dry": Fraction(0), "gap": 3},
    {"dry_after_rain": Fraction(5, 6), "dry_after_dry": Fraction(1, 2), "gap": 6},
]


def solve(dry_after_rain=Fraction(5, 6), dry_after_dry=Fraction(1, 2), gap=2):
    """f_n = π + (1 − π)(p − q)ⁿ, then one more dry day."""
    p, q = Fraction(dry_after_dry), Fraction(dry_after_rain)
    if not 0 <= p <= 1 or not 0 <= q <= 1 or gap < 1:
        return None
    if 1 - p + q == 0:
        return None
    stationary = q / (1 - p + q)
    dry_then = stationary + (1 - stationary) * (p - q) ** gap
    return dry_then * p


def check(dry_after_rain=Fraction(5, 6), dry_after_dry=Fraction(1, 2), gap=2):
    """Independent: enumerate every weather sequence and add up the good ones."""
    p, q = Fraction(dry_after_dry), Fraction(dry_after_rain)
    if not 0 <= p <= 1 or not 0 <= q <= 1 or gap < 1:
        return None
    days = gap + 1                       # up to and including the second named day
    if days > 18:
        return None

    total = Fraction(0)
    for path in product((True, False), repeat=days):      # True = dry
        weight = Fraction(1)
        previous = True                                   # the known dry day
        for dry in path:
            step = p if previous else q
            weight *= step if dry else 1 - step
            previous = dry
        if path[gap - 1] and path[gap]:
            total += weight
    return total
