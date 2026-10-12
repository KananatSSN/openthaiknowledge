"""ข้อ 14 — ผลบวกของผลคูณเลขโดดที่ไม่เป็นศูนย์

สำหรับจำนวนนับ n ใด ๆ นิยามฟังก์ชัน p(n) เป็นผลคูณของเลขโดดที่ไม่เป็นศูนย์ของ n
ในระบบฐานสิบ (ตัวอย่างเช่น p(1023) = 1·2·3 = 6) จงหาค่าของ Σ p(n) เมื่อ n = 1 ถึง 99

A zero digit contributes a factor of 1, which is exactly what a zero *pad*
contributes — so pad every number to the same width and nothing changes. Over
all d-digit strings the product then factorises, one digit at a time:

    Σ p = (1 + 1 + 2 + ⋯ + 9)^d = 46^d

(the leading 1 is the zero digit's factor). That counts n = 0 as well, whose
padded string is all zeros and whose product is the empty product 1, so

    Σ_{n=1}^{10^d − 1} p(n) = 46^d − 1

and for d = 2 the sum is 46² − 1 = **2115**.

``solve`` runs the same factorisation digit by digit against an arbitrary limit
(a digit walk: for each position, every smaller digit frees the tail to 46^rest).
``check`` multiplies out the digits of every n from 1 to the limit.
"""

from __future__ import annotations

#: Σ p(n) for n = 1 … limit.
PARAMS = {"limit": 99}
ANSWER = 2115
VARIANTS = [
    {"limit": 9},
    {"limit": 100},
    {"limit": 999},
    {"limit": 1023},
    {"limit": 250},
    {"limit": 1},
]

#: 0 contributes a factor 1, and 1…9 contribute themselves.
_DIGIT_WEIGHT = 1 + sum(range(1, 10))


def solve(limit=99):
    """A digit walk over the limit: every smaller digit frees the whole tail."""
    if limit < 1:
        return None
    digits = [int(ch) for ch in str(limit)]
    total = 0
    prefix = 1                     # product of the nonzero digits fixed so far
    for i, digit in enumerate(digits):
        tail = _DIGIT_WEIGHT ** (len(digits) - i - 1)
        for smaller in range(digit):
            total += prefix * (smaller or 1) * tail
        prefix *= digit or 1
    total += prefix                # the limit itself
    return total - 1               # drop n = 0, whose padded product is 1


def check(limit=99):
    """Independent: multiply out the digits of every n up to the limit."""
    if limit < 1:
        return None
    if limit > 2 * 10 ** 6:
        return None
    total = 0
    for n in range(1, limit + 1):
        product = 1
        for ch in str(n):
            if ch != "0":
                product *= int(ch)
        total += product
    return total
