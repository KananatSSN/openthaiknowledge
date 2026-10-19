"""ข้อ 9 — ห.ร.ม. ของ (135⁹⁰ − 45⁹⁰)/90² กับ 90²  (135 = 3m, 45 = m, 90 = 2m, m = 45)

``solve`` takes the gcd of the two big integers.

``check`` works prime by prime instead: for each p dividing (2m)² it compares
v_p((3m)^e − m^e) − v_p((2m)²) with v_p((2m)²), where
v_p((3m)^e − m^e) = e·v_p(m) + v_p(3^e − 1) and v_p(3^e − 1) is found by
modular powers. The source's answer 2·3⁴·5² = 4050.
"""

from __future__ import annotations

from math import gcd

PARAMS = {"m": 45, "e": 90}
ANSWER = 4050
VARIANTS = [{"m": 11, "e": 76}, {"m": 7, "e": 10}, {"m": 30, "e": 44}, {"m": 3, "e": 4}]


def solve(m=45, e=90):
    square = (2 * m) ** 2
    return gcd(((3 * m) ** e - m**e) // square, square)


def _factor(n):
    out, f = {}, 2
    while f * f <= n:
        while n % f == 0:
            out[f] = out.get(f, 0) + 1
            n //= f
        f += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def check(m=45, e=90):
    square = _factor((2 * m) ** 2)
    result = 1
    for p, k in square.items():
        vm = _factor(m).get(p, 0)
        v3 = 0
        if p != 3:
            while pow(3, e, p ** (v3 + 1)) == 1:
                v3 += 1
        quotient = e * vm + v3 - k
        result *= p ** min(quotient, k)
    return result
