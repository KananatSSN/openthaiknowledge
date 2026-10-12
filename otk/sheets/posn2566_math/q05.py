"""ข้อ 5 — ค่าที่เป็นไปได้ทั้งหมดของ a/b² − b/a² − ab

ให้ a และ b เป็นจำนวนจริงที่ไม่เท่ากับศูนย์ โดยที่ a = b(a + 1)
จงหาค่าที่เป็นไปได้ทั้งหมดของ  a/b² − b/a² − ab

"All possible values" is a set, and here it has exactly one element — the
expression is **constant** on the whole curve.

From ``a = b(a + 1)`` comes ``b = a/(a + 1)`` (with a ≠ −1, and b ≠ 0 forces
a ≠ 0). Substituting and putting everything over the common denominator a(a+1):

    a/b² = (a+1)²/a        b/a² = 1/(a(a+1))        ab = a²/(a+1)

    a/b² − b/a² − ab = [ (a+1)³ − 1 − a³ ] / (a(a+1))

and the bracket is ``3a² + 3a = 3a(a + 1)``, which cancels the denominator
exactly:

    **the value is 3, always**

The cubes are what make it collapse — every other term of `(a+1)³` survives only
to be divided away.

``solve`` returns that constant after checking the constraint can be satisfied.
``check`` knows nothing about the algebra: it picks many admissible a, computes b
from the printed relation, evaluates the printed expression numerically, and
reports the common value only if every sample agrees.
"""

from __future__ import annotations

from fractions import Fraction

#: a = b(a + m) and the expression a/b^p − b/a^p − ab.
PARAMS = {"m": 1, "power": 2}
ANSWER = Fraction(3)
VARIANTS = [
    {"m": 2},
    {"m": 3},
    {"m": -1},
    {"power": 3},
    {"m": 2, "power": 3},
    {"m": 0},                     # a = ab forces b = 1: still constant
]


def solve(m=1, power=2):
    """3m, but only when the leftover term vanishes — and it needs m³ = 1.

    With b = a/(a + m) the expression over the common denominator a(a + m) is

        [ (a + m)³ − 1 − a³ ] / (a(a + m))  =  3m + (m³ − 1)/(a(a + m))

    so it is a single number exactly when ``m³ = 1``, i.e. m = 1 over the reals,
    and then it equals 3m = 3. Any other m leaves a term that still moves with a,
    and "all possible values" is then not one value at all.
    """
    if power != 2:
        return None                       # the cancellation is special to squares
    if m == 0:
        return None                       # b ≡ 1, and the expression is −1/a²
    if m ** 3 != 1:
        return None
    return Fraction(3 * m)


def check(m=1, power=2):
    """Independent: sample the curve and evaluate the printed expression.

    For each sampled a the partner b comes from ``a = b(a + m)`` exactly as
    printed, and the expression is evaluated numerically. A value is reported
    only when every admissible sample agrees to working precision — so a shape
    that is *not* constant returns None rather than one arbitrary sample.
    """
    values = []
    for step in range(1, 400):
        for a in (step * 0.37, -step * 0.53, step * 1.9):
            if abs(a) < 1e-9 or abs(a + m) < 1e-9:
                continue
            b = a / (a + m)
            if abs(b) < 1e-9:
                continue
            value = a / b ** power - b / a ** power - a * b
            values.append(value)
    if not values:
        return None
    first = values[0]
    if any(abs(v - first) > 1e-6 * max(1.0, abs(first)) for v in values):
        return None
    snapped = Fraction(first).limit_denominator(64)
    return snapped if abs(float(snapped) - first) < 1e-7 else first
