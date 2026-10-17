"""ข้อ 10 — มีอย่างน้อย 3 สีที่มีจำนวนธงเท่ากัน  (พิสูจน์)

The vertices of an N-gon of one colour form a coset of a subgroup of ℤ_N (a
regular polygon, at least 3 vertices). In a partition of ℤ_N into such cosets,
the smallest coset size occurs at least p times, p the least prime dividing the
largest index (the coset sums of roots of unity must cancel). For N = pʲ (j ≥ 2)
the least possible multiplicity is p. The solver returns p.

``check`` enumerates every partition of ℤ_N into cosets of proper subgroups of
order at least 3 and returns the least number of classes of the smallest size.
"""

from __future__ import annotations

PARAMS = {"prime": 3, "power": 3}
ANSWER = 3
VARIANTS = [{"prime": 3, "power": 2}, {"prime": 5, "power": 2}, {"prime": 7, "power": 2}, {"prime": 5, "power": 3}]


def solve(prime=3, power=3):
    assert power >= 2
    return prime


def check(prime=3, power=3):
    n = prime**power
    orders = [d for d in range(3, n) if n % d == 0]  # proper subgroups, polygon sizes
    best = [None]

    def go(covered, sizes):
        if covered == (1 << n) - 1:
            smallest = min(sizes)
            count = sizes.count(smallest)
            if len(sizes) >= 2 and (best[0] is None or count < best[0]):
                best[0] = count
            return
        x = next(i for i in range(n) if not covered >> i & 1)
        for order in orders:
            step = n // order
            coset = sum(1 << ((x + step * j) % n) for j in range(order))
            if not covered & coset:
                go(covered | coset, sizes + [order])

    go(0, [])
    return best[0]
