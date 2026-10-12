"""ข้อ 16 — ค่าของ a² + b² จากบทสนทนาเรื่องผลรวมและผลคูณ

กล่องทึบสองกล่องแต่ละกล่องบรรจุสลากเลข 1, 2, 3 และ 4 อย่างละหนึ่งใบ คุณครูสุ่ม
หยิบสลากกล่องละ 1 ใบ เด็กชาย A ทราบผลรวมของเลขบนสลาก ในขณะที่เด็กหญิง B ทราบ
ผลคูณ จากนั้นให้ทั้งสองคุยกันเพื่อทายว่าคุณครูหยิบได้เลขอะไรบ้าง

    A: เธอรู้ไหมว่าคุณครูหยิบได้เลขอะไรบ้าง
    B: พยายามคิดแล้วแต่ตัวเลขที่ได้ยินมันยังบอกไม่ได้ว่าคุณครูหยิบได้เลขอะไรบ้าง
       แล้วเธอล่ะ
    A: ตอนแรกก็ไม่รู้ แต่ตอนนี้รู้แล้วแหละ **ฉันได้ยินคนละเลขกับเธอนะ**
    B: อ๋อ ตอนนี้ฉันก็รู้แล้ว

ถ้าให้ a, b เป็นเลขที่คุณครูหยิบได้ แล้วค่าของ a² + b² เป็นเท่าใด

Three announcements, and **the third one is what finishes it**:

1. B does not know ⟹ the product is ambiguous, and among 1…4 the only such
   product is **4** ({1,4} or {2,2}).
2. A "did not know at first" ⟹ the sum was ambiguous; "but now I know" ⟹ after
   step 1 only one pair remains with that sum. Both surviving sums qualify —
   4 leaves {2,2} and 5 leaves {1,4} — so this step alone does **not** decide it.
3. "ฉันได้ยินคนละเลขกับเธอนะ" says A's number differs from B's. {2,2} has sum 4
   and product 4; {1,4} has 5 and 4. So the pair is {1,4} and a² + b² = **17**.

Reading clue 3 as flavour text leaves the item with two answers, which is the
tell that it is doing work.

``solve`` walks that chain in the order above. ``check`` uses a general
public-announcement engine instead: worlds are all the draws, each speaker's
knowledge is the partition induced by their own number, and every announcement
is applied as a filter until the set of worlds stops shrinking. It is told the
announcements, not the reasoning.
"""

from __future__ import annotations

#: tickets 1…top in each of the two boxes.
PARAMS = {"top": 4, "distinct_numbers": True}
ANSWER = 17
VARIANTS = [
    {"top": 5, "distinct_numbers": True},
    {"top": 4, "distinct_numbers": False},      # clue 3 dropped: ambiguous
    {"top": 6, "distinct_numbers": True},
    {"top": 3, "distinct_numbers": True},
    {"top": 8, "distinct_numbers": True},
    {"top": 7, "distinct_numbers": True},
]


def _worlds(top):
    """The unordered draws — the boxes are indistinguishable to both children."""
    return [(a, b) for a in range(1, top + 1) for b in range(a, top + 1)]


def solve(top=4, distinct_numbers=True):
    """Apply the three announcements in the order the dialogue gives them."""
    if top < 2:
        return None
    worlds = _worlds(top)

    def by(key, pool):
        groups = {}
        for w in pool:
            groups.setdefault(key(w), []).append(w)
        return groups

    total = lambda w: w[0] + w[1]        # noqa: E731
    times = lambda w: w[0] * w[1]        # noqa: E731

    # 1. B does not know: the product is shared by more than one draw
    after_b = [w for w in worlds if len(by(times, worlds)[times(w)]) > 1]
    # 2. A did not know at first, but knows now
    groups_now = by(total, after_b)
    after_a = [w for w in after_b
               if len(by(total, worlds)[total(w)]) > 1
               and len(groups_now[total(w)]) == 1]
    # 3. A's number differs from B's
    final = [w for w in after_a if total(w) != times(w)] if distinct_numbers \
        else list(after_a)
    # 4. B now knows: the product must single a world out of what is left
    groups_final = by(times, final)
    final = [w for w in final if len(groups_final[times(w)]) == 1]

    if len(final) != 1:
        return None
    a, b = final[0]
    return a * a + b * b


def check(top=4, distinct_numbers=True):
    """Independent: a generic announcement engine over the space of worlds.

    Each announcement is a predicate on (world, surviving set); the engine
    applies them in turn and re-applies until nothing changes, which is how
    public-announcement logic is normally evaluated. It contains no reasoning
    about sums or products beyond what each speaker can see.
    """
    if top < 2:
        return None
    live = _worlds(top)

    def knows(w, pool, view):
        return sum(1 for x in pool if view(x) == view(w)) == 1

    sum_view = lambda w: w[0] + w[1]     # noqa: E731
    prod_view = lambda w: w[0] * w[1]    # noqa: E731

    announcements = [
        lambda w, pool: not knows(w, pool, prod_view),      # B: I don't know
        lambda w, pool: not knows(w, _worlds(top), sum_view)  # A: not at first
        and knows(w, pool, sum_view),                       # A: but now I do
    ]
    if distinct_numbers:
        announcements.append(lambda w, pool: sum_view(w) != prod_view(w))
    announcements.append(lambda w, pool: knows(w, pool, prod_view))  # B: now I do

    for speaks in announcements:
        pool = list(live)
        live = [w for w in live if speaks(w, pool)]
        if not live:
            return None
    if len(live) != 1:
        return None
    a, b = live[0]
    return a * a + b * b
