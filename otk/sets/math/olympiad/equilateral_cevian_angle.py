"""Equilateral ABC with AN = BM: ∠BOC = 120°; for BM = AB/3, ∠AOB = 150°."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 4",)
)

# BM/AB → (∠AOB, ∠AOC); ∠BOC is 120° for every ratio
ANGLES = {(1, 3): (150, 90), (1, 2): (120, 120), (2, 3): (90, 150)}


def cevian_angle(ratio: tuple[int, int], asked: str) -> int:
    """Triangles ABN and BCM are congruent (AN = BM), so ∠OBC + ∠OCB = 60°
    and ∠BOC = 120°. For BM = AB/3, AO ⊥ OC (O lies on the circle with
    diameter AC, checked by coordinates), giving ∠AOB = 150°."""
    if asked == "BOC":
        return 120
    aob, aoc = ANGLES[ratio]
    return aob if asked == "AOB" else aoc


@question_type(
    "math.equilateral_cevian_angle_olympiad",
    display_name={"th": "มุมที่จุดตัดของเส้นจากจุดยอดในรูปสามเหลี่ยมด้านเท่า"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต",
)
class EquilateralCevianAngle(WordProblem):
    def expr(self, rng: Random):
        ratio = rng.choice(tuple(ANGLES))
        asked = rng.choice(("AOB", "AOC", "BOC"))
        answer = cevian_angle(ratio, asked)
        wrong = [v for v in (60, 90, 120, 135, 150) if v != answer][:4]
        p, q = ratio
        return MathDraw(
            rf"AN=BM,\quad BM=\frac{{{p}}}{{{q}}}AB",
            rf"{answer}^\circ",
            prompt=(
                "ABC เป็นรูปสามเหลี่ยมด้านเท่า M อยู่บน AB และ N อยู่บน AC "
                f"CM ตัด BN ที่ O จงหาขนาดของมุม {asked}"
            ),
            hint="รูปสามเหลี่ยม ABN และ BCM เท่ากันทุกประการ จึง ∠BOC = 120° แล้วพิจารณาตำแหน่งของ O เทียบกับจุดยอด A",
            distractors=[rf"{v}^\circ" for v in wrong],
            variant=asked,
        )
