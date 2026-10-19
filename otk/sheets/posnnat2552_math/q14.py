"""วันที่สอง ข้อ 4 — (m − n)² = kmn + m + n มีคำตอบเป็นจำนวนอนันต์  (พิสูจน์)

As a quadratic in m: m² − ((k + 2)n + 1)m + n² − n = 0, so with one root m the
other is (k + 2)n + 1 − m (Vieta), and (m, n) → ((k + 2)m + 1 − n, m) climbs
forever from (k + 3, 1). The solver returns the pair after `steps` jumps
(k = 1, 4 steps).

``check`` climbs with the quadratic formula (integer square root) instead of
Vieta's sum, verifying each pair in the original equation.
"""

from __future__ import annotations

from math import isqrt

PARAMS = {"k": 1, "steps": 4}
ANSWER = (232, 88)
VARIANTS = [{"k": 2, "steps": 3}, {"k": 5, "steps": 5}, {"steps": 1}]


def solve(k=1, steps=4):
    m, n = k + 3, 1
    for _ in range(steps):
        m, n = (k + 2) * m + 1 - n, m
    return (m, n)


def check(k=1, steps=4):
    m, n = k + 3, 1
    assert (m - n) ** 2 == k * m * n + m + n
    for _ in range(steps):
        n = m
        bq = (k + 2) * n + 1
        disc = bq * bq - 4 * (n * n - n)
        root = isqrt(disc)
        assert root * root == disc
        m = (bq + root) // 2
        assert (m - n) ** 2 == k * m * n + m + n
    return (m, n)
