"""ข้อ 4 — ผลคูณเทเลสโคปของ p(x) = x³+x+2 และ q(x) = x³+x−2

ให้ A เป็นเซตของจำนวนเต็มบวก n ≥ 3 ทั้งหมดที่สอดคล้องกับ
    p(3)p(4)⋯p(n) / (q(2)q(3)⋯q(n−1)) = target      (โจทย์: target = 84)
ผลบวกของสมาชิกทั้งหมดในเซต A เท่ากับเท่าใด

Method: with f(x) = x² + x + 2,
    p(x) = (x+1)·f(x−1)   and   q(x) = (x−1)·f(x),
so every f-factor cancels between numerator and denominator and what is left is
    [4·5⋯(n+1)] / [1·2⋯(n−2)] = (n−1)n(n+1)/6.
Setting that equal to the target leaves one cubic in n to search.

``check`` shares none of that: it multiplies the actual products out with exact
Fractions and compares. Cancellation is exactly the kind of step that hides an
off-by-one in the index range, so the brute force is the point here.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"target": 84, "n_max": 200}
ANSWER = 8
VARIANTS = [
    {"target": 20},          # (n−1)n(n+1) = 120 → n = 5
    {"target": 4},           # → n = 3
    {"target": 1330},
    {"target": 85},          # no integer n — empty set
    {"target": 84, "n_max": 40},
]


def ratio(n: int) -> Fraction:
    """The closed form of the telescoped quotient for a given n."""
    return Fraction((n - 1) * n * (n + 1), 6)


def solve(target=84, n_max=200):
    """Sum of every integer n ≥ 3 whose quotient equals ``target``."""
    return sum(n for n in range(3, n_max + 1) if ratio(n) == target)


def _p(x: int) -> int:
    return x ** 3 + x + 2


def _q(x: int) -> int:
    return x ** 3 + x - 2


def check(target=84, n_max=200):
    """Independent: build both products term by term, exactly.

    Kept to a smaller ceiling than ``solve`` because the products blow up; the
    quotient is strictly increasing in n, so once it passes the target no larger
    n can match and stopping early loses nothing.
    """
    total, num, den = 0, Fraction(1), Fraction(1)
    for n in range(3, min(n_max, 400) + 1):
        num *= _p(n)                       # p(3)…p(n)
        den *= _q(n - 1)                   # q(2)…q(n−1)
        if num / den == target:
            total += n
        elif num / den > target:
            break
    return total
