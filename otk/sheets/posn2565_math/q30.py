"""ข้อ 30 — จำนวนสิบสิ่งอันดับที่สอดคล้องเงื่อนไข

จงหาจำนวนสิบสิ่งอันดับ (x₁, x₂, …, x₁₀) ทั้งหมด ซึ่งสอดคล้องเงื่อนไขต่อไปนี้
    (1) {x₁, x₂, …, x₁₀} = {1, 2, …, 10}
    (2) x₁ − x₂ + x₃ − x₄ + x₅ − x₆ + x₇ − x₈ + x₉ − x₁₀ = 25

Condition (1) makes the tuple a permutation of 1…10, so the five odd positions
hold one 5-subset and the five even positions hold its complement. Writing A for
the odd-position sum and B for the even one,

    A + B = 55,   A − B = 25  ⟹  A = 40,  B = 15.

A 5-subset of {1,…,10} summing to 15 has no room to manoeuvre: the smallest such
sum is 1+2+3+4+5 = 15, so ``{1,2,3,4,5}`` is the *only* one. The small numbers
therefore occupy the even positions and 6…10 the odd ones, in any order:

    5! · 5! = 120 · 120 = **14400**

The target is at the very edge of what is achievable — one step further (27)
gives nothing at all, which is what makes the count so clean.

``solve`` counts the admissible subsets with a size-and-sum table and multiplies
by the two factorials. ``check`` enumerates: for a small rack it walks every
permutation and evaluates the alternating sum as printed, and for the full ten it
walks the C(10,5) position sets explicitly. Both routes must agree.
"""

from __future__ import annotations

from itertools import combinations, permutations
from math import factorial

#: a permutation of 1..n (n even) with the alternating sum equal to ``target``.
PARAMS = {"n": 10, "target": 25}
ANSWER = 14400
VARIANTS = [
    {"n": 10, "target": 5},
    {"n": 10, "target": 27},        # one step past the edge: no tuple at all
    {"n": 6, "target": 9},
    {"n": 8, "target": 4},          # a middling target: many subsets qualify
    {"n": 4, "target": 4},
    {"n": 10, "target": -25},       # the mirror image: same count
]


def halves(n=10, target=25):
    """(sum owed to the odd positions, half the length), or None if impossible."""
    if n <= 0 or n % 2:
        return None
    total = n * (n + 1) // 2
    if (total + target) % 2:
        return None
    return (total + target) // 2, n // 2


def solve(n=10, target=25):
    """Count of tuples: (# subsets of the right size and sum) × (n/2)!²."""
    got = halves(n, target)
    if got is None:
        return None
    want, half = got
    if want < 0 or want > n * (n + 1) // 2:
        return None
    # table[size][sum] — how many subsets of {1..n} of that size and sum
    table = [[0] * (want + 1) for _ in range(half + 1)]
    table[0][0] = 1
    for value in range(1, n + 1):
        for size in range(min(half, value), 0, -1):
            for total in range(want, value - 1, -1):
                table[size][total] += table[size - 1][total - value]
    return table[half][want] * factorial(half) ** 2


def check(n=10, target=25):
    """Independent: enumerate the arrangements themselves.

    For n ≤ 8 every permutation is generated and the alternating sum is evaluated
    exactly as the question prints it — no subsets, no factorials. For n = 10
    that is 3.6 million tuples, so the odd-position set is enumerated instead and
    the two orderings counted, with one full tuple per surviving set built and
    verified against the printed condition.
    """
    if n <= 0 or n % 2:
        return None
    values = list(range(1, n + 1))

    def alternating(seq) -> int:
        return sum(v if i % 2 == 0 else -v for i, v in enumerate(seq))

    if n <= 8:
        return sum(1 for p in permutations(values) if alternating(p) == target)

    half = n // 2
    count = 0
    for odd_slots in combinations(values, half):
        even_slots = [v for v in values if v not in odd_slots]
        witness = []
        for a, b in zip(odd_slots, even_slots):
            witness += [a, b]
        if alternating(witness) != target:
            continue
        count += factorial(half) ** 2
    return count
