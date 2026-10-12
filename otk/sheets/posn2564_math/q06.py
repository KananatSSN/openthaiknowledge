"""ข้อ 6 — ผลรวม B(1) + B(2) + ⋯ + B(99)

จงหาค่าของ B(1) + B(2) + ⋯ + B(99) เมื่อ สำหรับทุก ๆ จำนวนนับ n
B(n) = จำนวนของเลขโดดที่แตกต่างกันของ n ถ้า 9 เป็นเลขโดดของ n, และ B(n) = 0
ถ้า 9 ไม่เป็นเลขโดดของ n  (เช่น B(191) = 2 และ B(524) = 0)

Only the numbers that *contain* the digit contribute, and each contributes how
many **distinct** digits it has — so 99 counts 1, not 2. Splitting 1…99 by hand:

    9                    → 1
    19, 29, …, 89  (8×)  → 2 each = 16
    90, 91, …, 98  (9×)  → 2 each = 18
    99                   → 1

for a total of **36**. The trap is 99 and, in longer ranges, every repdigit.

``solve`` counts without listing anything: for each set S of digits containing
the required one, it counts the numbers of each length whose digit set is exactly
S by inclusion–exclusion, and weights by |S|. ``check`` simply walks the range
and applies the printed definition to each number.
"""

from __future__ import annotations

from itertools import combinations

#: sum B(n) for n = 1 … hi, where B counts distinct digits when `digit` occurs.
PARAMS = {"digit": 9, "hi": 99}
ANSWER = 36
#: only full 1…10^k − 1 ranges — `solve`'s counting has no closed form for a
#: ragged top, and it says so by returning None rather than guessing.
VARIANTS = [
    {"digit": 1, "hi": 99},
    {"digit": 0, "hi": 99},
    {"digit": 7, "hi": 999},
    {"digit": 9, "hi": 9},
    {"digit": 5, "hi": 999},
    {"digit": 2, "hi": 9999},
]


def _exactly(length, allowed):
    """Count `length`-digit numbers (no leading zero) using only `allowed`."""
    if not allowed:
        return 0
    lead = len([d for d in allowed if d != 0])
    if lead == 0:
        return 0
    return lead * len(allowed) ** (length - 1)


def solve(digit=9, hi=99):
    """Sum |S| over digit sets S ∋ digit, weighted by how many numbers have set S.

    The count of numbers whose digit set is *exactly* S comes from inclusion–
    exclusion over subsets of S, and only the lengths that fit entirely below hi
    are handled in closed form — anything ragged is refused.
    """
    if not 0 <= digit <= 9 or hi < 1:
        return None
    length = len(str(hi))
    if hi != 10 ** length - 1:
        return None              # closed form only for a full 1…10^k − 1 range
    total = 0
    digits = range(10)
    for size in range(1, 11):
        for subset in combinations(digits, size):
            if digit not in subset:
                continue
            for width in range(1, length + 1):
                exact = 0
                for drop in range(size):
                    sign = (-1) ** drop
                    for smaller in combinations(subset, size - drop):
                        exact += sign * _exactly(width, smaller)
                total += size * exact
    return total


def check(digit=9, hi=99):
    """Independent: apply the printed definition to every n in the range."""
    if not 0 <= digit <= 9 or hi < 1:
        return None
    if hi > 2_000_000:
        return None
    mark = str(digit)
    total = 0
    for n in range(1, hi + 1):
        text = str(n)
        if mark in text:
            total += len(set(text))
    return total
