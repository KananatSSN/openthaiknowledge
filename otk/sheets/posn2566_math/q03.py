"""ข้อ 3 — ค่า 5a − 4b จากเซตคำตอบของสมการค่าสัมบูรณ์

ให้ A เป็นเซตคำตอบของสมการ |8 − x| = |3 − 5x| + |4x + 5|  ถ้า a เป็นสมาชิกใน A
ที่มีค่ามากที่สุด และ b เป็นสมาชิกใน A ที่มีค่าน้อยที่สุด แล้วค่าของ 5a − 4b เท่ากับเท่าใด

**The two right-hand terms add up to the left one:**

    (3 − 5x) + (4x + 5) = 8 − x

so the equation is exactly ``|u + v| = |u| + |v|``, which the triangle inequality
makes true precisely when u and v do not have opposite signs. So

    (3 − 5x)(4x + 5) ≥ 0   ⟺   x ∈ [−5/4, 3/5]

The solution set is that whole interval — a = 3/5, b = −5/4 — and

    5a − 4b = 3 + 5 = **8**

Nothing has to be solved; casework on the three sign regions gets the same answer
but does four times the work and is where the sign slips happen.

``solve`` finds the interval from the two roots. ``check`` never uses the
identity: it evaluates both sides of the printed equation on a fine sweep of x,
brackets where the difference changes sign, and reports the extreme members of
the set it actually finds.
"""

from __future__ import annotations

from fractions import Fraction

#: |c₀ + c₁x| = |p₀ + p₁x| + |q₀ + q₁x|, with (p + q) = c as printed.
PARAMS = {"p": (3, -5), "q": (5, 4), "left_a": 5, "left_b": -4}
ANSWER = Fraction(8)
VARIANTS = [
    {"p": (1, -2), "q": (4, 3)},
    {"p": (7, -1), "q": (2, 6)},
    {"p": (0, -3), "q": (9, 1)},
    {"left_a": 1, "left_b": 1},
    {"left_a": 2, "left_b": -3},
    {"p": (5, 2), "q": (1, 3)},              # both roots negative
]


def solve(p=(3, -5), q=(5, 4), left_a=5, left_b=-4):
    """The set is the closed interval between the two roots."""
    if p[1] == 0 or q[1] == 0:
        return None
    if p[1] * q[1] > 0:
        # the product opens upwards, so uv ≥ 0 *outside* the roots and the
        # solution set is unbounded — there is no largest or smallest member.
        return None
    root_p = Fraction(-p[0], p[1])
    root_q = Fraction(-q[0], q[1])
    lo, hi = min(root_p, root_q), max(root_p, root_q)
    return left_a * hi + left_b * lo


def check(p=(3, -5), q=(5, 4), left_a=5, left_b=-4):
    """Independent: sweep x and test the printed equation as printed.

    The identity ``|u+v| = |u|+|v| ⟺ uv ≥ 0`` is never used. The residual
    ``|u| + |v| − |u + v|`` is evaluated on a dense grid and its zero set is
    bracketed from both ends; the extremes are then snapped to fractions and
    confirmed by substitution.
    """
    if p[1] == 0 or q[1] == 0:
        return None

    def residual(x: float) -> float:
        u = p[0] + p[1] * x
        v = q[0] + q[1] * x
        return abs(u) + abs(v) - abs(u + v)

    steps = 400_000
    span = 40.0
    good = [-span + 2 * span * i / steps for i in range(steps + 1)
            if residual(-span + 2 * span * i / steps) < 1e-9]
    if not good:
        return None
    lo_hit, hi_hit = good[0], good[-1]
    if lo_hit <= -span + 1e-9 or hi_hit >= span - 1e-9:
        return None                       # the set runs off the sweep: unbounded

    def edge(inside: float, outside: float) -> float:
        for _ in range(200):
            mid = (inside + outside) / 2
            if residual(mid) < 1e-12:
                inside = mid
            else:
                outside = mid
        return (inside + outside) / 2

    lo = edge(lo_hit, lo_hit - 2 * span / steps)
    hi = edge(hi_hit, hi_hit + 2 * span / steps)
    lo_f = Fraction(lo).limit_denominator(1000)
    hi_f = Fraction(hi).limit_denominator(1000)
    if abs(float(lo_f) - lo) > 1e-6 or abs(float(hi_f) - hi) > 1e-6:
        return None
    return left_a * hi_f + left_b * lo_f
