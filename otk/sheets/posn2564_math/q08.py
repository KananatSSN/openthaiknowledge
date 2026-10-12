"""ข้อ 8 — เดิมชั้น ม. 3 มีกี่ห้อง

โรงเรียนแห่งหนึ่งมีนักเรียนชั้น ม. 3 จำนวนเท่ากันในทุก ๆ ห้องเรียน จากสถานการณ์
การระบาดของโรคติดเชื้อไวรัส COVID-19 เพื่อให้เกิดระยะห่างตามมาตรการ DMHTT
ทำให้ต้องจัดห้องเรียนเพิ่มอีก 6 ห้อง และพบว่าจำนวนนักเรียนต่อห้องลดลงจากเดิม
30% พอดี จงหาว่าเดิมชั้น ม. 3 นี้มีกี่ห้อง

The head count never appears in the answer. With N students and r rooms, the new
occupancy is N/(r + 6) and the old is N/r, so "down by 30% พอดี" says

    N/(r + 6) = (1 − 30/100)·N/r   ⟹   r = (1 − p)·(r + extra)

and N cancels. Solving, r = extra·(100 − p)/p = 6·70/30 = **14 ห้อง**.

That cancellation is the point of the question: the data look insufficient, and
the number of students really is irrelevant.

``solve`` uses that closed form. ``check`` refuses to cancel anything: it picks
a concrete cohort — a head count divisible by both room counts — and searches
for the room counts whose measured occupancy drop is exactly the printed
percentage, then confirms the answer does not depend on the cohort it chose.
"""

from __future__ import annotations

from fractions import Fraction

#: `extra` more rooms drops the per-room count by `drop` percent.
PARAMS = {"extra": 6, "drop": 30}
ANSWER = 14
VARIANTS = [
    {"extra": 6, "drop": 25},
    {"extra": 4, "drop": 20},
    {"extra": 9, "drop": 30},
    {"extra": 5, "drop": 50},
    {"extra": 3, "drop": 10},
    {"extra": 6, "drop": 0},        # no drop at all: impossible
]


def solve(extra=6, drop=30):
    """r = extra·(100 − drop)/drop, when that is a whole number of rooms."""
    if extra <= 0 or not 0 < drop < 100:
        return None
    rooms = Fraction(extra * (100 - drop), drop)
    if rooms.denominator != 1 or rooms <= 0:
        return None
    return int(rooms)


def check(extra=6, drop=30):
    """Independent: fill real classrooms and measure the drop.

    A cohort size is chosen for each candidate room count so that both layouts
    divide evenly, the two occupancies are compared as an actual ratio, and the
    surviving room count must be the same for two different cohorts — so nothing
    relies on the head count cancelling.
    """
    if extra <= 0 or not 0 < drop < 100:
        return None
    wanted = 1 - Fraction(drop, 100)
    answers = []
    for multiple in (1, 7):
        good = []
        for rooms in range(1, 500):
            students = multiple * rooms * (rooms + extra)
            before = Fraction(students, rooms)
            after = Fraction(students, rooms + extra)
            if after == wanted * before:
                good.append(rooms)
        if len(good) != 1:
            return None
        answers.append(good[0])
    if len(set(answers)) != 1:
        return None
    return answers[0]
