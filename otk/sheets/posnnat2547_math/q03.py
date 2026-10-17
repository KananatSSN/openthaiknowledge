"""ข้อ 3 — สมการที่มีราก u³, v³, w³ เมื่อ u, v, w เป็นรากของ x³ − 5x² + 4x − 3

With e₁, e₂, e₃ the elementary sums: Σu³ = e₁³ − 3e₁e₂ + 3e₃; the products uv,
vw, wu have elementary sums e₂, e₁e₃, e₃², so Σ(uv)³ = e₂³ − 3e₁e₂e₃ + 3e₃²;
and (uvw)³ = e₃³. The answer (a, b, c) means x³ − ax² + bx − c = 0:
(74, −89, 27).

``check`` runs Newton's identities to the power sums p₃, p₆, p₉ of u, v, w
(the power sums of the cubes), then inverts Newton for the new elementary sums.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"e1": 5, "e2": 4, "e3": 3}
ANSWER = (74, -89, 27)
VARIANTS = [{"e1": 1, "e2": 1, "e3": 1}, {"e1": 0, "e2": -3, "e3": 2}, {"e1": 6, "e2": 11, "e3": 6}, {"e1": -2, "e2": 7, "e3": -5}]


def solve(e1=5, e2=4, e3=3):
    return (e1**3 - 3 * e1 * e2 + 3 * e3, e2**3 - 3 * e1 * e2 * e3 + 3 * e3 * e3, e3**3)


def check(e1=5, e2=4, e3=3):
    e = [Fraction(1), Fraction(e1), Fraction(e2), Fraction(e3)]
    p = [Fraction(3)]
    for k in range(1, 10):
        total = sum((-1) ** (i - 1) * e[i] * p[k - i] for i in range(1, min(k, 3) + 1) if k - i >= 1)
        if k <= 3:
            total += (-1) ** (k - 1) * k * e[k]
        p.append(total)
    s1, s2, s3 = p[3], p[6], p[9]  # power sums of the cubes
    f1 = s1
    f2 = (f1 * s1 - s2) / 2
    f3 = (s3 - f1 * s2 + f2 * s1) / 3
    return tuple(int(v) for v in (f1, f2, f3))
