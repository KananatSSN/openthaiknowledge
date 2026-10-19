"""ข้อ 7 — O₁O₂ คงตัวเมื่อ E ทำให้ BE ∥ AD  (พิสูจน์)

Take E on CD with BE ∥ AD. Then ∠BEP = ∠ADP = θ, so PA = 2R₁ sin θ and
PB = 2R₂ sin θ, and both radii make the angle 90° − θ with their chords: a
spiral similarity at P takes A, B to O₁, O₂ with ratio 1/(2 sin θ). Hence
O₁O₂ = AB/(2 sin ∠ADC) for every P. The solver returns that length.

``check`` builds a quadrilateral with ∠ADC = θ, places E, computes both
circumcentres for many P on CD, confirms the distance does not move, and
returns it.
"""

from __future__ import annotations

from math import cos, hypot, radians, sin

PARAMS = {"side": 2, "angle": 60}
ANSWER = 1.1547005383792517
VARIANTS = [{"side": 3, "angle": 45}, {"side": 2, "angle": 90}, {"side": 5, "angle": 120}]
TOL = 1e-9


def solve(side=2, angle=60):
    return side / (2 * sin(radians(angle)))


def _circumcentre(p, q, r):
    ax, ay = p
    bx, by = q
    cx, cy = r
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return ux, uy


def check(side=2, angle=60):
    t = radians(angle)
    D, C = (0.0, 0.0), (12.0, 0.0)
    A = (4 * cos(t), 4 * sin(t))
    B = (A[0] + side * cos(radians(-10)), A[1] + side * sin(radians(-10)))
    E = (B[0] - B[1] / sin(t) * cos(t), 0.0)
    assert 0 < E[0] < C[0]
    lengths = []
    for x in (0.7, 2.3, 5.1, 8.9, 11.4):
        if abs(x - E[0]) < 1e-6:
            continue
        P = (x, 0.0)
        o1 = _circumcentre(A, P, D)
        o2 = _circumcentre(B, P, E)
        lengths.append(hypot(o1[0] - o2[0], o1[1] - o2[1]))
    assert max(lengths) - min(lengths) < 1e-9
    return lengths[0]
