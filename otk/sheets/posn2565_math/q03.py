"""ข้อ 3 — ค่าที่เป็นไปได้ทั้งหมดของ 5a − 4b + 3c − 2d

กำหนดให้ a, b, c และ d เป็นจำนวนจริงซึ่งสอดคล้องกับระบบสมการ
    a − 2b + 3c − 4d = 5
    4a − 3b + 2c − d = 10
จงหาค่าที่เป็นไปได้ทั้งหมดของ 5a − 4b + 3c − 2d

Two equations in four unknowns leave a two-parameter family, so the target is
determined **only if its coefficient row is a linear combination of the two given
rows**. Here it is:

    (5,−4,3,−2) = (1/5)(1,−2,3,−4) + (6/5)(4,−3,2,−1)

and therefore the value is forced to (1/5)(5) + (6/5)(10) = 1 + 12 = **13**,
whatever a, b, c, d happen to be.

``solve`` finds the two multipliers from a 2×2 sub-system and then *verifies* the
combination reproduces all four coefficients — without that check it would return
a number for a target that is actually free to be anything. ``check`` never looks
at the rows: it generates many different solutions of the system and evaluates
the target on each, returning the common value only if they all agree.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

#: the two given rows with their right-hand sides, and the row being asked for.
PARAMS = {"row1": (1, -2, 3, -4), "rhs1": 5,
          "row2": (4, -3, 2, -1), "rhs2": 10,
          "target": (5, -4, 3, -2)}
ANSWER = Fraction(13)
VARIANTS = [
    {"target": (5, -5, 5, -5)},                     # r1 + r2: forced
    {"target": (1, 0, 0, 0)},                       # not a combination: free
    {"rhs1": 2, "rhs2": -3},
    {"row2": (2, -4, 6, -8), "rhs2": 10},           # r2 = 2·r1: target now free
    {"row2": (2, -4, 6, -8), "rhs2": 11},           # …and here, inconsistent
    {"row2": (2, -4, 6, -8), "rhs2": 10,
     "target": (3, -6, 9, -12)},                    # a multiple of the one row
    {"target": (9, -8, 7, -6)},
]


def _multiple(row, target):
    """λ with λ·row = target, or None."""
    lam = None
    for r, t in zip(row, target):
        if r == 0:
            if t != 0:
                return None
            continue
        cur = Fraction(t, r)
        if lam is not None and cur != lam:
            return None
        lam = cur
    return Fraction(0) if lam is None else lam


def _combination(row1, row2, target):
    """(α, β) with α·row1 + β·row2 = target, or None if there is no such pair."""
    n = len(target)
    for i in range(n):
        for j in range(i + 1, n):
            det = row1[i] * row2[j] - row1[j] * row2[i]
            if det == 0:
                continue
            a = Fraction(target[i] * row2[j] - target[j] * row2[i], det)
            b = Fraction(row1[i] * target[j] - row1[j] * target[i], det)
            if all(a * row1[k] + b * row2[k] == target[k] for k in range(n)):
                return a, b
            return None                     # a unique candidate, and it failed
    return None                             # the two rows are dependent


def solve(row1=(1, -2, 3, -4), rhs1=5, row2=(4, -3, 2, -1), rhs2=10,
          target=(5, -4, 3, -2)):
    """The forced value of the target row, or None when it is not determined."""
    if len(row1) != len(row2) != len(target):
        return None
    combo = _combination(row1, row2, target)
    if combo is not None:
        a, b = combo
        return a * rhs1 + b * rhs2

    # Dependent rows: the two equations are one equation (or none), so the
    # target is forced only if it is a multiple of that single row — and the
    # system has to be consistent in the first place.
    base, base_rhs = (row1, rhs1) if any(row1) else (row2, rhs2)
    if not any(base):
        return Fraction(0) if rhs1 == rhs2 == 0 and not any(target) else None
    for other, other_rhs in ((row1, rhs1), (row2, rhs2)):
        mu = _multiple(base, other)
        if mu is None or mu * base_rhs != other_rhs:
            return None                     # inconsistent: no solutions at all
    lam = _multiple(base, target)
    return None if lam is None else lam * base_rhs


def check(row1=(1, -2, 3, -4), rhs1=5, row2=(4, -3, 2, -1), rhs2=10,
          target=(5, -4, 3, -2)):
    """Independent: build actual solutions of the system and evaluate the target.

    The augmented matrix is row-reduced exactly, the free variables are swept
    over a grid and the pivots solved for, giving genuinely different points of
    the solution set; if the target takes the same value at all of them it is
    forced, and if it does not it is free. Nothing here inspects the coefficient
    rows for a linear combination, and an inconsistent system is detected as a
    zero row with a non-zero right-hand side rather than by a special case.
    """
    n = len(target)
    if len(row1) != len(row2) != n:
        return None
    # Exact row reduction of [row1 | rhs1 ; row2 | rhs2].
    mat = [[Fraction(v) for v in row1] + [Fraction(rhs1)],
           [Fraction(v) for v in row2] + [Fraction(rhs2)]]
    pivots: list[int] = []
    r = 0
    for col in range(n):
        pick = next((i for i in range(r, len(mat)) if mat[i][col] != 0), None)
        if pick is None:
            continue
        mat[r], mat[pick] = mat[pick], mat[r]
        lead = mat[r][col]
        mat[r] = [v / lead for v in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][col] != 0:
                f = mat[i][col]
                mat[i] = [a - f * b for a, b in zip(mat[i], mat[r])]
        pivots.append(col)
        r += 1
    if any(all(row[k] == 0 for k in range(n)) and row[n] != 0 for row in mat):
        return None                                   # no solutions at all

    free = [c for c in range(n) if c not in pivots]
    values = set()
    for combo in itertools.product((Fraction(0), Fraction(4), Fraction(-9, 2)),
                                   repeat=len(free)):
        x = [Fraction(0)] * n
        for col, val in zip(free, combo):
            x[col] = val
        for i, col in enumerate(pivots):
            x[col] = mat[i][n] - sum(mat[i][c] * x[c] for c in free)
        assert sum(Fraction(row1[k]) * x[k] for k in range(n)) == rhs1
        assert sum(Fraction(row2[k]) * x[k] for k in range(n)) == rhs2
        values.add(sum(Fraction(target[k]) * x[k] for k in range(n)))
    if len(values) != 1:
        return None
    return next(iter(values))
