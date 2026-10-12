"""ข้อ 10 — ค่า x + y ที่มากที่สุด

ให้ x, y ∈ ℝ โดยที่ 3x² + 3y² = 7 และ x³ + y³ = 3 จงหาค่า x + y ที่มากที่สุด

Both conditions are symmetric, so write s = x + y and p = xy:

    x² + y² = s² − 2p = 7/3        ⟹  p = (s² − 7/3)/2
    x³ + y³ = s³ − 3ps = 3

Substituting the first into the second and clearing denominators,

    2s³ − 3s(s² − 7/3) = 6   ⟹   −s³ + 7s = 6   ⟹   s³ − 7s + 6 = 0

which factors as ``(s − 1)(s − 2)(s + 3) = 0``. So s ∈ {1, 2, −3} — but **the
reality condition throws one away**: x and y are real only when ``s² ≥ 4p``, i.e.

    s² ≥ 2s² − 14/3   ⟹   s² ≤ 14/3 ≈ 4.667

and s = −3 gives 9, far too big. Of the survivors the largest is **2** (with
p = 5/6, discriminant 2/3 > 0 — a genuine real pair).

Discarding s = −3 is the whole item; taking the largest root of the cubic gives
2 as well here, but only by luck of ordering.

Two things had to be got right, and the cross-check found both. ``solve`` must
take **all** real roots of the cubic, not just the rational ones — the largest
admissible root need not be rational — and ``check`` must handle the case where
the two curves *touch* rather than cross: at s = 2 the point is x = y = 1, a
double root where the residual never changes sign.

``solve`` finds the cubic's real roots numerically and applies the reality test.
``check`` never forms the cubic: it sweeps x, solves the circle for y, and
measures the residual of ``x³ + y³ − t``, bisecting its sign changes *and*
refining its local minima before reporting the largest sum it actually finds.
"""

from __future__ import annotations

from fractions import Fraction
from math import acos, cos, pi, sqrt

#: k(x² + y²) = c and x³ + y³ = t.
PARAMS = {"k": 3, "c": 7, "t": 3}
ANSWER = 2
#: the roots are found numerically, so an irrational answer only
#: agrees to working precision.
TOL = 1e-7
VARIANTS = [
    {"k": 1, "c": 2, "t": 2},
    {"k": 2, "c": 10, "t": 11},
    {"k": 3, "c": 7, "t": -3},
    {"k": 1, "c": 5, "t": 9},
    {"k": 3, "c": 7, "t": 100},        # no real pair at all
    {"k": 0, "c": 7, "t": 3},
]


def _snap(value: float):
    """An int or a small fraction when the value is one, else the float itself."""
    if abs(value - round(value)) < 1e-9:
        return int(round(value))
    close = Fraction(value).limit_denominator(64)
    return close if abs(float(close) - value) < 1e-9 else value


def real_roots(squares: float, t: float) -> list[float]:
    """Real s with s³ − 3·squares·s + 2t = 0, in closed form.

    The cubic is already depressed (no s² term), so Cardano applies directly:
    with p = −3·squares and q = 2t the sign of −4p³ − 27q² says how many real
    roots there are, and the three-root case is read off with cosines.
    """
    p_coef, q_coef = -3.0 * squares, 2.0 * t
    if abs(p_coef) < 1e-15 and abs(q_coef) < 1e-15:
        return [0.0]
    discriminant = -4 * p_coef ** 3 - 27 * q_coef ** 2
    if discriminant > 0:                       # three distinct real roots
        radius = 2 * sqrt(-p_coef / 3)
        inner = 3 * q_coef / (p_coef * radius)
        inner = max(-1.0, min(1.0, inner))
        angle = acos(inner) / 3
        return [radius * cos(angle - 2 * pi * k / 3) for k in (0, 1, 2)]
    if abs(discriminant) < 1e-12:              # a repeated root
        if abs(p_coef) < 1e-15:
            return [0.0]
        single = 3 * q_coef / p_coef
        double = -3 * q_coef / (2 * p_coef)
        return sorted({single, double})
    # one real root
    inner = q_coef * q_coef / 4 + p_coef ** 3 / 27
    root = sqrt(inner)
    first, second = -q_coef / 2 + root, -q_coef / 2 - root

    def cbrt(value: float) -> float:
        return (value ** (1 / 3)) if value >= 0 else -((-value) ** (1 / 3))

    return [cbrt(first) + cbrt(second)]


def solve(k=3, c=7, t=3):
    """Largest s = x + y over the real roots of the cubic that keep x, y real."""
    if k == 0:
        return None
    squares = c / k                                # x² + y²
    if squares < 0:
        return None
    good = [s for s in real_roots(squares, t) if s * s <= 2 * squares + 1e-9]
    if not good:
        return None
    return _snap(max(good))


def check(k=3, c=7, t=3):
    """Independent: sweep x, solve the circle for y, and measure the cubic.

    For each x on ``k(x² + y²) = c`` both branches of y are formed and
    ``x³ + y³ − t`` is evaluated. Sign changes are bisected, and local minima of
    the residual are refined too — without that, a tangency such as x = y = 1
    is invisible. No symmetric functions and no cubic in s appear anywhere.
    """
    if k == 0:
        return None
    squares = c / k
    if squares < 0:
        return None
    radius = sqrt(squares)

    sums = []
    for branch in (1, -1):
        def residual(x: float, branch=branch) -> float:
            return x ** 3 + (branch * sqrt(max(squares - x * x, 0.0))) ** 3 - t

        steps = 200_000
        step = 2 * radius / steps
        window = [(-radius, residual(-radius))]
        for i in range(1, steps + 1):
            x = -radius + 2 * radius * i / steps
            cur = residual(x)
            prev_x, prev = window[-1]
            hits = []
            if cur == 0.0:
                hits.append(x)
            elif prev * cur < 0:
                lo, hi = prev_x, x
                for _ in range(200):
                    mid = (lo + hi) / 2
                    if residual(lo) * residual(mid) <= 0:
                        hi = mid
                    else:
                        lo = mid
                hits.append((lo + hi) / 2)
            window.append((x, cur))
            if len(window) == 3:
                (xa, fa), (xb, fb), (xc, fc) = window
                if abs(fb) < abs(fa) and abs(fb) < abs(fc):
                    # the curves may touch here without ever crossing
                    left, right = xb - step, xb + step
                    for _ in range(200):
                        m1 = left + (right - left) / 3
                        m2 = right - (right - left) / 3
                        if abs(residual(m1)) < abs(residual(m2)):
                            right = m2
                        else:
                            left = m1
                    hits.append((left + right) / 2)
                window.pop(0)
            for hit in hits:
                y = branch * sqrt(max(squares - hit * hit, 0.0))
                if abs(hit ** 3 + y ** 3 - t) < 1e-7:
                    sums.append(hit + y)

    if not sums:
        return None
    return _snap(max(sums))
