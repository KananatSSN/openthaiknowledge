"""ข้อ 7 — ถ้า S₁, S₂, S₃ เป็นจำนวนเต็มและ 6 | 5S₁ − 3S₂ − 2S₃ แล้ว Sₙ เป็นจำนวนเต็มทุก n  (พิสูจน์)

The condition makes e₂ = (S₁² − S₂)/2 and e₃ = (S₁³ − 3S₁S₂ + 2S₃)/6 integers,
and Newton's recurrence Sₙ = e₁Sₙ₋₁ − e₂Sₙ₋₂ + e₃Sₙ₋₃ keeps Sₙ integral. The
solver returns Sₙ (S₁, S₂, S₃ = 1, 3, 1 and n = 10: 3).

``check`` finds a, b, c as the roots of t³ − e₁t² + e₂t − e₃ (Durand–Kerner)
and adds their n-th powers.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"s1": 1, "s2": 3, "s3": 1, "n": 10}
ANSWER = 3
TOL = 1e-7
VARIANTS = [{"s1": 2, "s2": 6, "s3": 2, "n": 7}, {"s1": 0, "s2": 2, "s3": 3, "n": 9}, {"n": 4}]


def solve(s1=1, s2=3, s3=1, n=10):
    e1 = Fraction(s1)
    e2 = Fraction(s1 * s1 - s2, 2)
    e3 = Fraction(s1**3 - 3 * s1 * s2 + 2 * s3, 6)
    s = [Fraction(3), e1, e1 * e1 - 2 * e2]
    s.append(e1 * s[2] - e2 * s[1] + 3 * e3)
    while len(s) <= n:
        s.append(e1 * s[-1] - e2 * s[-2] + e3 * s[-3])
    return s[n]


def check(s1=1, s2=3, s3=1, n=10):
    e1 = s1
    e2 = (s1 * s1 - s2) / 2
    e3 = (s1**3 - 3 * s1 * s2 + 2 * s3) / 6

    def poly(z):
        return ((z - e1) * z + e2) * z - e3

    roots = [complex(0.4, 0.9) ** k for k in range(3)]
    for _ in range(1000):
        new = []
        for i, r in enumerate(roots):
            denom = 1
            for j, w in enumerate(roots):
                if i != j:
                    denom *= r - w
            new.append(r - poly(r) / denom)
        roots = new
    return sum(r**n for r in roots).real
