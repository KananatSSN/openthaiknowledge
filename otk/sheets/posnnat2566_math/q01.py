"""ข้อ 1 — ผลคูณของจำนวนเต็มเรียงกัน 20 จำนวนไม่เป็นกำลังสองสมบูรณ์  (พิสูจน์)

Twenty consecutive integers prime to 23 cover p − 3 = 20 consecutive non-zero
residues, so by Wilson's theorem their product is −1 divided by the two missing
residues. Starting at residue 1 the missing ones are 21, 22, so the product is
≡ −1/2 ≡ 11 (mod 23), a non-residue: not a square. The solver returns the
residue of the product of p − 3 consecutive integers from residue `first`.

``check`` multiplies the integers out modulo p and, for the source, confirms the
result is a quadratic non-residue mod 23.
"""

from __future__ import annotations

PARAMS = {"prime": 23, "first": 1}
ANSWER = 11
VARIANTS = [{"prime": 7, "first": 3}, {"prime": 31, "first": 2}, {"prime": 47, "first": 1}]


def solve(prime=23, first=1):
    skipped = [r % prime for r in range(first + prime - 3, first + prime)]  # the three left out
    missing = [r for r in skipped if r]  # 0 is one of them
    inverse = pow(missing[0] * missing[1], -1, prime)
    return -inverse % prime


def check(prime=23, first=1):
    a = 3 * prime + first
    value = 1
    for x in range(a, a + prime - 3):
        value = value * x % prime
    if prime == 23 and first == 1:
        assert pow(value, (prime - 1) // 2, prime) == prime - 1
    return value
