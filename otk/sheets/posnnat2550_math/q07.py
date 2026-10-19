"""ข้อ 7 — a⁴ + b⁴ + c⁴ เมื่อ a + b + c = 1, a² + b² + c² = 2, a³ + b³ + c³ = 3

Newton: e₁ = 1, e₂ = (p₁² − p₂)/2 = −1/2, e₃ = (p₃ − e₁p₂ + e₂p₁)/3 = 1/6, and
p₄ = e₁p₃ − e₂p₂ + e₃p₁ = 25/6.

``check`` finds the three complex roots of t³ − e₁t² + e₂t − e₃ by the
Durand–Kerner iteration, confirms p₁, p₂, p₃, and sums the fourth powers.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"p1": 1, "p2": 2, "p3": 3}
ANSWER = Fraction(25, 6)
TOL = 1e-9
VARIANTS = [{"p1": -1, "p2": 6, "p3": 8}, {"p1": 0, "p2": 0, "p3": 3}, {"p1": 3, "p2": 5, "p3": 9}]


def solve(p1=1, p2=2, p3=3):
    e1 = Fraction(p1)
    e2 = (e1 * e1 - p2) / 2
    e3 = (p3 - e1 * p2 + e2 * p1) / 3
    return e1 * p3 - e2 * p2 + e3 * p1


def check(p1=1, p2=2, p3=3):
    e1 = p1
    e2 = (p1 * p1 - p2) / 2
    e3 = (p3 - e1 * p2 + e2 * p1) / 3

    def poly(z):
        return ((z - e1) * z + e2) * z - e3

    roots = [complex(0.4, 0.9) ** k for k in range(3)]
    for _ in range(500):
        new = []
        for i, r in enumerate(roots):
            denom = 1
            for j, s in enumerate(roots):
                if i != j:
                    denom *= r - s
            new.append(r - poly(r) / denom)
        roots = new
    for k, want in ((1, p1), (2, p2), (3, p3)):
        assert abs(sum(r**k for r in roots) - want) < 1e-9
    return sum(r**4 for r in roots).real
