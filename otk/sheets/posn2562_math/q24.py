"""ข้อ 24 — จำนวนวิธีเลือกช่อง 3 ช่องที่ต่างแถวและต่างหลักกัน

พิจารณาตารางขนาด 4×5 ซึ่งมีทั้งหมด 20 ช่อง จงหาจำนวนวิธีในการเลือกช่อง 3 ช่อง
จากตาราง โดยที่แต่ละช่องที่เลือกมาอยู่ต่างแถวและต่างหลักกันทั้งหมด

Pick which rows are used, pick which columns are used, then match them up —
that last step is where the factorial comes from and where the count is usually
lost:

    C(4, 3) · C(5, 3) · 3! = 4 · 10 · 6 = **240**

Choosing 3 rows out of 4 and 3 columns out of 5 fixes a 3×3 sub-grid; inside it
the three cells must form a permutation matrix, and there are 3! of those.
Writing ``C(4,3)·C(5,3)`` alone gives 40 and forgets the matching; writing
``4·5·3·4·2·3/6`` is the same 240 counted by placement.

In general the answer is ``C(r, k)·C(c, k)·k!`` — zero once k exceeds either
dimension.

``solve`` uses that product. ``check`` enumerates the cells: it walks every
k-subset of the r·c cells and keeps the ones whose rows are all different and
whose columns are all different, which is the condition exactly as printed.
"""

from __future__ import annotations

from itertools import combinations
from math import comb, factorial

#: a rows × cols grid, choosing this many cells.
PARAMS = {"rows": 4, "cols": 5, "pick": 3}
ANSWER = 240
VARIANTS = [
    {"rows": 3, "cols": 3, "pick": 2},
    {"rows": 4, "cols": 4, "pick": 4},
    {"rows": 2, "cols": 6, "pick": 2},
    {"rows": 5, "cols": 5, "pick": 3},
    {"rows": 3, "cols": 4, "pick": 4},     # more cells than rows: impossible
    {"rows": 4, "cols": 5, "pick": 1},
]


def solve(rows=4, cols=5, pick=3):
    """C(rows, pick) · C(cols, pick) · pick! — choose, choose, then match."""
    if rows < 1 or cols < 1 or pick < 0:
        return None
    if pick > rows or pick > cols:
        return 0
    return comb(rows, pick) * comb(cols, pick) * factorial(pick)


def check(rows=4, cols=5, pick=3):
    """Independent: enumerate the cell subsets and test the printed condition.

    Every ``pick``-subset of the rows·cols cells is generated and kept only when
    all its row indices are distinct and all its column indices are distinct.
    No binomial coefficient and no factorial appear.
    """
    if rows < 1 or cols < 1 or pick < 0:
        return None
    cells = [(r, c) for r in range(rows) for c in range(cols)]
    if comb(len(cells), pick) > 2 * 10 ** 6:
        return None
    total = 0
    for choice in combinations(cells, pick):
        used_rows = {r for r, _ in choice}
        used_cols = {c for _, c in choice}
        if len(used_rows) == pick and len(used_cols) == pick:
            total += 1
    return total
