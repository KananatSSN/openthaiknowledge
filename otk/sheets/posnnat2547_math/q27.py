"""วันที่สอง ข้อ 6 — a + b + c ≥ 1/a + 1/b + 1/c ⇒ a³ + b³ + c³ ≥ a + b + c  (พิสูจน์)

With S = Σa and the constraint Σa ≥ q²Σ(1/a): Σ1/a ≥ n²/S gives S ≥ nq, and
the power-mean inequality gives Σa³ ≥ S³/n² ≥ nq³ (equality at every a = q).
For the source (n = 3, q = 1): S ≥ 3, so Σa³ ≥ S³/9 ≥ S, which is the claim.
The solver returns the minimum of Σa³ over the constraint, n·q³.

``check`` minimises Σa³ numerically over the feasible region by coordinate
search from an asymmetric start, projecting back onto the constraint by scaling.
"""

from __future__ import annotations

PARAMS = {"n": 3, "q": 1}
ANSWER = 3
TOL = 1e-6
VARIANTS = [{"q": 2}, {"n": 2}, {"n": 4, "q": 3}, {"n": 5, "q": 1}]


def solve(n=3, q=1):
    return n * q**3


def check(n=3, q=1):
    def feasible(a):
        need = q * q * sum(1 / v for v in a)
        total = sum(a)
        if total >= need:
            return a
        scale = (need / total) ** 0.5  # scaling by λ multiplies Σa by λ and Σ1/a by 1/λ
        return [v * scale for v in a]

    a = feasible([q * (1 + 0.3 * i) for i in range(n)])
    best = sum(v**3 for v in a)
    step = 0.5 * q
    while step > 1e-9:
        improved = False
        for i in range(n):
            for sign in (1, -1):
                trial = list(a)
                trial[i] = max(trial[i] + sign * step, 1e-9)
                trial = feasible(trial)
                value = sum(v**3 for v in trial)
                if value < best - 1e-15:
                    a, best, improved = trial, value, True
        if not improved:
            step /= 2
    return best
