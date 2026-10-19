"""วันที่สอง ข้อ 2 — สามจำนวนเต็มต่างกันต้องมีคู่ที่ 10 | a³b − ab³  (พิสูจน์)

a³b − ab³ = ab(a − b)(a + b) is always even, and divisible by 5 when 5 | ab or
a² ≡ b² (mod 5); nonzero squares mod 5 are 1, 4, so among three numbers not
divisible by 5 two squares agree. The solver counts the good pairs of a given
set by those residue conditions (S = {1, 2, 3}: only {2, 3}, so 1).

``check`` evaluates a³b − ab³ modulo 10 for every pair.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"values": (1, 2, 3)}
ANSWER = 1
VARIANTS = [{"values": (-52, 12, 37, 42, 48)}, {"values": (1, 2, 4, 7)}, {"values": (3, 8, 13, 21, 34, 55)}]


def solve(values=(1, 2, 3)):
    return sum(1 for a, b in combinations(values, 2) if a * b % 5 == 0 or (a * a - b * b) % 5 == 0)


def check(values=(1, 2, 3)):
    return sum(1 for a, b in combinations(values, 2) if (a**3 * b - a * b**3) % 10 == 0)
