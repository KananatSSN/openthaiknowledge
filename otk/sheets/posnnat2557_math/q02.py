"""ข้อ 2 — f(xy − 1) + f(x)f(y) = 2xy − 1

x = 0 gives f(−1) + f(0)f(y) = −1 for all y, so f(0) = 0 and f(−1) = −1; then
f(1) = ±1. f(1) = 1 makes f additive and multiplicative, so f(x) = x;
f(1) = −1 makes −f multiplicative with −f(x + 1) = −f(x) + 2x + 1, so
f(x) = −x². The answer is the sorted tuple of f(n) over both (n = 3: −9, 3).

``check`` tries every quadratic ax² + bx + c with small integer coefficients on
a spread of points and evaluates the survivors at n.
"""

from __future__ import annotations

from itertools import product

PARAMS = {"n": 3}
ANSWER = (-9, 3)
VARIANTS = [{"n": -2}, {"n": 5}, {"n": 10}]


def solve(n=3):
    return tuple(sorted((n, -n * n)))


def check(n=3):
    pts = (-3, -1, 0, 1, 2, 4)
    found = []
    for a, b, c in product(range(-3, 4), repeat=3):
        def f(t, a=a, b=b, c=c):
            return a * t * t + b * t + c

        if all(f(x * y - 1) + f(x) * f(y) == 2 * x * y - 1 for x in pts for y in pts):
            found.append(f(n))
    return tuple(sorted(found))
