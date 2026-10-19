"""Largest S with every pairwise sum a square, given two members a and b."""

from __future__ import annotations

from itertools import combinations
from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 1",))


def _square(v: int) -> bool:
    return v >= 0 and isqrt(v) ** 2 == v


def candidates(a: int, b: int) -> list[int]:
    """c + a = u², c + b = v² means (v − u)(v + u) = b − a with factors of
    equal parity; b − a ≡ 2 (mod 4) leaves none (the source: 2087 − 2009 = 78)."""
    diff, found = b - a, []
    for d1 in range(1, isqrt(diff) + 1):
        if diff % d1 == 0 and (d1 + diff // d1) % 2 == 0:
            u = (diff // d1 - d1) // 2
            c = u * u - a
            if c > 0 and c not in (a, b):
                found.append(c)
    return sorted(set(found))


def largest_set(a: int, b: int) -> int:
    """Two plus the largest clique of candidates with square pairwise sums."""
    pool = candidates(a, b)
    for size in range(len(pool), 0, -1):
        for group in combinations(pool, size):
            if all(_square(x + y) for x, y in combinations(group, 2)):
                return 2 + size
    return 2


def _pairs():
    found = []
    for s in range(20, 60):
        for a in range(10, s * s // 2):
            b = s * s - a
            if b > a and b - a <= 400:
                found.append((a, b, largest_set(a, b)))
    return found


PAIRS = tuple(_pairs()[::7])


@question_type(
    "math.sum_square_set_size_olympiad",
    display_name={"th": "เซตที่ผลบวกทุกคู่เป็นกำลังสองสมบูรณ์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวนเชิงพีชคณิต",
)
class SumSquareSetSize(WordProblem):
    def expr(self, rng: Random):
        a, b, answer = rng.choice(PAIRS)
        wrong = [v for v in dict.fromkeys([2, 3, 4, 5, 1]) if v != answer]
        return MathDraw(
            rf"{a}\in S,\quad {b}\in S",
            str(answer),
            prompt="S เป็นเซตของจำนวนนับที่ผลบวกของสมาชิกสองตัวใด ๆ ที่ต่างกันเป็นกำลังสองสมบูรณ์ จำนวนสมาชิกมากที่สุดที่เป็นไปได้ของ S คือเท่าใด",
            hint="สมาชิก c ตัวที่สามต้องทำให้ c + a และ c + b เป็นกำลังสองทั้งคู่ แยกตัวประกอบผลต่าง b − a",
            distractors=[str(v) for v in wrong],
        )
