"""ข้อ 9 — มี aₖ ที่ aₖ² + aₖ + 2023 มีตัวประกอบอย่างน้อย k ตัว  (พิสูจน์)

2023 = 7·17², so a ≡ 0 (mod 7) is a root of a² + a + 2023 mod 7, and it is simple
(the derivative 2a + 1 ≡ 1). Hensel lifts it to a unique root modulo 7ᵏ with
a ≡ 0 (mod 7); then 7ᵏ divides aₖ² + aₖ + 2023, which has at least k + 1
divisors. The solver lifts the root digit by digit (C = 2023, k = 3).

``check`` tries every a < 7ᵏ with a ≡ 0 (mod 7), asserts exactly one works, and
returns it.
"""

from __future__ import annotations

PARAMS = {"constant": 2023, "exponent": 3}
ANSWER = 182
VARIANTS = [{"constant": 2023, "exponent": 2}, {"constant": 70, "exponent": 4}, {"constant": 21, "exponent": 5}]


def solve(constant=2023, exponent=3):
    root, modulus = 0, 7
    for _ in range(1, exponent):
        value = root * root + root + constant
        digit = -(value // modulus) * pow(2 * root + 1, -1, 7) % 7
        root += digit * modulus
        modulus *= 7
    return root


def check(constant=2023, exponent=3):
    m = 7**exponent
    hits = [a for a in range(0, m, 7) if (a * a + a + constant) % m == 0]
    assert len(hits) == 1
    return hits[0]
