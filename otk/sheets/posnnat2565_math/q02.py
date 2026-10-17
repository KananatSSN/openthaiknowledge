"""ข้อ 2 — ค่าต่ำสุดของ Σ ij f(xᵢ, xⱼ)

f(xᵢ, xⱼ) = sᵢsⱼ with sᵢ = ±1 by the parity of xᵢ, and ⌈n/2⌉ of the xᵢ are odd.
Twice the sum is (Σ i·sᵢ)² − Σ i², and sums of ⌈n/2⌉ distinct indices fill an
interval, so Σ i·sᵢ reaches the least value of its parity, (n(n + 1)/2) mod 2.
The minimum is ((n(n + 1)/2 mod 2)² − Σ i²)/2 (n = 2565: −2814263707).

``check`` builds an explicit choice of ⌈n/2⌉ positions for the odd numbers with
the right sum and evaluates Σ ij f directly; for n ≤ 12 it also tries every
choice of positions.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"n": 2565}
ANSWER = -2814263707
VARIANTS = [{"n": 5}, {"n": 8}, {"n": 12}, {"n": 100}]


def solve(n=2565):
    total = n * (n + 1) // 2
    squares = n * (n + 1) * (2 * n + 1) // 6
    r = total % 2
    return (r * r - squares) // 2


def _score(n, plus):
    acc, prefix = 0, 0
    for i in range(1, n + 1):
        s = 1 if i in plus else -1
        acc += i * s * prefix
        prefix += i * s
    return acc


def check(n=2565):
    k = (n + 1) // 2
    total = n * (n + 1) // 2
    target = (total + total % 2) // 2  # sum of the plus positions
    chosen = list(range(1, k + 1))
    need = target - sum(chosen)
    for idx in range(k - 1, -1, -1):
        room = n - (k - 1 - idx) - chosen[idx]
        step = min(room, need)
        chosen[idx] += step
        need -= step
    assert need == 0 and len(set(chosen)) == k
    best = _score(n, set(chosen))
    if n <= 12:
        exhaustive = min(_score(n, set(c)) for c in combinations(range(1, n + 1), k))
        assert exhaustive == best
    return best
