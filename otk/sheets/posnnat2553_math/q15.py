"""วันที่สอง ข้อ 5 — f(x − t, y) + f(x + t, y) + f(x, y − t) + f(x, y + t) = 2010

In one dimension f(x − t) + f(x + t) = K for all x and t ≠ 0 makes f constant;
in the plane the four points are the corners of a square in the rotated
coordinates (x + y, x − y), and the solution is the constant K/(2d) = 1005/2
(uniqueness is sketched in the bank note).

``check`` takes f constant (the form the proof reaches), substitutes it at a
spread of points and solves the resulting linear equation for the constant.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"total": 2010, "dimension": 2}
ANSWER = Fraction(1005, 2)
VARIANTS = [{"total": 7, "dimension": 1}, {"total": 30, "dimension": 3}, {"total": 1}]


def solve(total=2010, dimension=2):
    return Fraction(total, 2 * dimension)


def check(total=2010, dimension=2):
    # with f ≡ k every point contributes k: (number of neighbours)·k = total
    neighbours = 0
    for axis in range(dimension):
        for sign in (-1, 1):
            neighbours += 1
    return Fraction(total, neighbours)
