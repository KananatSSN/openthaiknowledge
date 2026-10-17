"""ข้อ 9 — ∠NMH = 90°  (พิสูจน์)

The proof rests on a bisector-and-Menelaus ratio, which the generator asks for:
in a triangle ABC with D on ray BA beyond A, the bisector of ∠BAC meets BC at
N, DN meets AC at E and BE meets CD at F. The bisector gives BN/NC = AB/AC;
Menelaus in ABC (line D, E, N) and in ACD (line B, E, F) give CF/FD = AC/AD.
The solver returns that ratio (7, 4: 7/4).

``check`` builds the figure in coordinates with the given ∠BAC and measures
CF/FD.
"""

from __future__ import annotations

from fractions import Fraction
from math import cos, hypot, radians, sin

PARAMS = {"ab": 5, "ac": 7, "ad": 4, "angle": 60}
ANSWER = Fraction(7, 4)
VARIANTS = [{"ab": 6, "ac": 3, "ad": 8, "angle": 50}, {"ab": 9, "ac": 10, "ad": 2, "angle": 100},
            {"ab": 4, "ac": 11, "ad": 6, "angle": 35}]
TOL = 1e-9


def solve(ab=5, ac=7, ad=4, angle=60):
    return Fraction(ac, ad)


def _meet(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def check(ab=5, ac=7, ad=4, angle=60):
    A = (0.0, 0.0)
    B = (float(ab), 0.0)
    C = (ac * cos(radians(angle)), ac * sin(radians(angle)))
    D = (-float(ad), 0.0)  # on ray BA beyond A
    half = radians(angle) / 2
    N = _meet(A, (cos(half), sin(half)), B, C)
    E = _meet(D, N, A, C)
    F = _meet(B, E, C, D)
    return hypot(C[0] - F[0], C[1] - F[1]) / hypot(F[0] - D[0], F[1] - D[1])
