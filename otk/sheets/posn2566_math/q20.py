"""ข้อ 20 — ค่า m ที่น้อยที่สุดที่ทำให้ 2^(2^m) − 1 หารด้วย 2^1024 + 1 ลงตัว

จงหาจำนวนเต็ม m ที่น้อยที่สุดที่ 2^(2^m) − 1 หารด้วย 2^1024 + 1 ลงตัว

This is the Fermat-number factorisation:

    2^(2^m) − 1 = (2¹ − 1)(2¹ + 1)(2² + 1)(2⁴ + 1)…(2^(2^(m−1)) + 1)
               = ∏_{j=0}^{m−1} F_j

where F_j = 2^(2^j) + 1 is the j-th Fermat number.

2^1024 + 1 = 2^(2^10) + 1 = F_10.

So F_10 | 2^(2^m) − 1  iff  m ≥ 11.  **Answer: 11.**

``solve`` identifies the exponent and returns it + 1.
``check`` uses exact big-integer division.
"""

from __future__ import annotations

#: Find least m such that (2^(2^m) − 1) is divisible by (2^exp + 1).
PARAMS = {"exp": 1024}
ANSWER = 11
VARIANTS = [
    {"exp": 1},       # F₀ = 3, need m ≥ 1 → 1
    {"exp": 2},       # F₁ = 5, need m ≥ 2 → 2
    {"exp": 4},       # F₂ = 17, need m ≥ 3 → 3
    {"exp": 8},       # F₃ = 257, need m ≥ 4 → 4
    {"exp": 16},      # F₄ = 65537, need m ≥ 5 → 5
    {"exp": 512},     # F₉ = 2^512 + 1, need m ≥ 10 → 10
]


def _is_power_of_two(n: int) -> int | None:
    """Return k if n = 2^k, else None."""
    if n < 1:
        return None
    if n & (n - 1):
        return None
    return n.bit_length() - 1


def solve(exp=1024):
    """F_k = 2^(2^k) + 1 divides 2^(2^m) − 1 iff m > k, so m = k + 1."""
    k = _is_power_of_two(exp)
    if k is None:
        return None      # 2^exp + 1 is not a Fermat number
    return k + 1


def check(exp=1024):
    """Independent: verify divisibility by exact big-integer arithmetic.

    Check that 2^(2^m) ≡ 1 (mod 2^exp + 1) by repeated squaring mod the
    divisor, starting from m = 1 upward.
    """
    k = _is_power_of_two(exp)
    if k is None:
        return None

    modulus = (1 << exp) + 1      # 2^exp + 1
    # 2^(2^m) mod modulus: start with 2 and square m times.
    for m in range(1, 100):
        val = pow(2, 1 << m, modulus)     # 2^(2^m) mod modulus
        if (val - 1) % modulus == 0:
            return m
    return None
