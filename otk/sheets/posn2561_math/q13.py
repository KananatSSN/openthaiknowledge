"""ข้อ 13 — รากที่สามของ 3⁷(9 − 5⁵) + 5¹⁰(81 − 5⁵)

จงหารากที่ 3 ของ 3⁷(9 − 5⁵) + 5¹⁰(81 − 5⁵)

Expanded, the printed expression is

    3⁹ − 3⁷·5⁵ + 3⁴·5¹⁰ − 5¹⁵

and with u = 3³ = 27 and v = 5⁵ = 3125 those four terms are exactly

    u³ − 3u²v + 3uv² − v³ = (u − v)³

because 3u² = 3·3⁶ = 3⁷ and 3u = 81. So the cube root is

    27 − 3125 = **−3098**

and no 15-digit number ever has to be formed. The disguise is that the printed
grouping ``3⁷(9 − 5⁵) + 5¹⁰(81 − 5⁵)`` splits the binomial across the *wrong*
pairs of terms: 3⁷·9 belongs with 3⁷·5⁵, and 5¹⁰·81 with 5¹⁰·5⁵.

``solve`` returns ``a^m − b^k``. ``check`` refuses the identity: it builds the
four-term integer outright and extracts an exact integer cube root by bisection,
so a wrong exponent anywhere shows up as a number with no cube root at all.
"""

from __future__ import annotations

#: the expression is u³ − 3u²v + 3uv² − v³ with u = a^m and v = b^k.
PARAMS = {"a": 3, "m": 3, "b": 5, "k": 5}
ANSWER = -3098
VARIANTS = [
    {"a": 2, "m": 4, "b": 3, "k": 3},
    {"a": 5, "m": 2, "b": 2, "k": 5},
    {"a": 7, "m": 3, "b": 7, "k": 3},      # u = v: the cube root is 0
    {"a": 10, "m": 4, "b": 3, "k": 7},
    {"a": 2, "m": 10, "b": 5, "k": 4},
    {"a": 3, "m": 1, "b": 2, "k": 1},
]


def solve(a=3, m=3, b=5, k=5):
    """The binomial collapses: the cube root is u − v."""
    if m < 0 or k < 0:
        return None
    return a ** m - b ** k


def check(a=3, m=3, b=5, k=5):
    """Independent: form the four-term integer and take its cube root exactly.

    Nothing here knows the expression is a cube. The bisection is on |value|,
    and the result is cubed again and compared with the value before it is
    returned — if the four terms were ever anything but ``(u − v)³`` this
    returns None instead of a plausible-looking number.
    """
    if m < 0 or k < 0:
        return None
    u, v = a ** m, b ** k
    value = u ** 3 - 3 * u * u * v + 3 * u * v * v - v ** 3
    if value == 0:
        return 0

    sign = 1 if value > 0 else -1
    magnitude = abs(value)
    lo, hi = 0, 1
    while hi ** 3 < magnitude:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** 3 < magnitude:
            lo = mid + 1
        else:
            hi = mid
    if lo ** 3 != magnitude:
        return None
    return sign * lo
