"""ข้อ 2 — (x − a₁)⋯(x − a₂₀₁₂) = (1006!)² มีรากจำนวนเต็มได้อย่างมาก 1 ค่า  (พิสูจน์)

At most two of the x − aᵢ share an absolute value, so sorted by absolute value
the i-th is at least ⌈i/2⌉ and |Π| ≥ (k!)²(k + 1 if 2k + 1 terms). An integer
root forces {x − aᵢ} = {±1, …, ±k}, and two roots would give two shifts of the
same set. The solver returns the least |product| of `count` distinct non-zero
integers (6: 36).

``check`` searches every set of `count` distinct non-zero integers in a window.
"""

from __future__ import annotations

from itertools import combinations
from math import factorial, prod

PARAMS = {"count": 6}
ANSWER = 36
VARIANTS = [{"count": 1}, {"count": 3}, {"count": 5}]


def solve(count=6):
    k, odd = divmod(count, 2)
    return factorial(k) ** 2 * (k + 1 if odd else 1)


def check(count=6):
    window = [v for v in range(-count, count + 1) if v]
    return min(abs(prod(c)) for c in combinations(window, count))
