"""ข้อ 23 — จำนวนครั้งของการจับมือทั้งหมด

ณ งานเลี้ยงหนึ่ง มีผู้ร่วมงานทั้งหมด 50 คน แต่ละคนได้รับหมายเลขตามลำดับการเข้างาน
ตั้งแต่ 1 ถึง 50 ผู้ร่วมงานทักทายจับมือกันทั้งหมด 2 รอบ ดังนี้
    รอบที่ 1  คนที่มีหมายเลข i จับมือกับคนที่มีหมายเลข i+1 สำหรับ i = 1, 2, …, 49
              และคนที่ 50 จับกับคนที่ 1
    รอบที่ 2  คนที่มีหมายเลขคู่จับมือกับคนที่มีหมายเลขมากกว่าตัวเองทั้งหมดที่ยังไม่เคย
              จับมือกัน
อยากทราบว่าในงานนี้จะมีการจับมือทักทายกันทั้งหมดกี่ครั้ง

Round 1 is a cycle on the 50 guests, so it is **50** handshakes — the wrap-around
50–1 is what makes it a cycle rather than a path.

In round 2 each even-numbered guest j reaches every larger number except the one
neighbour j+1 already met in round 1. (The other round-1 pair touching j is
{j−1, j}, whose partner is *smaller*, and the wrap pair {50, 1} likewise never
has 1 above 50.) So guest j contributes ``(50 − j) − 1`` new handshakes:

    j =  2 → 47,   j = 4 → 45,   …,   j = 48 → 1,   j = 50 → 0

which is the sum of the odd numbers up to 47, namely **24² = 576**. In total

    50 + 576 = **626**

and in general, for n guests with n even, ``n + (n/2 − 1)²``.

``solve`` uses that closed form. ``check`` builds the actual set of unordered
pairs — round 1 first, then round 2 added to the same set — and counts it, so
any double-counting between the rounds would show up immediately.
"""

from __future__ import annotations

#: how many guests, numbered 1..people.
PARAMS = {"people": 50}
ANSWER = 626
VARIANTS = [
    {"people": 6},
    {"people": 10},
    {"people": 4},
    {"people": 100},
    {"people": 2},
    {"people": 7},          # odd: the even guests no longer pair off cleanly
]


def solve(people=50):
    """n + (n/2 − 1)² — the cycle plus the new pairs each even guest makes."""
    if people < 3 or people % 2:
        return None
    return people + (people // 2 - 1) ** 2


def check(people=50):
    """Independent: build the set of pairs and count it.

    Round 1 is added as unordered pairs, then round 2 adds every (even, larger)
    pair to the *same* set — so a handshake that both rounds would produce is
    stored once, exactly as the story requires, rather than being subtracted by
    an argument.
    """
    if people < 3 or people % 2:
        return None
    shaken = set()
    for i in range(1, people + 1):
        partner = i % people + 1                 # 50 wraps round to 1
        shaken.add(frozenset((i, partner)))
    for j in range(2, people + 1, 2):
        for k in range(j + 1, people + 1):
            shaken.add(frozenset((j, k)))
    return len(shaken)
