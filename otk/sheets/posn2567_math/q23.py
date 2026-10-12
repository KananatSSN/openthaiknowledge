"""ข้อ 23 — ความน่าจะเป็นที่ผลคูณหารด้วย 10 ลงตัว

กล่องใบหนึ่งบรรจุบัตรตัวเลข 9 ใบ หมายเลข 1 ถึง 9  สุ่มหยิบบัตร 3 ใบ ทีละใบแบบใส่คืน
จงหาความน่าจะเป็นที่ผลคูณของหมายเลขบนบัตรทั้งสามเป็นจำนวนที่หารด้วย 10 ลงตัว
(เขียนคำตอบเป็นเศษส่วนอย่างต่ำ)

Divisible by 10 means the draw contains at least one multiple of 5 **and** at
least one even number, so inclusion–exclusion on the two failures:

    favourable = n^k - (n - F)^k - (n - E)^k + (n - F - E + T)^k

where F counts the multiples of 5 in 1..n, E the evens, and T the multiples of 10
(added back because the last term counts values that are neither). For n = 9,
k = 3 that is 729 - 512 - 125 + 64 = 156, and

    156/729 = **52/243**.

``check`` enumerates all n^k draws and tests each product, so it needs no
inclusion–exclusion at all — the variants stay small enough for that to run.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

#: cards 1..top, drawn `draws` times with replacement.
PARAMS = {"top": 9, "draws": 3}
ANSWER = Fraction(52, 243)
VARIANTS = [
    {"top": 9, "draws": 2},
    {"top": 10, "draws": 3},           # a multiple of 10 is now in the box
    {"top": 20, "draws": 2},
    {"top": 12, "draws": 4},
    {"top": 4, "draws": 3},            # no multiple of 5: impossible
    {"top": 9, "draws": 0},            # degenerate
]


def solve(top=9, draws=3):
    """P(product divisible by 10), by inclusion–exclusion on the two conditions."""
    if top < 1 or draws < 1:
        return None
    fives = top // 5
    evens = top // 2
    tens = top // 10
    neither = top - fives - evens + tens
    good = (top ** draws - (top - fives) ** draws
            - (top - evens) ** draws + neither ** draws)
    return Fraction(good, top ** draws)


def check(top=9, draws=3):
    """Independent: enumerate every draw and divide the products that end in 0."""
    if top < 1 or draws < 1:
        return None
    if top ** draws > 2 * 10 ** 6:                # keep the enumeration honest
        return None
    good = 0
    for combo in itertools.product(range(1, top + 1), repeat=draws):
        product = 1
        for v in combo:
            product *= v
        good += product % 10 == 0
    return Fraction(good, top ** draws)
