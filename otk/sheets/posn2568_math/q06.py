"""ข้อ 6 — ช่วงของ a ที่ทำให้ควอร์ติกมีรากจริง 4 รากต่างกัน

จงหาเซตของจำนวนจริง a ทั้งหมดที่ทำให้สมการ
    x⁴ − a·x² − (135/4)·a + 2025 = 0        (ทั่วไป: x⁴ − a·x² − K·a + C = 0)
มีคำตอบเป็นจำนวนจริงที่แตกต่างกันทั้งหมด 4 คำตอบ

Method: substitute t = x². The quartic has four distinct real roots exactly when
the quadratic t² − a·t + (C − K·a) has two distinct *positive* roots, i.e. all
three of

    discriminant  a² + 4K·a − 4C > 0      →  a > −2K + 2√(K²+C)   (or very negative)
    sum of roots  a > 0
    product       C − K·a > 0             →  a < C/K

Intersecting those leaves one open interval. For the sheet's K = 135/4, C = 2025
it is 45 < a < 60.

``check`` ignores all of that and asks numpy: sample a densely, count the
distinct real roots of the quartic itself, and report where the count is 4.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"k_num": 135, "k_den": 4, "c": 2025}
ANSWER = (45.0, 60.0)
VARIANTS = [
    {"k_num": 1, "k_den": 1, "c": 4},
    {"k_num": 10, "k_den": 1, "c": 100},
    {"k_num": 135, "k_den": 4, "c": 1024},
    {"k_num": 7, "k_den": 2, "c": 49},
    {"k_num": 3, "k_den": 1, "c": 9},
]


def solve(k_num=135, k_den=4, c=2025):
    """The open interval (lo, hi) of a giving four distinct real roots."""
    k = Fraction(k_num, k_den)
    disc_lo = -2 * k + 2 * math.sqrt(float(k * k + c))   # a² + 4Ka − 4C > 0
    lo = max(0.0, float(disc_lo))                        # with sum-of-roots a > 0
    hi = float(Fraction(c) / k)                          # product C − Ka > 0
    if lo >= hi:
        return None
    return (lo, hi)


def root_count(a: float, k: float, c: float, tol=1e-7) -> int:
    """Distinct real roots of x⁴ − a·x² − k·a + c, counted numerically."""
    import numpy as np
    roots = np.roots([1.0, 0.0, -a, 0.0, c - k * a])
    real = sorted(float(r.real) for r in roots if abs(r.imag) < tol)
    distinct = [r for i, r in enumerate(real) if i == 0 or r - real[i - 1] > tol]
    return len(distinct)


def check(k_num=135, k_den=4, c=2025, samples=4000, span=4.0):
    """Independent: find the four-real-root region by counting roots directly.

    Scans a wide window, keeps the a values that really do give four distinct
    real roots, then bisects each edge to pin the boundary. No use is made of
    the discriminant algebra above.
    """
    k = k_num / k_den
    hi_guess = c / k
    a_max = max(hi_guess * span, 10.0)
    xs = [(-a_max) + 2 * a_max * i / samples for i in range(samples + 1)]
    good = [a for a in xs if root_count(a, k, c) == 4]
    if not good:
        return None

    def edge(inside: float, outside: float) -> float:
        for _ in range(200):
            mid = (inside + outside) / 2
            if root_count(mid, k, c) == 4:
                inside = mid
            else:
                outside = mid
        return (inside + outside) / 2

    step = 2 * a_max / samples
    return (edge(good[0], good[0] - step), edge(good[-1], good[-1] + step))
