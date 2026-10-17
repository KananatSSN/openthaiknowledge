"""ข้อ 3 — มีเซกเตอร์มุมแหลมที่มีจุดฟ้ามากกว่าจุดชมพู 100 จุดพอดี  (พิสูจน์)

Cut Ω into four quarter sectors (turned slightly so no boundary meets a point,
then shrunk to acute ones). Their blue − pink excesses add to 2565 − 2022 = 543,
so one is at least ⌈543/4⌉ = 136. Sweeping a sector edge across that quarter
changes the excess by ±1 at a time from 0 up to it, so it passes 100. The
solver returns the guaranteed excess ⌈(blue − pink)/4⌉.

``check`` scatters the points: many pseudo-random configurations and one evenly
spread one. For each it finds the best quarter, confirms its excess is at least
the guarantee and that sweeping inside it hits the target exactly, and returns
the smallest best excess seen (the even spread attains the guarantee).
"""

from __future__ import annotations

from random import Random

PARAMS = {"blue": 2565, "pink": 2022, "target": 100}
ANSWER = 136
VARIANTS = [{"blue": 100, "pink": 60, "target": 5}, {"blue": 50, "pink": 49, "target": 1},
            {"blue": 300, "pink": 100, "target": 30}]


def solve(blue=2565, pink=2022, target=100):
    return -(-(blue - pink) // 4)


def _best_quarter(points, target):
    best = None
    for q in range(4):
        inside = sorted((ang, w) for ang, w in points if 90 * q < ang < 90 * (q + 1))
        excess = sum(w for _, w in inside)
        if best is None or excess > best[0]:
            best = (excess, inside)
    excess, inside = best
    if target <= excess:
        running, seen = 0, {0}
        for _, w in inside:
            running += w
            seen.add(running)
        assert target in seen
    return excess


def check(blue=2565, pink=2022, target=100):
    rng = Random(2565)
    results = []
    for _ in range(20):
        pts = [(rng.uniform(0.001, 359.999), 1) for _ in range(blue)]
        pts += [(rng.uniform(0.001, 359.999), -1) for _ in range(pink)]
        results.append(_best_quarter(pts, target))
    # even spread: each pink sits just after a blue, the surplus blues spaced evenly
    surplus = blue - pink
    pts = []
    slots = pink + surplus
    for j in range(slots):
        base = 360 * (j + 0.25) / slots
        pts.append((base, 1))
        if j * surplus // slots == (j + 1) * surplus // slots:
            pts.append((base + 0.1 * 360 / slots, -1))
    assert sum(1 for _, w in pts if w > 0) == blue and sum(1 for _, w in pts if w < 0) == pink
    results.append(_best_quarter(pts, target))
    floor = -(-(blue - pink) // 4)
    assert min(results) >= floor
    return min(results)
