"""ข้อ 2 — BC ที่มากที่สุดเมื่อ PD = PE และรัศมีวงกลมแนบในเป็น r

PD = PE with ∠B ≠ ∠C makes AEPD cyclic, so ∠BPC = 180° − A = 90° + A/2 and
A = 60°. Then BC = r(cot(B/2) + cot(C/2)) with B + C = 120°, largest at the
boundary C = 30°, B = 90°: r(3 + √3).

``check`` builds each triangle in coordinates: for C from 30° up it bisects on
B for PD = PE (measured from the bisector feet and the incentre), scales to
inradius r and keeps the longest BC.
"""

from __future__ import annotations

from math import cos, radians, sin, sqrt

PARAMS = {"r": 1}
ANSWER = 4.732050807568877
VARIANTS = [{"r": 2}, {"r": 3}, {"r": 5}]
TOL = 1e-6


def solve(r=1):
    return r * (3 + sqrt(3))


def _gap(b_deg, c_deg):
    b, c = radians(b_deg), radians(c_deg)
    a = radians(180 - b_deg - c_deg)
    la, lb, lc = sin(a), sin(b), sin(c)  # sides opposite A, B, C (scale)
    B = (0.0, 0.0)
    C = (la, 0.0)
    A = (lc * cos(b), lc * sin(b))
    total = la + lb + lc
    inc = ((la * A[0] + lb * B[0] + lc * C[0]) / total, (la * A[1] + lb * B[1] + lc * C[1]) / total)
    # D on CA from the B-bisector: AD/DC = AB/BC; E on AB from the C-bisector: AE/EB = CA/BC
    D = ((la * A[0] + lc * C[0]) / (la + lc), (la * A[1] + lc * C[1]) / (la + lc))
    E = ((la * A[0] + lb * B[0]) / (la + lb), (la * A[1] + lb * B[1]) / (la + lb))
    pd = ((D[0] - inc[0]) ** 2 + (D[1] - inc[1]) ** 2) ** 0.5
    pe = ((E[0] - inc[0]) ** 2 + (E[1] - inc[1]) ** 2) ** 0.5
    return pd - pe, la, inc[1]


def check(r=1):
    best = 0.0
    c_deg = 30.0
    while c_deg < 59.5:
        lo, hi = c_deg + 1e-6, 180 - c_deg - 1e-6
        # scan for a sign change of PD − PE with B > C, then bisect
        steps = 400
        prev_b, prev = lo, _gap(lo, c_deg)[0]
        for i in range(1, steps + 1):
            b = lo + (hi - lo) * i / steps
            cur = _gap(b, c_deg)[0]
            if (prev < 0) != (cur < 0):
                x, y = prev_b, b
                for _ in range(80):
                    mid = (x + y) / 2
                    if (_gap(mid, c_deg)[0] < 0) == (prev < 0):
                        x = mid
                    else:
                        y = mid
                _, side, inr = _gap((x + y) / 2, c_deg)
                best = max(best, side * r / inr)
                break
            prev_b, prev = b, cur
        c_deg += 0.5
    return best
