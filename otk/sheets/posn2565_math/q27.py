"""ข้อ 27 — เศษจากการหาร ⌊a⌋ ด้วย 1000

สำหรับจำนวนจริง a ใด ๆ กำหนดให้ ⌊a⌋ คือจำนวนเต็มมากที่สุดที่น้อยกว่าหรือเท่ากับ a
ถ้า a = 1000¹⁰/(10¹⁰ + 11) แล้วเศษจากการหาร ⌊a⌋ ด้วย 1000 มีค่าเท่ากับเท่าใด

Write x = 10¹⁰, so ``1000¹⁰ = 10³⁰ = x³`` and the fraction is ``x³/(x + 11)``.
Dividing out,

    x³/(x + c) = x² − cx + c² − c³/(x + c),   c = 11

and ``c³ = 1331`` is far smaller than ``x + c = 10¹⁰ + 11``, so the last term is
strictly between 0 and 1 and

    ⌊a⌋ = x² − cx + c² − 1.

Modulo 1000 the first two terms vanish (x = 10¹⁰ is a multiple of 1000), leaving

    ⌊a⌋ mod 1000 = c² − 1 = **120**.

The trap is reading the leading ``1000¹⁰`` as ``10¹⁰`` — the numerator is x³, not
x, and the cube is what produces the ``c² − 1``.

``solve`` uses that closed form; ``check`` builds the two integers and lets
Python's big integers do the floor division and the remainder, touching none of
the algebra.
"""

from __future__ import annotations

#: a = (10^k)³ / (10^k + c); the remainder is taken modulo ``mod``.
PARAMS = {"k": 10, "c": 11, "mod": 1000}
ANSWER = 120
VARIANTS = [
    {"k": 10, "c": 7, "mod": 1000},
    {"k": 12, "c": 11, "mod": 1000},
    {"k": 6, "c": 5, "mod": 100},
    {"k": 9, "c": 2, "mod": 1000},
    {"k": 4, "c": 30, "mod": 1000},        # c³ > x + c: the floor shifts
    {"k": 10, "c": 0, "mod": 1000},        # exact division, no floor at all
]


def solve(k=10, c=11, mod=1000):
    """⌊x³/(x+c)⌋ mod ``mod`` with x = 10^k, from the division identity."""
    if k <= 0 or c < 0 or mod <= 1:
        return None
    x = 10 ** k
    if c == 0:
        return (x * x) % mod
    if c ** 3 >= x + c:            # the identity's remainder term is not < 1
        return None
    return (x * x - c * x + c * c - 1) % mod


def check(k=10, c=11, mod=1000):
    """Independent: form the two integers and divide them.

    ``(10^k)³`` and ``10^k + c`` are built as plain integers and floor-divided —
    no expansion, no bound on c³ — and the remainder is read off the result. The
    guard is applied afterwards so that the two routes agree on which constants
    the closed form is entitled to.
    """
    if k <= 0 or c < 0 or mod <= 1:
        return None
    x = 10 ** k
    if c != 0 and c ** 3 >= x + c:
        return None
    numerator = (10 ** (3 * k))
    assert numerator == x ** 3
    return (numerator // (x + c)) % mod
