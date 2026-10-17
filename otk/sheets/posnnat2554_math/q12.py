"""ข้อ 12 — จำนวนวิธีติดป้าย "หลินปิง" บนเก้าอี้ 3m = 7662 ตัว (m = 2554)

A labelling works when some rotation k gives f(a + k) ≡ f(a) − 1 for all a. That
is the condition f(a + d) ≡ f(a) + s with d = gcd(k, 3m) | m and s ∈ {1, 2}.
When 3 ∤ m every such set lies in one of the two disjoint sets for d = m, each of
size 3^m, so the count is 2·3^m, written "2·3^2554". (The official key's
3² + 3¹²⁷⁷ + 3²⁵⁵⁴ counts one direction per period only.)

``check`` counts the union over all rotations k directly: each k gives the
cyclic group ⟨(k, −1)⟩ in Z_{3m} × Z₃, which it reduces to a generator (g, s)
with g = gcd(k, 3m); it runs inclusion–exclusion over those generators, where
an intersection is the labellings invariant under the generated group (none if
the group contains a pure label shift, else 3^G with G the gcd of the shifts).
The integer total is written as c·3^t.
"""

from __future__ import annotations

from itertools import combinations
from math import gcd

PARAMS = {"m": 2554}
ANSWER = '2·3^2554'
VARIANTS = [{"m": 1}, {"m": 2}, {"m": 5}, {"m": 10}]


def solve(m=2554):
    assert m % 3
    return f"2·3^{m}"


def _ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = _ext_gcd(b, a % b)
    return g, y, x - (a // b) * y


def _invariant_count(pairs, n):
    """Labellings f with f(a + gᵢ) = f(a) + sᵢ for every pair: the shifts generate
    G = gcd(gᵢ, n); the labels must come from one homomorphism G·t ↦ σ·t."""
    big, coeffs = n, [0] * len(pairs)
    for i, (g, _) in enumerate(pairs):
        new, x, y = _ext_gcd(big, g)
        coeffs = [c * x for c in coeffs]
        coeffs[i] = y
        big = new
    sigma = sum(c * s for c, (_, s) in zip(coeffs, pairs)) % 3
    if (n // big) * sigma % 3:
        return 0
    if any((g // big) * sigma % 3 != s % 3 for g, s in pairs):
        return 0
    return 3**big


def check(m=2554):
    n = 3 * m
    pairs = set()
    for k in range(1, n):
        g = gcd(k, n)
        if (n // g) % 3:
            continue  # ⟨(k, −1)⟩ then contains a pure label shift: no labelling
        u = pow(k // g, -1, n // g)  # k·u ≡ g (mod n)
        pairs.add((g, (-u) % 3))
    pairs = sorted(pairs)
    total = 0
    for size in range(1, len(pairs) + 1):
        for subset in combinations(pairs, size):
            total += (-1) ** (size + 1) * _invariant_count(subset, n)
    t = 0
    while total % 3 == 0:
        total //= 3
        t += 1
    return f"{total}·3^{t}"
