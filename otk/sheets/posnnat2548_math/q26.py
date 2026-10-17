"""วันที่สอง ข้อ 5 — จำนวนวิธีจัดแถวตอนบ่าย (50 คน)

The students placed so far always form a block of morning neighbours (a new
student must know someone in the block, so stands next to one of its ends).
After the first student, each one extends the block left or right: 2^(n − 1).

``check`` counts the extension orders by a dynamic programme over intervals:
ways(l, r) = ways(l + 1, r) + ways(l, r − 1), with single students as starts.
"""

from __future__ import annotations

from functools import lru_cache

PARAMS = {"n": 50}
ANSWER = 562949953421312
VARIANTS = [{"n": 1}, {"n": 2}, {"n": 8}, {"n": 30}]


def solve(n=50):
    return 2 ** (n - 1)


def check(n=50):
    @lru_cache(maxsize=None)
    def ways(left, right):
        if left == right:
            return 1
        return ways(left + 1, right) + ways(left, right - 1)

    return ways(1, n)
