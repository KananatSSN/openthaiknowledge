"""ข้อ 1 — ค่าของ (x+a)/(x−a) เมื่อ x² + a² = 6ax

กำหนดให้ a และ x เป็นจำนวนจริง โดยที่ 0 < a < x และ x² + a² = 6ax
จงหาค่าของ (x + a)/(x − a)

Squaring the wanted ratio is the whole idea:

    ((x+a)/(x−a))² = (x² + 2ax + a²)/(x² − 2ax + a²)

and the *given* relation replaces x² + a² in both places at once, leaving
(6ax + 2ax)/(6ax − 2ax) = 8ax/4ax = 2. Since x > a > 0 the ratio is positive, so
it is **√2** — and note neither a nor x is ever determined, only their ratio.

In general, x² + a² = k·ax gives ((x+a)/(x−a))² = (k+2)/(k−2), so the answer is
rational exactly when (k+2)/(k−2) is a perfect square of a rational.

``solve`` returns that closed form. ``check`` never touches the identity: it
fixes a = 1, solves the quadratic x² − kx + 1 = 0 for the root with x > 1, and
evaluates the ratio numerically.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: x² + a² = k·a·x, with 0 < a < x.
PARAMS = {"k": 6}
ANSWER = math.sqrt(2)
TOL = 1e-9
VARIANTS = [
    {"k": 3},
    {"k": 4},
    {"k": 5},
    {"k": 10},
    {"k": 18},
    {"k": 2},        # x = a, so x > a fails and there is no answer
]


def solve(k=6):
    """√((k+2)/(k−2)) — the ratio squared is (k+2)/(k−2)."""
    if k <= 2:
        return None          # x > a > 0 needs two distinct positive roots
    ratio = Fraction(k + 2, k - 2)
    return math.sqrt(ratio)


def check(k=6):
    """Independent: build the actual x for a = 1 and measure the ratio.

    x² − kx + 1 = 0 has roots that multiply to 1, so the larger one is the x > a
    the stem asks for. Nothing here knows that the answer squares to (k+2)/(k−2).
    """
    if k <= 2:
        return None
    disc = k * k - 4
    if disc <= 0:
        return None
    a = 1.0
    x = (k + math.sqrt(disc)) / 2
    if not x > a > 0:
        return None
    if abs(x * x + a * a - k * a * x) > 1e-9 * max(1.0, k * a * x):
        return None
    return (x + a) / (x - a)
