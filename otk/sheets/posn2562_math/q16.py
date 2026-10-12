"""ข้อ 16 — ค่าของ (ab + a + 1)/b

ให้ a และ b เป็นจำนวนจริง ซึ่ง ab ≠ 1 ถ้า a² + 12a + 3 = 0 และ 3b² + 12b + 1 = 0
จงหาค่าของ (ab + a + 1)/b

The second equation is the **reciprocal** of the first. Dividing it by b²,

    3b² + 12b + 1 = 0   ⟹   3 + 12·(1/b) + (1/b)² = 0

so ``1/b`` satisfies ``x² + 12x + 3 = 0`` — the very equation a satisfies. The
condition ``ab ≠ 1`` says a ≠ 1/b, so a and 1/b are the *two distinct roots* of
that quadratic, and Vieta hands over both symmetric functions:

    a + 1/b = −12,   a · (1/b) = 3

The requested expression splits into exactly those two:

    (ab + a + 1)/b = a + a/b + 1/b = (a + 1/b) + (a/b) = −12 + 3 = **−9**

In general the answer is ``q − p`` for ``x² + px + q`` and its reverse
``qx² + px + 1`` — the constant term minus the linear one, with nothing else
needed. The roots themselves are irrational here and never have to be computed.

``solve`` returns q − p after checking the roots are real and distinct.
``check`` finds the four roots numerically, pairs each a with each b, discards
the pairs with ab = 1, and evaluates the printed expression on what is left.
"""

from __future__ import annotations

from math import sqrt

#: a² + p·a + q = 0 and q·b² + p·b + 1 = 0.
PARAMS = {"p": 12, "q": 3}
ANSWER = -9
VARIANTS = [
    {"p": 7, "q": 2},
    {"p": 10, "q": 5},
    {"p": -6, "q": 4},
    {"p": 5, "q": -3},
    {"p": 2, "q": 3},          # no real roots
    {"p": 4, "q": 4},          # a double root: ab = 1 is forced
]


def solve(p=12, q=3):
    """(ab + a + 1)/b = (a + 1/b) + a/b = −p + q."""
    disc = p * p - 4 * q
    if q == 0 or disc <= 0:            # need two distinct real roots
        return None
    return q - p


def check(p=12, q=3):
    """Independent: find the four roots, pair them, and evaluate as printed.

    Both quadratics are solved with the quadratic formula, every (a, b) pairing
    is formed, the ones with ab = 1 are thrown out by the printed condition, and
    ``(ab + a + 1)/b`` is computed directly. A value is reported only if every
    surviving pair agrees — the reciprocal relationship is never invoked.
    """
    disc_a = p * p - 4 * q
    if q == 0 or disc_a <= 0:
        return None
    disc_b = p * p - 4 * q                       # of q·b² + p·b + 1
    if disc_b <= 0:
        return None
    a_roots = [(-p + s * sqrt(disc_a)) / 2 for s in (1, -1)]
    b_roots = [(-p + s * sqrt(disc_b)) / (2 * q) for s in (1, -1)]

    values = []
    for a in a_roots:
        for b in b_roots:
            if abs(b) < 1e-12 or abs(a * b - 1) < 1e-9:
                continue
            values.append((a * b + a + 1) / b)
    if not values:
        return None
    if max(values) - min(values) > 1e-6 * max(1.0, abs(values[0])):
        return None
    got = sum(values) / len(values)
    return round(got) if abs(got - round(got)) < 1e-7 else got
