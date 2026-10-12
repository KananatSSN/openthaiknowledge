"""เทคนิคคูณด้วย 11

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


@question_type("math.multiply_11",
               display_name={"th": "เทคนิคคูณด้วย 11"}, level={"th": "เทคนิคคิดเลขเร็ว"},
               topic="เทคนิคคูณด้วย 11")
class Multiply11(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(1, 9), rng.randint(1, 9)
        n = a * 10 + b
        return MathDraw(rf"{n} \times 11", rf"{n * 11}", hint=r"[a][a{+}b][b]")
