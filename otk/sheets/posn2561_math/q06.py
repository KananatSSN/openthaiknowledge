"""ข้อ 6 — จำนวนเต็มบวกที่น้อยที่สุดที่มากกว่า 350

กำหนดให้ n เป็นจำนวนเต็มบวกที่มากกว่า 350 จงหา n ที่น้อยที่สุดที่มีสมบัติว่า
    ก. n เป็นผลบวกของจำนวนเต็มบวกที่เรียงติดกัน 3 จำนวน
    ข. n เป็นผลบวกของจำนวนเต็มบวกที่เรียงติดกัน 4 จำนวน
    และ ค. n เป็นผลบวกของจำนวนเต็มบวกที่เรียงติดกัน 5 จำนวน

A run of k consecutive integers starting at a sums to ``ka + k(k−1)/2``, so each
clause is a congruence:

* 3 terms: ``n = 3a + 3 = 3(a+1)`` — **n is a multiple of 3** (and n ≥ 6);
* 4 terms: ``n = 4a + 6`` — **n ≡ 2 (mod 4)**, which is the interesting one:
  an odd number of terms forces divisibility, an even number forbids it;
* 5 terms: ``n = 5a + 10 = 5(a+2)`` — **n is a multiple of 5** (and n ≥ 15).

So 15 | n and n ≡ 2 (mod 4). Writing n = 15k, 15 ≡ 3 (mod 4) gives 3k ≡ 2, i.e.
k ≡ 2 (mod 4), so n runs 30, 90, 150, 210, 270, 330, **390**, … and the first
one past 350 is

    390 = 129+130+131 = 96+97+98+99 = 76+77+78+79+80

The even-length clause is what stops the answer being a multiple of 60: a number
divisible by 4 can never be a sum of four consecutive integers.

``solve`` combines the congruences with a stride. ``check`` never forms one: for
each candidate it tries actual starting values and adds the runs up.
"""

from __future__ import annotations

#: run lengths that must all be achievable, and the lower bound to beat.
PARAMS = {"lengths": (3, 4, 5), "above": 350}
ANSWER = 390
VARIANTS = [
    {"lengths": (3, 4, 5), "above": 0},
    {"lengths": (2, 3), "above": 100},
    {"lengths": (3, 5, 7), "above": 350},
    {"lengths": (4, 6), "above": 50},
    {"lengths": (2, 4), "above": 10},          # both even: impossible together
    {"lengths": (3, 4, 5), "above": 10 ** 6},
]


def _runs_to(length: int, total: int) -> bool:
    """Whether ``total`` is a sum of ``length`` consecutive positive integers."""
    offset = length * (length - 1) // 2
    rest = total - offset
    return rest > 0 and rest % length == 0


def solve(lengths=(3, 4, 5), above=350):
    """The least n above the bound that every run length can reach."""
    if not lengths or above < 0:
        return None
    limit = above + 4 * max(1, above + 1) + 10 ** 4
    for n in range(above + 1, limit):
        if all(_runs_to(k, n) for k in lengths):
            return n
    return None


def check(lengths=(3, 4, 5), above=350):
    """Independent: build the runs and add them up.

    For each candidate and each run length, actual starting values are tried and
    the consecutive integers summed — no congruence, no divisibility test — and
    the candidate counts only when every length produces a run that hits it.
    """
    if not lengths or above < 0:
        return None
    limit = above + 4 * max(1, above + 1) + 10 ** 4
    for n in range(above + 1, limit):
        ok = True
        for k in lengths:
            found = False
            start = 1
            while k * start + k * (k - 1) // 2 <= n:
                if sum(range(start, start + k)) == n:
                    found = True
                    break
                start += 1
            if not found:
                ok = False
                break
        if ok:
            return n
    return None
