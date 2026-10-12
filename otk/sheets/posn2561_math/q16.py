"""ข้อ 16 — เศษเหลือจากการหารด้วยพหุนามกำลังสอง

สมมติให้ P(x) เป็นพหุนามที่หารด้วย x − 2 และ x + 3 แล้วเหลือเศษ 5 และ −7 ตามลำดับ
จงหาเศษเหลือจากการหาร P(x) ด้วย x² + x − 6

``x² + x − 6 = (x − 2)(x + 3)``, so the remainder is at most linear: r(x) = mx + n.
Dividing ``P = (x−2)(x+3)Q + r`` by x − 2 and by x + 3 kills the quotient term
each time, so r takes the two printed values at the two roots:

    r(2) = 5      2m + n = 5
    r(−3) = −7   −3m + n = −7

Subtracting, 5m = 12, so m = 12/5 and n = 5 − 24/5 = 1/5:

    r(x) = (12x + 1)/5

``solve`` reads that pair straight off. ``check`` builds an *actual* polynomial
with the two printed remainders — a cubic through four interpolation conditions,
two of them chosen arbitrarily — and long-divides it by the quadratic. It does so
twice with different arbitrary conditions and refuses to answer unless the two
divisions give the same remainder, which is what makes the answer independent of
the polynomial it happened to invent.
"""

from __future__ import annotations

from fractions import Fraction

#: P(a) = ra and P(b) = rb; divide by (x − a)(x − b).
PARAMS = {"a": 2, "ra": 5, "b": -3, "rb": -7}
ANSWER = (Fraction(12, 5), Fraction(1, 5))
VARIANTS = [
    {"a": 1, "ra": 3, "b": 4, "rb": 9},
    {"a": -1, "ra": 0, "b": 5, "rb": 12},
    {"a": 2, "ra": 7, "b": -3, "rb": 7},      # a constant remainder
    {"a": 3, "ra": -2, "b": -2, "rb": 8},
    {"a": 0, "ra": 1, "b": 6, "rb": -5},
    {"a": 2, "ra": 5, "b": 2, "rb": 5},       # one root twice: not determined
]


def _interpolate(points: list[tuple[Fraction, Fraction]]) -> list[Fraction] | None:
    """Coefficients (ascending) of the polynomial through the given points."""
    size = len(points)
    rows = [[x ** j for j in range(size)] + [y] for x, y in points]
    for col in range(size):
        pivot = next((r for r in range(col, size) if rows[r][col] != 0), None)
        if pivot is None:
            return None
        rows[col], rows[pivot] = rows[pivot], rows[col]
        rows[col] = [v / rows[col][col] for v in rows[col]]
        for r in range(size):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col]
                rows[r] = [v - factor * w for v, w in zip(rows[r], rows[col])]
    return [rows[j][size] for j in range(size)]


def _divide(poly: list[Fraction], a: Fraction, b: Fraction) -> tuple[Fraction, Fraction]:
    """Remainder of ``poly`` on division by (x − a)(x − b), as (slope, constant)."""
    # long division by x² − (a+b)x + ab, highest degree first
    work = list(poly)
    for degree in range(len(work) - 1, 1, -1):
        lead = work[degree]
        if lead == 0:
            continue
        work[degree] = Fraction(0)
        work[degree - 1] += lead * (a + b)
        work[degree - 2] -= lead * a * b
    return work[1], work[0]


def solve(a=2, ra=5, b=-3, rb=-7):
    """The remainder is the line through (a, ra) and (b, rb)."""
    if a == b:
        return None
    slope = Fraction(ra - rb, 1) / Fraction(a - b, 1)
    return slope, Fraction(ra, 1) - slope * a


def check(a=2, ra=5, b=-3, rb=-7):
    """Independent: invent a P with those remainders and actually divide it.

    Two cubics are interpolated through ``(a, ra)``, ``(b, rb)`` and two further,
    deliberately arbitrary points; each is long-divided by (x − a)(x − b). If the
    remainder really is a property of P mod the quadratic the two agree, and the
    agreement is asserted rather than assumed.
    """
    if a == b:
        return None
    remainders = []
    for spare in ((Fraction(11), Fraction(4)), (Fraction(-7), Fraction(9))):
        extras = [(Fraction(a) + spare[0], spare[1]),
                  (Fraction(b) - spare[0], -spare[1])]
        points = [(Fraction(a), Fraction(ra)), (Fraction(b), Fraction(rb))] + extras
        if len({x for x, _ in points}) != len(points):
            return None
        poly = _interpolate(points)
        if poly is None:
            return None
        remainders.append(_divide(poly, Fraction(a), Fraction(b)))
    if remainders[0] != remainders[1]:
        return None
    return remainders[0]
