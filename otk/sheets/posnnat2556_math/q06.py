"""ข้อ 6 — (x² + y²)f(xy) = f(x)f(y)f(x² + y²)

For the family (x² + y²)ᵏ f(xy) = f(x)f(y)f(x² + y²): write f = xᵏh, then
h(xy) = h(x)h(y)h(x² + y²); y = 1 makes h a constant ±1 on [1, ∞), and
g = ±h is multiplicative and 1 on the positives, so h is ±1 or ±sign(x). That
is five functions for every k: 0, ±xᵏ, ±sign(x)xᵏ. For even k the last pair is
±sign(x)|x|ᵏ, not ±|x|ᵏ (which equals ±xᵏ). The source (k = 1) gives 0, x,
−x, |x|, −|x|. The answer is the sorted tuple of (f(−2), f(3)) over the
solutions.

``check`` tries every candidate c·s(x)·|x|ᵉ (c ∈ {−2, …, 2}, e ≤ 4, s = 1 or
sign) against the equation at many rational points and keeps the distinct
functions that pass.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"k": 1}
ANSWER = ((-2, -3), (-2, 3), (0, 0), (2, -3), (2, 3))
VARIANTS = [{"k": 2}, {"k": 3}, {"k": 4}]


def solve(k=1):
    def sign(t):
        return (t > 0) - (t < 0)

    funcs = [lambda t: 0]
    for c in (1, -1):
        funcs += [lambda t, c=c: c * t**k, lambda t, c=c: c * sign(t) * t**k]
    return tuple(sorted((f(-2), f(3)) for f in funcs))


def check(k=1):
    pts = [Fraction(v, 3) for v in (-7, -4, -3, -1, 0, 1, 2, 3, 5, 8)]
    survivors = set()
    for c in range(-2, 3):
        for e in range(0, 5):
            for signed in (False, True):
                def f(t, c=c, e=e, signed=signed):
                    sgn = (t > 0) - (t < 0)
                    return c * (sgn if signed else 1) * abs(t) ** e

                if all((x * x + y * y) ** k * f(x * y) == f(x) * f(y) * f(x * x + y * y)
                       for x in pts for y in pts):
                    survivors.add((f(Fraction(-2)), f(Fraction(3))))
    return tuple(sorted(survivors))
