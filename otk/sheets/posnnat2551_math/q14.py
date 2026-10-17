"""วันที่สอง ข้อ 4 — C(2n+1, 1) − C(2n+1, 3)·2008 + ⋯ หารด้วย 19 ไม่ลงตัว  (พิสูจน์)

The sum is ((1 + s)^(2n+1) − (1 − s)^(2n+1))/(2s) with s² = −2008. Mod 19,
s ≡ 5 and the sum is (6^(2n+1) + 4^(2n+1))/10, which vanishes only if
11^(2n+1) ≡ −1 — impossible since 11 has order 3. The solver evaluates that
closed form modulo p (n = 10: 9).

``check`` adds the binomial terms as integers and reduces.
"""

from __future__ import annotations

from math import comb

PARAMS = {"n": 10, "c": 2008, "p": 19}
ANSWER = 9
VARIANTS = [{"n": 1}, {"n": 2551}, {"n": 7, "c": 2, "p": 11}]


def solve(n=10, c=2008, p=19):
    s = next(x for x in range(p) if (x * x + c) % p == 0)
    value = (pow(1 + s, 2 * n + 1, p) - pow(1 - s, 2 * n + 1, p)) * pow(2 * s, -1, p)
    return value % p


def check(n=10, c=2008, p=19):
    return sum((-1) ** k * comb(2 * n + 1, 2 * k + 1) * c**k for k in range(n + 1)) % p
