"""ข้อ 3 — จำนวนชมรมมากสุด (19 คน, ชมรมที่มีหัวหน้าต้องมีสมาชิกเป็นจำนวนคี่)

Clubs are distinct non-empty subsets. Without the leader any non-empty subset
of the other n − 1 works (2^(n−1) − 1); with the leader, the leader plus an even
subset of the others (2^(n−2)). Total 2^18 − 1 + 2^17 = 393215.

``check`` runs over all 2^n subsets and counts the allowed ones.
"""

from __future__ import annotations

PARAMS = {"students": 19}
ANSWER = 393215
VARIANTS = [{"students": 2}, {"students": 5}, {"students": 12}]


def solve(students=19):
    return 2 ** (students - 1) - 1 + 2 ** (students - 2)


def check(students=19):
    count = 0
    for mask in range(1, 1 << students):
        if mask & 1 and bin(mask).count("1") % 2 == 0:  # bit 0 is the leader
            continue
        count += 1
    return count
