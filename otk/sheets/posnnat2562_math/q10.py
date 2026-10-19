"""ข้อ 10 — มี n คี่อนันต์จำนวนที่ n! + 1 ไม่เป็นจำนวนเฉพาะ  (พิสูจน์)

The proof reads n! modulo a prime p from Wilson's theorem: (p − 1)! =
n!·(n + 1)⋯(p − 1) ≡ n!·(−1)ᵏ·k! ≡ −1 with k = p − 1 − n, so
n! ≡ (−1)^(k+1)/k! (mod p). The solver returns n! mod p (p = 101, n = 97: k = 3).

``check`` multiplies n! out modulo p.
"""

from __future__ import annotations

from math import factorial

PARAMS = {"p": 101, "n": 97}
ANSWER = 17
VARIANTS = [{"p": 53, "n": 50}, {"p": 211, "n": 200}, {"p": 499, "n": 490}, {"p": 7, "n": 6}]


def solve(p=101, n=97):
    k = p - 1 - n
    return (-1) ** (k + 1) * pow(factorial(k), -1, p) % p


def check(p=101, n=97):
    value = 1
    for i in range(2, n + 1):
        value = value * i % p
    return value
