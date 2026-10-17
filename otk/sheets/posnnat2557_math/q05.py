"""ข้อ 5 — k มากสุดที่ (k + a/b)(k + b/c)(k + c/a) ≤ (Σ a/b)(Σ b/a)

For the family with the right side scaled by c: with S = Σ a/b and T = Σ b/a
(both ≥ 3, Π a/b = 1) the left side is k³ + k²S + kT + 1, and
c·ST − k²S − kT = c(S − k/c)(T − k²/c) − k³/c, smallest at S = T = 3, so k
works iff (k + 1)³ ≤ 9c. The source (c = 1) gives ∛9 − 1.

``check`` bisects on k, testing the inequality itself over a log-spaced grid of
(b, c) with a = 1 (the grid includes a = b = c).
"""

from __future__ import annotations

PARAMS = {"scale": 1}
ANSWER = 1.080083823051904
VARIANTS = [{"scale": 2}, {"scale": 3}, {"scale": 8}]
TOL = 1e-7


def solve(scale=1):
    return (9 * scale) ** (1 / 3) - 1


def _holds(k, scale, grid):
    for b in grid:
        for c in grid:
            a = 1.0
            s = a / b + b / c + c / a
            t = b / a + c / b + a / c
            if (k + a / b) * (k + b / c) * (k + c / a) > scale * s * t + 1e-12:
                return False
    return True


def check(scale=1):
    grid = [2 ** (j / 4) for j in range(-12, 13)]
    lo, hi = 0.0, 10.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if _holds(mid, scale, grid):
            lo = mid
        else:
            hi = mid
    return lo
