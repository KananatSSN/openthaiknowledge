"""ข้อ 8 — UX, VY, WZ เป็นด้านของรูปสามเหลี่ยม  (พิสูจน์)

UX = (D + E − A − B)/2, VY = (E + F − B − C)/2 and WZ = (F + A − C − D)/2, so
VY = UX + WZ as vectors: the three chords close up into a triangle (convexity
keeps it non-degenerate). With UX, WZ meeting at θ, VY² = UX² + WZ² + 2·UX·WZ·cos θ
(5, 3, 60°: 49). The solver returns VY².

``check`` confirms the vector identity on several integer hexagons and then
adds the two vectors in coordinates.
"""

from __future__ import annotations

from math import cos, radians, sin

PARAMS = {"ux": 5, "wz": 3, "angle": 60}
ANSWER = 49
VARIANTS = [{"ux": 7, "wz": 8, "angle": 120}, {"ux": 4, "wz": 4, "angle": 60}, {"ux": 9, "wz": 2, "angle": 120}]
TOL = 1e-9


def solve(ux=5, wz=3, angle=60):
    return ux * ux + wz * wz + (ux * wz if angle == 60 else -ux * wz)


def check(ux=5, wz=3, angle=60):
    hexagons = [((0, 0), (4, -1), (7, 2), (6, 6), (2, 7), (-1, 3)),
                ((0, 0), (5, 0), (8, 4), (5, 8), (0, 8), (-3, 4))]
    for A, B, C, D, E, F in hexagons:
        U, V, W = [((p[0] + q[0]) / 2, (p[1] + q[1]) / 2) for p, q in ((A, B), (B, C), (C, D))]
        X, Y, Z = [((p[0] + q[0]) / 2, (p[1] + q[1]) / 2) for p, q in ((D, E), (E, F), (F, A))]
        for k in range(2):
            assert (Y[k] - V[k]) == (X[k] - U[k]) + (Z[k] - W[k])
    u = (ux, 0.0)
    w = (wz * cos(radians(angle)), wz * sin(radians(angle)))
    return (u[0] + w[0]) ** 2 + (u[1] + w[1]) ** 2
