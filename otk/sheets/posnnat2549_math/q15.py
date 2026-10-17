"""ข้อ 15 — จำนวน n < 2549 ที่ x² + x − n มีรากเป็นจำนวนเต็ม

Roots r and −a − r with product −n give n = r(r + a); r(r + a) < N for
r = 1, …, 49 when a = 1 (49·50 = 2450, 50·51 = 2550).

``check`` tests each n by the discriminant a² + 4n being a perfect square of
the right parity.
"""

from __future__ import annotations

from math import isqrt

PARAMS = {"a": 1, "bound": 2549}
ANSWER = 49
VARIANTS = [{"a": 3, "bound": 4862}, {"a": 2, "bound": 50}, {"a": 9, "bound": 777}, {"bound": 2}]


def solve(a=1, bound=2549):
    r = 0
    while (r + 1) * (r + 1 + a) < bound:
        r += 1
    return r


def check(a=1, bound=2549):
    count = 0
    for n in range(1, bound):
        disc = a * a + 4 * n
        root = isqrt(disc)
        count += root * root == disc and (root - a) % 2 == 0
    return count
