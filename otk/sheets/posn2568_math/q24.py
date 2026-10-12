"""ข้อ 24 — ครึ่งวงกลมซ้อนกันในครึ่งวงกลมใหญ่

S เป็นครึ่งวงกลมใหญ่ เส้นผ่านศูนย์กลาง AB̅ ยาว 4 หน่วย ศูนย์กลางที่ O  ภายใน S มี
ครึ่งวงกลมเล็ก 2 รูป วางซ้อนกันในแนวดิ่ง โดยครึ่งวงกลมที่หนึ่งมีเส้นผ่านศูนย์กลาง CD̅
ขนานกับ AB̅ และส่วนโค้งสัมผัส AB̅ ที่ O  ครึ่งวงกลมที่สองมีเส้นผ่านศูนย์กลาง EF̅
ขนานกับ AB̅ และส่วนโค้งสัมผัส CD̅  จงหาความยาวของ EF̅

Method: every level is a chord of S, so a semicircle whose diameter sits at
height y has radius √(R² − y²); "its arc touches the level below" says that
radius also equals the gap y − y_prev. Setting those equal,
    (y − y_prev)² = R² − y²  ⟹  y = ( y_prev + √(2R² − y_prev²) ) / 2,
a one-line recursion down the stack from y₀ = 0. Two levels of it give
    y₁ = R/√2 ,  y₂ = R(√2+√6)/4 ,  EF = 2(y₂ − y₁) = R(√6 − √2)/2,
which at R = 2 is √6 − √2 ≈ 1.0353.

``check`` solves each level by bisecting the tangency condition directly instead
of using the quadratic formula, and asserts the endpoints really do land on S.
"""

from __future__ import annotations

import math

TOL = 1e-7

PARAMS = {"diameter": 4, "levels": 2}
ANSWER = 1.035276180410083            # √6 − √2
VARIANTS = [
    {"levels": 1},
    {"levels": 3},
    {"levels": 5},
    {"diameter": 10, "levels": 2},
    {"diameter": 7, "levels": 4},
]


def heights(diameter=4, levels=2) -> list[float]:
    """Heights of each stacked diameter above AB, innermost last."""
    radius = diameter / 2
    out, y = [], 0.0
    for _ in range(levels):
        y = (y + math.sqrt(2 * radius * radius - y * y)) / 2
        out.append(y)
    return out


def solve(diameter=4, levels=2):
    """Length of the topmost stacked diameter."""
    if levels < 1:
        raise ValueError("there must be at least one stacked semicircle")
    ys = heights(diameter, levels)
    below = ys[-2] if levels >= 2 else 0.0
    return 2 * (ys[-1] - below)


def check(diameter=4, levels=2):
    """Independent: bisect each tangency condition; verify the chord fits S."""
    radius = diameter / 2
    y_prev = 0.0
    for _ in range(levels):
        # want (y − y_prev) == √(R² − y²): the gap equals the chord half-width
        def gap_minus_radius(y: float, prev=y_prev) -> float:
            return (y - prev) - math.sqrt(max(0.0, radius * radius - y * y))

        lo, hi = y_prev, radius
        for _ in range(300):
            mid = (lo + hi) / 2
            if gap_minus_radius(mid) < 0:
                lo = mid
            else:
                hi = mid
        y_prev, y = y_prev, (lo + hi) / 2
        half = math.sqrt(max(0.0, radius * radius - y * y))
        assert abs(math.hypot(half, y) - radius) < 1e-9, \
            "the chord endpoints do not lie on the big semicircle"
        last_gap = y - y_prev
        y_prev = y
    return 2 * last_gap
