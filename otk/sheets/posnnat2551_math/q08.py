"""ข้อ 8 — 2551·543ⁿ − 2008·7ⁿ ไม่เป็นกำลังสองสมบูรณ์  (พิสูจน์)

Modulo 3: 2551 ≡ 1, 543 ≡ 0, 2008 ≡ 1 and 7 ≡ 1, so for n ≥ 1 the value is
≡ 1·0 − 1·1 = −1 ≡ 2, a non-residue mod 3. The solver returns
the least prime p for which A·Bⁿ − C·Dⁿ is a non-residue for every n ≥ 1 (one
period checked against the set of squares): 3.

``check`` evaluates the actual integers for n ≤ 2(p − 1) and tests each with
Euler's criterion.
"""

from __future__ import annotations

PARAMS = {"a": 2551, "b": 543, "c": 2008, "d": 7}
ANSWER = 3
VARIANTS = [{"a": 2 + 5 * 37, "b": 1 + 5 * 11, "c": 105, "d": 15}, {"a": 3 + 7 * 37, "b": 4 + 7 * 11, "c": 107, "d": 21}, {"a": 2 + 11 * 37, "b": 1 + 11 * 11, "c": 111, "d": 33}]

PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def solve(a=2551, b=543, c=2008, d=7):
    for p in PRIMES:
        squares = {x * x % p for x in range(p)}
        if all((a * pow(b, n, p) - c * pow(d, n, p)) % p not in squares for n in range(1, p)):
            return p
    return None


def check(a=2551, b=543, c=2008, d=7):
    for p in PRIMES:
        values = [a * b**n - c * d**n for n in range(1, 2 * (p - 1) + 1)]
        if all(v % p and pow(v % p, (p - 1) // 2, p) == p - 1 for v in values):
            return p
    return None
