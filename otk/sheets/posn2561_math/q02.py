"""ข้อ 2 — เลขหลักหน่วยของ 7^m

7^m มีเลขหลักหน่วยเป็นเลขใด เมื่อ m คือจำนวนหลักของ 25²⁵ × 8²⁰

The inner number is a power of ten in disguise:

    25²⁵ · 8²⁰ = 5⁵⁰ · 2⁶⁰ = 2¹⁰ · (2⁵⁰ · 5⁵⁰) = 1024 · 10⁵⁰

so it is 1024 followed by fifty zeros — 4 + 50 = **54 digits**, and m = 54.

Then only the last digit of 7⁵⁴ is wanted, and those cycle with period four:

    7, 9, 3, 1, 7, 9, 3, 1, …

54 ≡ 2 (mod 4), so the answer is the second entry: **9**.

Both halves are traps in their own way — counting the digits of 25²⁵·8²⁰ by
multiplying it out is unnecessary once the 2s and 5s are paired off, and reading
the cycle position as 54 mod 4 = 2 has to mean *the second* member, not the
zeroth.

``solve`` counts the digits with logarithms and reduces the exponent modulo the
observed cycle length. ``check`` does neither: it builds the integer, takes
``len(str(...))``, and hands the power to three-argument ``pow``. The logarithm
is the risky route, which is exactly why it is the one being checked.
"""

from __future__ import annotations

from math import log10

#: the inner number is a^p · b^q; the outer base is ``base``.
PARAMS = {"a": 25, "p": 25, "b": 8, "q": 20, "base": 7}
ANSWER = 9
VARIANTS = [
    {"a": 25, "p": 25, "b": 8, "q": 20, "base": 3},
    {"a": 4, "p": 10, "b": 5, "q": 12, "base": 7},
    {"a": 2, "p": 100, "b": 5, "q": 100, "base": 9},
    {"a": 25, "p": 6, "b": 8, "q": 5, "base": 2},
    {"a": 6, "p": 30, "b": 7, "q": 11, "base": 7},
    {"a": 1, "p": 5, "b": 1, "q": 5, "base": 7},        # the number is 1
]


def digits(a=25, p=25, b=8, q=20):
    """How many decimal digits a^p · b^q has, from logarithms."""
    if a < 1 or b < 1 or p < 0 or q < 0:
        return None
    if a == 1 and b == 1:
        return 1
    return int(p * log10(a) + q * log10(b)) + 1


def solve(a=25, p=25, b=8, q=20, base=7):
    """Units digit of base^m with m the digit count, via the last-digit cycle."""
    m = digits(a, p, q=q, b=b)
    if m is None or base < 0:
        return None
    seen, value, cycle = {}, 1 % 10, []
    while value not in seen:
        seen[value] = len(cycle)
        cycle.append(value)
        value = value * base % 10
    offset = seen[value]
    period = len(cycle) - offset
    index = m if m < offset else offset + (m - offset) % period
    return cycle[index]


def check(a=25, p=25, b=8, q=20, base=7):
    """Independent: build the number, count its digits, and use modular pow.

    ``a**p * b**q`` is formed as an exact integer and its digits counted by
    ``len(str(...))`` — no logarithm, so a floating-point boundary error cannot
    be shared — and the last digit comes from ``pow(base, m, 10)``, which knows
    nothing about cycles.
    """
    if a < 1 or b < 1 or p < 0 or q < 0 or base < 0:
        return None
    if p * log10(max(a, 2)) + q * log10(max(b, 2)) > 4000:
        return None                     # keep the exact integer manageable
    number = a ** p * b ** q
    m = len(str(number))
    return pow(base, m, 10)
