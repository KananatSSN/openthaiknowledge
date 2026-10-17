"""วันที่สอง ข้อ 6 — 1 + 3/(ab + bc + ca) ≥ 6/(a + b + c)  (พิสูจน์)

ab + bc + ca ≤ S²/3, so the left side is at least 1 + 9/S², and
1 + 9/S² − 6/S = (1 − 3/S)² ≥ 0. For t + u/(ab + bc + ca) ≥ k/(a + b + c) the
best constant is k = 2√(3tu); the source has t = 1, u = 3, k = 6.

``check`` minimises (t + u/(ab + bc + ca))·(a + b + c) numerically by
coordinate search from an asymmetric start.
"""

from __future__ import annotations

import math

PARAMS = {"t": 1, "u": 3}
ANSWER = 6
TOL = 1e-6
VARIANTS = [{"t": 3, "u": 4}, {"t": 2, "u": 6}, {"t": 1, "u": 12}]


def solve(t=1, u=3):
    return 2 * math.sqrt(3 * t * u)


def check(t=1, u=3):
    def value(v):
        a, b, c = v
        return (t + u / (a * b + b * c + c * a)) * (a + b + c)

    v, best, step = [0.5, 1.0, 2.0], None, 0.5
    best = value(v)
    while step > 1e-11:
        improved = False
        for i in range(3):
            for sign in (1, -1):
                trial = list(v)
                trial[i] = max(trial[i] + sign * step, 1e-9)
                val = value(trial)
                if val < best:
                    v, best, improved = trial, val, True
        if not improved:
            step /= 2
    return best
