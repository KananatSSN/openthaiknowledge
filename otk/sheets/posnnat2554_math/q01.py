"""ข้อ 1 — p | n!, q | (n − 1)! − 1 ⇒ p < q  (พิสูจน์)

q | (n − 1)! − 1 rules out q ≤ n − 1, and q = n would need (n − 1)! ≡ 1 (mod n),
against Wilson's −1 for n ≥ 3; so every such q exceeds n ≥ p. The solver returns
the least prime factor of (n − 1)! − 1 (n = 10: 11).

``check`` runs over primes q > 1 computing (n − 1)! modulo q step by step, and
returns the first q with (n − 1)! ≡ 1.
"""

from __future__ import annotations

from math import factorial

PARAMS = {"n": 10}
ANSWER = 11
VARIANTS = [{"n": 6}, {"n": 9}, {"n": 12}, {"n": 16}]


def solve(n=10):
    value, d = factorial(n - 1) - 1, 2
    while d * d <= value:
        if value % d == 0:
            return d
        d += 1
    return value


def check(n=10):
    q = 2
    while True:
        if all(q % f for f in range(2, int(q**0.5) + 1)):
            r = 1
            for k in range(2, n):
                r = r * k % q
            if r == 1 % q:
                return q
        q += 1
