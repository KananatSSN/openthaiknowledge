"""ข้อ 29 — ความน่าจะเป็นที่ชนะเกมทอดลูกเต๋าสามชั้น

เด็กชายพลทอดลูกเต๋าเที่ยงตรงลูกหนึ่งในเกมการแข่งขัน ซึ่งมีเงื่อนไข ดังนี้
ถ้าลูกเต๋าขึ้นแต้มมากกว่า 2 เขาจะชนะ ไม่เช่นนั้นเขาจะได้ทอดลูกเต๋าอีกครั้งหนึ่ง ซึ่งถ้าขึ้น
แต้มมากกว่า 3 เขาจะชนะ ไม่เช่นนั้นเขาจะได้ทอดลูกเต๋าอีกครั้งหนึ่ง ซึ่งถ้าขึ้นแต้มมากกว่า 4
เขาจะชนะ ถ้าไม่ได้ตามนี้ถือว่าแพ้ จงหาว่าเด็กชายพลมีความน่าจะเป็นที่จะชนะการแข่งขันนี้เป็นเท่าใด

The rounds are nested, so the win probability is a sum of disjoint paths — win
now, or survive and win later:

    P = 4/6 + (2/6)[ 3/6 + (3/6)(2/6) ]
      = 2/3 + (1/3)(1/2 + 1/6)
      = 2/3 + (1/3)(2/3) = 2/3 + 2/9 = **8/9**

The threshold *rises* each round while the number of faces stays put, so each
extra round is worth less than the one before; the whole game is barely better
than the first roll alone (2/3 → 8/9).

Careful with "มากกว่า": strictly greater. "มากกว่า 2" on a six-sided die is four
faces, not three.

``solve`` telescopes the nested rounds. ``check`` rolls the die: it enumerates
every sequence of outcomes for all the rounds and counts, with equal weight, the
sequences the printed rules call a win.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

#: a fair die of `faces` faces; round i is won by beating thresholds[i].
PARAMS = {"faces": 6, "thresholds": (2, 3, 4)}
ANSWER = Fraction(8, 9)
VARIANTS = [
    {"thresholds": (2, 3)},
    {"thresholds": (3, 4, 5)},
    {"faces": 8, "thresholds": (2, 3, 4)},
    {"faces": 6, "thresholds": (4,)},
    {"faces": 6, "thresholds": (5, 5, 5, 5)},
    {"faces": 4, "thresholds": (1, 2, 3)},
    {"faces": 6, "thresholds": (6, 6)},      # unwinnable
]


def solve(faces=6, thresholds=(2, 3, 4)):
    """Win now, or survive this round and win in one of the later ones."""
    if faces < 1 or not thresholds:
        return None
    if any(t < 0 or t > faces for t in thresholds):
        return None
    total = Fraction(0)
    survived = Fraction(1)
    for threshold in thresholds:
        total += survived * Fraction(faces - threshold, faces)
        survived *= Fraction(threshold, faces)
    return total


def check(faces=6, thresholds=(2, 3, 4)):
    """Independent: enumerate every sequence of rolls and apply the rules."""
    if faces < 1 or not thresholds:
        return None
    if any(t < 0 or t > faces for t in thresholds):
        return None
    if faces ** len(thresholds) > 5 * 10 ** 5:
        return None

    wins = 0
    for rolls in product(range(1, faces + 1), repeat=len(thresholds)):
        for roll, threshold in zip(rolls, thresholds):
            if roll > threshold:
                wins += 1
                break
    return Fraction(wins, faces ** len(thresholds))
