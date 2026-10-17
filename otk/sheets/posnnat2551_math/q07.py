"""ข้อ 7 — m + n เมื่อ m² + n² = 3789 และ (m, n) + [m, n] = 633

``solve`` scans m ≤ √S for n with m² + n² = S and checks gcd + lcm = T: m, n =
42, 45, so m + n = 87.

``check`` follows the gcd: with g = (m, n), m = gu, n = gv, g² | S and g | T;
for each such g it needs u² + v² = S/g² and uv = T/g − 1, so (u + v)² is a
perfect square, and coprimality is confirmed.
"""

from __future__ import annotations

from math import gcd, isqrt

PARAMS = {"square_sum": 3789, "gl_sum": 633}
ANSWER = 87
VARIANTS = [{"square_sum": 2 * 15 * 15, "gl_sum": 30}, {"square_sum": 13 * 13 + 26 * 26, "gl_sum": 39}, {"square_sum": 12 * 12 + 18 * 18, "gl_sum": 42}]


def solve(square_sum=3789, gl_sum=633):
    for m in range(1, isqrt(square_sum) + 1):
        rest = square_sum - m * m
        n = isqrt(rest)
        if n >= m and n * n == rest:
            g = gcd(m, n)
            if g + m * n // g == gl_sum:
                return m + n
    return None


def check(square_sum=3789, gl_sum=633):
    for g in range(1, isqrt(square_sum) + 1):
        if square_sum % (g * g) or gl_sum % g:
            continue
        s2, prod = square_sum // (g * g), gl_sum // g - 1
        total2 = s2 + 2 * prod
        root = isqrt(total2)
        if prod > 0 and root * root == total2:
            disc = root * root - 4 * prod
            r = isqrt(disc) if disc >= 0 else -1
            if r >= 0 and r * r == disc and (root + r) % 2 == 0:
                u, v = (root - r) // 2, (root + r) // 2
                if u > 0 and gcd(u, v) == 1:
                    return g * (u + v)
    return None
