"""ข้อ 10 — ต้องเติมน้ำสูงเป็นสัดส่วนเท่าใดของความสูงของทรงกระบอก

แก้วน้ำใบหนึ่งภายในเป็นทรงกระบอกตรง โดยความสูงของทรงกระบอกเป็นสามเท่าของรัศมี
และมีลูกแก้วทรงกลมซึ่งมีรัศมีเป็นครึ่งหนึ่งของรัศมีของทรงกระบอก จงหาว่าจะต้องเติมน้ำ
ให้สูงเป็นสัดส่วนเท่าใดของความสูงของทรงกระบอก เพื่อให้เมื่อนำลูกแก้วลูกนี้มาใส่ในแก้ว
น้ำแล้ว ระดับน้ำจะเพิ่มขึ้นจนเต็มแก้วพอดี

The marble displaces its own volume, so the water must start exactly that much
short of full. With cylinder radius R, height H = kR and marble radius R/m,

    πR²H - (4/3)π(R/m)³ = water,   so   h/H = 1 - 4/(3m³k).

For k = 3 and m = 2 that is 1 − 4/72 = **17/18**.

Two conditions the answer quietly needs, both checked: the marble has to fit
inside the glass (2R/m ≤ 2R and 2R/m ≤ H), and it has to end up submerged, or it
would displace less than its volume — here the final level is the brim, H, which
is well above the marble's top.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: height = k·radius; marble radius = radius/m.
PARAMS = {"k": 3, "m": 2}
ANSWER = Fraction(17, 18)
VARIANTS = [
    {"k": 4, "m": 2},
    {"k": 3, "m": 3},
    {"k": 2, "m": 1},          # the marble is as wide as the glass
    {"k": 6, "m": 4},
    {"k": 1, "m": 1},          # marble taller than the glass: it cannot go in
]
TOL = 1e-12


def solve(k=3, m=2):
    """h/H = 1 - 4/(3m³k)."""
    if k <= 0 or m < 1:
        return None
    if 2 > m * k:                                  # 2R/m > H: the marble won't fit
        return None
    return 1 - Fraction(4, 3 * m ** 3 * k)


def check(k=3, m=2):
    """Independent: compute the two volumes numerically and divide.

    The glass is given a concrete radius, the marble's volume comes from
    (4/3)πr³, and the water height is read off as volume/(πR²) — then the final
    level is asserted to be the brim and the marble asserted to be under it.
    """
    if k <= 0 or m < 1:
        return None
    if 2 > m * k:
        return None
    radius = 2.5
    height = k * radius
    marble = radius / m
    glass_volume = math.pi * radius ** 2 * height
    marble_volume = 4 / 3 * math.pi * marble ** 3
    water = glass_volume - marble_volume
    if water < 0:
        return None
    h = water / (math.pi * radius ** 2)
    assert abs((water + marble_volume) - glass_volume) < 1e-9
    assert 2 * marble <= height + 1e-12            # it fits in the glass
    return Fraction(h / height).limit_denominator(10 ** 6)
