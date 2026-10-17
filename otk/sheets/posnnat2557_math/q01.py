"""ข้อ 1 — BC · DE = BD · CE  (พิสูจน์)

AB = AC with ∠BAC = apex; E beyond B on ray AB with BE = BC, so triangle BCE
is isosceles with ∠CBE = 90° + apex/2 and ∠BEC = 45° − apex/4 (20° for the
source's 100°); that angle drives the proof. The solver returns ∠BEC.

``check`` places A at the origin with AB along the x-axis, builds C, D (AD = BC)
and E (BE = BC), measures ∠BEC from coordinates and, for apex 100°, confirms
BC · DE = BD · CE.
"""

from __future__ import annotations

from math import acos, cos, degrees, hypot, radians, sin

PARAMS = {"apex": 100}
ANSWER = 20.0
VARIANTS = [{"apex": 20}, {"apex": 60}, {"apex": 140}]
TOL = 1e-9


def solve(apex=100):
    return 45 - apex / 4


def check(apex=100):
    B = (1.0, 0.0)  # A at the origin, AB = AC = 1
    C = (cos(radians(apex)), sin(radians(apex)))
    bc = hypot(C[0] - B[0], C[1] - B[1])
    D = (bc, 0.0)
    E = (1.0 + bc, 0.0)
    u = (B[0] - E[0], B[1] - E[1])
    v = (C[0] - E[0], C[1] - E[1])
    angle = degrees(acos((u[0] * v[0] + u[1] * v[1]) / (hypot(*u) * hypot(*v))))
    if apex == 100:
        de, bd = abs(E[0] - D[0]), abs(D[0] - B[0])
        ce = hypot(C[0] - E[0], C[1] - E[1])
        assert abs(bc * de - bd * ce) < 1e-12
    return angle
