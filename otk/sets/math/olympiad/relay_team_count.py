"""Rectangles in a room × seat grid with an odd number of girls; the count is ≡ (R − 1)(L − 1)G (mod 2)."""

from __future__ import annotations

from itertools import combinations
from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันที่สอง ข้อ 5",))


def team_counts(girls: list[int], seats: int) -> tuple[int, int, int]:
    """Room r has girls in seats 1..girls[r]. A team is two rooms and two
    seat numbers; returns (one-girl teams, three-girl teams, all quadruples).
    Mod 2 each girl lies in (R − 1)(L − 1) quadruples, which is the source's
    parity argument."""
    one = three = 0
    for r, s in combinations(range(len(girls)), 2):
        for i, j in combinations(range(1, seats + 1), 2):
            g = (i <= girls[r]) + (j <= girls[r]) + (i <= girls[s]) + (j <= girls[s])
            one += g == 1
            three += g == 3
    return one, three, comb(len(girls), 2) * comb(seats, 2)


@question_type(
    "math.relay_team_count_olympiad",
    display_name={"th": "จำนวนทีมวิ่งผลัดจากสองห้องสองเลขที่"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class RelayTeamCount(WordProblem):
    def expr(self, rng: Random):
        rooms, seats = rng.randint(3, 6), rng.randint(4, 10)
        girls = [rng.randint(0, seats) for _ in range(rooms)]
        one, three, quads = team_counts(girls, seats)
        answer = one + three
        wrong = [v for v in dict.fromkeys([one, three, quads, quads - answer, answer + quads // 2]) if v != answer]
        listing = ", ".join(map(str, girls))
        return MathDraw(
            rf"{rooms}\times{seats}",
            str(answer),
            prompt=f"มีนักเรียน {rooms} ห้อง ห้องละ {seats} คน เลขที่ 1 ถึง {seats} จำนวนนักเรียนหญิงในแต่ละห้องคือ {listing} คน โดยนักเรียนหญิงของแต่ละห้องคือเลขที่ต้น ๆ ทีมวิ่งผลัดประกอบด้วยหญิง 1 ชาย 3 หรือหญิง 3 ชาย 1 มาจากสองห้อง ห้องละสองคนที่มีเลขที่ตรงกัน จงหาจำนวนวิธีตั้งทีม",
            hint="ทีมหนึ่งคือการเลือกสองห้องและสองเลขที่ นับเฉพาะกรณีที่มีนักเรียนหญิงเป็นจำนวนคี่",
            distractors=[str(v) for v in wrong],
        )
