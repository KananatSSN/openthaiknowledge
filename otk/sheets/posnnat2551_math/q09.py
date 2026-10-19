"""ข้อ 9 — จำนวนคู่อันดับ (A, B) ที่ A ⊆ B ⊆ {1, …, 10}

Each element is outside B, in B only, or in A: 3ⁿ = 59049.

``check`` runs over every B and adds 2^|B| (the choices of A inside it).
"""

from __future__ import annotations

PARAMS = {"n": 10}
ANSWER = 59049
VARIANTS = [{"n": 1}, {"n": 4}, {"n": 15}]


def solve(n=10):
    return 3**n


def check(n=10):
    return sum(2 ** bin(mask).count("1") for mask in range(1 << n))
