"""เทคนิคคูณด้วย 5

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


@question_type("math.multiply_by_5",
               display_name={"th": "เทคนิคคูณด้วย 5"}, level={"th": "เทคนิคคิดเลขเร็ว"},
               topic="เทคนิคคูณด้วย 5")
class MultiplyBy5(MathType):
    def expr(self, rng: Random, lo: int = 10, hi: int = 30):
        a = rng.randint(lo, hi)
        return MathDraw(rf"{a} \times 5", rf"{a * 5}",
                        hint=r"\times 10 \text{ then } \div 2")
