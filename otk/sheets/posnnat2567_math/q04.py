"""ข้อ 4 — จำนวนช่องสีม่วงน้อยที่สุด (88 × 253, x(c)y(c) ≥ 184)

For R = b·r rows, C = b·k columns and T = r·k with b ≥ r + 1: a row with few
purple cells forces its yellow cells' columns to be purple-heavy, which bounds
the total below by b·r·k; b disjoint r × k purple blocks attain it. The source
(b, r, k = 11, 8, 23) gives 2024. PARAMS uses a 2 × 6 grid so that ``check``
can try every colouring.

``check`` tries every set of purple cells by size and returns the least size
for which every yellow cell has x(c)·y(c) ≥ T.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"blocks": 2, "rows_per_block": 1, "columns_per_block": 3}
ANSWER = 6
VARIANTS = [{"blocks": 2, "rows_per_block": 1, "columns_per_block": 2},
            {"blocks": 2, "rows_per_block": 1, "columns_per_block": 4},
            {"blocks": 3, "rows_per_block": 1, "columns_per_block": 2}]


def solve(blocks=2, rows_per_block=1, columns_per_block=3):
    assert blocks >= rows_per_block + 1
    return blocks * rows_per_block * columns_per_block


def check(blocks=2, rows_per_block=1, columns_per_block=3):
    rows, cols = blocks * rows_per_block, blocks * columns_per_block
    threshold = rows_per_block * columns_per_block
    cells = [(r, c) for r in range(rows) for c in range(cols)]
    for size in range(len(cells) + 1):
        for purple in combinations(cells, size):
            chosen = set(purple)
            row_count = [sum((r, c) in chosen for c in range(cols)) for r in range(rows)]
            col_count = [sum((r, c) in chosen for r in range(rows)) for c in range(cols)]
            if all(row_count[r] * col_count[c] >= threshold for r, c in cells if (r, c) not in chosen):
                return size
    raise AssertionError
