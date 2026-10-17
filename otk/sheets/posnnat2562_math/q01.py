"""ข้อ 1 — P เป็นจุดศูนย์กลางวงกลมล้อมรอบ BDE และ A, C, D, E อยู่บนวงกลมเดียวกัน  (พิสูจน์)

With ∠BAE = 2α and ∠BCD = 2γ bisected by AC, P (on AC and on the circle with
diameter AB) is the foot of B on AC, so P is equidistant from B, E (reflections
in AB's bisector) and from B, D likewise: P is the circumcentre of BDE. Then
∠BPE = 180° − 2α, ∠BPD = 180° − 2γ, so ∠BDE = 90° − α, ∠DEB = 90° − γ and
∠DPE = 2(α + γ). The answer is (∠BDE, ∠DEB, ∠DPE) (α, γ = 20°, 30°:
70°, 60°, 100°).

``check`` builds the pentagon: A at the origin, C on the x-axis, B where the
two bisected rays meet, E and D as the feet of B on the other two rays. It
asserts PB = PD = PE and that A, C, D, E are concyclic, then measures the
three angles.
"""

from __future__ import annotations

from math import acos, cos, degrees, hypot, radians, sin

PARAMS = {"half_a": 20, "half_c": 30}
ANSWER = (70, 60, 100)
VARIANTS = [{"half_a": 25, "half_c": 35}, {"half_a": 15, "half_c": 40}, {"half_a": 30, "half_c": 30}]
TOL = 1e-9


def solve(half_a=20, half_c=30):
    return (90 - half_a, 90 - half_c, 2 * (half_a + half_c))


def _foot(point, origin, direction):
    t = (point[0] - origin[0]) * direction[0] + (point[1] - origin[1]) * direction[1]
    return (origin[0] + t * direction[0], origin[1] + t * direction[1])


def _angle(at, p, q):
    u = (p[0] - at[0], p[1] - at[1])
    v = (q[0] - at[0], q[1] - at[1])
    return degrees(acos((u[0] * v[0] + u[1] * v[1]) / (hypot(*u) * hypot(*v))))


def _circumcentre(p, q, r):
    ax, ay = p
    bx, by = q
    cx, cy = r
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return ux, uy


def check(half_a=20, half_c=30):
    a, g = radians(half_a), radians(half_c)
    A, C = (0.0, 0.0), (10.0, 0.0)
    # B on the ray from A at +α and the ray from C at 180° − γ
    t = 10.0 * sin(g) / sin(a + g)
    B = (t * cos(a), t * sin(a))
    E = _foot(B, A, (cos(a), -sin(a)))
    D = _foot(B, C, (-cos(g), -sin(g)))
    P = (B[0], 0.0)  # the circle on diameter AB meets AC again at B's foot
    pb, pd, pe = (hypot(B[0] - P[0], B[1] - P[1]), hypot(D[0] - P[0], D[1] - P[1]),
                  hypot(E[0] - P[0], E[1] - P[1]))
    assert abs(pb - pd) < 1e-9 and abs(pb - pe) < 1e-9
    o = _circumcentre(A, C, D)
    assert abs(hypot(E[0] - o[0], E[1] - o[1]) - hypot(A[0] - o[0], A[1] - o[1])) < 1e-9
    return (_angle(D, B, E), _angle(E, D, B), _angle(P, D, E))
