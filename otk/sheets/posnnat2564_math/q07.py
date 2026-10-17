"""ข้อ 7 — f : ℝ⁺ → ℝ ที่ f(xy) = f(x)f(y)f(x + y)

For the family f(xy) = s²f(x)f(y)f(x + y): if f(1) = 0 then x = 1 gives f ≡ 0.
Otherwise the pairs x, 1/x show f never vanishes, and x = 1 with the
equation's symmetry forces f(x + 1) = 1/(s²f(1)) for every x, so f is a constant
c with c = s²c³: c = ±1/s. The source (s = 1) gives f = 0, 1, −1. The answer
is the sorted tuple of the constants.

``check`` tries constants with denominators up to 12 and the non-constant
c·x, c/x, c·x² for small c against the equation at many positive points,
asserts no non-constant survives, and returns the surviving constants.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"scale": 1}
ANSWER = (Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1))
VARIANTS = [{"scale": 2}, {"scale": 3}, {"scale": 4}]


def solve(scale=1):
    return (Fraction(-1, scale), Fraction(0), Fraction(1, scale))


def check(scale=1):
    pts = [Fraction(v, 3) for v in (1, 2, 3, 5, 7, 11)]
    k = scale * scale

    def ok(f):
        return all(f(x * y) == k * f(x) * f(y) * f(x + y) for x in pts for y in pts)

    found = sorted({Fraction(n, d) for d in range(1, 13) for n in range(-2 * d, 2 * d + 1)
                    if ok(lambda t, c=Fraction(n, d): c)})
    for c in (Fraction(1), Fraction(-1), Fraction(1, 2), Fraction(2)):
        for shape in (lambda t, c=c: c * t, lambda t, c=c: c / t, lambda t, c=c: c * t * t):
            assert not ok(shape)
    return tuple(found)
