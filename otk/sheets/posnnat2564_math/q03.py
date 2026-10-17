"""ข้อ 3 — ค่าต่ำสุดของ aᵃbc + bᵇca + cᶜab เมื่อ ab + bc + ca = abc

For the family ab + bc + ca = abc/s: 1/a + 1/b + 1/c = 1/s gives abc ≥ (3s)³ by
AM–GM, and F = abc(a^(a−1) + b^(b−1) + c^(c−1)) is smallest at a = b = c = 3s,
giving 3(3s)^(3s+2). The source (s = 1) gives 729.

``check`` evaluates F on a grid of (a, b) around 3s with c fixed by the
constraint, and returns the least value found (the grid contains a = b = 3s).
"""

from __future__ import annotations

PARAMS = {"scale": 1}
ANSWER = 729
VARIANTS = [{"scale": 2}, {"scale": 3}, {"scale": 4}]
TOL = 1e-9


def solve(scale=1):
    return 3 * (3 * scale) ** (3 * scale + 2)


def check(scale=1):
    s = scale
    best = None
    for i in range(-30, 61):
        for j in range(-30, 61):
            a, b = 3 * s * (1 + i / 60), 3 * s * (1 + j / 60)
            inv = 1 / s - 1 / a - 1 / b
            if inv <= 0:
                continue
            c = 1 / inv
            if c > 12 * s:
                continue
            value = a**a * b * c + b**b * c * a + c**c * a * b
            best = value if best is None else min(best, value)
    return best
