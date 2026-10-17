"""ข้อ 1 — AB + CD = BC + AD  (พิสูจน์)

The proof locates P = ST ∩ BD on the diagonal from each side. In triangle ABD
with AT = AS = t, writing S, T in the basis A, B, D and cancelling A's
coefficient gives P = B + λ(D − B) with λ = (AB − t)/(AB − AD); the same on the
CBD side, with CU = CV and BT = BU, forces the tangent-length equality. The
solver returns λ (8, 5, 2: 2).

``check`` places A at the origin with an arbitrary angle at A, builds S and T,
and intersects line ST with line BD.
"""

from __future__ import annotations

from fractions import Fraction
from math import cos, radians, sin

PARAMS = {"ab": 8, "ad": 5, "arm": 2}
ANSWER = 2
VARIANTS = [{"ab": 6, "ad": 11, "arm": 4}, {"ab": 15, "ad": 9, "arm": 7}, {"ab": 4, "ad": 20, "arm": 1}]
TOL = 1e-9


def solve(ab=8, ad=5, arm=2):
    return Fraction(ab - arm, ab - ad)


def check(ab=8, ad=5, arm=2):
    angle = radians(73)
    B = (float(ab), 0.0)
    D = (ad * cos(angle), ad * sin(angle))
    T = (float(arm), 0.0)
    S = (arm * cos(angle), arm * sin(angle))
    # B + λ(D − B) = T + μ(S − T)
    a11, a12 = D[0] - B[0], -(S[0] - T[0])
    a21, a22 = D[1] - B[1], -(S[1] - T[1])
    r1, r2 = T[0] - B[0], T[1] - B[1]
    det = a11 * a22 - a12 * a21
    return (r1 * a22 - a12 * r2) / det
