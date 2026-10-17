"""วันที่สอง ข้อ 1 — หาฟังก์ชัน f ทั้งหมดที่ Σf(xᵢ + xᵢ₊₁) + f(Σxᵢ) ≤ Σf(2xᵢ)  (2550 ตัวแปร)

With g = f − f(0) and an even number n ≥ 4 of variables: x₁ = x₂ = a, the rest
0, gives g(a) ≤ 0; the alternating x = (t, −t, …) gives 0 ≤ g(2t) + g(−2t);
so g ≡ 0 and f is constant. The solver states the consequence on the
quadratic family f(x) = αx² + βx + γ: only α = β = 0 survives, answer (0, 0).

``check`` tests the inequality for every (α, β) on a grid against the
substitutions above and random vectors, and returns the survivors.
"""

from __future__ import annotations

import random

PARAMS = {"n_vars": 2550}
ANSWER = (0, 0)
VARIANTS = [{"n_vars": 4}, {"n_vars": 6}, {"n_vars": 10}]


def solve(n_vars=2550):
    return (0, 0)


def check(n_vars=2550):
    rng = random.Random(1)
    tests = []
    for a in (-2.0, -0.5, 0.7, 3.0):
        tests.append([a, a] + [0.0] * (n_vars - 2))
    for t in (-1.5, 0.4, 2.0):
        tests.append([t if i % 2 == 0 else -t for i in range(n_vars)])
    for _ in range(5):
        tests.append([rng.uniform(-3, 3) for _ in range(n_vars)])
    survivors = []
    for alpha in (-2, -1, 0, 1, 2):
        for beta in (-2, -1, 0, 1, 2):
            def f(x, alpha=alpha, beta=beta):
                return alpha * x * x + beta * x + 5

            ok = all(
                sum(f(u + v) for u, v in zip(xs, xs[1:])) + f(sum(xs)) <= sum(f(2 * u) for u in xs) + 1e-6
                for xs in tests
            )
            if ok:
                survivors.append((alpha, beta))
    assert len(survivors) == 1
    return survivors[0]
