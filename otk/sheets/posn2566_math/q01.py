"""ข้อ 1 — ค่าของ f(111) จากฟังก์ชันนิยามซ้อน

ให้ f เป็นฟังก์ชัน โดยที่  f(x) = x + 10 เมื่อ x < 100  และ  f(x) = f(f(x − 11))
เมื่อ x ≥ 100  จงหาค่าของ f(111)

This is McCarthy's function in disguise, and the whole item is noticing that the
recursion **collapses to a plateau**. For 100 ≤ x ≤ 110 the inner argument
x − 11 lands in 89…99, which is below the threshold, so

    f(x) = f(f(x − 11)) = f((x − 11) + 10) = f(x − 1)

Each such x hands the work to its predecessor, all the way down to f(99) = 109.
So f is constantly 109 on 100…110 — and then f(111) = f(f(100)) = f(109) = 109
as well, and by the same argument for every larger x.

    **f(111) = 109**

The rule in general, for `f(x) = x + a` below T and `f(f(x − b))` above: when
``a = b − 1`` the step above is exactly f(x−1), so f is constant at ``T + a − 1``
on the whole of [T, ∞). Iterating from 111 without noticing this is what makes
the question look like work.

``solve`` uses that plateau. ``check`` never evaluates a call: it fills a table
over [T − b, start] by *chaotic iteration*, applying the two printed rules to
whichever entries are already known and sweeping until nothing changes.
"""

from __future__ import annotations

#: f(x) = x + add below threshold, else f(f(x − back)).
PARAMS = {"start": 111, "threshold": 100, "add": 10, "back": 11}
ANSWER = 109
VARIANTS = [
    {"start": 100},
    {"start": 250},
    {"start": 99},
    {"start": 51, "threshold": 50, "add": 4, "back": 5},
    {"start": 1000, "threshold": 20, "add": 6, "back": 7},
    {"start": 111, "threshold": 100, "add": 10, "back": 3},
]


def solve(start=111, threshold=100, add=10, back=11):
    """The plateau: above the threshold f never moves off T + add − 1."""
    if back < 1 or add < 0:
        return None
    if start < threshold:
        return start + add
    if add == back - 1:
        return threshold + add - 1
    return _evaluate(start, threshold, add, back)


def _evaluate(start, threshold, add, back, budget=2_000_000):
    """Memoised evaluation with an explicit stack — no recursion limit."""
    memo: dict[int, int] = {}
    stack = [start]
    steps = 0
    while stack:
        steps += 1
        if steps > budget:
            return None
        x = stack[-1]
        if x in memo:
            stack.pop()
            continue
        if x < threshold:
            memo[x] = x + add
            stack.pop()
            continue
        inner = x - back
        if inner not in memo:
            stack.append(inner)
            continue
        outer = memo[inner]
        if outer not in memo:
            stack.append(outer)
            continue
        memo[x] = memo[outer]
        stack.pop()
    return memo[start]


def check(start=111, threshold=100, add=10, back=11):
    """Independent: fill a table by chaotic iteration until it stops changing.

    Nothing is *called*. Every x in the window gets `x + add` if it is below the
    threshold, and otherwise gets `table[table[x − back]]` as soon as both
    lookups happen to be filled in. Sweeping until a fixed point is reached is a
    different mechanism from following the recursion, and it does not care what
    order the values become known in.
    """
    if back < 1 or add < 0:
        return None
    if start < threshold:
        return start + add
    lo = min(threshold - back - 1, start - back - 1)
    hi = max(start, threshold + add + back) + back + add
    if hi - lo > 500_000:
        return None

    table: dict[int, int] = {x: x + add for x in range(lo, threshold)}
    for _ in range(hi - lo + 5):
        changed = False
        for x in range(threshold, hi + 1):
            if x in table:
                continue
            inner = table.get(x - back)
            if inner is None:
                continue
            outer = table.get(inner)
            if outer is None:
                continue
            table[x] = outer
            changed = True
        if start in table:
            return table[start]
        if not changed:
            return None
    return table.get(start)
