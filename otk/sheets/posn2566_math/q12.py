"""ข้อ 12 — คู่อันดับของจำนวนตรรกยะที่เป็นคำตอบของระบบสมการ

จงหาคู่อันดับของจำนวนตรรกยะ (x, y) ทั้งหมด ซึ่งเป็นคำตอบของระบบสมการ
    1 + x + xy = x²
    x²((1 + y)(x + y) + 1) = 1

x = 0 is impossible (the first equation would read 1 = 0), so the first equation
solves for y outright:

    y = x − 1 − 1/x

Then ``1 + y = x − 1/x`` and ``x + y = 2x − 1 − 1/x``, and the second equation
becomes, after multiplying through by x²,

    2x⁴ − x³ − 2x² + x = 1 − 1  ⟹  x(2x³ − x² − 2x + 1) = 0

The cubic factors by grouping — ``x²(2x − 1) − (2x − 1) = (2x − 1)(x² − 1)`` — so

    x ∈ {1/2, 1, −1}

and y = x − 1 − 1/x gives

    **(1/2, −5/2), (1, −1), (−1, −1)**

Both roots of x² − 1 survive, which is why there are three pairs and not two;
and every root is rational, so "rational solutions" and "real solutions" agree
here.

``solve`` does that elimination in exact fractions and finds the quartic's
rational roots by the rational-root theorem. ``check`` never eliminates
anything: it sweeps candidate rationals with bounded denominators and tests both
printed equations directly.
"""

from __future__ import annotations

from fractions import Fraction

#: c + x + xy = x²  and  x²((c + y)(x + y) + c) = rhs.
PARAMS = {"c": 1, "rhs": 1}
ANSWER = ((Fraction(-1), Fraction(-1)), (Fraction(1, 2), Fraction(-5, 2)),
          (Fraction(1), Fraction(-1)))
VARIANTS = [
    {"c": 2},
    {"rhs": 4},
    {"c": 1, "rhs": 2},
    {"c": 3, "rhs": 9},
    {"c": -1},
    {"c": 2, "rhs": 8},
]


def _poly_from(c, rhs):
    """Coefficients (ascending) of the quartic in x after eliminating y."""
    # y = x - c/x - 1 ⟹ c + y = x - c/x + (c - 1),  x + y = 2x - c/x - 1
    # x²((c+y)(x+y) + c) - rhs = 0, cleared of denominators:
    #   (x² + (c-1)x - c)(2x² - x - c) + c x² - rhs x² = 0
    left = [-c, c - 1, 1]                 # -c + (c-1)x + x²
    right = [-c, -1, 2]                   # -c - x + 2x²
    prod = [0] * 5
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            prod[i + j] += u * v
    prod[2] += c            # the + c inside the bracket
    prod[0] -= rhs          # ... and the right-hand side
    return prod


def _rational_roots(coeffs):
    """Every rational root of an integer polynomial, by the rational-root test."""
    while coeffs and coeffs[-1] == 0:
        coeffs = coeffs[:-1]
    if len(coeffs) < 2:
        return []
    shift = 0
    while coeffs[shift] == 0:
        shift += 1
    tail = coeffs[shift:]
    roots = [Fraction(0)] if shift else []

    def divisors(v):
        v = abs(v)
        return [d for d in range(1, v + 1) if v % d == 0] if v else [1]

    for p in divisors(tail[0]):
        for q in divisors(tail[-1]):
            for candidate in (Fraction(p, q), Fraction(-p, q)):
                value = sum(Fraction(co) * candidate ** i
                            for i, co in enumerate(tail))
                if value == 0 and candidate not in roots:
                    roots.append(candidate)
    return roots


def solve(c=1, rhs=1):
    """Eliminate y, then read the quartic's rational roots."""
    roots = _rational_roots(_poly_from(c, rhs))
    out = []
    for x in roots:
        if x == 0:
            continue
        y = x - Fraction(c) / x - 1
        if c + x + x * y != x * x:
            continue
        if x * x * ((c + y) * (x + y) + c) != rhs:
            continue
        out.append((x, y))
    return tuple(sorted(out)) if out else None


def check(c=1, rhs=1):
    """Independent: sweep rationals with small denominators against both equations."""
    out = []
    for q in range(1, 25):
        for p in range(-120, 121):
            if p == 0:
                continue
            x = Fraction(p, q)
            if x.denominator != q or abs(x.numerator) > 120:
                continue
            y = (x * x - c - x) / x
            if x * x * ((c + y) * (x + y) + c) == rhs and (x, y) not in out:
                out.append((x, y))
    return tuple(sorted(out)) if out else None
