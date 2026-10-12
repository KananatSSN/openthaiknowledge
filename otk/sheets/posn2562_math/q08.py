"""ข้อ 8 — เงินรางวัลรวมของ A, B และ C

การแข่งขันวิ่ง 200 เมตร รายการหนึ่งมีผู้เข้าแข่งขัน 5 คน ได้แก่นักเรียน A, B, C, D
และ E การแข่งขันนี้มีเงินรางวัลให้กับผู้ชนะเลิศ 7,000 บาท รางวัลที่สอง 5,000 บาท
รางวัลที่สาม 2,500 บาท รางวัลที่สี่ 1,500 บาท และรางวัลที่ห้า 500 บาท เมื่อแข่งขัน
เสร็จ A, B และ C ให้ข้อมูลดังนี้
    นักเรียน A: คนที่ถึงก่อนผมมีไม่น้อยกว่า 2 คน แต่ผมเข้าเส้นชัยก่อนนาย D
    นักเรียน B: ผมถึงเส้นชัยตามหลังนาย E เลย
    นักเรียน C: คนที่ถึงเส้นชัยหลังผมมีเพียง 2 คนเท่านั้น
นักเรียน A, B และ C ได้เงินรางวัลรวมกันเป็นเงินทั้งหมดกี่บาท

C's clue is the one that gives a position outright: exactly two people behind him
puts him **third**. A has at least two ahead of him, so A is third or worse — and
third is taken, so A is fourth or fifth; but A beat D, so A is **fourth** and D
is **fifth**. That leaves first and second for B and E, and B finished
*immediately* after E, so E is **first** and B is **second**:

    E, B, C, A, D

A collects the fourth prize, B the second and C the third:

    1,500 + 5,000 + 2,500 = **9,000**

The order is forced — there is exactly one arrangement — which is what makes the
question answerable at all.

``solve`` enumerates the 120 orders and filters them by the three statements.
``check`` builds instead of filtering: it seats C from his own clue and fits the
others around him one clue at a time, so an order that breaks a clue is never
constructed. Either way the placement has to come out unique.
"""

from __future__ import annotations

from itertools import permutations

#: prize per place, how many are ahead of A at minimum, how many are behind C.
PARAMS = {"prizes": (7000, 5000, 2500, 1500, 500), "ahead_of_a": 2,
          "behind_c": 2}
ANSWER = 9000
VARIANTS = [
    {"prizes": (10000, 6000, 3000, 2000, 1000), "ahead_of_a": 2, "behind_c": 2},
    {"prizes": (7000, 5000, 2500, 1500, 500), "ahead_of_a": 1, "behind_c": 2},
    {"prizes": (7000, 5000, 2500, 1500, 500), "ahead_of_a": 2, "behind_c": 3},
    {"prizes": (7000, 5000, 2500, 1500, 500), "ahead_of_a": 3, "behind_c": 2},
    {"prizes": (7000, 5000, 2500, 1500, 500), "ahead_of_a": 0, "behind_c": 1},
    {"prizes": (5, 4, 3, 2, 1), "ahead_of_a": 2, "behind_c": 2},
]
RUNNERS = "ABCDE"


def orders(ahead_of_a=2, behind_c=2):
    """Every finishing order consistent with the three statements."""
    out = []
    for order in permutations(RUNNERS):
        place = {who: i + 1 for i, who in enumerate(order)}
        if place["A"] - 1 < ahead_of_a or place["A"] > place["D"]:
            continue                                     # A's statement
        if place["B"] != place["E"] + 1:
            continue                                     # B's statement
        if len(RUNNERS) - place["C"] != behind_c:
            continue                                     # C's statement
        out.append(order)
    return out


def solve(prizes=(7000, 5000, 2500, 1500, 500), ahead_of_a=2, behind_c=2):
    """Total prize money for A, B and C — only when the order is forced."""
    if len(prizes) != len(RUNNERS):
        return None
    found = orders(ahead_of_a, behind_c)
    if len(found) != 1:
        return None
    place = {who: i for i, who in enumerate(found[0])}
    return sum(prizes[place[who]] for who in "ABC")


def check(prizes=(7000, 5000, 2500, 1500, 500), ahead_of_a=2, behind_c=2):
    """Independent: deduce the places one clue at a time, refusing any ambiguity.

    C's place comes straight from his own count, and the remaining runners are
    fitted around it clue by clue: A into a place with enough people ahead, D
    into a place behind A, then E and B as a consecutive pair in what is left.
    Only assignments that survive every clue are ever built — the 120 orders are
    never generated — and the answer is reported only if exactly one complete
    placement comes out.
    """
    size = len(RUNNERS)
    if len(prizes) != size:
        return None
    if not 0 <= behind_c < size:
        return None
    seat_c = size - behind_c
    if not 1 <= seat_c <= size:
        return None

    complete = set()
    free_after_c = [p for p in range(1, size + 1) if p != seat_c]
    for seat_a in free_after_c:
        if seat_a - 1 < ahead_of_a:
            continue
        for seat_d in free_after_c:
            if seat_d == seat_a or seat_d < seat_a:
                continue
            rest = [p for p in free_after_c if p not in (seat_a, seat_d)]
            for seat_e in rest:
                seat_b = seat_e + 1
                if seat_b not in rest:
                    continue
                complete.add((seat_a, seat_b, seat_c, seat_d, seat_e))
    if len(complete) != 1:
        return None
    seat_a, seat_b, seat_c, _, _ = next(iter(complete))
    return prizes[seat_a - 1] + prizes[seat_b - 1] + prizes[seat_c - 1]
