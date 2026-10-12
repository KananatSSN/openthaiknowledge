"""ข้อ 19 — จำนวนสับเซตที่ผลบวกของสมาชิกเท่ากับค่าที่กำหนด

กำหนดให้ A = {1, 2, ..., 67}  จงหาจำนวนของสับเซต H ทั้งหมดของเซต A โดยที่ผลบวก
ของสมาชิกทั้งหมดในเซต H มีค่าเท่ากับ 2272

The whole of A sums to 67·68/2 = 2278, so a subset summing to 2272 is exactly the
complement of a subset summing to **6**, and the count is the number of ways to
write 6 as a sum of distinct positive integers no larger than 67:

    6 = 6 = 1+5 = 2+4 = 1+2+3      →  **4**

Choosing the target so close to the total is the whole trick: the direct count is
a 67 × 2272 table, while the complement is four lines of paper.

``solve`` walks the complement's partitions into distinct parts; ``check`` runs
the full subset-sum DP against the *stated* target, so the two only agree if the
complement identity really holds and neither miscounts.
"""

from __future__ import annotations

#: the set is {1, ..., top} and the required subset sum is target.
PARAMS = {"top": 67, "target": 2272}
ANSWER = 4
VARIANTS = [
    {"top": 67, "target": 2270},
    {"top": 50, "target": 1265},        # total is 1275, so the complement is 10
    {"top": 30, "target": 450},         # the middle of the range: a big count
    {"top": 20, "target": 210},         # the whole set — exactly one subset
    {"top": 20, "target": 211},         # over the total — none at all
    {"top": 12, "target": 0},           # the empty set, and only it
]


def _distinct_partitions(total: int, largest: int) -> int:
    """Number of sets of distinct integers in 1..largest summing to total."""
    if total == 0:
        return 1
    if total < 0 or largest <= 0:
        return 0
    # take `largest`, or don't
    return (_distinct_partitions(total - largest, largest - 1)
            + _distinct_partitions(total, largest - 1))


def solve(top=67, target=2272):
    """Count by complement: subsets summing to target ↔ subsets summing to S-target."""
    if top < 1 or target < 0:
        return None
    whole = top * (top + 1) // 2
    if target > whole:
        return 0
    rest = whole - target
    small = min(target, rest)                 # count whichever side is cheaper
    return _distinct_partitions(small, top)


def check(top=67, target=2272):
    """Independent: the straight subset-sum DP over the target as printed."""
    if top < 1 or target < 0:
        return None
    ways = [0] * (target + 1)
    ways[0] = 1
    for k in range(1, top + 1):
        for s in range(target, k - 1, -1):
            ways[s] += ways[s - k]
    return ways[target]
