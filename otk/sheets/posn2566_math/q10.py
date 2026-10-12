"""ข้อ 10 — จำนวนคู่อันดับ (a, b) ที่ทำให้รากเป็นจำนวนเต็มบวกที่ต่างกัน

ให้ S เป็นเซตของคู่อันดับ (a, b) โดยที่ a, b ∈ {0, 1, 2, …, 9} และ a > b
จงหาจำนวนคู่อันดับ (a, b) ทั้งหมดในเซต S ที่ทำให้สมการ x² − ax + b = 0
มีคำตอบทั้งหมดเป็นจำนวนเต็มบวกที่แตกต่างกัน

The roots p and q are positive integers with p + q = a and pq = b, so the printed
condition ``a > b`` says

    p + q > pq   ⟺   (p − 1)(q − 1) < 1   ⟺   p = 1 or q = 1

**One root has to be 1.** That single line is the whole question: `a > b` is not
a range restriction, it is the constraint that collapses the search.

With p = 1 and q = k (k ≠ 1 for distinctness), a = k + 1 and b = k, so both stay
inside 0…9 exactly when 2 ≤ k ≤ 8 — seven pairs:

    (3,2), (4,3), (5,4), (6,5), (7,6), (8,7), (9,8)      **7**

``solve`` counts that range directly. ``check`` tests all 100 pairs by
factorising each quadratic and inspecting the roots it actually has.
"""

from __future__ import annotations

from math import isqrt

#: digits available to a and b: {0, 1, …, digits − 1}.
PARAMS = {"digits": 10}
ANSWER = 7
VARIANTS = [
    {"digits": 5},
    {"digits": 4},
    {"digits": 3},
    {"digits": 12},
    {"digits": 20},
    {"digits": 1},
]


def solve(digits=10):
    """One root is 1, so the pairs are (k+1, k) for 2 ≤ k ≤ digits − 2."""
    if digits < 1:
        return None
    # need k ≤ digits − 1 (for b) and k + 1 ≤ digits − 1 (for a), and k ≥ 2
    top = digits - 2
    return max(0, top - 2 + 1)


def check(digits=10):
    """Independent: factorise every quadratic and look at its roots."""
    if digits < 1:
        return None
    if digits > 4000:
        return None
    count = 0
    for a in range(digits):
        for b in range(digits):
            if a <= b:
                continue
            disc = a * a - 4 * b
            if disc <= 0:
                continue                       # equal or non-real roots
            root = isqrt(disc)
            if root * root != disc or (a - root) % 2:
                continue
            p, q = (a - root) // 2, (a + root) // 2
            if p > 0 and q > 0 and p != q:
                count += 1
    return count
