"""ข้อ 5 — จำนวนเต็มบวกที่น้อยที่สุด

จงหาจำนวนเต็มบวก a ที่น้อยที่สุดซึ่งเมื่อเขียน a ในระบบฐานสิบและตัดหลักแรก
(จากซ้ายมือสุด) ออกแล้วจะได้จำนวนเต็มบวก b โดยที่ a มีค่าเท่ากับ 29 เท่าของ b

Write a with d+1 digits and leading digit t, so a = t·10^d + b with b < 10^d.
Then a = 29b collapses to t·10^d = 28b, i.e. b = t·10^d/28.

28 = 4·7, and 10^d contributes no factor of 7, so 7 must divide t — and t is a
single digit, so t = 7 with no choice at all. That leaves b = 10^d/4, needing
d ≥ 2. The smallest is d = 2: b = 25, a = 725.

The leading digit being forced is the whole question; ``check`` finds the same
number by counting upwards, which knows none of that.
"""

from __future__ import annotations

PARAMS = {"multiplier": 29}
ANSWER = 725
VARIANTS = [
    {"multiplier": 13},
    {"multiplier": 21},
    {"multiplier": 41},
    {"multiplier": 26},
    {"multiplier": 51},
]


def solve(multiplier=29):
    """Smallest a whose leading digit removed leaves b with a = multiplier·b.

    a = t·10^d + b and a = m·b give t·10^d = (m-1)·b, so b = t·10^d/(m-1). Walk
    d upwards and take the smallest leading digit that makes b a whole number
    short enough to be the tail.
    """
    if multiplier < 2:
        return None
    for d in range(1, 12):
        best = None
        for t in range(1, 10):
            num = t * 10 ** d
            if num % (multiplier - 1):
                continue
            b = num // (multiplier - 1)
            if 0 < b < 10 ** d:
                a = num + b
                best = a if best is None else min(best, a)
        if best is not None:
            return best
    return None


def check(multiplier=29, limit=10 ** 7):
    """Independent: count upwards and test the definition on the digit string."""
    for a in range(10, limit):
        b = int(str(a)[1:])               # int() reads "025" as 25, as intended
        if b > 0 and a == multiplier * b:
            return a
    return None
