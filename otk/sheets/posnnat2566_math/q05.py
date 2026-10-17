"""ข้อ 5 — ค่าต่ำสุดของ ∠PQR

Points seeing a segment of ℓ at an obtuse angle θ lie inside an arc through its
ends; requiring every chord R sees at θ to be seen from Q at ≥ θ keeps R inside a
wedge at Q whose edge makes 270° − θ with QP. So the least ∠PQR is 270° − θ.

``check`` puts ℓ on the x-axis and Q = (0, 1). A chord of ℓ seen from R at θ
is cut by a circle through R whose centre C lies below ℓ at depth r·|cos θ|
(r = |RC|), and the points seeing that chord at ≥ θ are the inside of the
circle above ℓ. So the condition says |QC| ≤ |RC| for every such centre. ``check``
samples the centres along that curve (log-spaced out to 10¹²), confirms the
chord-angle reading on a few of them, and bisects on ∠PQR (R at distance 1/2)
for the boundary between failing and passing.
"""

from __future__ import annotations

from math import acos, cos, degrees, hypot, radians, sin

PARAMS = {"theta": 120}
ANSWER = 150
VARIANTS = [{"theta": 100}, {"theta": 140}, {"theta": 165}]
TOL = 1e-5


def solve(theta=120):
    return 270 - theta


def _angle(at, p, q):
    u = (p[0] - at[0], p[1] - at[1])
    v = (q[0] - at[0], q[1] - at[1])
    cosine = (u[0] * v[0] + u[1] * v[1]) / (hypot(*u) * hypot(*v))
    return degrees(acos(max(-1.0, min(1.0, cosine))))


def _centre(R, h, theta):
    """The centre (h, k), k < 0, of the circle through R whose chord on ℓ subtends θ."""
    c2 = cos(radians(theta)) ** 2
    qa = 1 - c2
    qb = 2 * c2 * R[1]
    qc = -c2 * ((h - R[0]) ** 2 + R[1] ** 2)
    return (h, (-qb - (qb * qb - 4 * qa * qc) ** 0.5) / (2 * qa))


def _passes(R, theta):
    Q = (0.0, 1.0)
    for j in range(-160, 481):
        for sign in (1, -1):
            C = _centre(R, R[0] + sign * 10 ** (j / 40), theta)
            r = hypot(R[0] - C[0], R[1] - C[1])
            if hypot(Q[0] - C[0], Q[1] - C[1]) > r * (1 + 1e-12):
                return False
            if j in (-40, 0, 40):  # the chord this circle cuts is seen from R at θ
                half = (r * r - C[1] * C[1]) ** 0.5
                assert abs(_angle(R, (C[0] - half, 0.0), (C[0] + half, 0.0)) - theta) < 1e-6
    return True


def check(theta=120):
    def R_at(alpha):
        # ∠PQR = alpha, measured from QP (straight down) towards +x
        return (0.5 * sin(radians(alpha)), 1.0 - 0.5 * cos(radians(alpha)))

    lo, hi = 90.0, 179.9  # fails at lo, passes at hi
    assert not _passes(R_at(lo), theta) and _passes(R_at(hi), theta)
    for _ in range(40):
        mid = (lo + hi) / 2
        if _passes(R_at(mid), theta):
            hi = mid
        else:
            lo = mid
    return hi
