"""ข้อ 5 — Σaᵢ² = Σbᵢ² ในการแข่งขันพบกันหมด 2010 คน  (พิสูจน์)

aᵢ + bᵢ = n − 1 and Σaᵢ = Σbᵢ, so Σaᵢ² − Σbᵢ² = (n − 1)(Σaᵢ − Σbᵢ) = 0. The
solver returns that difference (0).

``check`` plays a random tournament among n players and computes the sums.
"""

from __future__ import annotations

import random

PARAMS = {"n": 2010}
ANSWER = 0
VARIANTS = [{"n": 2}, {"n": 7}, {"n": 300}]


def solve(n=2010):
    return (n - 1) * 0  # Σaᵢ − Σbᵢ = 0: every game gives one win and one loss


def check(n=2010):
    rng = random.Random(n)
    wins = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            wins[i if rng.random() < 0.5 else j] += 1
    return sum(w * w for w in wins) - sum((n - 1 - w) ** 2 for w in wins)
