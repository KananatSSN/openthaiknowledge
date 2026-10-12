"""ข้อ 1 — ครูให้การบ้านกี่ข้อ

คุณครูคณิตศาสตร์ถามนักเรียนชาย 5 คนว่า "คาบที่แล้ว ครูให้การบ้านไว้กี่ข้อคะ"
    นาย ก: "ครูให้การบ้าน 8 ข้อครับ"
    นาย ข: "เยอะไปครับครู ครูให้การบ้านไม่ถึง 5 ข้อครับ"
    นาย ค: "ครูให้การบ้าน 8 ข้อ หรือ 9 ข้อนี่แหละครับ"
    นาย ง: "นาย ค จำผิดแล้วแหละ ครูให้การบ้านไม่เกิน 7 ข้อครับ"
    นาย จ: "ครูครับ ผมจำได้ว่าครูให้การบ้านมากกว่า 6 ข้อครับ"
เมื่อถามอีกครั้งหนึ่ง
    นาย ก: "นาย ข และ นาย ง พูดโกหกครับ"      นาย ข: "นาย จ พูดโกหกครับ"
    นาย ค: "นาย ก และ นาย ง พูดจริงครับ"       นาย ง: "นาย ข พูดโกหกครับ"
    นาย จ: "นาย ค พูดโกหกครับ"
หากนักเรียนแต่ละคนพูดจริงเท่านั้นหรือพูดโกหกเท่านั้น ครูให้การบ้านกี่ข้อ

The second round settles who is who, without any reference to the number. Write
Tₓ for "x is truthful"; each statement is true exactly when its speaker is:

    ก: ¬Tข ∧ ¬Tง = Tก      ข: ¬Tจ = Tข       ค: Tก ∧ Tง = Tค
    ง: ¬Tข = Tง            จ: ¬Tค = Tจ

From ง, ``Tง = ¬Tข``. Substituting into ก's equation, ``Tก = ¬Tข ∧ ¬Tง =
¬Tข ∧ Tข`` — **false whatever ข is**, so ก lies. Then ``Tค = Tก ∧ Tง`` is false
too, and since จ's equation gives ``Tค = Tข``, ข lies as well; ง and จ are
therefore both truthful.

    ก ✗   ข ✗   ค ✗   ง ✓   จ ✓

Now read round one with those labels: N ≠ 8 (ก lies), N ≥ 5 (ข lies), N ∉ {8, 9}
(ค lies), N ≤ 7 (ง true), N > 6 (จ true) — so **N = 7**.

``solve`` follows that order: it sifts the 32 truth assignments through round two
first, then applies round one. ``check`` goes the other way, and never enumerates
truth assignments at all: for each candidate N it *reads off* each boy's
truthfulness from whether his round-one claim holds, then tests round two
against those labels.
"""

from __future__ import annotations

from itertools import product

#: round-one claims as (operator, value), and round-two accusations as
#: (speaker index → tuple of (target index, "is truthful?")).
PARAMS = {
    "claims": (("eq", 8), ("lt", 5), ("in", (8, 9)), ("le", 7), ("gt", 6)),
    "accusations": (((1, False), (3, False)), ((4, False),),
                    ((0, True), (3, True)), ((1, False),), ((2, False),)),
    "limit": 20,
}
ANSWER = 7
VARIANTS = [
    {"claims": (("eq", 5), ("lt", 10), ("in", (5, 6)), ("le", 12), ("gt", 11)),
     "accusations": (((1, False), (3, False)), ((4, False),),
                     ((0, True), (3, True)), ((1, False),), ((2, False),)),
     "limit": 20},
    {"claims": (("eq", 2), ("lt", 3), ("in", (2, 9)), ("le", 4), ("gt", 3)),
     "accusations": (((1, False), (3, False)), ((4, False),),
                     ((0, True), (3, True)), ((1, False),), ((2, False),)),
     "limit": 12},
    {"claims": (("gt", 7), ("lt", 4), ("in", (1, 2)), ("le", 6), ("gt", 5)),
     "accusations": (((1, False), (3, False)), ((4, False),),
                     ((0, True), (3, True)), ((1, False),), ((2, False),)),
     "limit": 15},
    {"claims": (("eq", 20), ("lt", 14), ("in", (19, 20)), ("le", 17),
                ("gt", 16)),
     "accusations": (((1, False), (3, False)), ((4, False),),
                     ((0, True), (3, True)), ((1, False),), ((2, False),)),
     "limit": 25},
    {"claims": (("eq", 8), ("lt", 5), ("in", (8, 9)), ("le", 7), ("gt", 6)),
     "accusations": (((1, True), (3, True)), ((4, True),),
                     ((0, True), (3, True)), ((1, True),), ((2, True),)),
     "limit": 20},              # everyone confirms everyone: nothing is pinned
    {"claims": (("eq", 8), ("lt", 5), ("in", (8, 9)), ("le", 7), ("gt", 9)),
     "accusations": (((1, False), (3, False)), ((4, False),),
                     ((0, True), (3, True)), ((1, False),), ((2, False),)),
     "limit": 20},              # ง and จ now contradict: no number fits
]


def _holds(claim, number: int) -> bool:
    """Whether a round-one claim is true of ``number``."""
    op, value = claim
    if op == "eq":
        return number == value
    if op == "lt":
        return number < value
    if op == "le":
        return number <= value
    if op == "gt":
        return number > value
    if op == "ge":
        return number >= value
    return number in value


def solve(claims=PARAMS["claims"], accusations=PARAMS["accusations"], limit=20):
    """Round two first: sift the truth assignments, then apply round one."""
    if len(claims) != len(accusations):
        return None
    size = len(claims)
    consistent = []
    for labels in product((True, False), repeat=size):
        ok = True
        for speaker, targets in enumerate(accusations):
            said = all(labels[who] == truthful for who, truthful in targets)
            if said != labels[speaker]:
                ok = False
                break
        if ok:
            consistent.append(labels)

    hits = set()
    for labels in consistent:
        for number in range(limit + 1):
            if all(_holds(claim, number) == label
                   for claim, label in zip(claims, labels)):
                hits.add(number)
    if len(hits) != 1:
        return None
    return next(iter(hits))


def check(claims=PARAMS["claims"], accusations=PARAMS["accusations"], limit=20):
    """Independent: fix the number first and read the labels off round one.

    For each candidate number every boy's truthfulness is *determined* by whether
    his first claim holds — no assignment is guessed — and the round-two
    accusations are then tested against those labels. The 32 combinations are
    never enumerated, so a mistake in sifting them could not be shared.
    """
    if len(claims) != len(accusations):
        return None
    hits = set()
    for number in range(limit + 1):
        labels = tuple(_holds(claim, number) for claim in claims)
        ok = True
        for speaker, targets in enumerate(accusations):
            said = all(labels[who] == truthful for who, truthful in targets)
            if said != labels[speaker]:
                ok = False
                break
        if ok:
            hits.add(number)
    if len(hits) != 1:
        return None
    return next(iter(hits))
