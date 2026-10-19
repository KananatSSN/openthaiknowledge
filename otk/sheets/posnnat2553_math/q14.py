"""วันที่สอง ข้อ 4 — a₃ = √(a₁² + a₂²) ฯลฯ เป็นด้านของสามเหลี่ยม และ p₃² ≥ p₁² + p₂²  (พิสูจน์)

With x, y, z the squared sides, 16Δ² = 2xy + 2yz + 2zx − x² − y² − z² is a
Lorentzian quadratic form; adding the squared sides adds the vectors, and
Aczél's inequality gives 16Δ₃² ≥ (4Δ₁ + 4Δ₂)² > 0. The solver returns 16Δ₃²
for two given triangles ((3, 4, 5), (2, 3, 4)).

``check`` builds the third triangle from its side lengths in coordinates and
computes 16·area².
"""

from __future__ import annotations

import math

PARAMS = {"t1": (3, 4, 5), "t2": (2, 3, 4)}
ANSWER = 1291
TOL = 1e-9
VARIANTS = [{"t1": (5, 5, 6), "t2": (7, 8, 9)}, {"t2": (3, 4, 5)}, {"t1": (2, 2, 3), "t2": (6, 7, 11)}]


def solve(t1=(3, 4, 5), t2=(2, 3, 4)):
    x, y, z = (u * u + v * v for u, v in zip(t1, t2))
    return 2 * (x * y + y * z + z * x) - x * x - y * y - z * z


def check(t1=(3, 4, 5), t2=(2, 3, 4)):
    a, b, c = (math.sqrt(u * u + v * v) for u, v in zip(t1, t2))
    px = (c * c - b * b + a * a) / (2 * a)
    area = a * math.sqrt(c * c - px * px) / 2
    return 16 * area * area
