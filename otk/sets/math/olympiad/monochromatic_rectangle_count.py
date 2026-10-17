"""Two groups and two seat numbers whose four students share a gender; 4 × 7 forces one."""

from __future__ import annotations

from itertools import combinations
from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันที่สอง ข้อ 4",))


def rectangle_counts(girls: list[int], seats: int) -> tuple[int, int, int]:
    """Group r has girls in seats 1..girls[r]. Returns (all-girl, all-boy,
    all quadruples). The source shows 4 groups of 7 always have one: rows
    with the same majority gender share at most one seat of it, which a case
    count on 4-element seat sets rules out."""
    g = b = 0
    for r, s in combinations(range(len(girls)), 2):
        for i, j in combinations(range(1, seats + 1), 2):
            n = (i <= girls[r]) + (j <= girls[r]) + (i <= girls[s]) + (j <= girls[s])
            g += n == 4
            b += n == 0
    return g, b, comb(len(girls), 2) * comb(seats, 2)


@question_type(
    "math.monochromatic_rectangle_count_olympiad",
    display_name={"th": "จำนวนชุดนักเรียนเพศเดียวกันจากสองกลุ่มสองเลขที่"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class MonochromaticRectangleCount(WordProblem):
    def expr(self, rng: Random):
        groups, seats = rng.randint(3, 6), rng.randint(4, 9)
        girls = [rng.randint(0, seats) for _ in range(groups)]
        g, b, quads = rectangle_counts(girls, seats)
        answer = g + b
        odd = sum(1 for r, s in combinations(range(groups), 2) for i, j in combinations(range(1, seats + 1), 2) if ((i <= girls[r]) + (j <= girls[r]) + (i <= girls[s]) + (j <= girls[s])) % 2)
        wrong = [v for v in dict.fromkeys([g, b, quads, odd, quads - answer]) if v != answer]
        listing = ", ".join(map(str, girls))
        return MathDraw(
            rf"{groups}\times{seats}",
            str(answer),
            prompt=f"นักเรียนแบ่งเป็น {groups} กลุ่ม กลุ่มละ {seats} คน เลขที่ 1 ถึง {seats} จำนวนนักเรียนหญิงในแต่ละกลุ่มคือ {listing} คน โดยนักเรียนหญิงคือเลขที่ต้น ๆ ของกลุ่ม จงหาจำนวนวิธีเลือกสองกลุ่มและสองเลขที่ ที่นักเรียนทั้งสี่คนเป็นเพศเดียวกัน",
            hint="สำหรับแต่ละคู่กลุ่มและคู่เลขที่ ตรวจว่าทั้งสี่คนเป็นหญิงทั้งหมดหรือชายทั้งหมด นับทั้งสองกรณี",
            distractors=[str(v) for v in wrong],
        )
