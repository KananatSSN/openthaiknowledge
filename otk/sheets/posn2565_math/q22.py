"""ข้อ 22 — คู่อันดับ (a, b) ของกล่องลูกปิงปองสีส้มและชั้นวาง

มีลูกเทนนิส 2 ลูก ลูกปิงปองสีส้มและสีขาวอย่างละ 1 ลูก มีชั้นวางของ 4 ชั้น
(ชั้นบนสุดคือชั้นที่ 1 ถัดลงมาเป็นชั้นที่ 2, 3 และ 4) และมีกล่อง 4 ใบหมายเลข
5, 6, 7 และ 8  นำลูกบอลใส่กล่องละ 1 ลูกและวางกล่องบนชั้นละ 1 กล่อง โดย
    ก) ลูกเทนนิส 2 ลูกต้องอยู่บนชั้นที่ติดกัน
    ข) ลูกปิงปอง 2 ลูกจะไม่อยู่บนชั้นที่ติดกัน
    ค) กล่องหมายเลข 5 และ 7 จะไม่วางบนชั้นที่ติดกับชั้นที่กล่องหมายเลข 8 วางอยู่
ถ้าลูกปิงปองสีขาวอยู่ในกล่องหมายเลข 7 จงหาคู่อันดับ (a, b) ที่เป็นไปได้ทั้งหมด
เมื่อลูกปิงปองสีส้มอยู่ในกล่องหมายเลข a และวางบนชั้นที่ b

Rule (ค) alone almost finishes the puzzle. Every shelf next to box 8 must hold a
box that is neither 5 nor 7, and only box 6 qualifies — so box 8 can have **at
most one neighbour**, i.e. it sits on shelf 1 or shelf 4, with box 6 directly
beside it and boxes 5 and 7 taking the far pair of shelves:

    8 6 · ·   or   · · 6 8      (the two dots are 5 and 7 in some order)

That leaves four layouts. Filling them in, the white ping-pong ball is in box 7
and the two tennis balls must be adjacent while the two ping-pong balls must not
be, and exactly two placements survive — both with the orange ball in **box 8**:

    (a, b) = **(8, 1)** and **(8, 4)**

In (8, 1) the layout is 8 6 5 7: orange on shelf 1, white on shelf 4 (apart ✓),
tennis balls in boxes 6 and 5 on shelves 2 and 3 (adjacent ✓). In (8, 4) it is
7 5 6 8, the mirror image.

``solve`` enumerates the 4! box orders and the choice of the orange box, applying
the three rules to each. ``check`` never enumerates the layouts: it derives the
position of box 8 from rule (ค) by counting how many neighbours a shelf has,
builds only the layouts that survive, and then tests the ball rules by walking
the shelves. The two searches disagree if either rule is misread.
"""

from __future__ import annotations

import itertools

#: shelves 1..shelves, boxes first_box.. ; ``anchor`` is the box rule (ค) is
#: about, ``away`` the two that may not sit beside it, ``white`` the box holding
#: the white ping-pong ball.
PARAMS = {"shelves": 4, "first_box": 5, "anchor": 8, "away": (5, 7), "white": 7}
ANSWER = ((8, 1), (8, 4))
VARIANTS = [
    {"shelves": 4, "first_box": 5, "anchor": 8, "away": (5, 6), "white": 7},
    {"shelves": 4, "first_box": 5, "anchor": 5, "away": (7, 8), "white": 7},
    {"shelves": 4, "first_box": 1, "anchor": 4, "away": (1, 3), "white": 3},
    {"shelves": 4, "first_box": 5, "anchor": 8, "away": (5, 7), "white": 8},
    {"shelves": 4, "first_box": 5, "anchor": 8, "away": (6, 7), "white": 7},
    {"shelves": 4, "first_box": 5, "anchor": 6, "away": (5, 7), "white": 7},
]


def _boxes(shelves: int, first_box: int) -> list[int]:
    return list(range(first_box, first_box + shelves))


def _valid(shelf, boxes, white, orange, away, anchor) -> bool:
    """The three rules, given a box → shelf map and which box holds the orange."""
    if any(abs(shelf[b] - shelf[anchor]) == 1 for b in away if b != anchor):
        return False                                    # rule (ค)
    tennis = [b for b in boxes if b not in (white, orange)]
    if len(tennis) != 2 or abs(shelf[tennis[0]] - shelf[tennis[1]]) != 1:
        return False                                    # rule (ก)
    return abs(shelf[white] - shelf[orange]) != 1       # rule (ข)


def solve(shelves=4, first_box=5, anchor=8, away=(5, 7), white=7):
    """Every (orange box, its shelf) the three rules allow, sorted."""
    boxes = _boxes(shelves, first_box)
    if anchor not in boxes or white not in boxes or any(b not in boxes
                                                        for b in away):
        return None
    if shelves != 4:            # the ball count only matches a four-shelf rack
        return None
    hits = set()
    for order in itertools.permutations(boxes):
        shelf = {b: i + 1 for i, b in enumerate(order)}
        for orange in boxes:
            if orange == white:
                continue
            if _valid(shelf, boxes, white, orange, away, anchor):
                hits.add((orange, shelf[orange]))
    return tuple(sorted(hits)) if hits else None


def check(shelves=4, first_box=5, anchor=8, away=(5, 7), white=7):
    """Independent: place the anchor box from rule (ค) first, then fill the rest.

    Rule (ค) says every shelf adjacent to the anchor holds a box outside ``away``.
    So the anchor's shelf is counted against the supply of such boxes before any
    layout is built; only the shelves that pass get expanded, and the ball rules
    are then applied by scanning the rack top to bottom rather than by looking up
    a box → shelf map.
    """
    boxes = _boxes(shelves, first_box)
    if anchor not in boxes or white not in boxes or any(b not in boxes
                                                        for b in away):
        return None
    if shelves != 4:
        return None
    free = [b for b in boxes if b not in away and b != anchor]

    hits = set()
    for seat in range(1, shelves + 1):
        neighbours = [s for s in (seat - 1, seat + 1) if 1 <= s <= shelves]
        if len(neighbours) > len(free):
            continue                                    # rule (ค) cannot hold
        rest = [b for b in boxes if b != anchor]
        for filling in itertools.permutations(rest):
            rack = list(filling[:seat - 1]) + [anchor] + list(filling[seat - 1:])
            if any(rack[s - 1] in away for s in neighbours):
                continue
            for orange in boxes:
                if orange == white:
                    continue
                spots = {b: i + 1 for i, b in enumerate(rack)}
                tennis = [i + 1 for i, b in enumerate(rack)
                          if b not in (white, orange)]
                if len(tennis) != 2 or tennis[1] - tennis[0] != 1:
                    continue
                if abs(spots[white] - spots[orange]) == 1:
                    continue
                hits.add((orange, spots[orange]))
    return tuple(sorted(hits)) if hits else None
