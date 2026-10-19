"""ข้อ 16 — เลขสามหลักสุดท้ายของ 2^(2²⁰⁰⁴)

1000 = 8·125. Mod 8 an even base to a huge power is 0 (an odd base cycles with
period 2). Mod 125 the exponent reduces mod φ(125) = 100: 2²⁰⁰⁴ ≡ 16, so the
power is 2¹⁶ ≡ 36 (mod 125). The Chinese remainder theorem gives 536.

``check`` runs Python's modular power with the full exponent b^k.
"""

from __future__ import annotations

PARAMS = {"base": 2, "k": 2004}
ANSWER = 536
VARIANTS = [{"k": 10}, {"base": 3, "k": 57}, {"base": 7, "k": 2004}, {"base": 3, "k": 1000}]


def solve(base=2, k=2004):
    mod_125 = pow(base, pow(base, k, 100) + 100, 125)
    mod_8 = 0 if base % 2 == 0 else pow(base, pow(base, k, 2) + 2, 8)
    return next(v for v in range(mod_125, 1000, 125) if v % 8 == mod_8)


def check(base=2, k=2004):
    return pow(base, base**k, 1000)
