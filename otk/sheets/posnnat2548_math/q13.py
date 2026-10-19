"""ข้อ 13 — k คี่ทั้งหมดที่ k + (k + 5) + ⋯ + (k + 5(m − 1)) = 1372

The sum is m(2k + d(m − 1))/2, so m(2k + 5m − 5) = 2744 = 2³·7³; running over
the divisors m, only m = 7 gives a positive odd k: 181.

``check`` searches every (m, k) with mk ≤ N.
"""

from __future__ import annotations

PARAMS = {"total": 1372, "step": 5}
ANSWER = (181,)
VARIANTS = [{"total": 438, "step": 4}, {"total": 1000, "step": 3}, {"total": 999}, {"total": 210, "step": 7}]


def solve(total=1372, step=5):
    found = []
    for m in range(1, 2 * total + 1):
        if 2 * total % m == 0:
            twice = 2 * total // m - step * (m - 1)
            if twice > 0 and twice % 2 == 0 and twice // 2 % 2 == 1:
                found.append(twice // 2)
    return tuple(sorted(found))


def check(total=1372, step=5):
    found = set()
    for m in range(1, total + 1):
        for k in range(1, total // m + 1, 2):
            s = m * k + step * m * (m - 1) // 2
            if s == total:
                found.add(k)
            if s > total:
                break
    return tuple(sorted(found))
