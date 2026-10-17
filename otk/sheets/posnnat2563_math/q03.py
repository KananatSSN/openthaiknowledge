"""ข้อ 3 — f(a + b + c + d) = Σ f เมื่อ a, b, c, d เป็นด้านสี่เหลี่ยมแนบในวงกลม  (พิสูจน์)

The quadrilateral identity (sides with a + c = b + d) forces f additive, hence
f(p/q) = (p/q)·f(1) on the rationals. The solver returns f(p/q) from f(1)
(f(1) = 3, 5/2: 15/2).

``check`` tries every f(x) = αx + βx² + γ with small integer coefficients
against the identity on many tangential quadrilaterals (a + c = b + d, each side
less than the sum of the others), asserts only the linear ones survive, and
evaluates the survivor with f(1) = unit at p/q.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

PARAMS = {"unit": 3, "p": 5, "q": 2}
ANSWER = Fraction(15, 2)
VARIANTS = [{"unit": -2, "p": 7, "q": 3}, {"unit": 1, "p": 1, "q": 4}, {"unit": 5, "p": 9, "q": 1}]


def solve(unit=3, p=5, q=2):
    return Fraction(unit * p, q)


def _quads():
    out = []
    for a, b, c in product((Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5, 2)), repeat=3):
        d = a + c - b
        sides = (a, b, c, d)
        if d > 0 and all(2 * s < sum(sides) for s in sides):
            out.append(sides)
    return out


def check(unit=3, p=5, q=2):
    quads = _quads()
    survivors = []
    for alpha, beta, gamma in product(range(-6, 7), range(-3, 4), range(-3, 4)):
        def f(x, alpha=alpha, beta=beta, gamma=gamma):
            return alpha * x + beta * x * x + gamma

        if all(f(sum(s)) == sum(f(x) for x in s) for s in quads):
            survivors.append((alpha, beta, gamma))
    assert all(beta == gamma == 0 for _, beta, gamma in survivors)
    (alpha,) = [a for a, _, _ in survivors if a == unit]
    return alpha * Fraction(p, q)
