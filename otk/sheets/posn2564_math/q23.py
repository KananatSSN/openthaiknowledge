"""ข้อ 23 — จำนวนลูกบาศก์ m ที่มากที่สุด

มีลูกบาศก์ทรงตันที่ทำมาจากโลหะ 2 ชนิด ดังนี้
    ชนิดที่ 1 ลูกบาศก์มีความกว้าง 3 เซนติเมตร หนัก 200 กรัม จำนวน 100 ลูก
    ชนิดที่ 2 ลูกบาศก์มีความกว้าง 2 เซนติเมตร หนัก 400 กรัม จำนวน 100 ลูก
ให้ถัง A มีน้ำเต็มถังพอดี และเลือกลูกบาศก์รวม m ลูกจากทั้งสองชนิดข้างต้น
หลังจากนั้นทำการหย่อนลูกบาศก์ทั้งหมดที่เลือกมาลงไปในถัง A โดยไม่มีส่วนใดของ
ลูกบาศก์ลูกใดโผล่เหนือผิวน้ำ พบว่ามีน้ำล้นออกมาจากถัง A ไม่เกิน 1,000 ลูกบาศก์
เซนติเมตร ถ้าน้ำหนักรวมของลูกบาศก์ที่หย่อนลงไปเท่ากับ 20 กิโลกรัม แล้ว m มีค่า
เป็นไปได้มากที่สุดเท่ากับเท่าไร

By Archimedes (the stem spells it out in its หมายเหตุ) the overflow is the total
**volume**, and the weight is a second linear constraint. With i big cubes and
j small ones:

    200i + 400j = 20000   ⟹   i + 2j = 100
    27i + 8j ≤ 1000       ⟹   2700 − 46j ≤ 1000   ⟹   j ≥ 1700/46 = 36.96…

so j ≥ 37. **The count runs the other way from the intuition**: since
m = i + j = (100 − 2j) + j = 100 − j, maximising m means taking as *few* small
cubes as possible, so j = 37, i = 26 and **m = 63** (with 998 cm³ overflowing).

Both stocks are 100, and neither binds here — but a generator that varies the
weights can easily produce a draw where they do, which is why solve checks them.

``solve`` derives the bound on j in closed form. ``check`` enumerates every
(i, j) pair that satisfies both printed constraints and takes the largest total.
"""

from __future__ import annotations

#: side lengths (cm), weights (g), stock counts, target weight (g), max overflow.
PARAMS = {
    "big_side": 3, "big_weight": 200, "big_stock": 100,
    "small_side": 2, "small_weight": 400, "small_stock": 100,
    "weight": 20000, "overflow": 1000,
}
ANSWER = 63
VARIANTS = [
    {"weight": 10000, "overflow": 500},
    {"overflow": 1200},
    {"big_side": 4, "overflow": 2000},
    {"weight": 20000, "overflow": 700},
    {"small_weight": 500, "weight": 20000},
    {"weight": 20000, "overflow": 100},        # nothing fits
]


def solve(big_side=3, big_weight=200, big_stock=100,
          small_side=2, small_weight=400, small_stock=100,
          weight=20000, overflow=1000):
    """Solve the weight equation for i, then bound j by the volume.

    The weight equation pins i as a function of j, so the volume constraint is a
    single inequality in j; whichever end of the feasible range gives more cubes
    is then read off, since m = i + j is linear in j.
    """
    if min(big_side, small_side, big_weight, small_weight) <= 0:
        return None
    if weight <= 0 or overflow < 0:
        return None
    big_vol, small_vol = big_side ** 3, small_side ** 3
    best = None
    # i·big_weight + j·small_weight = weight, so i = (weight − j·small_weight)/big_weight
    top = weight // small_weight
    if top > 100_000:
        return None
    for j in range(top + 1):
        rest = weight - j * small_weight
        if rest < 0 or rest % big_weight:
            continue
        i = rest // big_weight
        if i > big_stock or j > small_stock:
            continue
        if i * big_vol + j * small_vol > overflow:
            continue
        if best is None or i + j > best:
            best = i + j
    return best


def check(big_side=3, big_weight=200, big_stock=100,
          small_side=2, small_weight=400, small_stock=100,
          weight=20000, overflow=1000):
    """Independent: enumerate over the *pairs* and take the best total.

    Both counts are swept within their stock, and each pair is tested against the
    printed weight and overflow directly — no equation is solved for either
    variable, so a sign slip in the algebra above would not be reproduced here.
    """
    if min(big_side, small_side, big_weight, small_weight) <= 0:
        return None
    if weight <= 0 or overflow < 0:
        return None
    if big_stock > 5000 or small_stock > 5000:
        return None
    big_vol, small_vol = big_side ** 3, small_side ** 3
    best = None
    for i in range(big_stock + 1):
        for j in range(small_stock + 1):
            if i * big_weight + j * small_weight != weight:
                continue
            if i * big_vol + j * small_vol > overflow:
                continue
            if best is None or i + j > best:
                best = i + j
    return best
