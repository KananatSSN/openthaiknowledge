"""ข้อ 11 — จำนวนฟังก์ชัน f : {1, …, 2550} → {61, 80, 84} ที่ Σf(k) หารด้วย 3 ลงตัว

61, 80, 84 cover all residues mod 3, so the first n − 1 values are free and the
last is forced: 3^(n−1). The answer is written "3^2549"; in general the solver
gives the count as an integer string unless it is a power of 3.

``check`` runs the residue dynamic programme (counts of partial sums mod 3)
with big integers and writes the result the same way.
"""

from __future__ import annotations

from itertools import product

PARAMS = {"values": (61, 80, 84), "n": 2550, "target": 0}
ANSWER = "3^2549"
VARIANTS = [{"n": 5, "target": 1}, {"values": (12, 15, 19), "n": 7}, {"values": (13, 16, 20), "n": 6, "target": 2}, {"values": (66, 89, 94), "n": 40}]


def _form(value):
    k, power = 0, 1
    while power < value:
        power *= 3
        k += 1
    return f"3^{k}" if power == value else str(value)


def solve(values=(61, 80, 84), n=2550, target=0):
    residues = sorted(v % 3 for v in values)
    if residues == [0, 1, 2]:
        return _form(3 ** (n - 1))
    count = sum(1 for f in product(values, repeat=n) if sum(f) % 3 == target)  # small n only
    return _form(count)


def check(values=(61, 80, 84), n=2550, target=0):
    counts = [1, 0, 0]
    for _ in range(n):
        new = [0, 0, 0]
        for r, c in enumerate(counts):
            for v in values:
                new[(r + v) % 3] += c
        counts = new
    return _form(counts[target])
