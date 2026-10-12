"""ข้อ 17 — นักเรียนที่ตอบถูกทั้งข้อ 1 และข้อ 2

นักเรียน 100 คน สอบ 4 ข้อ ตอบถูก 60, 70, 80, 90 คนตามลำดับ และไม่มีนักเรียนคนใด
ตอบถูกครบทั้ง 4 ข้อ  จงหาจำนวนนักเรียนที่ตอบถูกทั้งข้อ 1 และข้อ 2

Method: count *wrong* answers instead. There are Σ(N − cᵢ) = 40+30+20+10 = 100
wrong answers among 100 students, and "nobody got all four right" means every
student contributes at least one. Total equals the floor, so every student got
exactly one wrong — the four wrong-sets partition the class. Then the students
right on both 1 and 2 are those outside the first two wrong-sets:
    N − (N−c₁) − (N−c₂) = c₁ + c₂ − N = 30.
The argument only closes when Σ(N − cᵢ) == N exactly; ``solve`` refuses
otherwise rather than returning a number the data does not determine.

``check`` builds an explicit class roster with that partition, verifies all the
stated totals against it, and counts the students directly.
"""

from __future__ import annotations

PARAMS = {"students": 100, "c1": 60, "c2": 70, "c3": 80, "c4": 90}
ANSWER = 30
VARIANTS = [
    {"students": 50, "c1": 30, "c2": 35, "c3": 40, "c4": 45},
    {"students": 100, "c1": 70, "c2": 70, "c3": 80, "c4": 80},
    {"students": 200, "c1": 120, "c2": 140, "c3": 160, "c4": 180},
    {"students": 100, "c1": 50, "c2": 60, "c3": 90, "c4": 100},
    {"students": 10, "c1": 6, "c2": 7, "c3": 8, "c4": 9},
]


def _wrongs(students, c1, c2, c3, c4) -> list[int]:
    return [students - c for c in (c1, c2, c3, c4)]


def solve(students=100, c1=60, c2=70, c3=80, c4=90):
    """Students correct on both problems 1 and 2."""
    wrong = _wrongs(students, c1, c2, c3, c4)
    if any(w < 0 for w in wrong):
        raise ValueError("a correct-count exceeds the class size")
    if sum(wrong) != students:
        raise ValueError(
            f"wrong answers total {sum(wrong)}, not {students}; with nobody "
            "perfect the counts no longer force a unique overlap")
    return c1 + c2 - students


def check(students=100, c1=60, c2=70, c3=80, c4=90):
    """Independent: construct the roster the argument implies and count it."""
    wrong = _wrongs(students, c1, c2, c3, c4)
    if sum(wrong) != students:
        raise ValueError("counts do not force a unique overlap")

    # Student i is wrong on exactly one problem; hand them out in blocks.
    roster, at = [], 0
    for problem, count in enumerate(wrong):
        roster += [problem] * count
        at += count
    assert len(roster) == students

    for problem, count in enumerate((c1, c2, c3, c4)):
        got_right = sum(1 for missed in roster if missed != problem)
        assert got_right == count, f"roster gives {got_right} not {count}"
    assert all(missed is not None for missed in roster), "someone was perfect"
    return sum(1 for missed in roster if missed not in (0, 1))
