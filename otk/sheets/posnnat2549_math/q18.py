"""ข้อ 18 — เลือก 10 วันในเดือนพฤษภาคมไม่ให้ติดกัน

Shift the chosen days d₁ < ⋯ < d_k to dᵢ − (i − 1): distinct days among
D − k + 1, so C(22, 10) = 646646.

``check`` counts by a dynamic programme over the days (take a day only if the
previous one was not taken).
"""

from __future__ import annotations

from math import comb

PARAMS = {"days": 31, "k": 10}
ANSWER = 646646
VARIANTS = [{"days": 28, "k": 5}, {"days": 30, "k": 12}, {"days": 10, "k": 6}, {"k": 16}]


def solve(days=31, k=10):
    return comb(days - k + 1, k) if days - k + 1 >= 0 else 0


def check(days=31, k=10):
    # free[j] / taken[j]: ways with j chosen so far, last day free / taken
    free, taken = [1] + [0] * k, [0] * (k + 1)
    for _ in range(days):
        free, taken = [f + t for f, t in zip(free, taken)], [0] + free[:-1]
    return free[k] + taken[k]
