"""ข้อ 9 — ผลต่างระหว่างผลรวมคะแนนมากที่สุดกับน้อยที่สุด

น้องมิวและน้องแบ๊มแข่งเล่นเกมหมากฮอสกัน โดยในแต่ละเกม
    ผู้ชนะจะได้ 4 คะแนน
    ผู้แพ้จะได้ 0 คะแนน
    และถ้าเสมอจะได้คนละ 1 คะแนน
จงหาว่าเมื่อเล่นกันไปจนครบ 10 เกมแล้ว ผลรวมของคะแนนทั้งหมดของทั้งคู่ที่มีค่ามาก
ที่สุดที่เป็นไปได้ ต่างจากค่าน้อยที่สุดที่เป็นไปได้อยู่เท่าใด

Only the *combined* score matters, and each game contributes one of two amounts:

    decided:  4 + 0 = 4      drawn:  1 + 1 = 2

so the pair's total is ``4d + 2(g − d)`` where d is the number of decided games —
anywhere from ``2g`` (all drawn) to ``4g`` (none drawn). The difference is

    4·10 − 2·10 = 40 − 20 = **20**

i.e. ``g·(win + loss − 2·draw)``. Who wins which game never enters, which is why
the answer is so much smaller than the ten-game score space suggests.

``solve`` uses that closed form. ``check`` enumerates the number of decided games
from 0 to g, builds the combined score for each, and takes the actual maximum and
minimum of the list it produces.
"""

from __future__ import annotations

#: games played, and the points each outcome awards.
PARAMS = {"games": 10, "win": 4, "loss": 0, "draw": 1}
ANSWER = 20
VARIANTS = [
    {"games": 10, "win": 3, "loss": 0, "draw": 1},
    {"games": 7, "win": 4, "loss": 0, "draw": 1},
    {"games": 10, "win": 2, "loss": 0, "draw": 1},     # a draw pays the same
    {"games": 12, "win": 5, "loss": 1, "draw": 2},
    {"games": 10, "win": 1, "loss": 0, "draw": 1},     # draws pay more
    {"games": 0, "win": 4, "loss": 0, "draw": 1},
]


def solve(games=10, win=4, loss=0, draw=1):
    """|max total − min total| = games · |win + loss − 2·draw|."""
    if games < 0:
        return None
    return games * abs(win + loss - 2 * draw)


def check(games=10, win=4, loss=0, draw=1):
    """Independent: build every possible combined total and take the spread.

    The number of decided games runs from 0 to ``games``; each split gives a
    concrete combined score, and the answer is the difference between the largest
    and smallest of the scores actually produced. No identity is used, so a
    scoring scheme where draws pay *more* is handled by the same code.
    """
    if games < 0:
        return None
    totals = [decided * (win + loss) + (games - decided) * 2 * draw
              for decided in range(games + 1)]
    return max(totals) - min(totals)
