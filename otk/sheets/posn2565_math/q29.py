"""ข้อ 29 — พหุนามของเกาส์จากบทสนทนา

นักคณิตศาสตร์สองท่านสนทนากันดังนี้
    เกาส์   : ผมมีพหุนามอยู่พหุนามหนึ่งที่มีสัมประสิทธิ์เป็น**เลขโดด** (ตั้งแต่ 0 ถึง 9)
    ออยเลอร์ : ผลรวมของสัมประสิทธิ์ทั้งหมดในพหุนามนี้มีค่าเท่าใด
    เกาส์   : 3
    ออยเลอร์ : ถ้านำ 3 ไปแทนค่าในพหุนามนี้ล่ะ จะได้เท่าใด
    เกาส์   : 33
    ออยเลอร์ : ผมรู้แล้วล่ะว่าคุณมีพหุนามใด
เกาส์มีพหุนามใดตามบทสนทนานี้

The sum of the coefficients is ``P(1)``, so the two answers are ``P(1) = 3`` and
``P(3) = 33``. Coefficients are digits, hence non-negative, so ``P(1) = 3`` says
the coefficients are three 1s, or a 1 and a 2, or a single 3 — spread over
distinct powers. Testing the three shapes against ``P(3) = 33``:

* ``3·3^i = 33`` needs ``3^i = 11``: no;
* ``2·3^i + 3^j = 33``: i = 1 gives ``3^j = 27``, so **j = 3** ✓ (i = 0, 2 fail);
* ``3^i + 3^j + 3^k`` over distinct powers never reaches 33 (31, 37, 39, 13…).

So the polynomial is unique — which is exactly why Euler can say he knows it —

    **P(x) = x³ + 2x**,  coefficients (1, 0, 2, 0).

Because ``P(1) = 3`` is smaller than the base 3, the answer is really just 33
written in base 3 (1020₃); the digit bound of 9 is a red herring the small
coefficient sum defuses. That stops being true once ``P(1) ≥ b``, and there
``solve`` returns None unless one candidate survives anyway.

``solve`` walks the powers from the top down, pruning on the sum still owed;
``check`` works from the other end, peeling off the lowest coefficient by its
residue mod b. The two searches meet in the middle from opposite directions.
"""

from __future__ import annotations

#: P(1) = total, P(base) = value, coefficients in 0..max_digit.
PARAMS = {"total": 3, "value": 33, "base": 3, "max_digit": 9}
ANSWER = (1, 0, 2, 0)
VARIANTS = [
    {"total": 4, "value": 34, "base": 3, "max_digit": 9},
    {"total": 5, "value": 41, "base": 4, "max_digit": 9},
    {"total": 3, "value": 33, "base": 3, "max_digit": 2},   # tighter bound, same
    {"total": 6, "value": 134, "base": 5, "max_digit": 9},
    {"total": 2, "value": 82, "base": 3, "max_digit": 9},
    {"total": 12, "value": 33, "base": 3, "max_digit": 9},  # sum ≥ base: ambiguous
    {"total": 3, "value": 34, "base": 3, "max_digit": 9},   # no polynomial at all
]


def candidates(total=3, value=33, base=3, max_digit=9):
    """Every digit-coefficient polynomial with P(1) = total and P(base) = value."""
    if base < 2 or total < 0 or value < 0 or max_digit < 1:
        return None
    top = 0
    while base ** (top + 1) <= max(value, 1):
        top += 1

    found: list[tuple[int, ...]] = []

    def walk(rest_value: int, rest_total: int, power: int, acc: list[int]) -> None:
        if power < 0:
            if rest_value == 0 and rest_total == 0:
                found.append(tuple(acc))
            return
        weight = base ** power
        for coef in range(min(max_digit, rest_total, rest_value // weight) + 1):
            walk(rest_value - coef * weight, rest_total - coef, power - 1,
                 acc + [coef])

    walk(value, total, top, [])
    return found


def solve(total=3, value=33, base=3, max_digit=9):
    """The coefficients, highest power first — only when they are unique."""
    found = candidates(total, value, base, max_digit)
    if found is None:
        return None
    trimmed = set()
    for one in found:                                 # drop leading zeros first:
        while len(one) > 1 and one[0] == 0:           # x³+2x and 0x⁴+x³+2x are
            one = one[1:]                             # the same polynomial
        trimmed.add(one)
    if len(trimmed) != 1:
        return None
    return next(iter(trimmed))


def check(total=3, value=33, base=3, max_digit=9):
    """Independent: build the coefficients from the bottom up, by residues.

    The constant term must be congruent to the value modulo the base, which
    leaves at most a handful of choices; each is subtracted, the rest divided by
    the base, and the same question asked one power up. No pruning by the highest
    power and no descent — and every polynomial that comes out is evaluated at 1
    and at the base before it counts.
    """
    if base < 2 or total < 0 or value < 0 or max_digit < 1:
        return None

    found: set[tuple[int, ...]] = set()

    def peel(rest_value: int, rest_total: int, acc: list[int]) -> None:
        if rest_value == 0:
            if rest_total == 0:
                found.add(tuple(reversed(acc)) if acc else (0,))
            return
        if rest_total <= 0 or len(acc) > 64:
            return
        low = rest_value % base
        coef = low
        while coef <= min(max_digit, rest_total):
            peel((rest_value - coef) // base, rest_total - coef, acc + [coef])
            coef += base

    peel(value, total, [])
    verified = {c for c in found
                if sum(c) == total
                and sum(d * base ** i for i, d in enumerate(reversed(c))) == value}
    if len(verified) != 1:
        return None
    only = next(iter(verified))
    while len(only) > 1 and only[0] == 0:            # drop leading zeros
        only = only[1:]
    return only
