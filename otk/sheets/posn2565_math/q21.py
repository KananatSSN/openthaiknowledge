"""ข้อ 21 — ค่าของ a³ + b³ + c⁴ − 1/a³ + 1/b³ + 1/c⁴

กำหนดให้ a, b, c เป็นจำนวนจริง ซึ่ง b > 0 และสอดคล้องกับสมการต่อไปนี้
    a = 1 + 1/a ,  b² = 3 − 1/b² ,  c³ = 2 − 1/c³
จงหาค่าของ  a³ + b³ + c⁴ − 1/a³ + 1/b³ + 1/c⁴

The point of the item is that none of a, b, c is ever computed. Each equation
hands over one *symmetric combination*, and the requested expression is built
only out of those:

* ``a = 1 + 1/a`` says ``a − 1/a = 1``, and
  ``a³ − 1/a³ = (a − 1/a)³ + 3(a − 1/a) = 1 + 3 = 4``.
  (Both roots ``(1 ± √5)/2`` give this, so the ambiguity is harmless.)
* ``b² = 3 − 1/b²`` says ``b² + 1/b² = 3``, hence ``(b + 1/b)² = 5`` and, since
  ``b > 0``, ``b + 1/b = √5``. Then
  ``b³ + 1/b³ = (b + 1/b)³ − 3(b + 1/b) = 5√5 − 3√5 = 2√5``.
* ``c³ = 2 − 1/c³`` says ``c³ + 1/c³ = 2``, i.e. ``(c³ − 1)² = 0``, so ``c³ = 1``
  and the only real ``c`` is 1 — giving ``c⁴ + 1/c⁴ = 2``.

Note the sign pattern in the question: it is ``(a³ − 1/a³) + (b³ + 1/b³) +
(c⁴ + 1/c⁴)``, a *difference* on the first bracket and sums on the other two.

    4 + 2√5 + 2 = **6 + 2√5** ≈ 10.4721

In general, with ``a − 1/a = m``, ``b² + 1/b² = s`` and ``c³ + 1/c³ = t``, the
value is ``m³ + 3m + (s − 1)√(s + 2) + u^(4/3) + u^(−4/3)`` where ``u`` solves
``u + 1/u = t``. The last piece is unambiguous even when ``t > 2``: the two roots
of that quadratic are ``u`` and ``1/u``, which the expression treats alike.

``solve`` uses those closed forms; ``check`` never touches them — it solves each
printed equation numerically for every real root and evaluates the expression on
each, refusing to answer unless they all agree.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt, sqrt

#: a − 1/a = m, b² + 1/b² = s, c³ + 1/c³ = t (the sheet: 1, 3, 2).
PARAMS = {"m": 1, "s": 3, "t": 2}
ANSWER = 10.47213595499958
TOL = 1e-9
VARIANTS = [
    {"m": 2, "s": 3, "t": 2},
    {"m": 1, "s": 7, "t": 2},
    {"m": -3, "s": 2, "t": 2},        # b² + 1/b² = 2 forces b = 1
    {"m": 1, "s": 3, "t": 5},         # c³ ≠ 1, but c⁴ + 1/c⁴ is still pinned
    {"m": 0, "s": 14, "t": 3},
    {"m": 1, "s": 1, "t": 2},         # no real b at all
    {"m": 1, "s": 3, "t": 1},         # no real c at all
]


def exact_form(m=1, s=3, t=2):
    """(rational part, surd coefficient, radicand) when the answer is p + q√d.

    Only available where c³ = 1 (t = 2); returns None otherwise, and the surd is
    reduced to (q, d) with d square-free-ish — enough for the generator's TeX.
    """
    if t != 2 or s < 2:
        return None
    rational = Fraction(m ** 3 + 3 * m + 2)
    coef, rad = Fraction(s - 1), s + 2
    root = isqrt(rad)
    if root * root == rad:                       # the surd collapses
        return rational + coef * root, Fraction(0), 0
    for factor in range(isqrt(rad), 1, -1):
        if rad % (factor * factor) == 0:
            coef, rad = coef * factor, rad // (factor * factor)
            break
    return rational, coef, rad


def solve(m=1, s=3, t=2):
    """The value of the expression, from the three symmetric combinations."""
    if s < 2 or t < 2:            # b² + 1/b² ≥ 2 and c³ + 1/c³ ≥ 2 for real b, c
        return None
    first = m ** 3 + 3 * m                       # a³ − 1/a³
    w = sqrt(s + 2)
    second = w ** 3 - 3 * w                      # b³ + 1/b³
    u = (t + sqrt(t * t - 4)) / 2                # c³
    third = u ** Fraction(4, 3) + u ** Fraction(-4, 3)
    return float(first + second + third)


def check(m=1, s=3, t=2):
    """Independent: find every real a, b, c from the printed equations and evaluate.

    Each equation is turned back into the polynomial the sheet prints
    (a² − ma − 1 = 0, b⁴ − sb² + 1 = 0, c⁶ − tc³ + 1 = 0), its real roots are
    located by bisection on a dense sweep, and the expression is computed
    directly from the numbers. Nothing here knows that a − 1/a is m or that
    b + 1/b is √(s+2); if the value depended on *which* root was taken, the
    disagreement would surface as None.
    """
    def real_roots(f, lo=-50.0, hi=50.0, steps=200_000):
        found, prev, px = [], f(lo), lo
        for i in range(1, steps + 1):
            x = lo + (hi - lo) * i / steps
            cur = f(x)
            if cur == 0.0:
                found.append(x)
            elif prev * cur < 0:
                a_, b_ = px, x
                for _ in range(200):
                    mid = (a_ + b_) / 2
                    if f(a_) * f(mid) <= 0:
                        b_ = mid
                    else:
                        a_ = mid
                found.append((a_ + b_) / 2)
            prev, px = cur, x
        return found

    a_roots = [x for x in real_roots(lambda x: x * x - m * x - 1)
               if abs(x) > 1e-9]
    b_roots = [x for x in real_roots(lambda x: x ** 4 - s * x * x + 1)
               if x > 1e-9]
    c_roots = [x for x in real_roots(lambda x: x ** 6 - t * x ** 3 + 1)
               if abs(x) > 1e-9]
    if not a_roots or not b_roots or not c_roots:
        return None

    values = [a ** 3 - 1 / a ** 3 + b ** 3 + 1 / b ** 3 + c ** 4 + 1 / c ** 4
              for a in a_roots for b in b_roots for c in c_roots]
    if max(values) - min(values) > 1e-6:
        return None
    return float(sum(values) / len(values))
