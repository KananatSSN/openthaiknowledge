"""ข้อ 5 — ผลบวกเลขโดดของ (99…9)³

ให้ S(m) แทนผลบวกของเลขโดดของ m ในระบบฐานสิบ  ถ้า N = 99…9 มี n หลัก
และ S(N³) = target (โจทย์: target = 486) แล้ว n เท่ากับเท่าใด

Method: N = 10ⁿ − 1, so
    N³ = 10³ⁿ − 3·10²ⁿ + 3·10ⁿ − 1
which, written out, is  (n−1) nines, an 8, (n−1) zeros, a 9, (n−1) nines, a 1 —
digit sum 9(n−1) + 8 + 9 + 9(n−1) + 1 = 18n. So n = target/18, and the question
has an answer exactly when 18 divides the target.

``check`` computes N³ as a Python int and adds up its digits. Python's bignums
make that exact at any n worth asking about, so the two methods are genuinely
independent — one is a claimed pattern, the other is the thing itself.
"""

from __future__ import annotations

PARAMS = {"target": 486, "digit": 9, "base": 10, "power": 3}
ANSWER = 27
VARIANTS = [
    {"target": 18},
    {"target": 900},
    {"target": 487},        # not a multiple of 18 → no such n
    {"target": 54},
    {"target": 180},
    {"target": 28, "digit": 7, "base": 8},
]


def digit_sum(m: int, base: int = 10) -> int:
    total = 0
    while m:
        m, r = divmod(m, base)
        total += r
    return total


def solve(target=486, digit=9, base=10, power=3):
    """n such that S(N^power) == target, for N made of n copies of ``digit``.

    Closed form only for the sheet's own case (all-nines cubed in base ten,
    where the digit sum is exactly 18n); anything else falls through to a
    search, so the tunables stay honest instead of silently returning nonsense.
    """
    if digit == base - 1 and power == 3:
        n, rem = divmod(target, 2 * (base - 1))     # 18n when base is ten
        return n if rem == 0 and n >= 1 else None
    return _search(target, digit, base, power)


def _search(target, digit, base, power, n_max=200):
    for n in range(1, n_max + 1):
        if digit_sum(_repdigit(n, digit, base) ** power, base) == target:
            return n
    return None


def _repdigit(n: int, digit: int, base: int) -> int:
    """The n-digit number whose every digit is ``digit``."""
    return digit * (base ** n - 1) // (base - 1)


def check(target=486, digit=9, base=10, power=3, n_max=200):
    """Independent: raise the actual repdigit and add up the actual digits."""
    return _search(target, digit, base, power, n_max)
