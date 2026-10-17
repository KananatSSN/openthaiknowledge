"""ข้อ 3 — 2 55…5 3 (เลข 5 จำนวน n ตัว) หารด้วย 2553 ลงตัวสำหรับ n มากมายอนันต์  (พิสูจน์)

With n copies of b the number is a·10^(n+1) + b·10·R_n + c (R_n the repunit);
once one n works, adding a period of 10 modulo the relevant factor repeats the
hit. The solver returns the least n > 2 that works.

``check`` builds the decimal string and divides.
"""

from __future__ import annotations

PARAMS = {"a": 2, "b": 5, "c": 3}
ANSWER = 5
VARIANTS = [{"a": 1, "b": 3, "c": 7}, {"a": 4, "b": 1, "c": 9}, {"a": 7, "b": 0, "c": 1}]


def solve(a=2, b=5, c=3):
    modulus = int(f"{a}{b}{b}{c}")
    for n in range(3, 20000):
        rep = (pow(10, n, 9 * modulus) - 1) // 9 % modulus
        if (a * pow(10, n + 1, modulus) + b * 10 * rep + c) % modulus == 0:
            return n
    return None


def check(a=2, b=5, c=3):
    modulus = int(f"{a}{b}{b}{c}")
    for n in range(3, 20000):
        if int(f"{a}{str(b) * n}{c}") % modulus == 0:
            return n
    return None
