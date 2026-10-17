"""ข้อ 15 — n มากที่สุด ≤ 2004 ที่ 169 | 3^(3n+3) − 27

3^(3n+3) − 27 = 27(27ⁿ − 1) and q ∤ 27, so 27ⁿ ≡ 1 (mod q²): n must be a
multiple of the order of 27 modulo q². For q = 13, 27 ≡ 1 (mod 13) but not
mod 169, so the order is 13 and the answer is 2002.

``check`` tests every n ≤ bound directly.
"""

from __future__ import annotations

PARAMS = {"q": 13, "bound": 2004}
ANSWER = 2002
VARIANTS = [{"q": 7}, {"q": 11, "bound": 1234}, {"q": 5, "bound": 777}, {"q": 17}]


def solve(q=13, bound=2004):
    modulus, k, x = q * q, 1, 27 % (q * q)
    while x != 1:
        x = x * 27 % modulus
        k += 1
    return bound - bound % k


def check(q=13, bound=2004):
    modulus = q * q
    return max(n for n in range(1, bound + 1) if (pow(3, 3 * n + 3, modulus) - 27) % modulus == 0)
