"""ข้อ 17 — นักเรียน B ได้รับเงินจากครูรวมกี่บาท

นักเรียน 5 คน (A B C D และ E) ได้รับรางวัลคนละ 1 เหรียญ และ 1 ธนบัตร เท่านั้น
เหรียญมูลค่า ห้าสิบสตางค์ หนึ่งบาท สองบาท ห้าบาท สิบบาท อย่างละ 1 เหรียญ และ
ธนบัตรมูลค่าใบละ ยี่สิบบาท ห้าสิบบาท หนึ่งร้อยบาท ห้าร้อยบาท หนึ่งพันบาท อย่างละ
1 ใบ ปรากฏว่า

  • นักเรียน B, ผู้ได้ธนบัตรยี่สิบบาท, ผู้ได้ธนบัตรห้าสิบบาท, ผู้ได้เหรียญสองบาท
    และผู้ได้เหรียญห้าสิบสตางค์ เป็นคนละคนกัน
  • นักเรียน D ไม่ได้ธนบัตรยี่สิบบาท     • ผู้ได้เหรียญห้าสิบสตางค์ คือ นักเรียน A
  • ธนบัตรที่นักเรียน C ได้มีมูลค่าหนึ่งร้อยบาท   • นักเรียน D ได้เหรียญห้าบาท
  • นักเรียน E ไม่ได้เหรียญหนึ่งบาท
  • ผู้ได้เหรียญหนึ่งบาทไม่ได้ธนบัตรหนึ่งพันบาท

จากข้อมูลข้างต้นอยากทราบว่านักเรียน B ได้รับเงินจากครูรวมกี่บาท

**The first bullet names five pairwise-distinct people out of five**, so it is
not a weak constraint — it is a partition. A holds the 50-satang coin, so
{20-note holder, 50-note holder, 2-baht holder} = {C, D, E} exactly. From there
the chain is forced:

    C holds the 100 note  ⟹ C is the 2-baht holder
    D is barred from 20   ⟹ D holds the 50 note, and E the 20
    E refuses the 1-baht  ⟹ B holds it (A, C, D are taken)
    the 1-baht holder is barred from the 1000 ⟹ B holds the 500, A the 1000

so **B = 1 + 500 = 501 บาท**.

``solve`` propagates those deductions in that order. ``check`` searches all
120 × 120 assignments of coins and notes to the five children and keeps every one
that satisfies the seven printed bullets — so uniqueness is *measured*, not
argued, and the search returns exactly one assignment.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations

#: coin values in baht (50 satang = 1/2) and note values in baht.
PARAMS = {
    "coins": (Fraction(1, 2), 1, 2, 5, 10),
    "notes": (20, 50, 100, 500, 1000),
}
ANSWER = Fraction(501)
VARIANTS = [
    {"coins": (Fraction(1, 2), 1, 2, 5, 20)},
    {"notes": (20, 50, 100, 500, 2000)},
    {"coins": (Fraction(1, 4), 1, 2, 5, 10)},
    {"notes": (20, 50, 100, 400, 1000)},
    {"coins": (Fraction(1, 2), 1, 2, 5, 10), "notes": (20, 50, 100, 500, 800)},
    {"coins": (Fraction(1, 2), 3, 2, 5, 10)},
]

PEOPLE = ("A", "B", "C", "D", "E")


def _roles(coins, notes):
    """Index the values the clues refer to by position, not by number."""
    return {
        "small": coins[0],    # ห้าสิบสตางค์
        "one": coins[1],      # หนึ่งบาท
        "two": coins[2],      # สองบาท
        "five": coins[3],     # ห้าบาท
        "note20": notes[0],
        "note50": notes[1],
        "note100": notes[2],
        "note1000": notes[4],
    }


def _satisfies(coin_of, note_of, r):
    """The seven printed bullets, as written."""
    holder = lambda mapping, value: next(  # noqa: E731
        p for p in PEOPLE if mapping[p] == value)
    if len({"B", holder(note_of, r["note20"]), holder(note_of, r["note50"]),
            holder(coin_of, r["two"]), holder(coin_of, r["small"])}) != 5:
        return False
    if note_of["D"] == r["note20"]:
        return False
    if coin_of["A"] != r["small"]:
        return False
    if note_of["C"] != r["note100"]:
        return False
    if coin_of["D"] != r["five"]:
        return False
    if coin_of["E"] == r["one"]:
        return False
    if note_of[holder(coin_of, r["one"])] == r["note1000"]:
        return False
    return True


def solve(coins=PARAMS["coins"], notes=PARAMS["notes"]):
    """Propagate the deductions in the order the bullets force them."""
    if len(set(coins)) != 5 or len(set(notes)) != 5:
        return None
    r = _roles(coins, notes)
    coin_of = {"A": r["small"], "D": r["five"]}
    note_of = {"C": r["note100"]}

    # bullet 1 partitions everyone: {20, 50, two-baht} go to C, D, E
    # C already holds the 100 note, so C takes the two-baht coin
    coin_of["C"] = r["two"]
    # D is barred from the 20, so D takes the 50 and E the 20
    note_of["D"] = r["note50"]
    note_of["E"] = r["note20"]
    # the one-baht coin cannot be E's, and A, C, D are placed, so it is B's
    coin_of["B"] = r["one"]
    coin_of["E"] = next(c for c in coins if c not in coin_of.values())
    # the one-baht holder is barred from the 1000 note
    left = [n for n in notes if n not in note_of.values()]
    note_of["B"] = next(n for n in left if n != r["note1000"])
    note_of["A"] = next(n for n in left if n != note_of["B"])

    if not _satisfies(coin_of, note_of, r):
        return None
    return Fraction(coin_of["B"]) + note_of["B"]


def check(coins=PARAMS["coins"], notes=PARAMS["notes"]):
    """Independent: search every assignment and keep the ones that fit.

    No deduction at all — 120 coin permutations against 120 note permutations,
    each tested against the seven bullets. The answer is accepted only if
    exactly one assignment survives, so the puzzle's uniqueness is checked too.
    """
    if len(set(coins)) != 5 or len(set(notes)) != 5:
        return None
    r = _roles(coins, notes)
    found = set()
    for cp in permutations(coins):
        coin_of = dict(zip(PEOPLE, cp))
        if coin_of["A"] != r["small"] or coin_of["D"] != r["five"]:
            continue
        for np_ in permutations(notes):
            note_of = dict(zip(PEOPLE, np_))
            if _satisfies(coin_of, note_of, r):
                found.add(Fraction(coin_of["B"]) + note_of["B"])
    if len(found) != 1:
        return None
    return found.pop()
