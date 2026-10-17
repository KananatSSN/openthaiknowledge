"""วันที่สอง ข้อ 5 — วัน 5 วัน หนังสือ 16 เล่ม: ต้องมีสองวันสองเล่มที่ไม่มีใครยืม หรือมีสี่คนเพศเดียวกัน  (พิสูจน์)

Each column (book) picks a set of rows (days); a rectangle-free choice lets two
columns share at most one row, so every pair of rows is used by at most one
column. The solver returns the largest rectangle-free number of marked cells
in an r × c grid by a search over column sets (3 × 4: 7).

``check`` tries every subset of cells directly.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

PARAMS = {"rows": 3, "cols": 4}
ANSWER = 7
VARIANTS = [{"rows": 2, "cols": 5}, {"rows": 4, "cols": 4}, {"rows": 3, "cols": 3}]


def solve(rows=3, cols=4):
    subsets = [tuple(s) for size in range(rows + 1) for s in combinations(range(rows), size)]

    @lru_cache(maxsize=None)
    def best(col, used):
        if col == cols:
            return 0
        top = 0
        for s in subsets:
            pairs = frozenset(combinations(s, 2))
            if pairs & used:
                continue
            top = max(top, len(s) + best(col + 1, used | pairs))
        return top

    return best(0, frozenset())


def check(rows=3, cols=4):
    cells = [(r, c) for r in range(rows) for c in range(cols)]
    best = 0
    for mask in range(1 << len(cells)):
        size = bin(mask).count("1")
        if size <= best:
            continue
        chosen = {cells[i] for i in range(len(cells)) if mask >> i & 1}
        if not any({(r1, c1), (r1, c2), (r2, c1), (r2, c2)} <= chosen
                   for r1, r2 in combinations(range(rows), 2) for c1, c2 in combinations(range(cols), 2)):
            best = size
    return best
