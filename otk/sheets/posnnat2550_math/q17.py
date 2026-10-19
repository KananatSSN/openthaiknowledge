"""ข้อ 17 — ผลคูณของจำนวนเต็ม n ทั้งหมดที่ n² + 59n + 881 เป็นกำลังสองสมบูรณ์

4(n² + bn + c) = 4m² gives (2n + b − 2m)(2n + b + 2m) = b² − 4c = −43, a prime;
the factor pairs give 2n + 59 = ±21: n = −19, −40, product 760.

``check`` scans n over a wide window and multiplies the hits.
"""

from __future__ import annotations

from math import isqrt, prod

PARAMS = {"b": 59, "c": 881}
ANSWER = 760
VARIANTS = [{"b": 33, "c": 263}, {"b": 11, "c": 25}, {"b": 21, "c": 101}]


def solve(b=59, c=881):
    d = b * b - 4 * c
    found = set()
    for e in range(1, abs(d) + 1):
        if d % e == 0:
            for x in (e, -e):
                y = d // x
                if y >= x and (y - x) % 4 == 0 and (x + y) % 2 == 0 and ((x + y) // 2 - b) % 2 == 0:
                    found.add(((x + y) // 2 - b) // 2)
    return prod(sorted(found))


def check(b=59, c=881):
    hits = [n for n in range(-20000, 20001) if n * n + b * n + c >= 0 and isqrt(n * n + b * n + c) ** 2 == n * n + b * n + c]
    return prod(hits)
