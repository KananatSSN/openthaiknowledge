"""ข้อ 1 — BX = CY  (พิสูจน์)

The power of A gives AE·AB = AF·AC, and the isosceles right triangles give
AP = AC√2, AR = AB√2, so AE/AF = AP/AR = AC/AB with ∠EAP = ∠FAR: triangles
AEP and AFR are similar and FR/EP = AB/AC. That similarity drives the proof.
The solver returns AB/AC from the coordinates in PARAMS (Γ the unit circle,
B and C at the given polar angles, A inside).

``check`` builds P and R outside the triangle, E and F as the second
intersections of BA and CA with Γ, X and Y as the second intersections of EP
and FR with Γ; it asserts ∠BAC is acute and BX = CY, and returns FR/EP.
"""

from __future__ import annotations

from math import cos, hypot, radians, sin

PARAMS = {"a": (0.1, 0.2), "b_angle": 240, "c_angle": 300}
ANSWER = 1.0743705893179352
VARIANTS = [{"a": (-0.2, 0.3), "b_angle": 240, "c_angle": 300},
            {"a": (0.3, -0.1), "b_angle": 240, "c_angle": 300},
            {"a": (0.0, 0.4), "b_angle": 220, "c_angle": 290}]
TOL = 1e-9


def solve(a=(0.1, 0.2), b_angle=240, c_angle=300):
    B = (cos(radians(b_angle)), sin(radians(b_angle)))
    C = (cos(radians(c_angle)), sin(radians(c_angle)))
    return hypot(B[0] - a[0], B[1] - a[1]) / hypot(C[0] - a[0], C[1] - a[1])


def _second(point, toward):
    """Second intersection with the unit circle of the line from `point` (on it) toward `toward`."""
    dx, dy = toward[0] - point[0], toward[1] - point[1]
    t = -2 * (point[0] * dx + point[1] * dy) / (dx * dx + dy * dy)
    return (point[0] + t * dx, point[1] + t * dy)


def _apex(vertex, other, away_from):
    """P with ∠(other, vertex, P) = 90° and vertex·P = vertex·other, on the side away from `away_from`."""
    vx, vy = other[0] - vertex[0], other[1] - vertex[1]
    side = (other[0] - vertex[0]) * (away_from[1] - vertex[1]) - (other[1] - vertex[1]) * (away_from[0] - vertex[0])
    for px, py in ((-vy, vx), (vy, -vx)):
        cand = (vertex[0] + px, vertex[1] + py)
        s = (other[0] - vertex[0]) * (cand[1] - vertex[1]) - (other[1] - vertex[1]) * (cand[0] - vertex[0])
        if s * side < 0:
            return cand
    raise AssertionError


def check(a=(0.1, 0.2), b_angle=240, c_angle=300):
    A = a
    B = (cos(radians(b_angle)), sin(radians(b_angle)))
    C = (cos(radians(c_angle)), sin(radians(c_angle)))
    assert hypot(*A) < 1
    assert (B[0] - A[0]) * (C[0] - A[0]) + (B[1] - A[1]) * (C[1] - A[1]) > 0  # ∠BAC acute
    P = _apex(C, A, B)  # right angle at C, CP = CA
    R = _apex(B, A, C)  # right angle at B, BR = BA
    E = _second(B, A)
    F = _second(C, A)
    X = _second(E, P)
    Y = _second(F, R)
    assert abs(hypot(B[0] - X[0], B[1] - X[1]) - hypot(C[0] - Y[0], C[1] - Y[1])) < 1e-9
    return hypot(F[0] - R[0], F[1] - R[1]) / hypot(E[0] - P[0], E[1] - P[1])
