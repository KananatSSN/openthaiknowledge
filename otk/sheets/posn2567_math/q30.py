"""ข้อ 30 — นามสกุลและฟาร์มของนายเอ นายบี นายซี และนายดี

นายเอ นายบี นายซี และนายดี ทำงานอยู่ในฟาร์มวัว ฟาร์มกุ้ง ฟาร์มไก่ และฟาร์มหมู
นามสกุลของคนทั้งสี่โดยไม่เรียงตามชื่อคือ เบิกบาน ปันใจ มานะ และลือชัย
(1) แต่ละคนทำงานคนละฟาร์ม (2) มานะไม่ได้ทำงานในฟาร์มกุ้งหรือฟาร์มไก่
(3) นายซีทำงานในฟาร์มหมู (4) เบิกบานเป็นนามสกุลของนายดี
(5) นามสกุลของนายซีไม่ใช่ลือชัยหรือมานะ (6) มานะไม่ใช่นามสกุลของนายบี
(7) ลือชัยไม่ได้ทำงานในฟาร์มกุ้ง  จงหาว่าแต่ละคนมีนามสกุลอะไรและทำงานฟาร์มอะไร

The chain is forced and needs no search: (4) gives ดี = เบิกบาน, then (5) leaves
only ปันใจ for ซี, then (6) sends มานะ to เอ and ลือชัย to บี. For the farms, (3)
puts ซี in หมู, (2) then leaves only วัว for เอ (มานะ), (7) keeps บี (ลือชัย) out
of กุ้ง so บี takes ไก่, and ดี is left with กุ้ง:

    เอ มานะ/วัว · บี ลือชัย/ไก่ · ซี ปันใจ/หมู · ดี เบิกบาน/กุ้ง

``solve`` returns that as a tuple of (surname, farm) index pairs, one per person,
and ``None`` when the clues do not pin exactly one assignment — which matters,
because the generator moves three of the clues around and most of the moved
versions are ambiguous.

The two routes are a search and a deduction: ``solve`` enumerates all 4!·4! = 576
assignments and filters, while ``check`` applies the clues as elimination rules on
a candidate grid and only falls back to enumerating what the grid could not
decide.
"""

from __future__ import annotations

import itertools

#: 0 เบิกบาน, 1 ปันใจ, 2 มานะ, 3 ลือชัย · 0 วัว, 1 กุ้ง, 2 ไก่, 3 หมู
SURNAMES = ("เบิกบาน", "ปันใจ", "มานะ", "ลือชัย")
FARMS = ("วัว", "กุ้ง", "ไก่", "หมู")
PEOPLE = ("นายเอ", "นายบี", "นายซี", "นายดี")

MANA, LUECHAI, BOEKBAN = 2, 3, 0
SHRIMP, CHICKEN, PIG = 1, 2, 3

#: which person works the pig farm, who is เบิกบาน, and who cannot be มานะ.
PARAMS = {"pig_person": 2, "boekban_person": 3, "not_mana_person": 1}
ANSWER = ((2, 0), (3, 2), (1, 3), (0, 1))
VARIANTS = [
    {"pig_person": 0, "boekban_person": 3, "not_mana_person": 1},
    {"pig_person": 1, "boekban_person": 0, "not_mana_person": 2},
    {"pig_person": 3, "boekban_person": 1, "not_mana_person": 0},
    {"pig_person": 2, "boekban_person": 2, "not_mana_person": 1},   # clues clash
    {"pig_person": 0, "boekban_person": 1, "not_mana_person": 2},
]


def _ok(surname, farm, pig_person, boekban_person, not_mana_person) -> bool:
    """surname[p] and farm[p] are the indices assigned to person p."""
    mana = surname.index(MANA)
    luechai = surname.index(LUECHAI)
    return (farm[mana] not in (SHRIMP, CHICKEN)                 # clue 2
            and farm[pig_person] == PIG                          # clue 3
            and surname[boekban_person] == BOEKBAN               # clue 4
            and surname[pig_person] not in (LUECHAI, MANA)       # clue 5
            and surname[not_mana_person] != MANA                 # clue 6
            and farm[luechai] != SHRIMP)                         # clue 7


def solve(pig_person=2, boekban_person=3, not_mana_person=1):
    """The unique (surname, farm) per person, or None if the clues leave a choice."""
    hits = []
    for surname in itertools.permutations(range(4)):
        for farm in itertools.permutations(range(4)):
            if _ok(surname, farm, pig_person, boekban_person, not_mana_person):
                hits.append(tuple(zip(surname, farm)))
                if len(hits) > 1:
                    return None
    return hits[0] if hits else None


def check(pig_person=2, boekban_person=3, not_mana_person=1):
    """Independent: eliminate on a candidate grid, enumerate only what is left.

    Each person starts with all four surnames and all four farms possible; the
    clues that name a person outright are applied as strikes, singles are
    propagated, and whatever survives is enumerated. If the elimination alone
    settled it the enumeration confirms it; if it did not, the answer still comes
    out — but by a different road than ``solve``'s flat product.
    """
    surnames = [set(range(4)) for _ in range(4)]
    farms = [set(range(4)) for _ in range(4)]

    surnames[boekban_person] = {BOEKBAN}                          # clue 4
    surnames[pig_person] -= {LUECHAI, MANA}                       # clue 5
    surnames[not_mana_person] -= {MANA}                           # clue 6
    farms[pig_person] = {PIG}                                     # clue 3

    for _ in range(4):                                            # propagate singles
        for pool in (surnames, farms):
            for p, opts in enumerate(pool):
                if len(opts) == 1:
                    (only,) = opts
                    for other in range(4):
                        if other != p:
                            pool[other].discard(only)

    if any(not s for s in surnames) or any(not f for f in farms):
        return None

    hits = []
    for surname in itertools.product(*surnames):
        if len(set(surname)) != 4:
            continue
        for farm in itertools.product(*farms):
            if len(set(farm)) != 4:
                continue
            if _ok(surname, farm, pig_person, boekban_person, not_mana_person):
                hits.append(tuple(zip(surname, farm)))
                if len(hits) > 1:
                    return None
    return hits[0] if hits else None
