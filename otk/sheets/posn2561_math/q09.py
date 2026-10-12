"""ข้อ 9 — งบประมาณถมดินตามแนวชายฝั่งรอบเกาะ

เกาะแห่งหนึ่งมีรูปร่างและขนาดดังรูป (มุมฉากที่ A และที่ B, BC = 5 กม., AB = 3 กม.,
AD = 11 กม.) เจ้าของต้องการแบ่งเขตกลางเกาะเป็นเกาะฝั่งเหนือและเกาะฝั่งใต้ จากจุด A
ไปถึงจุด E บนด้าน CD เพื่อให้ความยาวรอบเกาะที่ติดทะเลของฝั่งเหนือเท่ากับความยาวรอบ
เกาะที่ติดทะเลของฝั่งใต้ หากผู้รับเหมาเสนอราคาถมดินตามแนวรอบเกาะที่ติดทะเลด้านฝั่ง
เหนือกิโลเมตรละ 5 ล้านบาท ฝั่งใต้กิโลเมตรละ 10 ล้านบาท และขายเหมาเป็นหน่วยเต็ม
กิโลเมตร เจ้าของเกาะจะใช้งบประมาณกี่ล้านบาท

The cut AE is inland, so it is **not** coastline — which is the whole trick. The
sea-facing edges are AB + BC + CE to the north and ED + DA to the south, and they
together make up the entire coast:

    AB + BC + CD + DA = 3 + 5 + √45 + 11 = 19 + 3√5 ≈ 25.7082

Making the two sides equal therefore means each is **exactly half the perimeter**,
≈ 12.8541 km, and E only has to exist on CD for that to be achievable (it does:
CE ≈ 4.854 < 3√5). The individual lengths never need to be found.

Land is sold in whole kilometres, so each side is billed at ⌈12.8541⌉ = 13 km:

    13 · 5 + 13 · 10 = 65 + 130 = **195** ล้านบาท

Two traps sit next to each other — counting AE as coastline, and rounding the
*total* rather than each side (here they agree, but they need not).

``solve`` uses the half-perimeter. ``check`` finds E: it slides a point along CD,
measures the two coastlines separately, bisects until they match, and bills what
it measured.
"""

from __future__ import annotations

from math import ceil, dist, hypot, isclose

#: right angles at A and B; AB, BC, AD in km, and the two prices per km.
PARAMS = {"ab": 3, "bc": 5, "ad": 11, "north": 5, "south": 10}
ANSWER = 195
VARIANTS = [
    {"ab": 3, "bc": 5, "ad": 11, "north": 4, "south": 9},
    {"ab": 6, "bc": 8, "ad": 20, "north": 5, "south": 10},
    {"ab": 4, "bc": 4, "ad": 12, "north": 5, "south": 10},
    {"ab": 3, "bc": 11, "ad": 5, "north": 5, "south": 10},   # C beyond D: no E
    {"ab": 3, "bc": 5, "ad": 11, "north": 1, "south": 1},
    {"ab": 0, "bc": 5, "ad": 11, "north": 5, "south": 10},
]


def corners(ab=3, bc=5, ad=11):
    """A, B, C, D with the right angles at A and B, or None if degenerate."""
    if ab <= 0 or bc <= 0 or ad <= 0 or bc >= ad:
        return None
    return (0.0, 0.0), (0.0, float(ab)), (float(bc), float(ab)), (float(ad), 0.0)


def solve(ab=3, bc=5, ad=11, north=5, south=10):
    """Each side is half the coast; bill each at the whole kilometre above it."""
    got = corners(ab, bc, ad)
    if got is None:
        return None
    a, b, c, d = got
    coast = ab + bc + dist(c, d) + ad
    half = coast / 2
    if not ab + bc <= half <= ab + bc + dist(c, d):
        return None                      # E would have to lie off the side CD
    billed = ceil(half - 1e-9)
    return billed * north + billed * south


def check(ab=3, bc=5, ad=11, north=5, south=10):
    """Independent: slide E along CD until the two coastlines agree, then bill.

    The north coast is measured as AB + BC + CE and the south as ED + DA, with E
    an actual point on the segment CD; their difference is bisected to zero. The
    two lengths are then rounded up *separately* and priced, so a case where they
    round differently would be handled correctly rather than by assumption.
    """
    got = corners(ab, bc, ad)
    if got is None:
        return None
    a, b, c, d = got
    side = dist(c, d)
    if side <= 0:
        return None

    def coasts(t: float):
        """(north, south) coastlines when E is a fraction t of the way C → D."""
        e = (c[0] + t * (d[0] - c[0]), c[1] + t * (d[1] - c[1]))
        return (ab + bc + hypot(e[0] - c[0], e[1] - c[1]),
                hypot(d[0] - e[0], d[1] - e[1]) + ad)

    def gap(t: float) -> float:
        first, second = coasts(t)
        return first - second

    if gap(0.0) * gap(1.0) > 0:
        return None
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if gap(lo) * gap(mid) <= 0:
            hi = mid
        else:
            lo = mid
    first, second = coasts((lo + hi) / 2)
    if not isclose(first, second, abs_tol=1e-9):
        return None
    return ceil(first - 1e-9) * north + ceil(second - 1e-9) * south
