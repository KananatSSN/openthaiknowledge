"""ข้อ 6 — n ที่น้อยที่สุดที่ (ก) ⇒ (ข) (กลุ่ม 100 คน: 197)

Condition (a): every k-subset has a player beating the other k − 1 and one
losing to them. A draw u–v leaves at most k − 3 players able to fail to beat
both, forcing n ≤ 2k − 4; a 3-cycle forces n ≤ 2k − 5. So for n ≥ 2k − 3 the
results are transitive without draws and the scores differ, while a draw with
k − 3 players above and k − 3 below shows 2k − 4 fails: the answer is
max(k, 2k − 3), and max(k, 2k − 4) when draws are not allowed. For k = 100 this
is 197; PARAMS uses k = 4 so that ``check`` can try every tournament.

``check`` enumerates every tournament (win/draw/loss for each pair) for n from k
upward and returns the least n for which (a) always implies (b).
"""

from __future__ import annotations

from itertools import combinations, product

PARAMS = {"group": 4, "draws": True}
ANSWER = 5
VARIANTS = [{"group": 3}, {"group": 2}, {"group": 4, "draws": False}, {"group": 3, "draws": False}]


def solve(group=4, draws=True):
    return max(group, 2 * group - 3 if draws else 2 * group - 4)


def check(group=4, draws=True):
    outcomes = (0, 1, 2) if draws else (0, 2)  # points to the first player of the pair
    for n in range(group, 2 * group + 2):
        pairs = list(combinations(range(n), 2))
        holds = True
        for results in product(outcomes, repeat=len(pairs)):
            beats = {}
            score = [0] * n
            for (i, j), r in zip(pairs, results):
                score[i] += r
                score[j] += 2 - r
                beats[(i, j)], beats[(j, i)] = r == 2, r == 0
            ok = all(
                any(all(beats[(w, o)] for o in s if o != w) for w in s)
                and any(all(beats[(o, w)] for o in s if o != w) for w in s)
                for s in combinations(range(n), group)
            )
            if ok and len(set(score)) < n:
                holds = False
                break
        if holds:
            return n
    return None
