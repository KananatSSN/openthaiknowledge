"""ข้อ 21 — ค่าต่ำสุดของ cos(α − β) + cos(β − γ) + cos(γ − α)

|Σ e^{iθ}|² = n + 2Σ_{i<j} cos(θᵢ − θⱼ) ≥ 0, with equality for equally spaced
angles, so the minimum is −n/2 = −3/2.

``check`` minimises over a grid of angles (θ₁ = 0) and refines by local search.
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import combinations, product

PARAMS = {"n": 3}
ANSWER = Fraction(-3, 2)
TOL = 1e-8
VARIANTS = [{"n": 2}, {"n": 4}, {"n": 5}]


def solve(n=3):
    return Fraction(-n, 2)


def check(n=3):
    def value(th):
        return sum(math.cos(a - b) for a, b in combinations(th, 2))

    steps = 12
    grid = [2 * math.pi * i / steps for i in range(steps)]
    best = min((value((0.0,) + rest), (0.0,) + rest) for rest in product(grid, repeat=n - 1))
    th, step = list(best[1]), 0.2
    current = best[0]
    while step > 1e-10:
        improved = False
        for i in range(1, n):
            for sign in (1, -1):
                trial = list(th)
                trial[i] += sign * step
                v = value(trial)
                if v < current:
                    th, current, improved = trial, v, True
        if not improved:
            step /= 2
    return current
