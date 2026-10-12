"""ข้อ 4 — ค่ามากที่สุดของ |x + y| จากสมการไดโอแฟนไทน์

ให้ x และ y เป็นจำนวนเต็มซึ่งสอดคล้องกับสมการ 1 + 68x + 66y = xy
จงหาค่ามากที่สุดที่เป็นไปได้ของ |x + y|

Simon's trick: collect the product and both linear terms into one factorisation.

    xy − 68x − 66y = 1   ⟹   (x − 66)(y − 68) = 1 + 66·68 = 4489 = 67²

so x − 66 runs over the divisors of 67², positive and negative, and

    x + y = 134 + d + 4489/d

The extremes come from the extreme divisors: d = 1 (or 4489) gives
134 + 4490 = 4624, and d = −1 (or −4489) gives 134 − 4490 = −4356. The middle
divisor d = ±67 gives 268 and 0.

    max |x + y| = **4624**

Note that 4489 = 67² is not an accident of the constants — ``1 + 66·68 =
1 + (67−1)(67+1) = 67²`` — which is why the divisor list is only three long.

``solve`` walks the divisors. ``check`` never factorises: it sweeps x, solves the
printed equation for y as a rational, and keeps the integer hits.
"""

from __future__ import annotations

#: 1 + a·x + b·y = xy over the integers.
PARAMS = {"a": 68, "b": 66, "c": 1}
ANSWER = 4624
VARIANTS = [
    {"a": 5, "b": 3, "c": 1},
    {"a": 10, "b": 10, "c": 0},
    {"a": 12, "b": 7, "c": 4},
    {"a": 68, "b": 66, "c": 2},
    {"a": 2, "b": 2, "c": 1},
    {"a": 30, "b": 20, "c": -5},
]


def solve(a=68, b=66, c=1):
    """(x − b)(y − a) = c + ab, so walk that number's divisors."""
    key = c + a * b
    if key == 0:
        return None                        # a whole line of solutions
    best = None
    magnitude = abs(key)
    if magnitude > 10 ** 12:
        return None
    d = 1
    divisors = []
    while d * d <= magnitude:
        if magnitude % d == 0:
            divisors += [d, magnitude // d]
        d += 1
    for d in set(divisors):
        for signed in (d, -d):
            x = b + signed
            y = a + key // signed
            total = abs(x + y)
            if best is None or total > best:
                best = total
    return best


def check(a=68, b=66, c=1):
    """Independent: sweep x and solve the printed equation for y.

    ``1 + ax + by = xy`` rearranges to ``y(x − b) = 1 + ax − 1 + …`` only after
    the same trick, so this does it the blunt way: for each integer x the
    equation is linear in y, and y is kept when the division comes out exact.
    """
    key = c + a * b
    if key == 0:
        return None
    best = None
    span = abs(key) + abs(a) + abs(b) + 2
    if span > 4 * 10 ** 6:
        return None
    for x in range(b - span, b + span + 1):
        denominator = x - b
        if denominator == 0:
            continue
        numerator = c + a * x
        if numerator % denominator:
            continue
        y = numerator // denominator
        if c + a * x + b * y != x * y:
            continue
        total = abs(x + y)
        if best is None or total > best:
            best = total
    return best
