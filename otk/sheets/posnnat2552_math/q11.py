"""วันที่สอง ข้อ 1 — ถ้า A₁ ≠ ∅ แล้ว A_k ≠ ∅ ทุก k  (พิสูจน์)

If p | a^m − b^m with p ∤ b, then a^m ≡ b^m and lifting gives
p^k | a^(m·p^(k−1)) − b^(m·p^(k−1)). The solver searches the least n with
p^k | aⁿ − bⁿ (a = 2, b = 3, p = 5, k = 3: 50).

``check`` computes the multiplicative order of a·b⁻¹ modulo p^k instead.
"""

from __future__ import annotations

PARAMS = {"a": 2, "b": 3, "p": 5, "k": 3}
ANSWER = 50
VARIANTS = [{"a": 4, "b": 7, "p": 3, "k": 4}, {"a": 10, "b": 3, "p": 7, "k": 2}, {"k": 1}]


def solve(a=2, b=3, p=5, k=3):
    modulus = p**k
    n = 1
    while (pow(a, n, modulus) - pow(b, n, modulus)) % modulus:
        n += 1
    return n


def check(a=2, b=3, p=5, k=3):
    modulus = p**k
    unit = a * pow(b, -1, modulus) % modulus
    n, x = 1, unit
    while x != 1:
        x = x * unit % modulus
        n += 1
    return n
