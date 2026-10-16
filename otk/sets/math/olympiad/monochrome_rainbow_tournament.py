"""Bound a colored complete graph with no two-equal-edge triangles."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def maximum_players(colors: int) -> int:
    """Sharp when colors-1 is prime, by affine-plane direction coloring."""
    if colors < 4:
        raise ValueError("at least four colors required")
    return (colors - 1) ** 2


@question_type(
    "math.monochrome_rainbow_tournament_olympiad",
    display_name={"th": "สามเหลี่ยมสีเดียวหรือสามสีในทัวร์นาเมนต์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class MonochromeRainbowTournament(WordProblem):
    def expr(self, rng: Random):
        colors = rng.choice((4, 6, 8, 12))
        answer = maximum_players(colors)
        return MathDraw(
            rf"q={colors}",
            str(answer),
            prompt=(
                "ผู้เล่นทุกคู่แข่งกันหนึ่งครั้งและติดป้ายผลการแข่งขันด้วยหนึ่งใน q สี "
                "โดยใช้สีอย่างน้อยสองสี ถ้าผู้เล่นสามคนใด ๆ มีป้ายของสามคู่ "
                "เป็นสีเดียวกันทั้งหมดหรือแตกต่างกันทั้งหมด จงหาจำนวนผู้เล่นมากที่สุด"
            ),
            hint=(
                "ขอบแต่ละสีแยกเป็นกลุ่มที่เชื่อมครบ; เปรียบเทียบขนาดกลุ่ม "
                "แล้วสร้างตัวอย่างด้วยทิศทางเส้นตรงในตารางพิกัดเศษเหลือ"
            ),
            distractors=[
                str(colors**2),  # allow one extra vertex in each direction class
                str(colors * (colors - 1)),  # forget the shared vertex
                str((colors - 1) * (colors - 2)),  # omit one direction class
                str(answer + 1),  # miss the final pigeonhole step
                str(answer - 1),  # overlook the affine-plane construction
            ],
        )
