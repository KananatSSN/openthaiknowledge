"""ข้อ 23 — อัตราส่วน CD : BD เมื่อ AO ตัดด้าน BC

ให้ ΔABC เป็นรูปสามเหลี่ยมมุมแหลม ที่แนบในวงกลมที่มี O เป็นจุดศูนย์กลาง ซึ่งเมื่อลาก
ส่วนของเส้นตรงจากจุด A ผ่านจุดศูนย์กลาง O ไปตัดกับด้าน BC ที่จุด D และลากส่วนของเส้นตรง
CO แล้วจะได้ ∠BAO = 15° และ ∠ACO = 45° จงหาอัตราส่วน CD : BD

O is the circumcentre, so OA = OB = OC and both named angles sit in isosceles
triangles: ∠OBA = ∠OAB = β and ∠OAC = ∠OCA = γ. Hence ∠A = β + γ, and the
inscribed-angle theorem turns the two central angles into the other two:

    ∠B = 90° − γ        ∠C = 90° − β

D is on the cevian AO, which splits ∠A into β (towards B) and γ (towards C), so
comparing the two triangles ABD and ACD on the shared altitude from D:

    CD/BD = (AC · sin γ) / (AB · sin β)

and the sine rule gives AC/AB = sin B / sin C = cos γ / cos β. The cosines pair
off with the sines:

    CD/BD = (sin γ cos γ)/(sin β cos β) = sin 2γ / sin 2β

At β = 15°, γ = 45° this is sin 90° / sin 30° = 1/(1/2) = **2**, i.e. CD : BD = 2 : 1.

Note the shape of the result: it depends on nothing but the two printed angles,
and it is 1 exactly when β = γ or β + γ = 90° — the second of which is the
right-angled case the word "มุมแหลม" excludes.

``solve`` evaluates sin 2γ / sin 2β. ``check`` draws the circle: it places A, B
and C from the central angles, intersects AO with BC, confirms that the two
printed angles really come out of the drawing and that D lands *between* B and C,
and then measures the two pieces with a ruler.
"""

from __future__ import annotations

from fractions import Fraction
from math import atan2, cos, degrees, hypot, pi, radians, sin

#: ∠BAO = bao and ∠ACO = aco, in degrees.
PARAMS = {"bao": 15, "aco": 45}
ANSWER = 2
TOL = 1e-7
VARIANTS = [
    {"bao": 20, "aco": 40},
    {"bao": 30, "aco": 30},        # isosceles: the ratio is 1
    {"bao": 10, "aco": 70},
    {"bao": 35, "aco": 50},
    {"bao": 45, "aco": 45},        # right angle at A: not an acute triangle
    {"bao": 5, "aco": 80},
]


def _snap(value: float):
    """An int or a small fraction when the value is one, else the float."""
    if abs(value - round(value)) < 1e-9:
        return int(round(value))
    close = Fraction(value).limit_denominator(64)
    return close if abs(float(close) - value) < 1e-9 else value


def solve(bao=15, aco=45):
    """CD : BD = sin 2γ / sin 2β."""
    if bao <= 0 or aco <= 0 or bao + aco >= 90:
        return None
    return _snap(sin(2 * radians(aco)) / sin(2 * radians(bao)))


def check(bao=15, aco=45):
    """Independent: draw the circle, find D, and measure CD and BD.

    A sits at the top of a unit circle; B and C are placed by their central
    angles ``180° − 2β`` and ``180° − 2γ``. The drawing is audited against the
    two angles it is supposed to show — ∠BAO and ∠ACO are recomputed from the
    coordinates — and D must fall strictly inside BC. Only then are the two
    segments measured.
    """
    if bao <= 0 or aco <= 0 or bao + aco >= 90:
        return None
    beta, gamma = radians(bao), radians(aco)
    top = pi / 2
    a = (cos(top), sin(top))
    b = (cos(top + pi - 2 * beta), sin(top + pi - 2 * beta))
    c = (cos(top - (pi - 2 * gamma)), sin(top - (pi - 2 * gamma)))
    origin = (0.0, 0.0)

    def angle(vertex, first, second) -> float:
        u = (first[0] - vertex[0], first[1] - vertex[1])
        v = (second[0] - vertex[0], second[1] - vertex[1])
        return abs(degrees(atan2(u[0] * v[1] - u[1] * v[0],
                                 u[0] * v[0] + u[1] * v[1])))

    if abs(angle(a, b, origin) - bao) > 1e-7:
        return None
    if abs(angle(c, a, origin) - aco) > 1e-7:
        return None

    # D = AO ∩ BC: solve A + u(O − A) = B + t(C − B) for t
    wx, wy = origin[0] - a[0], origin[1] - a[1]
    ex, ey = c[0] - b[0], c[1] - b[1]
    determinant = wx * (-ey) - (-ex) * wy
    if abs(determinant) < 1e-14:
        return None
    rhs = (b[0] - a[0], b[1] - a[1])
    t = (wx * rhs[1] - wy * rhs[0]) / determinant
    if not 0 < t < 1:
        return None
    d = (b[0] + t * ex, b[1] + t * ey)

    bd = hypot(d[0] - b[0], d[1] - b[1])
    cd = hypot(d[0] - c[0], d[1] - c[1])
    if bd <= 0:
        return None
    return _snap(cd / bd)
