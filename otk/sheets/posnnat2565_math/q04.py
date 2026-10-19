"""ข้อ 4 — n ที่มีพหุนามโมนิกดีกรี n ซึ่ง P(a)P(b) ≠ P(c) ทุกจำนวนเต็ม a, b, c

Degree 1: x + t takes every integer. Degree 2: x² + ux + v has
P(0)P(1 − u) = P(−v). For n ≥ 3 the monic x^(n−3)(x³ − x) + 2 is 2 modulo 3 at
every integer, and a product of two such values is 1 modulo 3. So exactly the
degrees n ≥ 3 work. The answer is the tuple of working degrees up to `limit`.

``check`` searches every x + t and x² + ux + v with |t|, |u|, |v| ≤ 4 for a, b, c
in a small range with P(a)P(b) = P(c), and for n ≥ 3 tests the witness at every
residue modulo 3 and at integers in a range.
"""

from __future__ import annotations

from itertools import product

PARAMS = {"limit": 6}
ANSWER = (3, 4, 5, 6)
VARIANTS = [{"limit": 3}, {"limit": 4}, {"limit": 9}]


def solve(limit=6):
    return tuple(range(3, limit + 1))


def _has_product(values):
    image = set(values.values())
    return any(values[a] * values[b] in image for a in values for b in values)


def check(limit=6):
    rng = range(-12, 13)
    for t in range(-4, 5):
        assert _has_product({x: x + t for x in rng})
    for u, v in product(range(-4, 5), repeat=2):
        vals = {x: x * x + u * x + v for x in range(-40, 41)}
        assert any(vals[a] * vals[b] in set(vals.values()) for a in rng for b in rng)
    works = []
    for n in range(1, limit + 1):
        if n < 3:
            continue

        def witness(x, n=n):
            return x ** (n - 3) * (x**3 - x) + 2

        assert all(witness(r) % 3 == 2 for r in range(3))
        vals = {witness(x) for x in range(-30, 31)}
        assert not any(p * q in vals for p in vals for q in vals)
        works.append(n)
    return tuple(works)
