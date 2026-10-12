"""ข้อ 14 — ชุดข้อมูล a, 2, b, 8, c, 13

โดยที่ a, b, c เป็นจำนวนเต็มบวก ชุดข้อมูลนี้มีค่าเฉลี่ยเลขคณิตและมัธยฐานเท่ากับ 10
และมีฐานนิยมเท่ากับ 8  ผลบวกของค่าสูงสุดกับค่าต่ำสุดของชุดข้อมูลนี้เท่ากับเท่าใด

Method: the mean pins a+b+c, so only two of the three unknowns are free and the
search is small. The binding condition is the mode: with 8 appearing once among
the fixed values, at least one of a, b, c must be 8 — and no *other* value may
tie it, which is what rules out the three-eights reading. The unique surviving
data set is 2, 8, 8, 12, 13, 17, so max + min = 19.

``solve`` searches (a, b) with c forced by the mean; ``check`` searches the
unordered multiset {a, b, c} instead. Both return ``None`` when the constants
admit two data sets with *different* max+min — for those the question has no
answer at all, and the generator skips them. (The mode = 7 variant below is one:
it is kept precisely to pin that behaviour down.)
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations_with_replacement

PARAMS = {"f1": 2, "f2": 8, "f3": 13, "mean": 10, "median": 10, "mode": 8,
          "hi": 60}
ANSWER = 19
VARIANTS = [
    {"f1": 3, "f2": 8, "f3": 13},
    {"mode": 2},
    {"mean": 9, "median": 9},
    {"f1": 2, "f2": 7, "f3": 13, "mode": 7},
    {"mean": 11, "median": 10},
]


def _valid(data: list[int], mean, median, mode) -> bool:
    ordered = sorted(data)
    n = len(ordered)
    if sum(ordered) != mean * n:
        return False
    mid = (ordered[n // 2 - 1] + ordered[n // 2]) / 2 if n % 2 == 0 \
        else ordered[n // 2]
    if mid != median:
        return False
    counts = Counter(ordered)
    top = max(counts.values())
    return counts[mode] == top and list(counts.values()).count(top) == 1


def datasets(f1=2, f2=8, f3=13, mean=10, median=10, mode=8, hi=60):
    """Every admissible full data set, as a sorted tuple (deduplicated)."""
    fixed = [f1, f2, f3]
    need = mean * (len(fixed) + 3) - sum(fixed)         # a + b + c
    out = set()
    for a in range(1, hi + 1):
        for b in range(1, hi + 1):
            c = need - a - b
            if 1 <= c <= hi and _valid(fixed + [a, b, c], mean, median, mode):
                out.add(tuple(sorted(fixed + [a, b, c])))
    return sorted(out)


def solve(f1=2, f2=8, f3=13, mean=10, median=10, mode=8, hi=60):
    """max + min of the data set, or None when nothing fits."""
    found = datasets(f1, f2, f3, mean, median, mode, hi)
    spans = {data[0] + data[-1] for data in found}
    # Not every choice of constants pins the data set down — some admit two data
    # sets with different spans, and then the question has no answer. Say so
    # rather than picking one; the generator only uses constants that survive.
    return spans.pop() if len(spans) == 1 else None


def check(f1=2, f2=8, f3=13, mean=10, median=10, mode=8, hi=60):
    """Independent: enumerate the unordered {a,b,c}, and demand uniqueness."""
    fixed = [f1, f2, f3]
    found = {tuple(sorted(fixed + list(trio)))
             for trio in combinations_with_replacement(range(1, hi + 1), 3)
             if _valid(fixed + list(trio), mean, median, mode)}
    spans = {data[0] + data[-1] for data in found}
    return spans.pop() if len(spans) == 1 else None
