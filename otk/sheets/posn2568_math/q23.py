"""ข้อ 23 — พื้นที่ของรูปสามเหลี่ยม ABE

วงกลมเล็กจุดศูนย์กลาง A รัศมี 15  วงกลมใหญ่จุดศูนย์กลาง B รัศมี 24  สัมผัสกันภายนอก
ที่จุด C  ให้ l₁ เป็นเส้นตรงผ่าน B และสัมผัสวงกลมเล็กที่ D  ให้ l₂ เป็นเส้นสัมผัสร่วม
ที่จุด C  ให้ E เป็นจุดตัดของ l₁ และ l₂  จงหาพื้นที่ของรูปสามเหลี่ยม ABE

Method: AB = r + R, and BD is a tangent from B to the small circle, so
BD = √((r+R)² − r²) = √(R² + 2rR). The tangent at C is perpendicular to AB, so
if h = EC then E is at height h above AB and BE² = R² + h². E also sees the
small circle along two tangents (EC and ED), so EC = ED and BE = BD − h.
Equating,
    (BD − h)² = R² + h²  ⟹  h = (BD² − R²)/(2·BD) = rR/BD,
and the triangle on base AB with apex height h has area ½(r+R)·rR/BD. For
r = 15, R = 24: BD = 36, h = 10, area = ½·39·10 = 195.

``check`` reconstructs the whole picture in coordinates — tangent point D from
the right angle at D, the line BD, its crossing with the vertical through C —
and takes the shoelace area of the triangle it actually gets.
"""

from __future__ import annotations

import math

TOL = 1e-7

PARAMS = {"r": 15, "big_r": 24}
ANSWER = 195.0
VARIANTS = [
    {"r": 3, "big_r": 4},
    {"r": 5, "big_r": 12},
    {"r": 24, "big_r": 15},
    {"r": 1, "big_r": 1},
    {"r": 7, "big_r": 30},
]


def height(r=15, big_r=24) -> float:
    """EC — how far E stands off the line AB."""
    bd = math.sqrt(big_r * big_r + 2 * r * big_r)
    return r * big_r / bd


def solve(r=15, big_r=24):
    """Area of triangle ABE."""
    return (r + big_r) * height(r, big_r) / 2


def check(r=15, big_r=24):
    """Independent: build A, B, C, D, E as points and take a shoelace area."""
    a = (0.0, 0.0)
    b = (r + big_r, 0.0)
    c = (r, 0.0)                                   # the external touch point

    # D is on the small circle with AD ⊥ DB, so ∠DAB has cosine r/|AB|.
    phi = math.acos(r / (r + big_r))
    d = (r * math.cos(phi), r * math.sin(phi))
    assert abs(math.dist(a, d) - r) < 1e-9
    assert abs((d[0] - a[0]) * (d[0] - b[0]) + (d[1] - a[1]) * (d[1] - b[1])) \
        < 1e-9, "AD is not perpendicular to DB — D is not the tangent point"

    # l₂ is the tangent at C: perpendicular to AB, i.e. the vertical x = r.
    # Cross it with the line through B and D.
    t = (c[0] - b[0]) / (d[0] - b[0])
    e = (c[0], b[1] + t * (d[1] - b[1]))
    assert abs(math.dist(e, c) - math.dist(e, d)) < 1e-7, \
        "the two tangents from E should be equal"

    return abs(a[0] * (b[1] - e[1]) + b[0] * (e[1] - a[1])
               + e[0] * (a[1] - b[1])) / 2
