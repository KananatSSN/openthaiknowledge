"""ข้อ 3 — ผลรวมระยะที่บันทึกเป็นศูนย์  (พิสูจน์)

A horizontal step at height y records +y when x grows and −y when it shrinks,
which is Δ(xy); a vertical step records ±x = Δ(xy) likewise. The record
telescopes to x₁y₁ − x₀y₀, which is 0 from (0, N) to (M, 0). The solver returns
that difference.

``check`` walks many pseudo-random lattice paths in the quadrant from start to
end, records each step by the source's rule (distance to the axis walked along,
signed by whether the walker moved away from the origin), and confirms every
path gives the same sum.
"""

from __future__ import annotations

from random import Random

PARAMS = {"start": (0, 4), "end": (5, 0)}
ANSWER = 0
VARIANTS = [{"start": (1, 2), "end": (3, 4)}, {"start": (0, 7), "end": (2, 0)},
            {"start": (6, 1), "end": (2, 5)}]


def solve(start=(0, 4), end=(5, 0)):
    return end[0] * end[1] - start[0] * start[1]


def _walk(rng, start, end):
    x, y = start
    total = 0
    for _ in range(40):  # wander first
        dx, dy = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        if x + dx < 0 or y + dy < 0:
            continue
        total += _record(x, y, dx, dy)
        x, y = x + dx, y + dy
    while (x, y) != end:
        if x != end[0]:
            dx, dy = (1 if end[0] > x else -1), 0
        else:
            dx, dy = 0, (1 if end[1] > y else -1)
        total += _record(x, y, dx, dy)
        x, y = x + dx, y + dy
    return total


def _record(x, y, dx, dy):
    before = x * x + y * y
    nx, ny = x + dx, y + dy
    distance = ny if dx else nx  # to the x-axis on a horizontal step, the y-axis on a vertical one
    assert distance == (y if dx else x)
    return distance if nx * nx + ny * ny > before else -distance


def check(start=(0, 4), end=(5, 0)):
    rng = Random(2557)
    sums = {_walk(rng, start, end) for _ in range(200)}
    assert len(sums) == 1
    return sums.pop()
