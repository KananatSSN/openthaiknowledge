"""วันที่สอง ข้อ 2 — นักเรียน 2010 คน: ต้องมีสามคนเดือน/เพศ/ภูมิภาคเดียวกันถกหัวข้อเดียวกัน  (พิสูจน์)

There are 12·2·5 = 120 classes (month, sex, region). (R − 1)·classes people
can avoid a one-topic triangle, where R is the Ramsey number for triangles in
`topics` colours; one more forces R people into a class. For 3 topics,
R(3, 3, 3) = 17 gives 1921 ≤ 2010. The solver returns (R − 1)·classes + 1 for
two topics, where R(3, 3) = 6 can be checked by brute force (601).

``check`` finds R(3, 3) by colouring the edges of Kₙ in every way, then applies
the same count.
"""

from __future__ import annotations

from itertools import combinations, product

PARAMS = {"classes": 120, "topics": 2}
ANSWER = 601
VARIANTS = [{"classes": 1}, {"classes": 7}, {"classes": 60}]


def solve(classes=120, topics=2):
    ramsey = {2: 6, 3: 17}[topics]
    return (ramsey - 1) * classes + 1


def check(classes=120, topics=2):
    assert topics == 2
    for n in range(3, 8):
        edges = list(combinations(range(n), 2))
        index = {e: i for i, e in enumerate(edges)}
        forced = True
        for colours in product((0, 1), repeat=len(edges)):
            if not any(colours[index[(a, b)]] == colours[index[(a, c)]] == colours[index[(b, c)]]
                       for a, b, c in combinations(range(n), 3)):
                forced = False
                break
        if forced:
            return (n - 1) * classes + 1
    return None
