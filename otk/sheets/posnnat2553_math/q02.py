"""ข้อ 2 — DF ในรูป x = BC, y = CF, z = BF

BCED is an isosceles trapezoid (DE ∥ BC) and EF ⟂ BC makes ∠DEF = 90°, so DF
is a diameter: DF = 2R = xyz/(2Δ) for triangle BCF, i.e.
2xyz/√(2x²y² + 2y²z² + 2z²x² − x⁴ − y⁴ − z⁴). PARAMS fixes x, y, z = 13, 14, 15.

``check`` places B, C, F in coordinates and measures the circumcircle's diameter.
"""

from __future__ import annotations

import math
from fractions import Fraction
from math import isqrt

PARAMS = {"x": 13, "y": 14, "z": 15}
ANSWER = Fraction(65, 4)
TOL = 1e-9
VARIANTS = [{"x": 5, "y": 5, "z": 6}, {"x": 9, "y": 10, "z": 17}, {"x": 20, "y": 13, "z": 21}]


def solve(x=13, y=14, z=15):
    sixteen = 2 * (x * x * y * y + y * y * z * z + z * z * x * x) - x**4 - y**4 - z**4
    root = isqrt(sixteen)
    return Fraction(2 * x * y * z, root) if root * root == sixteen else 2 * x * y * z / math.sqrt(sixteen)


def check(x=13, y=14, z=15):
    # B = (0, 0), C = (x, 0)
    fx = (z * z - y * y + x * x) / (2 * x)
    f = (fx, math.sqrt(z * z - fx * fx))
    # circumcentre on x = x/2
    cy = (f[0] ** 2 + f[1] ** 2 - x * f[0]) / (2 * f[1])
    return 2 * math.hypot(x / 2, cy)
