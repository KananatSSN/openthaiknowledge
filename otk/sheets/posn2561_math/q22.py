"""ข้อ 22 — ความยาว AR ในสี่เหลี่ยมด้านขนานที่ถูกตัดด้วยเส้นเดียว

ให้ ABCD เป็นรูปสี่เหลี่ยมด้านขนานที่ AB ∥ DC และ AD ∥ BC ซึ่งเมื่อลากส่วนของเส้นตรง
จากจุด A ไปตัดกับเส้นทแยงมุม BD ที่จุด R ไปตัดกับด้าน BC ที่จุด P และไปตัดกับส่วนต่อของ
ด้าน DC ที่จุด Q แล้ว จะได้ความยาวด้าน PR เท่ากับ a หน่วย และความยาวด้าน PQ เท่ากับ b
หน่วย ดังรูป จงหาความยาวด้าน AR

**The sheet states this one in letters**, so its published answer is a formula,
not a number: AR = √(a(a + b)). PARAMS instantiates it at a = 4, b = 5, where the
answer is the whole number 6.

Put B at the origin, C = (c, 0), A = (u, v) and D = A + (c, 0). A line from A
crossing BC at P = (p, 0), parametrised so that A is at s = 0 and P at s = 1,
meets the other two lines at

    R:  s = c/(p + c)        Q:  s = c/p

Both drop straight out of the incidence conditions — no similar triangles are
named. Writing L for |AP| and k = p/(p + c),

    AR = L(1 − k)      a = PR = Lk      b = PQ = L(1 − 2k)/k

Eliminating L and k: with x = 1/k, ``b/a = x² − 2x`` and ``AR = a(x − 1)``, so
x = 1 + √(1 + b/a) and

    AR = a√(1 + b/a) = √(a(a + b))

which is the classic ``AR² = PR(PR + PQ)`` — the three lengths along the
transversal are in geometric proportion. At a = 4, b = 5 that is √36 = **6**.

``solve`` returns the closed form. ``check`` builds an actual parallelogram in
coordinates, intersects the three lines by determinants, slides P until the
measured PQ : PR matches, rescales and *measures* AR — and does the whole thing
twice on two unrelated parallelograms, refusing to answer unless they agree.
That last part is what proves the answer really is shape-independent.
"""

from __future__ import annotations

from math import hypot, isqrt

#: PR = pr and PQ = pq along the transversal from A.
PARAMS = {"pr": 4, "pq": 5}
ANSWER = 6
TOL = 1e-6
VARIANTS = [
    {"pr": 3, "pq": 9},
    {"pr": 1, "pq": 3},
    {"pr": 2, "pq": 7},
    {"pr": 9, "pq": 7},
    {"pr": 5, "pq": 1},
    {"pr": 4, "pq": 0},        # Q at P: degenerate, no line does this
]


def solve(pr=4, pq=5):
    """AR = √(PR(PR + PQ))."""
    if pr <= 0 or pq <= 0:
        return None
    product = pr * (pr + pq)
    root = isqrt(product)
    if root * root == product:
        return root
    return product ** 0.5


def _intersect(p1, p2, p3, p4):
    """Intersection of line p1p2 with line p3p4, or None if parallel."""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    a1, b1, t1 = y2 - y1, x1 - x2, x1 * y2 - x2 * y1
    a2, b2, t2 = y4 - y3, x3 - x4, x3 * y4 - x4 * y3
    determinant = a1 * b2 - a2 * b1
    if abs(determinant) < 1e-14:
        return None
    return ((t1 * b2 - t2 * b1) / determinant,
            (a1 * t2 - a2 * t1) / determinant)


def _measure(shape, pr: float, pq: float) -> float | None:
    """Build one parallelogram, slide P to the printed ratio, measure AR."""
    u, v, c = shape
    b_pt, c_pt = (0.0, 0.0), (c, 0.0)
    a_pt, d_pt = (u, v), (u + c, v)

    def ratio(p: float) -> float | None:
        p_pt = (p, 0.0)
        r_pt = _intersect(a_pt, p_pt, b_pt, d_pt)
        q_pt = _intersect(a_pt, p_pt, d_pt, c_pt)
        if r_pt is None or q_pt is None:
            return None
        seg_r = hypot(p_pt[0] - r_pt[0], p_pt[1] - r_pt[1])
        seg_q = hypot(p_pt[0] - q_pt[0], p_pt[1] - q_pt[1])
        if seg_r <= 0:
            return None
        return seg_q / seg_r

    target = pq / pr
    lo, hi = 1e-9 * c, c * (1 - 1e-12)
    if (ratio(lo) or 0) < target or (ratio(hi) or 0) > target:
        return None
    for _ in range(300):                     # PQ/PR falls from +∞ to 0 across BC
        mid = (lo + hi) / 2
        value = ratio(mid)
        if value is None:
            return None
        if value == target:
            lo = hi = mid
            break
        if value > target:
            lo = mid
        else:
            hi = mid
    p = (lo + hi) / 2

    p_pt = (p, 0.0)
    r_pt = _intersect(a_pt, p_pt, b_pt, d_pt)
    if r_pt is None:
        return None
    seg_r = hypot(p_pt[0] - r_pt[0], p_pt[1] - r_pt[1])
    if seg_r <= 0:
        return None
    return hypot(a_pt[0] - r_pt[0], a_pt[1] - r_pt[1]) * pr / seg_r


def check(pr=4, pq=5):
    """Independent: measure AR in two unrelated parallelograms and compare."""
    if pr <= 0 or pq <= 0:
        return None
    first = _measure((1.7, 2.3, 3.1), float(pr), float(pq))
    second = _measure((-0.9, 4.4, 5.75), float(pr), float(pq))
    if first is None or second is None:
        return None
    if abs(first - second) > 1e-6 * max(1.0, first):
        return None                          # not shape-independent: something is wrong
    return (first + second) / 2
