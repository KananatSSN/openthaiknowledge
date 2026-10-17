"""ข้อ 7 — (p, q) ที่ aₚ | a_q เมื่อ a₁ = 1, aₙ₊₁ = aₙᵈ + 1

The earlier terms are positive and below aₚ, so modulo aₚ the sequence goes
a₁, …, aₚ₋₁, 0, then 1 = a₁ again: it is periodic with least period p, and
aₚ | a_q iff p | q. The answer is the tuple of q ≤ limit with aₚ | a_q.

``check`` runs the recurrence modulo aₚ directly up to the limit.
"""

from __future__ import annotations

PARAMS = {"d": 2, "p": 3, "limit": 20}
ANSWER = (3, 6, 9, 12, 15, 18)
VARIANTS = [{"d": 3, "p": 2, "limit": 30}, {"d": 2, "p": 4, "limit": 40}, {"d": 5, "p": 3, "limit": 25}]


def solve(d=2, p=3, limit=20):
    return tuple(range(p, limit + 1, p))


def check(d=2, p=3, limit=20):
    a = 1
    for _ in range(p - 1):
        a = a**d + 1
    modulus = a
    hits, value = [], 1
    for q in range(1, limit + 1):
        if value % modulus == 0:
            hits.append(q)
        value = (value**d + 1) % modulus
    return tuple(hits)
