"""ข้อ 18 — รัศมีของวงกลมเล็กสองวงที่แทรกอยู่ระหว่างวงกลมสองวง

จากรูป วงกลม A และวงกลม B มีรัศมีเป็น 4 หน่วย และ 1 หน่วยตามลำดับ วงกลมทั้งสอง
สัมผัสกันภายนอกและสัมผัสกับเส้นตรง L  สร้างวงกลมเล็กสองวงรัศมีเท่ากันเป็น r หน่วย
ซึ่งต่างสัมผัสกันภายนอก และสัมผัสกับเส้นตรง L โดยวงหนึ่งสัมผัสภายนอกกับวงกลม A
อีกวงหนึ่งสัมผัสภายนอกกับวงกลม B  จงหาค่าของ r

รูปประกอบ (extract/figures/item18.png): both big circles rest on L with the big
one on the left; the two equal small circles sit **between** them, side by side in
the gap, each touching L, the other small circle, and one big circle.

Two circles of radii ρ₁, ρ₂ that both touch a line and touch each other have
their touch points 2√(ρ₁ρ₂) apart. Reading the four touch points along L from A's
to B's therefore gives

    2√(R_A r) + 2r + 2√(R_B r) = 2√(R_A R_B)

and with s = √r that is s² + (√R_A + √R_B)s - √(R_A R_B) = 0, so

    s = ½(-(√R_A + √R_B) + √(R_A + 6√(R_A R_B) + R_B))
    r = s².

For R_A = 4, R_B = 1 the quadratic is s² + 3s - 2 = 0, s = (-3 + √17)/2, and

    r = (13 - 3√17)/2 ≈ 0.31534.

``solve`` returns that as a float — the value is irrational — and ``ANSWER``
records the surd it must reproduce. When both radii are perfect squares the
answer is a clean surd (M - N√D)/2, which :func:`exact_form` returns for the
generator to typeset; ``solve`` and :func:`exact_form` are checked against each
other by the tests.

``check`` never uses the 2√(ρ₁ρ₂) spacing rule: it places circles by solving the
tangency *distances* numerically and bisects r until the two small ones touch.
"""

from __future__ import annotations

import math

#: radii of the two big circles.
PARAMS = {"r_a": 4, "r_b": 1}
ANSWER = (13 - 3 * math.sqrt(17)) / 2
VARIANTS = [
    {"r_a": 1, "r_b": 1},          # equal, and the answer is 3 - 2√2
    {"r_a": 9, "r_b": 4},
    {"r_a": 16, "r_b": 1},
    {"r_a": 25, "r_b": 9},
    {"r_a": 3, "r_b": 2},          # not perfect squares — still a real radius
    {"r_a": 4, "r_b": 0},          # degenerate
]
TOL = 1e-9


def solve(r_a=4, r_b=1):
    """The common radius r of the two inserted circles."""
    if r_a <= 0 or r_b <= 0:
        return None
    p, q = math.sqrt(r_a), math.sqrt(r_b)
    s = (-(p + q) + math.sqrt((p + q) ** 2 + 4 * p * q)) / 2
    return s * s


def exact_form(r_a=4, r_b=1):
    """``(M, N, D)`` with r = (M - N√D)/2, when both radii are perfect squares.

    With p = √R_A and q = √R_B integers, s = (-(p+q) + √D)/2 for D = p²+6pq+q²,
    and r = s² = ((p+q)² + 2pq - (p+q)√D)/2. Any square factor of D is pulled out
    of the root so the printed form is reduced; ``None`` when a radius is not a
    perfect square and no such form exists.
    """
    p, q = math.isqrt(int(r_a)), math.isqrt(int(r_b))
    if p * p != r_a or q * q != r_b or r_a <= 0 or r_b <= 0:
        return None
    d, n = p * p + 6 * p * q + q * q, p + q
    k = 1                                       # pull square factors out of √D
    f = 2
    while f * f <= d:
        while d % (f * f) == 0:
            d //= f * f
            k *= f
        f += 1
    return (p + q) ** 2 + 2 * p * q, n * k, d


def _touch_x(big_r: float, big_x: float, r: float, right: bool) -> float:
    """x of a radius-r circle on the line, tangent externally to the big one.

    Solved from the distance between centres rather than from any spacing
    formula: the centres are (big_x, big_r) and (x, r), and tangency means the
    distance is big_r + r.
    """
    want = big_r + r
    lo, hi = big_x, big_x + 4 * (big_r + r) + 1.0
    if not right:
        lo, hi = big_x, big_x - 4 * (big_r + r) - 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if math.hypot(mid - big_x, r - big_r) < want:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def check(r_a=4, r_b=1):
    """Independent: build the four circles and bisect r until the two small touch."""
    if r_a <= 0 or r_b <= 0:
        return None
    ra, rb = float(r_a), float(r_b)
    # A rests at x = 0; B's centre is placed by its tangency to A and to the line.
    xb = math.sqrt((ra + rb) ** 2 - (ra - rb) ** 2)
    assert abs(math.hypot(xb, rb - ra) - (ra + rb)) < 1e-9

    def gap(r: float) -> float:
        x1 = _touch_x(ra, 0.0, r, right=True)
        x2 = _touch_x(rb, xb, r, right=False)
        return (x2 - x1) - 2 * r          # > 0 while the small circles still fit

    lo, hi = 1e-12, min(ra, rb)
    if gap(lo) < 0 or gap(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if gap(mid) > 0:
            lo = mid
        else:
            hi = mid
    r = (lo + hi) / 2
    x1 = _touch_x(ra, 0.0, r, right=True)
    x2 = _touch_x(rb, xb, r, right=False)
    assert abs(math.hypot(x1, r - ra) - (ra + r)) < 1e-6
    assert abs(math.hypot(x2 - xb, r - rb) - (rb + r)) < 1e-6
    assert abs(abs(x2 - x1) - 2 * r) < 1e-6
    return r


def _exact_value(r_a=4, r_b=1) -> float | None:
    """The surd form, evaluated — used by the tests to tie the two together."""
    form = exact_form(r_a, r_b)
    if form is None:
        return None
    m, n, d = form
    return (m - n * math.sqrt(d)) / 2
