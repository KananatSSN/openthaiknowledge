"""ข้อ 11 — x บวกน้อยสุดที่ 2²⁵⁴⁸ | x²⁰⁰⁵ + 1

For odd e, x^e ≡ y^e (mod 2^K) with x, y odd forces x ≡ y, because
(x^e − y^e)/(x − y) is a sum of e odd terms. Since (−1)^e = −1, x ≡ −1 and the
least positive x is 2^K − 1 (written "2^K-1").

``check`` lifts a solution bit by bit (Hensel): starting from x = 1 (mod 2), at
each power 2^j it keeps x or x + 2^(j−1), whichever satisfies x^e ≡ −1 (mod 2^j),
then writes the result in the same form.
"""

from __future__ import annotations

PARAMS = {"k": 2548, "e": 2005}
ANSWER = "2^2548-1"
VARIANTS = [{"k": 3, "e": 1}, {"k": 12, "e": 5}, {"k": 600, "e": 2333}, {"k": 2, "e": 2005}]


def solve(k=2548, e=2005):
    return f"2^{k}-1"


def check(k=2548, e=2005):
    x = 1
    for j in range(2, k + 1):
        modulus = 1 << j
        if (pow(x, e, modulus) + 1) % modulus:
            x += 1 << (j - 1)
        assert (pow(x, e, modulus) + 1) % modulus == 0
    exponent = (x + 1).bit_length() - 1
    assert x + 1 == 1 << exponent
    return f"2^{exponent}-1"
