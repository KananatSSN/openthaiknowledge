"""ข้อ 13 — พหุนามดีกรีน้อยที่สุดที่ P(1) = P(2) = 1 และ P(3) = 5

จงหาพหุนาม P(x) ที่มีดีกรีน้อยที่สุด ซึ่ง P(1) = P(2) = 1 และ P(3) = 5

Three conditions can always be met by a polynomial of degree ≤ 2, and here
degree 2 is forced: P(1) = P(2) would make a linear polynomial constant, and a
constant cannot also give P(3) = 5. So the interpolating quadratic *is* the
answer, and Newton's divided differences build it in one pass:

    P[1] = 1,  P[1,2] = 0,  P[1,2,3] = 2
    P(x) = 1 + 0·(x−1) + 2·(x−1)(x−2) = **2x² − 6x + 5**

``solve`` returns the coefficients from those divided differences, then trims any
leading zeros — which is what makes "least degree" a computation rather than an
assumption. ``check`` builds the Vandermonde system for each degree in turn,
starting at zero, and returns the first one that has an exact solution; it never
computes a divided difference.
"""

from __future__ import annotations

from fractions import Fraction

#: the printed (x, y) conditions.
PARAMS = {"points": ((1, 1), (2, 1), (3, 5))}
ANSWER = (2, -6, 5)
VARIANTS = [
    {"points": ((1, 1), (2, 1), (3, 7))},
    {"points": ((0, 1), (1, 2), (2, 5))},
    {"points": ((1, 3), (2, 3), (3, 3))},          # constant: degree 0
    {"points": ((1, 2), (2, 4), (3, 6))},          # linear: degree 1
    {"points": ((-1, 4), (0, 1), (2, 7))},
    {"points": ((1, 1), (2, 1), (3, 5), (4, 13))},
]


def _trim(coeffs):
    """Drop leading zeros; the highest power comes first."""
    out = list(coeffs)
    while len(out) > 1 and out[0] == 0:
        out.pop(0)
    return tuple(int(c) if isinstance(c, Fraction) and c.denominator == 1 else c
                 for c in out)


def solve(points=((1, 1), (2, 1), (3, 5))):
    """Newton's divided differences, expanded and trimmed to least degree."""
    pts = [(Fraction(x), Fraction(y)) for x, y in points]
    xs = [x for x, _ in pts]
    if len(set(xs)) != len(xs):
        return None
    table = [y for _, y in pts]
    coeffs = [table[0]]
    for step in range(1, len(pts)):
        table = [(table[i + 1] - table[i]) / (xs[i + step] - xs[i])
                 for i in range(len(table) - 1)]
        coeffs.append(table[0])

    # expand  Σ cₖ·Π(x − xᵢ)  into ordinary coefficients, highest power first
    poly = [Fraction(0)] * len(pts)
    basis = [Fraction(1)]                       # coefficients of Π(x − xᵢ)
    for k, c in enumerate(coeffs):
        for i, b in enumerate(basis):
            poly[len(poly) - 1 - i] += c * b
        if k < len(pts) - 1:                    # multiply basis by (x − x_k)
            shifted = [Fraction(0)] * (len(basis) + 1)
            for i, b in enumerate(basis):
                shifted[i + 1] += b
                shifted[i] -= b * xs[k]
            basis = shifted
    return _trim(poly)


def check(points=((1, 1), (2, 1), (3, 5))):
    """Independent: try every degree upwards and solve the linear system exactly.

    For degree d the conditions are a (len(points) × (d+1)) linear system in the
    coefficients; Gaussian elimination either solves it consistently for all the
    points or it does not, and the first degree that works is the least one. No
    interpolation formula is involved.
    """
    pts = [(Fraction(x), Fraction(y)) for x, y in points]
    if len({x for x, _ in pts}) != len(pts):
        return None
    for degree in range(len(pts)):
        width = degree + 1
        rows = [[x ** (degree - j) for j in range(width)] + [y] for x, y in pts]
        # eliminate
        pivot_row = 0
        pivots = []
        for col in range(width):
            sel = next((r for r in range(pivot_row, len(rows)) if rows[r][col] != 0),
                       None)
            if sel is None:
                continue
            rows[pivot_row], rows[sel] = rows[sel], rows[pivot_row]
            head = rows[pivot_row][col]
            rows[pivot_row] = [v / head for v in rows[pivot_row]]
            for r in range(len(rows)):
                if r != pivot_row and rows[r][col] != 0:
                    factor = rows[r][col]
                    rows[r] = [a - factor * b
                               for a, b in zip(rows[r], rows[pivot_row])]
            pivots.append(col)
            pivot_row += 1
        if any(all(v == 0 for v in row[:width]) and row[width] != 0 for row in rows):
            continue                            # inconsistent at this degree
        if len(pivots) < width:
            continue                            # underdetermined: not least degree
        coeffs = [Fraction(0)] * width
        for r, col in enumerate(pivots):
            coeffs[col] = rows[r][width]
        return _trim(coeffs)
    return None
