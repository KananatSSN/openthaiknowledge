"""ข้อ 6 — มีผู้มีความเสี่ยงสูง เมื่อมีผู้มีเชื้อ 901 คนในห้อง 60 × 60  (พิสูจน์)

Split the hall into 2 × 2 blocks. No infected sits in another's zone (left,
right, front), so two infected in one block sit at opposite corners, and then
the block's third seat is in both their zones. So with nobody at high risk each
block holds at most one infected: at most (rows/2)(columns/2) = 900 < 901. The
solver returns that bound; PARAMS uses a 4 × 4 hall so that ``check`` can try
every seating (the source 60 × 60 gives 900).

``check`` tries every set of infected seats in the hall, keeps those with no
infected in another's zone and no seat in two zones, and returns the largest.
"""

from __future__ import annotations

PARAMS = {"rows": 4, "columns": 4}
ANSWER = 4
VARIANTS = [{"rows": 2, "columns": 4}, {"rows": 2, "columns": 6}, {"rows": 4, "columns": 2}]


def solve(rows=4, columns=4):
    return (rows // 2) * (columns // 2)


def check(rows=4, columns=4):
    cells = [(r, c) for r in range(rows) for c in range(columns)]
    index = {cell: i for i, cell in enumerate(cells)}
    zones = [[index[z] for z in ((r, c - 1), (r, c + 1), (r - 1, c)) if z in index] for r, c in cells]
    best = 0
    for mask in range(1 << len(cells)):
        size = bin(mask).count("1")
        if size <= best:
            continue
        hits = [0] * len(cells)
        ok = True
        for i in range(len(cells)):
            if mask >> i & 1:
                for j in zones[i]:
                    hits[j] += 1
                    if mask >> j & 1 or hits[j] > 1:
                        ok = False
                        break
                if not ok:
                    break
        if ok:
            best = size
    return best
