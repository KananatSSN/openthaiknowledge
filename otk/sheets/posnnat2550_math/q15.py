"""ข้อ 15 — (222!)¹¹¹ + 111^(222!) + (111!)²²² + 222^(111!) มอดุโล 2007 = 9·223

With h = (p − 1)/2: mod p the terms are (−1)^h (Wilson), then 1, 1, 1 (each
exponent is a multiple of p − 1, or even); mod 9 the first and third vanish,
and the second and fourth vanish when 3 | h, 3 | p − 1. CRT gives 225.

``check`` takes every term modulo 9p with Python's modular powers.
"""

from __future__ import annotations

from math import factorial

PARAMS = {"p": 223}
ANSWER = 225
VARIANTS = [{"p": 113}, {"p": 101}, {"p": 251}, {"p": 199}]


def solve(p=223):
    h = (p - 1) // 2
    mod_p = [(-1) ** h % p, 1, 1, 1]
    mod_9 = [0, 0 if h % 3 == 0 else 1, 0, 0 if (p - 1) % 3 == 0 else 1]
    total = 0
    for r, s in zip(mod_p, mod_9):
        total += next(x for x in range(s, 9 * p, 9) if x % p == r)
    return total % (9 * p)


def check(p=223):
    h, modulus = (p - 1) // 2, 9 * p
    big, half = factorial(p - 1), factorial(h)
    return (pow(big, h, modulus) + pow(h, big, modulus) + pow(half, p - 1, modulus) + pow(p - 1, half, modulus)) % modulus
