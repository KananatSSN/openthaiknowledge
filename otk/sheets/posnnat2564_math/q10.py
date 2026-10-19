"""ข้อ 10 — มีราก z₁ ≠ z₂ ที่ |z₁ − z₂| < 1  (พิสูจน์)

aₙ = a_(d−n) makes the roots closed under z ↦ 1/z (a₀ = a_d ≠ 0), so at least
⌈d/2⌉ lie in the closed unit disk. Cut it into six 60° sectors; two roots in
one sector are less than 1 apart (barring the boundary cases the proof treats).
Spreading the roots as evenly as possible, the sectors still hold at least
6·C(q, 2) + ρ·q pairs, where ⌈d/2⌉ = 6q + ρ. The solver returns that count
(d = 13: 1).

``check`` distributes ⌈d/2⌉ roots over six sectors in every possible way and
returns the least number of same-sector pairs.
"""

from __future__ import annotations

from itertools import combinations_with_replacement

PARAMS = {"degree": 13}
ANSWER = 1
VARIANTS = [{"degree": 14}, {"degree": 25}, {"degree": 35}]


def solve(degree=13):
    inside = (degree + 1) // 2
    q, rho = divmod(inside, 6)
    return 6 * q * (q - 1) // 2 + rho * q


def check(degree=13):
    inside = (degree + 1) // 2
    best = None
    for placement in combinations_with_replacement(range(6), inside):
        counts = [placement.count(s) for s in range(6)]
        pairs = sum(c * (c - 1) // 2 for c in counts)
        best = pairs if best is None else min(best, pairs)
    return best
