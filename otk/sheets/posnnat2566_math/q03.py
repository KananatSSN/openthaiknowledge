"""ข้อ 3 — f(x)f(y)f(x − y) = x²f(y) − y²f(x)

For the family f(x)f(y)f(x − y) = c[x²f(y) − y²f(x)] with c = s²: x = y gives
f(0) = 0 or f(x)² f(0) = 0, then y = 0 and y = x/2 pin f to an odd function with
f(x)² = c x², and the equation rules out mixing signs. So f = 0, sx or −sx. The
source (s = 1) gives f = 0, x, −x. The answer is the sorted tuple of f(t) over
the solutions.

``check`` tries every f = αx + βx² + γ with |α| ≤ 12, |β|, |γ| ≤ 3 against the
equation at many rational points and evaluates the survivors at t.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

PARAMS = {"scale": 1, "point": 3}
ANSWER = (-3, 0, 3)
VARIANTS = [{"scale": 2, "point": -5}, {"scale": 3, "point": 2}, {"scale": 4, "point": 7}]


def solve(scale=1, point=3):
    m = scale * abs(point)
    return (-m, 0, m)


def check(scale=1, point=3):
    c = scale * scale
    pts = [Fraction(v, 2) for v in (-5, -2, -1, 0, 1, 3, 4)]
    found = set()
    for alpha, beta, gamma in product(range(-12, 13), range(-3, 4), range(-3, 4)):
        def f(x, alpha=alpha, beta=beta, gamma=gamma):
            return alpha * x + beta * x * x + gamma

        if all(f(x) * f(y) * f(x - y) == c * (x * x * f(y) - y * y * f(x)) for x in pts for y in pts):
            found.add(f(Fraction(point)))
    return tuple(sorted(found))
