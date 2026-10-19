"""ข้อ 5 — เซตคำตอบของ Σₖ₌₁²ⁿ √(x² − 2kx + k²) = |2nx − n − 2n²|

The left side is Σ|x − k| and the right side is |Σ(x − k)|; the triangle
inequality is an equality iff every x − k has the same sign: x ≤ 1 or x ≥ 2n.
The answer (1, 2n) encodes (−∞, 1] ∪ [2n, ∞). The sheet states a general n;
PARAMS fixes n = 5 to have a number to check.

``check`` samples x on a fine grid and reads off where equality holds.
"""

from __future__ import annotations

PARAMS = {"n": 5}
ANSWER = (1, 10)
VARIANTS = [{"n": 1}, {"n": 2}, {"n": 7}, {"n": 12}]


def solve(n=5):
    return (1, 2 * n)


def check(n=5):
    holds = []
    for i in range(-400, 4 * n * 100 + 400):
        x = i / 100
        lhs = sum(abs(x - k) for k in range(1, 2 * n + 1))
        if abs(lhs - abs(2 * n * x - n - 2 * n * n)) < 1e-9:
            holds.append(x)
    left = max(x for x in holds if x < n + 0.5)
    right = min(x for x in holds if x > n + 0.5)
    return (round(left), round(right))
