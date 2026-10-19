"""ข้อ 7 — Σ|f(k) − f(−k)| มากสุด ⇔ f(k)f(−k) < 0 ทุก k  (พิสูจน์)

Σ(larger) − Σ(smaller) over n pairs is at most (1 + ⋯ + n) − (−1 − ⋯ − n) =
n(n + 1), reached exactly when the n larger values are 1..n and the smaller
−1..−n: f(0) = 0 and each pair takes one sign each. Those bijections number
n!²·2ⁿ. The answer is (maximum, number of maximisers); the source has
n = 2562, PARAMS uses n = 3 so that ``check`` can try every bijection.

``check`` runs over all bijections of {−n, …, n}, takes the maximum, counts the
maximisers and asserts each has f(k)f(−k) < 0 for every k.
"""

from __future__ import annotations

from itertools import permutations
from math import factorial

PARAMS = {"n": 3}
ANSWER = (12, 288)
VARIANTS = [{"n": 1}, {"n": 2}, {"n": 4}]


def solve(n=3):
    return (n * (n + 1), factorial(n) ** 2 * 2**n)


def check(n=3):
    domain = list(range(-n, n + 1))
    best, hits = -1, []
    for image in permutations(domain):
        f = dict(zip(domain, image))
        total = sum(abs(f[k] - f[-k]) for k in range(1, n + 1))
        if total > best:
            best, hits = total, [f]
        elif total == best:
            hits.append(f)
    assert all(f[k] * f[-k] < 0 for f in hits for k in range(1, n + 1))
    return (best, len(hits))
