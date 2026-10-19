"""ข้อ 8 — P/Q เมื่อผู้ได้คะแนนสูงสุดได้ 4n − 1

Every game hands out at least 2 points, so the 4n players average at least
4n − 1; a top score of 4n − 1 forces equality: same-sex games are all draws and
each girl draws n boys and loses to n. Draws 2n(2n − 1) + 2n² of C(4n, 2):
P/Q = (3n − 1)/(4n − 1).

``check`` plays out that tournament with the source's scoring rules, confirms
every player scores exactly 4n − 1, and counts the drawn games.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

PARAMS = {"n": 1}
ANSWER = Fraction(2, 3)
VARIANTS = [{"n": 2}, {"n": 3}, {"n": 5}]


def solve(n=1):
    return Fraction(3 * n - 1, 4 * n - 1)


def check(n=1):
    boys, girls = list(range(2 * n)), list(range(2 * n, 4 * n))
    score = [0] * (4 * n)
    draws = games = 0
    for i, j in combinations(range(4 * n), 2):
        games += 1
        if (i in boys) == (j in boys):  # same sex: draw, 1 point each
            score[i] += 1
            score[j] += 1
            draws += 1
        else:
            boy, girl = (i, j) if i in boys else (j, i)
            k = girls.index(girl)
            if (boys.index(boy) - k) % (2 * n) < n:  # the girl draws n boys
                score[girl] += 2
                draws += 1
            else:  # and loses to the other n: the boy gets 2
                score[boy] += 2
    assert max(score) == 4 * n - 1 == min(score)
    return Fraction(draws, games)
