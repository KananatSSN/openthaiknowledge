"""ข้อ 14 — n นับน้อยสุดที่ 2549 | n²⁵⁴⁵ − 2541

By Fermat n²⁵⁴⁵ ≡ n⁻³ and 2541 ≡ −8 = −2³, so (−2n)³ ≡ 1; cubing is a
bijection because 3 ∤ 2548, hence −2n ≡ 1 and n ≡ −1/2 = 1274.

``check`` tries every n below p.
"""

from __future__ import annotations

PARAMS = {"p": 2549, "j": 2}
ANSWER = 1274
VARIANTS = [{"p": 599, "j": 7}, {"p": 503, "j": 3}, {"p": 1019, "j": 5}, {"j": 4}]


def solve(p=2549, j=2):
    return -pow(j, -1, p) % p


def check(p=2549, j=2):
    return next(n for n in range(1, p) if pow(n, p - 4, p) == (p - j**3) % p)
