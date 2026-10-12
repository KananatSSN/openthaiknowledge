"""ข้อ 11 — ค่า x² + y² จากสมการไดโอแฟนไทน์

ให้ x และ y เป็นจำนวนเต็มที่สอดคล้องสมการ y² + 2x²y² = 96x² + 864 จงหา x² + y²

Group the y's and give the coefficient a name: with ``d = a·x² + 1`` the equation
``y²(1 + a x²) = b x² + c`` becomes, after multiplying by a and replacing
``a x² = d − 1``,

    d · (a y² − b) = a c − b

so **d divides ac − b** — a finite list. Here a = 2, b = 96, c = 864, so
ac − b = 1632 = 2⁵·3·17 and d must additionally be odd (``d ≡ 1 mod a``) with
``(d − 1)/a`` a perfect square. That leaves d ∈ {1, 3, 17, 51}:

    d =  1 → x² =  0, y² = (96 + 1632)/2 = 864   not a square
    d =  3 → x² =  1, y² = (96 +  544)/2 = 320   not a square
    d = 17 → x² =  8                             not a square
    d = 51 → x² = 25, y² = (96 +   32)/2 =  64   ✓  y = ±8

One survivor, so x² + y² = 25 + 64 = **89**.

``solve`` walks the divisors of ac − b. ``check`` never factorises anything: it
sweeps a grid of (x, y) and tests the printed equation as printed. The bound on
the sweep is the only thing it borrows — ``d ≤ |ac − b|`` — and even that only
because an unbounded loop cannot terminate.
"""

from __future__ import annotations

from math import isqrt

#: y² + a·x²·y² = b·x² + c over the integers.
PARAMS = {"a": 2, "b": 96, "c": 864}
ANSWER = 89
VARIANTS = [
    {"a": 1, "b": 48, "c": 834},
    {"a": 3, "b": 32, "c": 160},
    {"a": 4, "b": 72, "c": 108},
    {"a": 2, "b": 104, "c": 280},
    {"a": 3, "b": 72, "c": 700},
    {"a": 2, "b": 96, "c": 300},        # no integer point at all
    {"a": 1, "b": 22, "c": 324},        # x = 0 is the only survivor
]


def _square_root(value: int) -> int | None:
    if value < 0:
        return None
    root = isqrt(value)
    return root if root * root == value else None


def solve(a=2, b=96, c=864):
    """The one value of x² + y², from the divisors of ac − b."""
    if a < 1:
        return None
    key = a * c - b
    if key == 0:
        # y² = b/a for every x — infinitely many points, no single answer.
        return None

    found = set()
    magnitude = abs(key)
    for d in range(1, magnitude + 1):
        if magnitude % d or (d - 1) % a:
            continue
        x_square = _square_root((d - 1) // a)
        if x_square is None:
            continue
        numerator = b + key // d
        if numerator < 0 or numerator % a:
            continue
        y_square = _square_root(numerator // a)
        if y_square is None:
            continue
        found.add((d - 1) // a + numerator // a)
    if len(found) != 1:
        return None
    return found.pop()


def check(a=2, b=96, c=864):
    """Independent: test the printed equation over a grid of (x, y).

    No divisor argument and no rearrangement — ``y*y + a*x*x*y*y`` is formed and
    compared with ``b*x*x + c`` directly. Only the extent of the grid comes from
    the algebra, because a sweep has to stop somewhere.
    """
    if a < 1:
        return None
    key = a * c - b
    if key == 0:
        return None
    x_max = isqrt(max(abs(key), 1) // a) + 2
    y_max = isqrt(abs(b) // a + abs(c)) + 2
    if (x_max + 1) * (y_max + 1) > 4 * 10 ** 6:
        return None

    found = set()
    for x in range(x_max + 1):
        for y in range(y_max + 1):
            if y * y + a * x * x * y * y == b * x * x + c:
                found.add(x * x + y * y)
    if len(found) != 1:
        return None
    return found.pop()
