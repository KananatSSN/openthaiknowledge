"""กำลังสองของจำนวนลงท้ายด้วย 5

คณิตศาสตร์ · เทคนิคคิดเลขเร็ว · เสริมทักษะ
Indicators: —

Sets moved here from: math.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType

PROVENANCE = Provenance("original")


@question_type("math.five_square",
               display_name={"th": "กำลังสองของจำนวนลงท้ายด้วย 5"},
               level={"th": "เทคนิคคิดเลขเร็ว"}, topic="กำลังสองของจำนวนลงท้ายด้วย 5")
class FiveSquare(MathType):
    def expr(self, rng: Random, lo: int = 1, hi: int = 9):
        a = rng.randint(lo, hi)
        return MathDraw(rf"{a}5^{{2}}", rf"{a * (a + 1)}25", hint=r"[a \times (a{+}1)][25]")
