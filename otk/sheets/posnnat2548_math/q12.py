"""ข้อ 12 — จำนวน n คู่ 0 ≤ n ≤ 100 ที่ 5 | n²·2^(2n²) + 1

n even: 4 | n², so 2^(2n²) = 16^(n²/2) ≡ 1 (mod 5) and n² ≡ −1, i.e.
n ≡ 2, 3 (mod 5); with n even that is n ≡ 2, 8 (mod 10). (For odd n the same
reasoning gives n ≡ 1, 9 (mod 10).) Count in [0, N]: 20.

``check`` evaluates n²·2^(2n²) + 1 modulo 5 for each n.
"""

from __future__ import annotations

PARAMS = {"last": 100, "parity": 0}
ANSWER = 20
VARIANTS = [{"last": 257}, {"parity": 1}, {"last": 333, "parity": 1}, {"last": 9}]


def solve(last=100, parity=0):
    residues = (2, 8) if parity == 0 else (1, 9)
    return sum(1 for n in range(last + 1) if n % 10 in residues)


def check(last=100, parity=0):
    return sum(1 for n in range(parity, last + 1, 2) if (n * n * pow(2, 2 * n * n, 5) + 1) % 5 == 0)
