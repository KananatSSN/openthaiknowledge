"""Maximize Σ|f(k) − f(−k)| over bijections of {−n, …, n}."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 7",)
)


def antipodal_maximum(n: int) -> int:
    """Σ(larger) − Σ(smaller) over n pairs is at most (1+…+n) − (−1−…−n)."""
    return n * (n + 1)


def antipodal_maximizers(n: int) -> int:
    """f(0) = 0 and every pair {f(k), f(−k)} takes one sign each: the
    positives go to the pairs in n! ways, the negatives in n!, and each pair
    chooses which of k, −k is positive."""
    return factorial(n) ** 2 * 2**n


@question_type(
    "math.antipodal_bijection_maximum_olympiad",
    display_name={"th": "ผลบวกมากสุดของ |f(k) − f(−k)| ของฟังก์ชันหนึ่งต่อหนึ่งทั่วถึง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class AntipodalBijectionMaximum(WordProblem):
    def expr(self, rng: Random):
        setup = "ให้ A = {−n, …, n} และ f : A → A เป็นฟังก์ชันหนึ่งต่อหนึ่งทั่วถึง "
        if rng.randrange(2):
            n = rng.randint(10, 3000)
            answer = antipodal_maximum(n)
            options = [n * n, 2 * n * n, n * (n + 1) // 2, n * (2 * n + 1),
                       n * (n - 1), (n + 1) ** 2]
            return MathDraw(
                rf"n={n},\quad \sum_{{k=1}}^{{{n}}}\left|f(k)-f(-k)\right|",
                str(answer),
                prompt=setup + "จงหาค่ามากสุดที่เป็นไปได้ของผลบวกต่อไปนี้",
                hint="แต่ละพจน์คือ (ค่ามากในคู่) − (ค่าน้อยในคู่) ผลรวมจึงไม่เกินผลบวกค่าบวก n ตัวลบผลบวกค่าลบ n ตัว",
                distractors=[str(v) for v in options if v != answer],
                variant="maximum",
            )
        n = rng.randint(2, 6)
        answer = antipodal_maximizers(n)
        options = [
            factorial(n) ** 2,  # forget which of k, −k takes the positive value
            factorial(n) * 2**n,  # match only the positives
            factorial(2 * n),
            2 * answer,  # double-count the reflection f ↦ −f
            factorial(n) ** 2 * 2 ** (n - 1),
            factorial(2 * n + 1),
        ]
        return MathDraw(
            rf"n={n},\quad \sum_{{k=1}}^{{{n}}}\left|f(k)-f(-k)\right|",
            str(answer),
            prompt=setup + "จงหาจำนวนฟังก์ชัน f ที่ทำให้ผลบวกต่อไปนี้มีค่ามากสุด",
            hint="ค่ามากสุดเกิดเมื่อ f(0) = 0 และ f(k), f(−k) มีเครื่องหมายต่างกันทุก k",
            distractors=[str(v) for v in dict.fromkeys(options) if v != answer],
            variant="count",
        )
