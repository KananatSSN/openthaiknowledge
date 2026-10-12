"""ข้อ 18 — ค่าของ c

กำหนดให้ x เป็นจำนวนจริง และ
    a = x + (x+1) + (x+2) + ... + (x+10),
    b = 8 + 16 + 24 + 32 + ... + 80,
    c = 88x
ถ้า 4a² + b + c + 4 = 0 แล้วจงหาค่าของ c (ตอบเป็นจำนวนเต็ม)

a is 11x + 55 and b is 8(1+2+…+10) = 440, so the condition reads

    4(11x+55)² + 88x + 444 = 0,  i.e.  484x² + 4928x + 12544 = 0

whose discriminant is exactly zero — it is (22x + 112)². The single root is
x = −56/11 and

    c = 88x = **−448**.

The constants are built for that: with n terms, T = n(n+1)/2, b = 8T and
c = Kx, the quadratic is a perfect square precisely when K = 8(n+1), and then

    x = -(T+1)/(n+1),   c = -8(T+1)

so the sheet's answer is −8·56. ``solve`` uses that closed form; ``check``
assembles the sums term by term and solves the quadratic it actually gets.
"""

from __future__ import annotations

from fractions import Fraction

#: a runs x, x+1, …, x+terms; the answer is c = coef·x.
PARAMS = {"terms": 10}
ANSWER = -448
VARIANTS = [
    {"terms": 4},
    {"terms": 7},
    {"terms": 15},
    {"terms": 1},
    {"terms": 0},          # a single term: still well posed
]


def coefficients(terms=10):
    """(number of summands, T, b, K) — the constants the printed item shows."""
    if terms < 0:
        return None
    count = terms + 1
    t = terms * (terms + 1) // 2
    return count, t, 8 * t, 8 * count


def solve(terms=10):
    """c = -8(T+1), the value forced by the perfect-square condition."""
    got = coefficients(terms)
    if got is None:
        return None
    _, t, _, _ = got
    return -8 * (t + 1)


def check(terms=10):
    """Independent: build a, b and c as sums and solve 4a² + b + c + 4 = 0.

    a is expanded coefficient by coefficient from the actual list of summands,
    b is added up term by term, and the quadratic is solved with exact rationals
    — the perfect-square identity is asserted rather than assumed, and the root
    is substituted back into the original condition before c is reported.
    """
    got = coefficients(terms)
    if got is None:
        return None
    count, _, _, k = got

    # a = Σ (x + j) = count·x + Σ j
    lin, const = count, sum(range(terms + 1))
    b = sum(8 * j for j in range(1, terms + 1))

    # 4(lin·x + const)² + b + k·x + 4 = 0
    qa = 4 * lin * lin
    qb = 8 * lin * const + k
    qc = 4 * const * const + b + 4
    if qa == 0:
        return None if qb == 0 else -k * Fraction(-qc, qb)
    disc = qb * qb - 4 * qa * qc
    assert disc == 0, f"the constants no longer give a double root: {disc}"
    x = Fraction(-qb, 2 * qa)
    assert 4 * (lin * x + const) ** 2 + b + k * x + 4 == 0
    value = k * x
    return int(value) if value.denominator == 1 else value
