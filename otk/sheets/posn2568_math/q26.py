"""ข้อ 26 — ขนาดของ ∠AFE

ABC เป็นรูปสามเหลี่ยมแนบในวงกลม โดยมี ∠ABC = 43° และ ∠ACB = 67°
ให้ DE̅ เป็นเส้นผ่านศูนย์กลางของวงกลมตัด AB̅ ที่จุด F และ AD̅ แบ่งครึ่ง ∠BAC
ขนาดของ ∠AFE เท่ากับกี่องศา

Method: AD bisecting ∠BAC puts D at the midpoint of arc BC not containing A, so
walking the circle A → B → D → C → A covers arcs 2C, A, A, 2B. Taking E as D's
antipode puts it 180° round, at arc distance 2C + A − 180 from A. ∠AFE is the
exterior angle of triangle AFD at F, so
    ∠AFE = ∠FAD + ∠ADE = A/2 + (2C + A − 180)/2 = A + C − 90 = 90° − B,
and the ∠ACB given in the question turns out not to matter at all: the answer is
90° − ∠ABC = 47°.

That independence is exactly the kind of claim worth distrusting, so ``check``
builds the circle, both chords, their crossing point F, and measures ∠AFE with a
dot product — for the given angles *and* for other ∠ACB with ∠ABC held fixed.
"""

from __future__ import annotations

import math

TOL = 1e-7

PARAMS = {"abc_deg": 43, "acb_deg": 67}
ANSWER = 47.0
VARIANTS = [
    {"abc_deg": 43, "acb_deg": 80},       # same answer, different ∠ACB
    {"abc_deg": 30, "acb_deg": 75},
    {"abc_deg": 60, "acb_deg": 70},
    {"abc_deg": 20, "acb_deg": 100},
    {"abc_deg": 75, "acb_deg": 55},
]


def solve(abc_deg=43, acb_deg=67):
    """∠AFE in degrees."""
    bac = 180 - abc_deg - acb_deg
    if min(bac, abc_deg, acb_deg) <= 0:
        raise ValueError("not a triangle")
    if abc_deg >= 90:
        raise ValueError("E falls on the far arc; the figure no longer applies")
    return 90.0 - abc_deg


def _point(deg: float) -> tuple[float, float]:
    return (math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def check(abc_deg=43, acb_deg=67):
    """Independent: construct the circle and measure the angle at F."""
    bac = 180 - abc_deg - acb_deg
    # Arc positions around the unit circle, A at 0.
    pos_a = 0.0
    pos_b = 2 * acb_deg                      # arc AB = 2·∠ACB
    pos_d = pos_b + bac                      # D bisects arc BC (= 2·∠BAC)
    pos_c = pos_b + 2 * bac
    pos_e = (pos_d + 180) % 360

    a, b, c, d, e = (_point(p) for p in (pos_a, pos_b, pos_c, pos_d, pos_e))

    # Sanity: the inscribed angles really are the ones asked for.
    def angle(u, v, w):
        v1 = (u[0] - v[0], u[1] - v[1])
        v2 = (w[0] - v[0], w[1] - v[1])
        cos = (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))
        return math.degrees(math.acos(max(-1.0, min(1.0, cos))))

    assert abs(angle(a, b, c) - abc_deg) < 1e-7, "∠ABC came out wrong"
    assert abs(angle(a, c, b) - acb_deg) < 1e-7, "∠ACB came out wrong"
    assert abs(angle(b, a, d) - angle(c, a, d)) < 1e-7, "AD does not bisect ∠BAC"
    assert math.hypot(d[0] + e[0], d[1] + e[1]) < 1e-9, "DE is not a diameter"

    # F = line AB ∩ line DE
    def cross(p, q, r, s):
        x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
        x3, y3, x4, y4 = r[0], r[1], s[0], s[1]
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t1 = x1 * y2 - y1 * x2
        t2 = x3 * y4 - y3 * x4
        return ((t1 * (x3 - x4) - (x1 - x2) * t2) / den,
                (t1 * (y3 - y4) - (y1 - y2) * t2) / den)

    f = cross(a, b, d, e)
    return angle(a, f, e)
