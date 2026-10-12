"""ข้อ 7 — ความน่าจะเป็นที่จำนวนสัตว์ในคอกเป็นจำนวนเฉพาะ

ชาวบ้านคนหนึ่งเลี้ยงหมูและเป็ดไว้ทั้งหมด 9 คอก แต่ละคอกต้องประกอบด้วยทั้งหมูและเป็ด
โดยที่แต่ละคอกมีจำนวนรวมของสัตว์ทั้งสองชนิดแตกต่างกันทั้งหมด แต่มีจำนวนขารวมกัน
40 ขาเท่ากันทุกคอก  หากสุ่มเลือกมาคอกหนึ่ง จงหาความน่าจะเป็นที่จำนวนรวมของสัตว์
คอกนั้นเป็นจำนวนเฉพาะ

A pig has 4 legs and a duck 2, so a pen with p pigs and d ducks satisfies
``4p + 2d = 40``, i.e. ``2p + d = 20``. Both counts are at least 1, so
``1 ≤ p ≤ 9``, and the head count is

    p + d = p + (20 − 2p) = **20 − p**,

running over 11, 12, …, 19 as p runs from 9 down to 1 — exactly nine values, all
different. So the "all different" in the story is not a restriction to be applied
but a **determination**: there are nine pens and nine possible head counts, so
the pens are precisely those.

Primes among 11…19 are 11, 13, 17 and 19 — four of them — so the probability is
**4/9**.

``solve`` derives the head-count range and counts primes. ``check`` enumerates
(pigs, ducks) pairs, tabulates the head counts, and verifies that each appears
exactly once and that there are as many as there are pens before counting with a
sieve.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

#: number of pens, legs per pen, and legs on each of the two animals.
PARAMS = {"pens": 9, "legs": 40, "big": 4, "small": 2}
ANSWER = Fraction(4, 9)
VARIANTS = [
    {"pens": 10, "legs": 44, "big": 4, "small": 2},
    {"pens": 7, "legs": 32, "big": 4, "small": 2},
    {"pens": 4, "legs": 20, "big": 4, "small": 2},
    {"pens": 3, "legs": 24, "big": 6, "small": 4},
    {"pens": 12, "legs": 40, "big": 4, "small": 2},   # more pens than head counts
    {"pens": 9, "legs": 41, "big": 4, "small": 2},    # odd leg total: no pen at all
]


def _is_prime(n: int) -> bool:
    return n >= 2 and all(n % f for f in range(2, isqrt(n) + 1))


def solve(pens=9, legs=40, big=4, small=2):
    """Fraction of the pens whose head count is prime."""
    if pens <= 0 or legs <= 0 or big <= small or small <= 0:
        return None
    totals = set()
    for p in range(1, legs // big + 1):
        rest = legs - big * p
        if rest <= 0 or rest % small:
            continue
        totals.add(p + rest // small)
    if len(totals) != pens:
        return None
    return Fraction(sum(1 for t in totals if _is_prime(t)), pens)


def check(pens=9, legs=40, big=4, small=2):
    """Independent: enumerate the pens as (pigs, ducks) pairs and tabulate them.

    Every pair with at least one of each animal and the printed leg total is
    listed and grouped by head count; the story's "all different" is then
    verified as a property of that table — one pen per total, and as many totals
    as pens — before a sieve counts the primes.
    """
    if pens <= 0 or legs <= 0 or big <= small or small <= 0:
        return None
    counts: dict[int, int] = {}
    for p in range(1, legs // big + 1):
        for d in range(1, legs // small + 1):
            if big * p + small * d == legs:
                counts[p + d] = counts.get(p + d, 0) + 1
    if len(counts) != pens or any(n != 1 for n in counts.values()):
        return None
    limit = max(counts) + 1
    sieve = [True] * limit
    for i in range(min(2, limit)):
        sieve[i] = False
    for i in range(2, isqrt(limit - 1) + 1):
        if sieve[i]:
            for j in range(i * i, limit, i):
                sieve[j] = False
    return Fraction(sum(1 for t in counts if sieve[t]), pens)
