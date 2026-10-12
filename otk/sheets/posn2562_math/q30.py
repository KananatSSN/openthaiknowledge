"""ข้อ 30 — วันเกิดของส้ม

ฟ้าเล่นเกมทายวันเกิดของส้มในเดือนกันยายนซึ่งเป็นเดือนเกิดของส้มพอดี ถ้าฟ้าทายวันที่
เกิดของส้มถูก ส้มจะให้ของขวัญกับฟ้า ซึ่งในเดือนกันยายน ส้มจะพูดจริงในวันที่ตรงกับเลข
ที่วันเกิดของเธอเท่านั้น และโกหกในวันอื่น ๆ ทั้งหมด โดยส้มพูดกับฟ้าในช่วง 3 วันที่ติดต่อ
กันในเดือนกันยายน ดังนี้
    - วันแรก ส้มพูดว่า "ฉันพูดโกหกในวันที่ 7, 11, 14, 18, 20, 23, 26 และ 29"
    - วันต่อมา ส้มพูดว่า "วันนี้เป็นวันที่ 6, 10, 11, 13, 14, 17, 18, 22, 23, 25, 26,
      28 หรือ 29"
    - และ วันสุดท้าย ส้มพูดว่า "ฉันพูดโกหกในวันที่ 5, 10, 13, 16, 17, 22, 25 และ 28"
จากข้อมูลที่ให้มา วันเกิดของส้มคือวันที่เท่าไหร่ในเดือนกันยายน

Som is truthful on exactly one day of the month — her birthday B — so each
utterance is true precisely when it is made on day B. Translating the three
statements, with the days being d, d+1, d+2:

* "I lie on every day in S" is true ⟺ **B ∉ S** (none of those days is the
  truthful one);
* "today is one of S" is true ⟺ **the day it is said ∈ S**.

Since d, d+1, d+2 are distinct, at most one of the three can be the birthday, so
at most one statement is true. There are **four** cases, not three — the birthday
need not fall inside the three-day window at all:

* **B = d**: needs B ∉ S₁, B ∈ S₃ and B+1 ∉ S₂. But every member of S₃ has its
  successor in S₂, so nothing survives.
* **B = d+1**: needs B ∈ S₁ *and* B ∈ S₃ — and those two lists are disjoint.
* **B = d+2**: needs B ∈ S₁, B ∉ S₃ and B−1 ∉ S₂. Walking S₁ = {7, 11, 14, 18,
  20, 23, 26, 29}, the predecessors 6, 10, 13, 17, 22, 25, 28 are all in S₂ —
  except for **B = 20**, whose predecessor 19 is not.
* **B outside the window**: all three statements are lies, which needs
  B ∈ S₁ ∩ S₃ — empty here, but not in general.

So the three days were 18, 19, 20 and the birthday is **20**: on the 18th and
19th Som lied, and on the 20th she told the truth.

``solve`` walks that four-way case analysis, with no search over the calendar.
``check`` builds the month instead: for each candidate birthday it writes out
the full 30-day truthful/lying schedule and evaluates the three utterances
against it, keeping only the birthdays where every day comes out consistent.
"""

from __future__ import annotations

#: the two "I lie on …" lists, the "today is …" list, and the month length.
PARAMS = {"first": (7, 11, 14, 18, 20, 23, 26, 29),
          "middle": (6, 10, 11, 13, 14, 17, 18, 22, 23, 25, 26, 28, 29),
          "last": (5, 10, 13, 16, 17, 22, 25, 28),
          "days": 30}
ANSWER = 20
VARIANTS = [
    {"first": (7, 11, 14, 18, 20, 23, 26, 29),
     "middle": (6, 10, 11, 13, 14, 17, 18, 22, 23, 25, 26, 28, 29),
     "last": (5, 10, 13, 16, 17, 22, 25, 28), "days": 31},
    {"first": (1, 7, 8, 20), "middle": (7, 12, 16, 19, 20, 28),
     "last": (11, 15, 19, 27), "days": 28},                    # birthday 7
    {"first": (11, 14, 20, 25, 27),
     "middle": (4, 8, 10, 14, 19, 20, 22, 24, 26),
     "last": (3, 7, 13, 19, 21), "days": 30},                  # birthday 14
    {"first": (9, 14, 16, 20, 27, 28),
     "middle": (4, 6, 7, 8, 13, 15, 18, 19, 25, 26),
     "last": (3, 5, 6, 17, 24), "days": 28},                   # birthday 28
    {"first": (7, 11, 14, 18, 20, 23, 26, 29),
     "middle": (6, 10, 11, 13, 14, 17, 18, 22, 23, 25, 26, 28),
     "last": (5, 10, 13, 16, 17, 22, 25, 28), "days": 30},     # 29 dropped: two fit
    {"first": (), "middle": (), "last": (), "days": 30},   # no information
    {"first": (1,), "middle": (1,), "last": (1,), "days": 3},
]


def build(birthday: int, s1_extra, s3_extra, days: int = 30):
    """Construct a puzzle whose only answer is ``birthday``.

    Reverse-engineering the sheet's own three lists shows exactly how it was
    built, and reproduces them character for character from B = 20:

    * S₁ holds the birthday plus decoys, S₃ holds decoys only, and the two are
      **disjoint** — that alone kills the "B = d+1" and "B outside" cases, which
      both need B in S₁ ∩ S₃.
    * S₂ then contains the *predecessor* of every decoy in S₁ (killing their
      "B = d+2" case) and the *successor* of every member of S₃ (killing their
      "B = d" case), while carefully omitting B − 1.

    That last omission is what lets the real birthday through, so the decoy
    B − 2 must not be in S₃ or its successor would put B − 1 back in S₂.
    """
    if not 3 <= birthday <= days:
        return None
    s1 = {birthday} | {x for x in s1_extra if 1 <= x <= days and x != birthday}
    s3 = {y for y in s3_extra if 1 <= y <= days and y != birthday}
    if s1 & s3 or birthday - 2 in s3:
        return None
    s2 = {x - 1 for x in s1 if x != birthday and x > 1}
    s2 |= {y + 1 for y in s3 if y < days}
    if birthday - 1 in s2:
        return None
    return tuple(sorted(s1)), tuple(sorted(s2)), tuple(sorted(s3))


def solve(first=(7, 11, 14, 18, 20, 23, 26, 29),
          middle=(6, 10, 11, 13, 14, 17, 18, 22, 23, 25, 26, 28, 29),
          last=(5, 10, 13, 16, 17, 22, 25, 28), days=30):
    """The one birthday consistent with the three utterances, by case analysis."""
    if days < 3:
        return None
    s1, s2, s3 = set(first), set(middle), set(last)
    starts = range(1, days - 1)
    hits = set()

    # B = d: the first statement is the true one.
    hits |= {b for b in starts
             if b not in s1 and b in s3 and b + 1 not in s2}
    # B = d+1: the middle statement is the true one.
    hits |= {b for b in range(2, days)
             if b in s1 and b in s2 and b in s3 and b - 1 in starts}
    # B = d+2: the last statement is the true one.
    hits |= {b for b in range(3, days + 1)
             if b in s1 and b not in s3 and b - 1 not in s2 and b - 2 in starts}
    # B outside the window: every statement is a lie, and some window fits.
    hits |= {b for b in range(1, days + 1)
             if b in s1 and b in s3
             and any(d + 1 not in s2 and b not in (d, d + 1, d + 2)
                     for d in starts)}

    if len(hits) != 1:
        return None
    return next(iter(hits))


def check(first=(7, 11, 14, 18, 20, 23, 26, 29),
          middle=(6, 10, 11, 13, 14, 17, 18, 22, 23, 25, 26, 28, 29),
          last=(5, 10, 13, 16, 17, 22, 25, 28), days=30):
    """Independent: write out the month's schedule and test every utterance.

    For each candidate birthday the whole month is laid out as a list of
    truthful/lying days; the three statements are then evaluated against *that
    list* — "I lie on S" is checked by looking up every day of S in the schedule,
    not by a membership shortcut — and the day is kept only if each utterance's
    truth value matches the schedule on the day it was made.
    """
    if days < 3:
        return None
    s1, s2, s3 = set(first), set(middle), set(last)
    hits = set()
    for birthday in range(1, days + 1):
        truthful = [day == birthday for day in range(days + 1)]
        for start in range(1, days - 1):
            trio = (start, start + 1, start + 2)
            claims = [
                all(not truthful[day] for day in s1 if day <= days),
                trio[1] in s2,
                all(not truthful[day] for day in s3 if day <= days),
            ]
            if all(claim == truthful[day] for claim, day in zip(claims, trio)):
                hits.add(birthday)
    if len(hits) != 1:
        return None
    return next(iter(hits))
