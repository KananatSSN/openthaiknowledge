"""ข้อ 1 — φ(2n) | n!  (พิสูจน์)

The (n − 1)! n-cycles on n points fall into groups of φ(n), one per generator of
the cyclic subgroup they generate, so φ(n) | (n − 1)!. For odd n φ(2n) = φ(n);
for even n φ(2n) = 2φ(n) and the factor n supplies the 2. The solver returns
n!/φ(2n) with φ from the Euler product (n = 10: 453600).

``check`` counts the residues prime to 2n directly, asserts the division is
exact, and for n ≤ 6 also counts the n-cycles and the cyclic subgroups they
generate.
"""

from __future__ import annotations

from itertools import permutations
from math import factorial, gcd

PARAMS = {"n": 10}
ANSWER = 453600
VARIANTS = [{"n": 1}, {"n": 6}, {"n": 7}, {"n": 12}]


def _phi(m):
    result, rest, p = m, m, 2
    while p * p <= rest:
        if rest % p == 0:
            result -= result // p
            while rest % p == 0:
                rest //= p
        p += 1
    if rest > 1:
        result -= result // rest
    return result


def solve(n=10):
    return factorial(n) // _phi(2 * n)


def _is_n_cycle(perm):
    seen, x = 0, 0
    for _ in range(len(perm)):
        x = perm[x]
        seen += 1
        if x == 0:
            break
    return seen == len(perm)


def check(n=10):
    phi_2n = sum(1 for k in range(1, 2 * n + 1) if gcd(k, 2 * n) == 1)
    assert factorial(n) % phi_2n == 0
    if n <= 6:
        cycles = [p for p in permutations(range(n)) if _is_n_cycle(p)]
        groups = set()
        for p in cycles:
            power, members = tuple(range(n)), []
            for _ in range(n):
                power = tuple(p[i] for i in power)
                members.append(power)
            groups.add(frozenset(members))
        phi_n = sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)
        assert len(cycles) == factorial(n - 1) == len(groups) * phi_n
    return factorial(n) // phi_2n
