"""ข้อ 17 — ค่าของ f(−1) − 4f(0)

กำหนดให้ f(x) = x⁴ + ax³ + bx² + cx + d เมื่อ a, b, c, d เป็นจำนวนจริง และสำหรับ
แต่ละ k = 1, 2, 3 เศษที่ได้จากการหาร f(x) ด้วย x − k เท่ากับ k²
จงหาค่าของ f(−1) − 4f(0)

The remainder theorem turns the three conditions into f(k) = k², so
g(x) = f(x) − x² is monic of degree four with roots 1, 2 and 3:

    f(x) = x² + (x-1)(x-2)(x-3)(x-r)

for an unknown r — the quartic is **not** determined. But

    f(-1) = 1 + (-2)(-3)(-4)(-1-r) = 25 + 24r
    f(0)  = 0 + (-1)(-2)(-3)(0-r)  = 6r

and 25 + 24r − 4·6r = **25**: the multiplier 4 is exactly what makes r cancel.
That is the item. With nodes n₁, n₂, n₃ and remainders R(k) it generalises to

    m = P(-1)/P(0),   answer = R(-1) - P(-1) - m·R(0),   P(x) = Π(x - nᵢ)

and only that m kills the free root. ``solve`` returns ``None`` when m is not a
whole number, since the question would then have to print a fraction as its own
multiplier.
"""

from __future__ import annotations

from fractions import Fraction

#: the three nodes, the remainder quadratic R(x) = r2·x² + r1·x + r0.
PARAMS = {"nodes": (1, 2, 3), "r2": 1, "r1": 0, "r0": 0}
ANSWER = Fraction(25)
VARIANTS = [
    {"nodes": (1, 2, 3), "r2": 0, "r1": 1, "r0": 0},
    {"nodes": (1, 2, 3), "r2": 2, "r1": -1, "r0": 5},
    {"nodes": (1, 2, 4), "r2": 1, "r1": 0, "r0": 0},
    {"nodes": (2, 3, 4), "r2": 1, "r1": 0, "r0": 0},
    {"nodes": (1, 2, 5), "r2": 1, "r1": 0, "r0": 0},
    {"nodes": (0, 1, 2), "r2": 1, "r1": 0, "r0": 0},     # P(0) = 0: no multiplier
]


def _p(x, nodes):
    out = Fraction(1)
    for n in nodes:
        out *= x - n
    return out


def multiplier(nodes=(1, 2, 3)):
    """The m for which f(-1) - m·f(0) no longer depends on the free root."""
    p0 = _p(0, nodes)
    if p0 == 0 or len(set(nodes)) != 3:
        return None
    m = _p(-1, nodes) / p0
    return m if m.denominator == 1 else None


def solve(nodes=(1, 2, 3), r2=1, r1=0, r0=0):
    """f(-1) - m·f(0) = R(-1) - P(-1) - m·R(0)."""
    m = multiplier(nodes)
    if m is None:
        return None

    def r(x):
        return r2 * x * x + r1 * x + r0

    return Fraction(r(-1)) - _p(-1, nodes) - m * r(0)


def check(nodes=(1, 2, 3), r2=1, r1=0, r0=0):
    """Independent: build the quartic at several free roots and evaluate it.

    For each candidate r the polynomial f(x) = R(x) + Π(x-nᵢ)·(x-r) is written
    out and its remainders on division by x - nᵢ are confirmed to be R(nᵢ) — the
    condition as the question states it — before f(-1) - m·f(0) is computed.
    Agreement across unrelated r is the claim being tested.
    """
    m = multiplier(nodes)
    if m is None:
        return None

    def r(x):
        return Fraction(r2) * x * x + r1 * x + r0

    values = set()
    for free in (Fraction(0), Fraction(7), Fraction(-5, 3), Fraction(11, 2)):
        def f(x, free=free):
            return r(x) + _p(x, nodes) * (x - free)

        for n in nodes:                       # remainder on division by x - n
            assert f(Fraction(n)) == r(n)
        values.add(f(Fraction(-1)) - m * f(Fraction(0)))
    if len(values) != 1:
        return None
    return next(iter(values))
