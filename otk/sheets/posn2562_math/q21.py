"""ข้อ 21 — ขนาดของ ∠DCE ในพจน์ของ α

กำหนด ABCD เป็นรูปสี่เหลี่ยมจัตุรัสดังรูป โดยมี E เป็นจุดกึ่งกลางของด้าน AD และ
∠CEF = 90° ให้ ∠BCF = α จงหาขนาดของ ∠DCE ในพจน์ของ α
(คำตอบต้องไม่อยู่ในรูปของฟังก์ชันตรีโกณมิติ)

The instruction "no trigonometric functions" is the hint: the answer is linear
in α, which can only happen if **CE bisects ∠DCF**. It does — and only because
E is the *midpoint*.

Put A = (0,1), D = (1,1), B = (0,0), C = (1,0) and E = (e, 1) with F = (0, f) on
AB. The right angle at E forces

    EC · EF = 0  ⟹  f = 1 − e(1 − e)

and, writing the two tangents at C, ``tan∠DCE = 1 − e`` while
``tan∠DCF = 1/f``. The bisection ``∠DCF = 2∠DCE`` therefore says

    1/(1 − e + e²) = 2(1 − e)/(e(2 − e))   ⟺   2e³ − 5e² + 6e − 2 = 0
                                           ⟺   (2e − 1)(e² − 2e + 2) = 0

and the quadratic has no real root, so **e = 1/2 is the only position on AD**
where the bisection holds. The midpoint in the statement is not a convenience;
it is the whole hypothesis.

Given the bisection, ∠BCD = 90° splits as ``α + ∠FCE + ∠ECD`` with the last two
equal, so

    ∠DCE = (90° − α)/2 = **45° − α/2**

(numerically α = 36.87° and ∠DCE = 26.57°).

Two more angles at C come out linear for free: ``∠DCF = 90° − α`` and
``∠ECB = 45° + α/2``. Since the midpoint is forced, the generator varies *which*
of the three is asked for rather than the figure.

``solve`` tests the cubic exactly and returns the coefficient pair. ``check``
measures instead: it builds the square, finds F from the right angle, reads the
angles off with ``atan2``, confirms ∠DCE and ∠FCE really are equal, and verifies
the linear formula on the numbers before reporting the same pair.
"""

from __future__ import annotations

from fractions import Fraction
from math import atan2, degrees, isclose

#: E divides AD at num/den from A; ``ask`` picks which angle at C is wanted.
PARAMS = {"num": 1, "den": 2, "ask": "dce"}
ANSWER = (Fraction(45), Fraction(-1, 2))
VARIANTS = [
    {"num": 2, "den": 4, "ask": "dce"},      # the same point, written differently
    {"num": 1, "den": 2, "ask": "dcf"},      # ∠DCF = 90° − α
    {"num": 1, "den": 2, "ask": "ecb"},      # ∠ECB = 45° + α/2
    {"num": 1, "den": 3, "ask": "dce"},      # not the midpoint: no linear answer
    {"num": 2, "den": 3, "ask": "dce"},
    {"num": 1, "den": 1, "ask": "dce"},      # E = D
    {"num": 5, "den": 10, "ask": "ecb"},
]
#: every angle at C that the bisection makes linear in α.
ASKS = {"dce": (Fraction(45), Fraction(-1, 2)),
        "dcf": (Fraction(90), Fraction(-1)),
        "ecb": (Fraction(45), Fraction(1, 2))}


def bisects(num=1, den=2) -> bool | None:
    """Whether CE bisects ∠DCF, from the exact cubic 2e³ − 5e² + 6e − 2 = 0."""
    if den <= 0 or not 0 < num <= den:
        return None
    e = Fraction(num, den)
    if e >= 1:
        return None
    return 2 * e ** 3 - 5 * e ** 2 + 6 * e - 2 == 0


def solve(num=1, den=2, ask="dce"):
    """(constant, coefficient of α) with the asked angle = constant + coef·α."""
    got = bisects(num, den)
    if got is None or not got or ask not in ASKS:
        return None
    return ASKS[ask]


def check(num=1, den=2, ask="dce"):
    """Independent: build the square, find F, and measure the two angles.

    F comes from solving the printed right angle at E numerically; ∠DCE and
    ∠FCE are then read off the coordinates with ``atan2``. They have to come out
    equal — that is the bisection the linear answer depends on — and ∠DCE has to
    match 45° − α/2 on the numbers before the pair is reported.
    """
    if den <= 0 or not 0 < num <= den or ask not in ASKS:
        return None
    e = num / den
    if e >= 1:
        return None
    d, b, c = (1.0, 1.0), (0.0, 0.0), (1.0, 0.0)
    point_e = (e, 1.0)

    # EC · EF = 0 with F = (0, f): (1 − e)(0 − e) + (0 − 1)(f − 1) = 0
    f = 1 - e * (1 - e)
    if not 0 <= f <= 1:
        return None
    point_f = (0.0, f)
    ec = (c[0] - point_e[0], c[1] - point_e[1])
    ef = (point_f[0] - point_e[0], point_f[1] - point_e[1])
    if abs(ec[0] * ef[0] + ec[1] * ef[1]) > 1e-12:
        return None

    def angle_at_c(p, q) -> float:
        first = atan2(p[1] - c[1], p[0] - c[0])
        second = atan2(q[1] - c[1], q[0] - c[0])
        out = abs(degrees(first - second)) % 360
        return min(out, 360 - out)

    alpha = angle_at_c(b, point_f)
    dce = angle_at_c(d, point_e)
    fce = angle_at_c(point_f, point_e)
    if not isclose(dce, fce, abs_tol=1e-9):
        return None
    measured = {"dce": dce,
                "dcf": angle_at_c(d, point_f),
                "ecb": angle_at_c(point_e, b)}[ask]
    constant, coefficient = ASKS[ask]
    if not isclose(measured, float(constant) + float(coefficient) * alpha,
                   abs_tol=1e-9):
        return None
    return ASKS[ask]
