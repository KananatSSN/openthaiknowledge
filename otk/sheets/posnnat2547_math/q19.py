"""ข้อ 19 — a, b, c ที่ทำให้ a + 2b + 3c สูงสุดเมื่อ 9a² + 4b² + c² = 91

Cauchy–Schwarz: (Σ cᵢxᵢ)² ≤ (Σ wᵢxᵢ²)(Σ cᵢ²/wᵢ), with equality when wᵢxᵢ/cᵢ
is constant: xᵢ = (cᵢ/wᵢ)·t with t² = K/Σ(cᵢ²/wᵢ). Here t = 3 and
(a, b, c) = (1/3, 3/2, 9).

``check`` uses the sphere picture instead: with uᵢ = √wᵢ·xᵢ on the sphere of
radius √K, the linear form is a dot product with vᵢ = cᵢ/√wᵢ, maximised at
u = √K·v/|v|.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"weights": (9, 4, 1), "coeffs": (1, 2, 3), "k": 91}
ANSWER = (Fraction(1, 3), Fraction(3, 2), Fraction(9))
VARIANTS = [{"weights": (1, 4, 9), "coeffs": (1, 2, 3), "k": 49}, {"weights": (4, 1, 9), "coeffs": (2, 1, 1), "k": 52}, {"coeffs": (3, 2, 1), "k": 10}]


def solve(weights=(9, 4, 1), coeffs=(1, 2, 3), k=91):
    w_total = sum(Fraction(c * c, w) for c, w in zip(coeffs, weights))
    t = math.sqrt(k / w_total)
    return tuple(c * t / w for c, w in zip(coeffs, weights))


def check(weights=(9, 4, 1), coeffs=(1, 2, 3), k=91):
    v = [c / math.sqrt(w) for c, w in zip(coeffs, weights)]
    norm = math.sqrt(sum(x * x for x in v))
    u = [math.sqrt(k) * x / norm for x in v]
    return tuple(ui / math.sqrt(w) for ui, w in zip(u, weights))
