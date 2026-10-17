"""ข้อ 5 — AC เมื่อ ∠A = 90°, D บน AC, AF ⟂ BC และ BD = DC = CF = 2

CF = AC²/BC (similar triangles) and BD² = AB² + (AC − t)² = t² with t = 2 give
BC = AC²/t and AC⁴/t² − AC² + (AC − t)² = t², i.e. AC³ = 2t³: AC = 2∛2.

``check`` bisects AC on the original equations f(x) = x⁴/t² − x² + (x − t)² − t².
"""

from __future__ import annotations

PARAMS = {"t": 2}
ANSWER = 2 * 2 ** (1 / 3)
TOL = 1e-9
VARIANTS = [{"t": 1}, {"t": 5}, {"t": 13}]


def solve(t=2):
    return t * 2 ** (1 / 3)


def check(t=2):
    def f(x):
        return x**4 / t**2 - x * x + (x - t) ** 2 - t * t

    lo, hi = float(t), 3.0 * t
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(lo) < 0) == (f(mid) < 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
