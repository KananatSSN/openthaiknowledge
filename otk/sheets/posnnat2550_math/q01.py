"""ข้อ 1 — AC เมื่อส่วนโค้ง AC ยาว 1/3 ของวงกลม และ AC − OD = 2

Arc AC subtends 120°, so AC = R√3; with OA on the x-axis and OB on the y-axis,
C = (−R/2, R√3/2) and OD = R√3/2. Hence AC − OD = AC/2 and AC = 2·2 = 4.

``check`` places C at 120° on a circle of radius R, measures AC and OD, and
scales R so that AC − OD matches.
"""

from __future__ import annotations

import math

PARAMS = {"difference": 2}
ANSWER = 4
VARIANTS = [{"difference": 1}, {"difference": 5}, {"difference": 17}]


def solve(difference=2):
    return 2 * difference


def check(difference=2):
    c = (math.cos(math.radians(120)), math.sin(math.radians(120)))
    ac, od = math.dist((1.0, 0.0), c), c[1]
    return ac * difference / (ac - od)
