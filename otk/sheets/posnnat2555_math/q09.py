"""ข้อ 9 — P(x) ≥ (x + 1)ⁿ เมื่อ x > 0 และ P มีรากจริงทั้งหมด  (พิสูจน์)

The roots are −rᵢ with rᵢ > 0 and Πrᵢ = 1, so P(t) = Π(t + rᵢ) ≥
(t + (Πrᵢ)^(1/n))ⁿ = (t + 1)ⁿ by Hölder. The solver returns the minimum of P(t)
over such polynomials (n = 4, t = 2: 81).

``check`` minimises Π(t + rᵢ) numerically over positive rᵢ with product 1.
"""

from __future__ import annotations

import math

PARAMS = {"n": 4, "t": 2}
ANSWER = 81
TOL = 1e-7
VARIANTS = [{"n": 2, "t": 1}, {"n": 3, "t": 5}, {"n": 5, "t": 1}]


def solve(n=4, t=2):
    return (t + 1) ** n


def check(n=4, t=2):
    def value(logs):
        roots = [math.exp(v) for v in logs] + [math.exp(-sum(logs))]
        return math.prod(t + r for r in roots)

    logs = [0.3 * (i + 1) for i in range(n - 1)]
    best, step = value(logs), 0.5
    while step > 1e-12:
        improved = False
        for i in range(n - 1):
            for sign in (1, -1):
                trial = list(logs)
                trial[i] += sign * step
                val = value(trial)
                if val < best:
                    logs, best, improved = trial, val, True
        if not improved:
            step /= 2
    return best
