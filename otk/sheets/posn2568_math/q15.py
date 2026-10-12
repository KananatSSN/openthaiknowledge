"""ข้อ 15 — การแจกของขวัญ

มีของขวัญที่แตกต่างกัน 4 ชิ้น แจกให้นักเรียน 4 คน โดยต้องมีนักเรียนได้รับของขวัญ
อย่างน้อย 3 คน  จงหาจำนวนวิธีทั้งหมด

Method: a distribution is a function gifts → students, so counting by the size
of the image and using surjection counts,
    answer = Σ_{i ≥ least} C(students, i) · Surj(gifts, i),
    Surj(g, i) = Σ_{j} (−1)^j C(i, j) (i−j)^g   (inclusion–exclusion).
For 4 gifts, 4 students and "at least 3 receive": 4! + C(4,3)·Surj(4,3)
= 24 + 4·36 = 168.

``check`` enumerates all students^gifts assignments and counts distinct
recipients — no formula, no inclusion–exclusion.
"""

from __future__ import annotations

from itertools import product
from math import comb

PARAMS = {"gifts": 4, "students": 4, "least": 3}
ANSWER = 168
VARIANTS = [
    {"least": 4},
    {"least": 1},
    {"gifts": 5, "students": 4, "least": 3},
    {"gifts": 3, "students": 5, "least": 2},
    {"gifts": 6, "students": 3, "least": 3},
]


def surjections(gifts: int, onto: int) -> int:
    """Functions from ``gifts`` labelled items onto exactly ``onto`` labels."""
    return sum((-1) ** j * comb(onto, j) * (onto - j) ** gifts
               for j in range(onto + 1))


def solve(gifts=4, students=4, least=3):
    """Ways to hand out all gifts so at least ``least`` students get one."""
    return sum(comb(students, i) * surjections(gifts, i)
               for i in range(least, min(students, gifts) + 1))


def check(gifts=4, students=4, least=3):
    """Independent: enumerate every assignment and count the recipients."""
    return sum(1 for assign in product(range(students), repeat=gifts)
               if len(set(assign)) >= least)
