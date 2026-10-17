"""ข้อ 5 — n ที่ลบด้านทีละสามด้านได้หมด

The n × n grid has 2n(n + 1) unit sides, so 3 | 2n(n + 1) is needed; a
boundary-parity argument excludes the even n other than 2, and constructions
cover n = 2 and every n ≡ 3, 5 (mod 6). The answer is the tuple of working
sizes up to `limit`.

``check`` rejects a grid whose side count is not a multiple of 3 and otherwise
searches every order of moves (memoised on the remaining sides); that is exact
for each n ≤ 4, which is as far as PARAMS goes.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

PARAMS = {"limit": 4}
ANSWER = (2, 3)
VARIANTS = [{"limit": 1}, {"limit": 2}, {"limit": 3}]


def solve(limit=4):
    return tuple(n for n in range(1, limit + 1) if n == 2 or (n >= 3 and n % 6 in (3, 5)))


def _erasable(n):
    ids = {}

    def side(key):
        return ids.setdefault(key, len(ids))

    if 2 * n * (n + 1) % 3:
        return False
    cells = [(side(("h", r, c)), side(("h", r + 1, c)), side(("v", r, c)), side(("v", r, c + 1)))
             for r in range(n) for c in range(n)]

    @lru_cache(maxsize=None)
    def go(mask):
        if mask == 0:
            return True
        for sides in cells:
            live = [e for e in sides if mask >> e & 1]
            for trio in combinations(live, 3):
                rest = mask
                for e in trio:
                    rest &= ~(1 << e)
                if go(rest):
                    return True
        return False

    return go((1 << len(ids)) - 1)


def check(limit=4):
    assert limit <= 4
    return tuple(n for n in range(1, limit + 1) if _erasable(n))
