"""ข้อ 2 — จำนวนเซตย่อยของ {1, …, n} ที่ (ค่ามากสุด − ค่าน้อยสุด) = k

n − k choices of the smallest element m; the k − 1 numbers strictly between m
and m + k are free: (n − k)·2^(k−1). The sheet states general n, k; PARAMS fixes
n = 10, k = 4.

``check`` enumerates all subsets.
"""

from __future__ import annotations

PARAMS = {"n": 10, "k": 4}
ANSWER = 48
VARIANTS = [{"n": 5, "k": 1}, {"n": 12, "k": 7}, {"n": 8, "k": 7}, {"k": 2}]


def solve(n=10, k=4):
    return (n - k) * 2 ** (k - 1)


def check(n=10, k=4):
    count = 0
    for mask in range(1, 1 << n):
        members = [i + 1 for i in range(n) if mask >> i & 1]
        count += max(members) - min(members) == k
    return count
