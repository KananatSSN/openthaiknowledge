"""Choosing k of D days with no two consecutive: C(D − k + 1, k)."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 18",))


MONTHS = (("กุมภาพันธ์ (28 วัน)", 28), ("เมษายน", 30), ("พฤษภาคม", 31), ("มิถุนายน", 30), ("ธันวาคม", 31))


def spaced_choices(days: int, k: int) -> int:
    """Remove one day after each of the first k − 1 chosen days: the choices
    match k-subsets of D − k + 1 days (source: May, k = 10 → C(22, 10) = 646646)."""
    return comb(days - k + 1, k)


@question_type(
    "math.nonadjacent_days_olympiad",
    display_name={"th": "จำนวนวิธีเลือกวันที่ไม่ติดกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class NonadjacentDays(WordProblem):
    def expr(self, rng: Random):
        month, days = rng.choice(MONTHS)
        k = rng.randint(3, 12)
        answer = spaced_choices(days, k)
        wrong = [v for v in dict.fromkeys([comb(days, k), comb(days - k, k), comb(days - k + 1, k - 1), comb(days - k - 1, k), comb(days - k + 2, k)]) if v != answer]
        return MathDraw(
            rf"k={k}",
            str(answer),
            prompt=f"ในเดือน{month} ตำรวจต้องการตั้งด่านตรวจ k วัน โดยไม่ตั้งด่าน 2 วันติดกัน จะจัดวันตั้งด่านได้ทั้งหมดกี่วิธี",
            hint="ถ้าเลือกวัน d₁ < d₂ < … < d_k ที่ไม่ติดกัน แล้ว d₁, d₂ − 1, …, d_k − (k − 1) เป็นวันที่ต่างกันจากวันทั้งหมด D − k + 1 วัน",
            distractors=[str(v) for v in wrong],
        )
