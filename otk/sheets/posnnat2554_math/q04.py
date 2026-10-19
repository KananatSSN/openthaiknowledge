"""ข้อ 4 — มีสองห้องที่แต่ละห้องมีนักเรียนต่างชาติสองคนผลต่างเลขที่เท่ากันและเพศเดียวกัน  (พิสูจน์)

A room with b students gives b − 1 distinct differences from its lowest seat,
all in 1..L − 1; if no difference repeats across rooms, Σ(b − 1) ≤ L − 1, so at
most R + L − 1 students fit, and R + L − 1 is attainable. The solver returns the
forcing count R + L (3 rooms of 4 seats: 7).

``check`` searches every set of occupied (room, seat) cells for the largest one
with no difference shared by two rooms, and adds 1.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"rooms": 3, "seats": 4}
ANSWER = 7
VARIANTS = [{"rooms": 2, "seats": 3}, {"rooms": 2, "seats": 5}, {"rooms": 3, "seats": 3}]


def solve(rooms=3, seats=4):
    return rooms + seats


def check(rooms=3, seats=4):
    cells = [(r, s) for r in range(rooms) for s in range(seats)]
    best = 0
    for mask in range(1 << len(cells)):
        size = bin(mask).count("1")
        if size <= best:
            continue
        diffs = {}
        clash = False
        for r in range(rooms):
            seats_r = [s for (rr, s) in cells if rr == r and mask >> (rr * seats + s) & 1]
            own = {b - a for a, b in combinations(sorted(seats_r), 2)}
            for d in own:
                if d in diffs:
                    clash = True
                diffs[d] = r
        if not clash:
            best = size
    return best + 1
