"""ข้อ 6 — จำนวนวิธียกป้ายให้ทุกแถวและหลักมีป้ายน้ำเงินเป็นจำนวนคี่ (21 × 21)

Choose the top-left (r − 1) × (c − 1) block freely; each row and column fixes
its last cell, and the corner is consistent iff r ≡ c (mod 2). So there are
2^((r−1)(c−1)) ways when r and c have the same parity and none otherwise
(21 × 21: 2⁴⁰⁰).

``check`` solves the parity conditions as a linear system over GF(2): it
eliminates the r + c equations on rc unknowns, checks consistency, and returns
2^(rc − rank); for grids up to 3 × 4 it also counts every colouring.
"""

from __future__ import annotations

from itertools import product

PARAMS = {"rows": 21, "columns": 21}
ANSWER = 2582249878086908589655919172003011874329705792829223512830659356540647622016841194629645353280137831435903171972747493376
VARIANTS = [{"rows": 3, "columns": 3}, {"rows": 2, "columns": 4}, {"rows": 3, "columns": 4}, {"rows": 5, "columns": 7}]


def solve(rows=21, columns=21):
    if (rows - columns) % 2:
        return 0
    return 2 ** ((rows - 1) * (columns - 1))


def check(rows=21, columns=21):
    n = rows * columns
    eqs = []
    for r in range(rows):
        eqs.append((sum(1 << (r * columns + c) for c in range(columns)), 1))
    for c in range(columns):
        eqs.append((sum(1 << (r * columns + c) for r in range(rows)), 1))
    rank, pivots = 0, []
    for mask, rhs in eqs:
        for pmask, prhs, bit in pivots:
            if mask >> bit & 1:
                mask ^= pmask
                rhs ^= prhs
        if mask == 0:
            if rhs:
                return 0
            continue
        pivots.append((mask, rhs, mask.bit_length() - 1))
        rank += 1
    count = 2 ** (n - rank)
    if n <= 12:
        brute = sum(1 for cells in product((0, 1), repeat=n)
                    if all(sum(cells[r * columns:(r + 1) * columns]) % 2 for r in range(rows))
                    and all(sum(cells[r * columns + c] for r in range(rows)) % 2 for c in range(columns)))
        assert brute == count
    return count
