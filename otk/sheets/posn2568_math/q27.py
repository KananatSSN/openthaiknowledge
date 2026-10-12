"""ข้อ 27 — นับรูปสี่เหลี่ยมมุมฉากที่ไม่มีช่องสีดำอยู่ภายใน

กำหนดตารางขนาด 7×7  จงหาจำนวนของรูปสี่เหลี่ยมมุมฉากทั้งหมดที่สร้างขึ้นได้โดยลากเส้น
ตามแนวเส้นในตาราง โดยที่ต้องไม่มีช่องสีดำใด ๆ อยู่ภายในเลย

The figure is the data: the black cells form a plus centred on the middle cell.
They were read off the PDF with ``sheetpipe.extract.read_cell_grid`` rather than
by eye — see ``FIGURE`` below, which is that reader's output verbatim:

    .......
    .......
    ...#...
    ..###..
    ...#...
    .......
    .......

Method: fix the two vertical lines (a column span) and sweep the bottom edge
down the grid. For each bottom row, every rectangle is legal exactly down to the
row after the last blocked row seen inside that column span, so the count for
that bottom edge is one subtraction — O(cols²·rows) overall instead of checking
every rectangle against every black cell.

``check`` is that quadruple loop, testing each of the C(8,2)² rectangles against
each black cell.
"""

from __future__ import annotations

from itertools import product

FIGURE = ("""
.......
.......
...#...
..###..
...#...
.......
.......
""").strip()

PARAMS = {"rows": 7, "cols": 7,
          "blocked": ((2, 3), (3, 2), (3, 3), (3, 4), (4, 3))}
ANSWER = 336
VARIANTS = [
    {"blocked": ()},                       # no black cells → C(8,2)² = 784
    {"blocked": ((3, 3),)},
    {"blocked": ((0, 0), (6, 6))},
    {"rows": 4, "cols": 5, "blocked": ((1, 2), (2, 2))},
    {"rows": 3, "cols": 3, "blocked": ((1, 1),)},
]


def solve(rows=7, cols=7, blocked=()):
    """Rectangles on the grid lines containing no blocked cell."""
    bad = set(blocked)
    total = 0
    for c1 in range(cols):
        for c2 in range(c1 + 1, cols + 1):
            # rows carrying a blocked cell inside the column span [c1, c2)
            hit = {r for r, c in bad if c1 <= c < c2}
            last_bad = -1
            for r2 in range(1, rows + 1):
                if r2 - 1 in hit:
                    last_bad = r2 - 1
                total += r2 - last_bad - 1
    return total


def check(rows=7, cols=7, blocked=()):
    """Independent: test every rectangle against every blocked cell."""
    bad = set(blocked)
    count = 0
    for r1, c1 in product(range(rows), range(cols)):
        for r2, c2 in product(range(r1 + 1, rows + 1), range(c1 + 1, cols + 1)):
            if not any(r1 <= r < r2 and c1 <= c < c2 for r, c in bad):
                count += 1
    return count
