"""ข้อ 15 — สมาชิกที่มากที่สุดของเซตจำนวนสี่หลักจากเลขโดด A, B, C, D

ให้จำนวนนับสามหลักในรูปฐานสิบ 4 จำนวน คือ 33A, 5B6, 6C3 และ D11 เมื่อ
A, B, C, D ∈ {0, 1, 2, …, 9} และค่าเฉลี่ยเลขคณิตของทั้งสี่จำนวนมีค่าเท่ากับ 500
ให้ S แทนเซตของจำนวนสี่หลักทั้งหมดที่เกิดจากนำเลขโดด A, B, C และ D ทุกตัวมาจัดเรียง
เป็นจำนวนที่มีสี่หลัก  จงหาสมาชิกของเซต S ที่มีค่ามากที่สุด

The mean of 500 means the four numbers total 2000. The fixed digits contribute
330 + 506 + 603 + 11 = 1450, so the letters must supply

    A + 10B + 10C + 100D = 550

Everything but A is a multiple of ten, so **A = 0**, and then B + C + 10D = 55.
Since B + C ≤ 18 this forces D ∈ {4, 5}:

    D = 4 → B + C = 15        D = 5 → B + C = 5

The largest four-digit arrangement wants the largest digits, so take D = 4 with
{B, C} = {9, 6}: the digit multiset is {0, 4, 6, 9} and the answer is **9640**.
(The D = 5 branch tops out at 5500.)

Note the letters are not unique — S is the set of arrangements over *every*
admissible (A, B, C, D), and the question asks for the largest member of all
of them.

``solve`` searches the digit assignments and arranges each one. ``check`` walks
the four-digit numbers downwards instead, asking of each whether its digits can
be dealt out to A, B, C, D so that the printed mean comes out — the first one
that can is the answer.
"""

from __future__ import annotations

from itertools import permutations, product

#: each template is a 3-digit string; a letter marks the unknown digit's place.
PARAMS = {"templates": ("33A", "5B6", "6C3", "D11"), "mean": 500}
ANSWER = 9640
VARIANTS = [
    {"mean": 400},
    {"mean": 600},
    {"templates": ("1A2", "B34", "5C6", "78D"), "mean": 500},
    {"templates": ("A11", "2B2", "33C", "D44"), "mean": 300},
    {"mean": 999},                       # unreachable
    {"templates": ("AB1", "2C3", "4D5", "678"), "mean": 400},
]

_LETTERS = "ABCDEFGH"


def _value(template: str, digits: dict) -> int:
    return int("".join(digits.get(ch, ch) for ch in template))


def solve(templates=("33A", "5B6", "6C3", "D11"), mean=500):
    """Try each digit assignment, then read the best arrangement off the multiset."""
    letters = sorted({ch for t in templates for ch in t if ch in _LETTERS})
    if not letters or len(letters) > 6:
        return None
    total = mean * len(templates)
    best = None
    for combo in product(range(10), repeat=len(letters)):
        digits = {ch: str(d) for ch, d in zip(letters, combo)}
        if sum(_value(t, digits) for t in templates) != total:
            continue
        for order in permutations(combo):
            if order[0] == 0:
                continue
            value = int("".join(str(d) for d in order))
            if best is None or value > best:
                best = value
    return best


def check(templates=("33A", "5B6", "6C3", "D11"), mean=500):
    """Independent: walk the four-digit numbers down and test each digit multiset.

    Instead of searching over (A, B, C, D) this searches over *answers*: for each
    candidate number, its digits are dealt out to the letters in every order and
    the printed mean is tested. The first candidate that works is the largest.
    """
    letters = sorted({ch for t in templates for ch in t if ch in _LETTERS})
    if not letters or len(letters) > 6:
        return None
    total = mean * len(templates)
    lo = 10 ** (len(letters) - 1)
    hi = 10 ** len(letters) - 1
    if hi - lo > 200_000:
        return None
    for value in range(hi, lo - 1, -1):
        digits_of = [int(ch) for ch in str(value)]
        for order in permutations(digits_of):
            digits = {ch: str(d) for ch, d in zip(letters, order)}
            if sum(_value(t, digits) for t in templates) == total:
                return value
    return None
