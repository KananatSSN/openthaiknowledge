"""ข้อ 4 — ผลบวกของอายุลูกสาวทั้งสามคน

ครอบครัวหนึ่ง มีสมาชิกทั้งหมด 5 คน ประกอบด้วย พ่อ แม่ และลูกสาว 3 คน โดยที่
ลูกสาว 2 คนโตเป็นฝาแฝดกัน ถ้าผลคูณของอายุของลูกสาวทั้งสามคนเท่ากับ 48 แล้วผลบวก
ของอายุของลูกสาวทั้งสามคนมีค่าเท่าใด (อายุคิดเป็นจำนวนเต็มปี)

The twins are the **older** two, so their common age t is strictly greater than
the youngest child's age y, and ``t²·y = 48``:

    t = 1 → y = 48 ✗    t = 2 → y = 12 ✗    t = 3 → 9 ∤ 48 ✗    t = 4 → y = 3 ✓

Only ``t = 4, y = 3`` survives, and the sum is **4 + 4 + 3 = 11**.

Both halves of the wording earn their keep. "2 คนโต" makes the twins the larger
age; drop it and (2, 2, 12) fits equally well and gives 16 instead. The
five-member family and the parents are scenery.

``solve`` walks the square divisors; ``check`` enumerates every non-decreasing
triple with the given product and applies the twin and ordering conditions as
written, reporting nothing unless exactly one sum survives.
"""

from __future__ import annotations

#: product of the three ages; the twins are the two oldest.
PARAMS = {"product": 48}
ANSWER = 11
VARIANTS = [
    {"product": 36},
    {"product": 72},
    {"product": 12},
    {"product": 100},
    {"product": 30},          # no square factor fits: nothing works
    {"product": 1},           # all three would be 1, so the twins are not older
]


def solve(product=48):
    """2t + y where t²·y = product and y < t — only when that is unique."""
    if product <= 0:
        return None
    hits = set()
    t = 1
    while t * t <= product:
        if product % (t * t) == 0:
            y = product // (t * t)
            if 1 <= y < t:
                hits.add(2 * t + y)
        t += 1
    if len(hits) != 1:
        return None
    return next(iter(hits))


def check(product=48):
    """Independent: enumerate age triples and test the story's words on each.

    Every triple a ≤ b ≤ c with a·b·c = product is generated, then kept only when
    the two *older* ages are equal and the youngest is strictly smaller — the
    twin condition read off the sentence rather than encoded as t²y.
    """
    if product <= 0:
        return None
    sums = set()
    for a in range(1, product + 1):
        if product % a:
            continue
        rest = product // a
        for b in range(a, rest + 1):
            if rest % b:
                continue
            c = rest // b
            if c < b:
                continue
            if b == c and a < b:          # the two older ones are the twins
                sums.add(a + b + c)
    if len(sums) != 1:
        return None
    return next(iter(sums))
