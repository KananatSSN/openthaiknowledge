"""ข้อ 13 — เลข 1 จำนวน 1862 ตัว มอดุโล 2006

R_k = (10^k − 1)/9; taking 10^k mod 9M keeps the division exact: 781.

``check`` builds the repunit as an integer.
"""

from __future__ import annotations

PARAMS = {"k": 1862, "modulus": 2006}
ANSWER = 781
VARIANTS = [{"k": 650, "modulus": 2831}, {"k": 6}, {"k": 3000, "modulus": 999}, {"modulus": 7}]


def solve(k=1862, modulus=2006):
    return (pow(10, k, 9 * modulus) - 1) // 9 % modulus


def check(k=1862, modulus=2006):
    return int("1" * k) % modulus
