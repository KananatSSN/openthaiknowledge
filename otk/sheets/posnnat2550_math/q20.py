"""วันที่สอง ข้อ 2 — ต้องมีกลุ่มชาย k หญิง n − k ที่ได้พวงมาลัยอย่างน้อย m พวง  (พิสูจน์)

Boys and girls each hold C = Σcⱼ ≥ m garlands in all. A random group of k boys
and n − k girls holds kC/n + (n − k)C/n = C on average, so some group holds at
least m. The solver returns the average C (couples 3, 1, 4 → 8).

``check`` deals the garlands to named students (a fixed shuffle), then averages
over every group exactly.
"""

from __future__ import annotations

import random
from fractions import Fraction
from itertools import combinations

PARAMS = {"couples": (3, 1, 4), "n": 6, "k": 5}
ANSWER = 8
VARIANTS = [{"couples": (1, 1, 1, 1), "n": 4, "k": 2}, {"couples": (5, 2), "n": 5, "k": 1}, {"couples": (2, 6, 3), "n": 7, "k": 3}]


def solve(couples=(3, 1, 4), n=6, k=5):
    return Fraction(sum(couples))


def check(couples=(3, 1, 4), n=6, k=5):
    rng = random.Random(7)
    boys, girls = [0] * n, [0] * n
    for c in couples:
        for i in rng.sample(range(n), c):
            boys[i] += 1
        for i in rng.sample(range(n), c):
            girls[i] += 1
    groups = [sum(boys[i] for i in bs) + sum(girls[j] for j in gs)
              for bs in combinations(range(n), k) for gs in combinations(range(n), n - k)]
    assert max(groups) >= len(couples)
    return Fraction(sum(groups), len(groups))
