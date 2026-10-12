"""ข้อ 12 — จำนวนวิเศษสามหลัก

จำนวนเต็มบวกสามหลัก n = abc (a ≠ 0) กำหนด
    d(n) = a² + b² + c²      และ      s(n) = a + 2b + c
เรียก n ว่า "จำนวนวิเศษ" ถ้า d(n) ≤ 2·s(n)  มีจำนวนวิเศษทั้งหมดกี่จำนวน

Method: the condition separates by digit — completing the square in each of the
three variables turns d(n) ≤ 2s(n) into
    (a−1)² + (b−2)² + (c−1)² ≤ 6,
so a digit can only stray a little from (1, 2, 1) and the count is a small
convolution rather than a scan of all 900 numbers.

``check`` is that scan of all 900 numbers, straight from the definitions.
"""

from __future__ import annotations

PARAMS = {"wa": 1, "wb": 2, "wc": 1, "scale": 2}
ANSWER = 45
VARIANTS = [
    {"scale": 1},
    {"scale": 3},
    {"wa": 1, "wb": 1, "wc": 1},
    {"wa": 2, "wb": 2, "wc": 2, "scale": 2},
    {"wa": 3, "wb": 1, "wc": 4, "scale": 2},
]


def solve(wa=1, wb=2, wc=1, scale=2):
    """Count of three-digit n with a²+b²+c² ≤ scale·(wa·a + wb·b + wc·c).

    Completing the square gives Σ(digit − scale·w/2)² ≤ scale²(wa²+wb²+wc²)/4,
    a ball condition, so the digits are counted independently per shell.
    """
    budget = scale ** 2 * (wa * wa + wb * wb + wc * wc)     # times 4
    count = 0
    for a in range(1, 10):
        da = (2 * a - scale * wa) ** 2
        if da > budget:
            continue
        for b in range(10):
            db = da + (2 * b - scale * wb) ** 2
            if db > budget:
                continue
            for c in range(10):
                if db + (2 * c - scale * wc) ** 2 <= budget:
                    count += 1
    return count


def check(wa=1, wb=2, wc=1, scale=2):
    """Independent: test every three-digit number against the raw definition."""
    count = 0
    for n in range(100, 1000):
        a, b, c = n // 100, (n // 10) % 10, n % 10
        if a * a + b * b + c * c <= scale * (wa * a + wb * b + wc * c):
            count += 1
    return count
