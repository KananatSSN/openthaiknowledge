"""ข้อ 10 — (26!)²⁶ + (27!)²⁷ มอดุโล 29

Wilson: 28! ≡ −1 and 28 ≡ −1 give 27! ≡ 1 and 26! ≡ 1/27 ≡ −1/2. In general
((p − 3)!)^e₁ + ((p − 2)!)^e₂ ≡ (−1/2)^e₁ + 1: here (−1/2)²⁶ = 4, total 5.

``check`` computes the factorials and powers directly.
"""

from __future__ import annotations

from math import factorial

PARAMS = {"p": 29, "e1": 26, "e2": 27}
ANSWER = 5
VARIANTS = [{"p": 23, "e1": 10, "e2": 34}, {"p": 11, "e1": 3, "e2": 5}, {"p": 97, "e1": 200, "e2": 7}, {"e1": 7}]


def solve(p=29, e1=26, e2=27):
    half = pow(2, -1, p)
    return (pow(-half % p, e1, p) + 1) % p


def check(p=29, e1=26, e2=27):
    return (pow(factorial(p - 3), e1, p) + pow(factorial(p - 2), e2, p)) % p
