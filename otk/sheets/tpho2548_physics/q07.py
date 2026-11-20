"""Theory 2.1: the work to bring four protons from infinity to the corners of a square of side a is (4 + sqrt 2) k e^2/a, the sum over the six pairs. Adapted: equal charges q at the corners of a w x h rectangle (the square is w = h); returns the work in units of k q^2 (lengths in m)."""

from math import sqrt


def solve(width=1.0, height=1.0):
    diagonal = sqrt(width**2 + height**2)
    return 2 / width + 2 / height + 2 / diagonal


def check(width=1.0, height=1.0):
    # Bring the charges in one at a time and add each one's potential energy.
    corners = [(0, 0), (width, 0), (width, height), (0, height)]
    work = 0.0
    for i, (x, y) in enumerate(corners):
        work += sum(1 / sqrt((x - a) ** 2 + (y - b) ** 2) for a, b in corners[:i])
    return work


PARAMS = {"width": 1.0, "height": 1.0}
VARIANTS = [{"width": 3, "height": 4}, {"width": 0.5, "height": 1.2}, {"width": 8, "height": 15}]
ANSWER = 5.414213562373095
TOL = 1e-9
