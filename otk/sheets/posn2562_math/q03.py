"""ข้อ 3 — ผลบวกของรากจริงทั้งหมด

จงหาผลบวกของรากจริงทั้งหมดของสมการ  2x² − 10x + 7 + 4√(x² − 5x + 3) = 31

The polynomial part and the radicand are the *same* quadratic in disguise. With
``u = x² − 5x + 3`` — exactly what sits under the root —

    2x² − 10x + 7 = 2(x² − 5x) + 7 = 2(u − 3) + 7 = 2u + 1

so the equation collapses to ``2u + 4√u + 1 = 31``, i.e. ``u + 2√u − 15 = 0``.
With w = √u ≥ 0 that factors as ``(w + 5)(w − 3) = 0``, and only **w = 3** is
admissible, so u = 9 and

    x² − 5x + 3 = 9  ⟹  x² − 5x − 6 = 0  ⟹  x = 6, −1,

both with u ≥ 0. Their sum is **5**.

The trap is squaring the printed equation, which drags the ``w = −5`` branch in
as a pair of extraneous roots. ``solve`` follows the substitution and keeps only
the admissible branch; ``check`` never substitutes anything — it sweeps the real
line, brackets sign changes of the printed left-hand side, and bisects.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt, sqrt

#: p·x² + q·x + r + k·√(x² + s·x + t) = target, with the radicand shared.
PARAMS = {"p": 2, "q": -10, "r": 7, "k": 4, "s": -5, "t": 3, "target": 31}
ANSWER = 5
VARIANTS = [
    {"p": 2, "q": -10, "r": 7, "k": 4, "s": -5, "t": 3, "target": 55},
    {"p": 1, "q": -4, "r": 0, "k": 2, "s": -4, "t": 1, "target": 12},
    {"p": 3, "q": 6, "r": 1, "k": 6, "s": 2, "t": -3, "target": 40},
    {"p": 2, "q": -10, "r": 7, "k": 4, "s": -5, "t": 3, "target": 1},
    {"p": 5, "q": 15, "r": -2, "k": 10, "s": 3, "t": 1, "target": 63},
    {"p": 2, "q": -10, "r": 7, "k": 4, "s": -5, "t": 3, "target": -99},
]


def _rational_sqrt(value: Fraction):
    """√value as a Fraction when it is one, else None."""
    n, d = value.numerator, value.denominator
    rn, rd = isqrt(n), isqrt(d)
    return Fraction(rn, rd) if rn * rn == n and rd * rd == d else None


def _roots(a, b, c):
    """Rational roots of ax² + bx + c, or None when any is irrational."""
    a, b, c = Fraction(a), Fraction(b), Fraction(c)
    if a == 0:
        return [] if b == 0 else [-c / b]
    disc = b * b - 4 * a * c
    if disc < 0:
        return []
    root = _rational_sqrt(disc)
    if root is None:
        return None
    return sorted({(-b + sign * root) / (2 * a) for sign in (1, -1)})


def solve(p=2, q=-10, r=7, k=4, s=-5, t=3, target=31):
    """Sum of the real roots, through the shared quadratic."""
    if p == 0 or k == 0:
        return None
    if Fraction(q, p) != Fraction(s):        # the radicand is not the same quadratic
        return None
    offset = r - p * t                       # px² + qx + r = p·u + offset
    # p·w² + k·w + (offset − target) = 0 with w = √u ≥ 0
    disc = k * k - 4 * p * (offset - target)
    if disc < 0:
        return None
    root = sqrt(disc)
    total = Fraction(0)
    found = False
    for sign in (1, -1):
        w = (-k + sign * root) / (2 * p)
        if w < 0:
            continue
        # x² + sx + (t − u) = 0 with u = w²; its root sum is −s whenever it has
        # two real roots, and −s/2 at a double root — u itself never shows up.
        inner = s * s - 4 * (t - w * w)
        if abs(inner) < 1e-9:                # too close to call: refuse
            return None
        if inner < 0:
            continue
        found = True
        total += Fraction(-s)
    if not found:
        return None
    return int(total) if total.denominator == 1 else total


def check(p=2, q=-10, r=7, k=4, s=-5, t=3, target=31):
    """Independent: bracket the printed expression numerically and bisect.

    The left-hand side is evaluated exactly as written — undefined where the
    radicand is negative — over a dense sweep; every sign change is bisected and
    every candidate substituted back before it counts. Nothing is squared, so the
    extraneous branch never appears in the first place.
    """
    if p == 0 and k == 0:
        return None

    def lhs(x: float):
        inside = x * x + s * x + t
        if inside < 0:
            return None
        return p * x * x + q * x + r + k * sqrt(inside) - target

    lo, hi, steps = -400.0, 400.0, 400_000
    step = (hi - lo) / steps
    roots: list[float] = []
    window: list[tuple[float, float | None]] = [(lo, lhs(lo))]
    for i in range(1, steps + 1):
        x = lo + (hi - lo) * i / steps
        cur = lhs(x)
        prev_x, prev = window[-1]
        if cur is not None and prev is not None:
            if cur == 0.0:
                roots.append(x)
            elif prev * cur < 0:
                a_, b_ = prev_x, x
                for _ in range(200):
                    mid = (a_ + b_) / 2
                    fa, fm = lhs(a_), lhs(mid)
                    if fa is None or fm is None:
                        break
                    if fa * fm <= 0:
                        b_ = mid
                    else:
                        a_ = mid
                roots.append((a_ + b_) / 2)
        # The expression can also vanish exactly where its own domain ends, with
        # no sign change and no interior minimum; those edges are found by
        # bisecting on whether the left-hand side is defined at all.
        if (cur is None) != (prev is None):
            inside, outside = (prev_x, x) if cur is None else (x, prev_x)
            for _ in range(200):
                mid = (inside + outside) / 2
                if lhs(mid) is None:
                    outside = mid
                else:
                    inside = mid
            roots.append(inside)
        window.append((x, cur))
        # A root the curve only touches — where √u vanishes — makes no sign
        # change at all, so local minima of |lhs| are refined as well.
        if len(window) == 3:
            (xa, fa), (xb, fb), (xc, fc) = window
            if None not in (fa, fb, fc) and abs(fb) < abs(fa) and abs(fb) < abs(fc):
                left, right = xb - step, xb + step
                for _ in range(200):
                    m1, m2 = left + (right - left) / 3, right - (right - left) / 3
                    f1, f2 = lhs(m1), lhs(m2)
                    if f1 is None or f2 is None:
                        break
                    if abs(f1) < abs(f2):
                        right = m2
                    else:
                        left = m1
                roots.append((left + right) / 2)
            window.pop(0)

    kept = set()
    for x in roots:
        got = lhs(x)
        if got is not None and abs(got) < 1e-6:
            snapped = Fraction(x).limit_denominator(10 ** 4)
            kept.add(snapped if abs(float(snapped) - x) < 1e-7 else
                     Fraction(x).limit_denominator(10 ** 9))
    if not kept:
        return None
    total = sum(kept, Fraction(0))
    return int(total) if total.denominator == 1 else total
