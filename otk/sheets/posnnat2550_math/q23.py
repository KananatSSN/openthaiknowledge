"""วันที่สอง ข้อ 5 — จำนวนวิธีตั้งทีมวิ่งผลัดเป็นจำนวนคี่  (พิสูจน์)

A team is two rooms and two seat numbers with an odd number of girls, so the
count ≡ Σ(girls among the four) (mod 2), and each student lies in
(R − 1)(L − 1) such quadruples: count ≡ (R − 1)(L − 1)·G (mod 2). The solver
returns that parity (10 rooms of 50, 271 girls: 1, odd).

``check`` seats the girls in a concrete arrangement (first seats, room by
room), counts the teams exactly and takes the parity.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"rooms": 10, "seats": 50, "girls": 271}
ANSWER = 1
VARIANTS = [{"rooms": 4, "seats": 8, "girls": 13}, {"rooms": 3, "seats": 6, "girls": 9}, {"rooms": 5, "seats": 5, "girls": 10}]


def solve(rooms=10, seats=50, girls=271):
    return (rooms - 1) * (seats - 1) * girls % 2


def check(rooms=10, seats=50, girls=271):
    per_room = [min(seats, max(0, girls - r * seats)) for r in range(rooms)]
    teams = 0
    for r, s in combinations(range(rooms), 2):
        for i, j in combinations(range(1, seats + 1), 2):
            g = (i <= per_room[r]) + (j <= per_room[r]) + (i <= per_room[s]) + (j <= per_room[s])
            teams += g % 2
    return teams % 2
