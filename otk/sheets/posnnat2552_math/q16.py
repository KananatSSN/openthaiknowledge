"""วันที่สอง ข้อ 6 — พหุนาม (−1)ⁿxⁿ + a₁xⁿ⁻¹ + ⋯ + aₙ, {aᵢ} = {0, 1}, รากจริงต่างกันทั้งหมด

The answer is x² + x, −x³ + x and −x³ + x² + x, recorded as coefficient tuples
(1, 0), (0, 1, 0), (1, 1, 0). ``solve`` tests every 0/1 coefficient tuple up to
degree n by counting sign changes on a fine grid (all roots lie in |x| < 2).

``check`` counts distinct real roots exactly with a Sturm sequence in fractions.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

PARAMS = {"max_degree": 5}
ANSWER = ((0, 1, 0), (1, 0), (1, 1, 0))
VARIANTS = [{"max_degree": 2}, {"max_degree": 3}, {"max_degree": 6}]


def _candidates(max_degree):
    for n in range(1, max_degree + 1):
        for coeffs in product((0, 1), repeat=n):
            if set(coeffs) == {0, 1}:
                yield coeffs


def solve(max_degree=5):
    found = []
    for coeffs in _candidates(max_degree):
        n = len(coeffs)

        def value(x, coeffs=coeffs, n=n):
            return (-1) ** n * x**n + sum(c * x ** (n - i) for i, c in enumerate(coeffs, start=1))

        xs = [-3 + 6 * i / 6000 + 1e-7 for i in range(6001)]
        if sum(1 for u, v in zip(xs, xs[1:]) if value(u) * value(v) < 0) == n:
            found.append(coeffs)
    return tuple(sorted(found))


def _rem(num, den):
    num = list(num)
    while len(num) >= len(den) and any(num):
        lead = num[0] / den[0]
        for i in range(len(den)):
            num[i] -= lead * den[i]
        num.pop(0)
    while num and num[0] == 0:
        num.pop(0)
    return num


def _sturm_distinct_real(poly):
    deriv = [c * (len(poly) - 1 - i) for i, c in enumerate(poly[:-1])]
    seq = [poly, deriv]
    while True:
        r = _rem(seq[-2], seq[-1])
        if not r:
            break
        seq.append([-c for c in r])

    def changes(at_plus):
        signs = []
        for p in seq:
            deg = len(p) - 1
            lead = p[0]
            s = lead if at_plus else lead * (-1) ** deg
            if s:
                signs.append(s > 0)
        return sum(1 for u, v in zip(signs, signs[1:]) if u != v)

    return changes(False) - changes(True)


def check(max_degree=5):
    found = []
    for coeffs in _candidates(max_degree):
        n = len(coeffs)
        poly = [Fraction((-1) ** n)] + [Fraction(c) for c in coeffs]
        if _sturm_distinct_real(poly) == n:
            # n distinct real roots needs no repeated root: gcd(P, P′) constant
            found.append(coeffs)
    return tuple(sorted(found))
