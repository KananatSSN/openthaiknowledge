"""ข้อ 18 — สั่งอาหารกล่องให้ครบงบพอดี

งบประมาณ 39,600 บาท ต้องใช้ให้หมดพอดี  ราคากล่องละ 90 / 60 / 30 บาท
เงื่อนไข: จำนวนกล่องรวมไม่เกิน 580 กล่อง และจำนวนกล่องราคาถูกที่สุดต้องมีอย่างน้อย
2 เท่าของกล่องราคากลาง  โรงเรียนต้องสั่งกล่องราคาแพงที่สุดอย่างน้อยที่สุดกี่กล่อง

Method: relax to the reals first. Writing the budget as p1·x + p2·y + p3·z = B
and eliminating z, the box cap becomes a lower bound on 2x + y and the ratio
condition an upper bound on y; combining them removes y entirely and leaves a
single inequality in x. For the sheet's numbers that is 5x ≥ 1640, so x ≥ 328 —
and x = 328 is attainable (y = 84, z = 168, exactly 580 boxes).

``solve`` computes that relaxation bound and searches upward from it. ``check``
ignores the bound entirely and scans every (x, y) from zero — which is exactly
what would expose a bound that skipped a feasible smaller x, so the two together
police each other rather than ``solve`` re-checking its own work.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"p1": 90, "p2": 60, "p3": 30, "budget": 39600, "max_boxes": 580,
          "ratio": 2}
ANSWER = 328
VARIANTS = [
    {"budget": 30000, "max_boxes": 450},
    {"ratio": 1},
    {"ratio": 3},
    {"p1": 100, "p2": 50, "p3": 25, "budget": 20000, "max_boxes": 500},
    {"budget": 39600, "max_boxes": 700},
]


def feasible(x, p1=90, p2=60, p3=30, budget=39600, max_boxes=580, ratio=2):
    """A (y, z) completing this x, or None."""
    rest = budget - p1 * x
    if rest < 0:
        return None
    for y in range(rest // p2 + 1):
        left = rest - p2 * y
        if left % p3:
            continue
        z = left // p3
        if z >= ratio * y and x + y + z <= max_boxes:
            return (y, z)
    return None


def lower_bound(p1=90, p2=60, p3=30, budget=39600, max_boxes=580, ratio=2):
    """Real relaxation: the smallest x any solution can have.

    From p1·x + p2·y + p3·z = B, the total is x + y + z = x + (B − p1·x −
    (p3−p2)·y)/p3 … eliminating z through both constraints leaves a linear
    bound; solved for x below.
    """
    b, m, r = Fraction(budget), Fraction(max_boxes), Fraction(ratio)
    p1, p2, p3 = Fraction(p1), Fraction(p2), Fraction(p3)
    # box cap:  x + y + (B − p1x − p2y)/p3 ≤ m   ⟹  y(p3 − p2) ≥ …
    # ratio:    (B − p1x − p2y)/p3 ≥ r·y         ⟹  y ≤ (B − p1x)/(p2 + r·p3)
    # Substituting the ratio bound into the cap gives one inequality in x.
    cap_coef = 1 - p1 / p3                       # coefficient of x in the cap
    y_coef = 1 - p2 / p3                         # coefficient of y in the cap
    slack = m - b / p3
    y_max_num, y_max_den = (b, p2 + r * p3)      # y ≤ (B − p1x)/(p2 + r·p3)
    if y_coef >= 0:                              # cap does not bind through y
        return 0
    # cap:  cap_coef·x + y_coef·y ≤ slack, worst case at the largest y
    #       cap_coef·x + y_coef·(B − p1·x)/(p2 + r·p3) ≤ slack
    a = cap_coef - y_coef * p1 / y_max_den
    c = slack - y_coef * y_max_num / y_max_den
    if a == 0:
        return 0
    bound = c / a if a > 0 else c / a
    return max(0, -(-bound.numerator // bound.denominator)) if a < 0 else 0


def solve(p1=90, p2=60, p3=30, budget=39600, max_boxes=580, ratio=2):
    """Fewest boxes of the most expensive item, or None if nothing fits."""
    start = lower_bound(p1, p2, p3, budget, max_boxes, ratio)
    for x in range(start, budget // p1 + 1):
        if feasible(x, p1, p2, p3, budget, max_boxes, ratio):
            return x
    return None


def check(p1=90, p2=60, p3=30, budget=39600, max_boxes=580, ratio=2):
    """Independent: scan every (x, y) from zero, no bound, no pruning."""
    for x in range(budget // p1 + 1):
        rest = budget - p1 * x
        for y in range(rest // p2 + 1):
            left = rest - p2 * y
            if left % p3 == 0:
                z = left // p3
                if z >= ratio * y and x + y + z <= max_boxes:
                    return x
    return None
