"""เส้นขนาน

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.2/*

Sets moved here from: math, math_diagrams_geo, math_geometry.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _img, _math_q
from otk.sets._support.math_diagrams_geo import PARALLEL_TWO, angle_at, parallel_alt
from otk.sets._support.math_geometry import _POLYGONS

PROVENANCE = Provenance("original")


@question_type("math.cointerior_angle",
               display_name={"th": "มุมภายในบนข้างเดียวกันของเส้นขนาน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class CointeriorAngle(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(40, 140)
        prompt = rng.choice((
            f"เส้นขนานถูกตัดด้วยเส้นตัด มุมภายในบนข้างเดียวกันมุมหนึ่ง {a} องศา อีกมุมหนึ่งมีขนาดเท่าใด?",
            f"AB ขนานกับ CD มีเส้นตัด EF ตัด AB ที่ G และตัด CD ที่ H ถ้า ∠BGH = {a}° "
            f"∠GHD มีขนาดกี่องศา",
            f"ถนนสองสายขนานกัน มีถนนอีกสายตัดผ่าน มุมภายในบนข้างเดียวกันของเส้นตัดมุมหนึ่ง"
            f"มีขนาด {a} องศา อีกมุมหนึ่งมีขนาดกี่องศา",
        ))
        return MathDraw("", str(180 - a), prompt=prompt,
                        distractors=[str(a), str(90 - a), str(360 - a)])


@question_type("math.transversal_picture_m2", display_name={"th": "หาขนาดของมุมจากรูปเส้นขนานและเส้นตัด"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class TransversalPictureM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(PARALLEL_TWO)
        (g, lab), (xp, _), (yp, _) = p.marks
        x, y = angle_at(p.theta, xp), angle_at(p.theta, yp)
        img = _img(p.asset_id, parallel_alt(p))
        ask, ans, wrongs = rng.choice((
            ("x + y", x + y, [x - y if x > y else y - x, 2 * x, 180]),
            ("x - y", x - y, [x + y, y - x, 0]),
            ("y", y, [180 - y, x if x != y else 180 - x, 90]),
        ))
        return _math_q([text("เส้นตรงสองเส้นในรูปขนานกัน จงหาค่าของ"), content_math(ask), img],
                       str(ans), [str(w) for w in wrongs], self.topic)


# Filed with ม.2 เส้นขนาน, where (n − 2) × 180° follows from a triangle's 180°;
# it was once listed under ป.1 shapes, where learners only name the shapes.
@question_type("math.polygon_angle_sum", display_name={"th": "ผลบวกมุมภายใน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class PolygonAngleSum(WordProblem):
    """(n − 2) × 180°, which is really "how many triangles does it cut into"."""

    def expr(self, rng: Random, sides_lo: int = 3, sides_hi: int = 10):
        name, n = rng.choice([p for p in _POLYGONS if sides_lo <= p[1] <= sides_hi])
        total = (n - 2) * 180
        return MathDraw("", str(total),
                        prompt=f"ผลบวกของมุมภายในทั้งหมดของ{name}เท่ากับกี่องศา",
                        distractors=[str(n * 180), str((n - 1) * 180), "360"])


@question_type("math.transversal_angle_chain",
               display_name={"th": "มุมบนเส้นตัดขวางของเส้นขนาน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class TransversalAngleChain(WordProblem):
    def expr(self, rng: Random, lo: int = 25, hi: int = 155):
        a = rng.randint(lo, hi)
        kind, value = rng.choice([
            ("มุมแย้ง", a), ("มุมภายในบนข้างเดียวกันของเส้นตัด", 180 - a),
            ("มุมภายนอกที่อยู่ตรงข้ามกัน", a),
        ])
        return MathDraw(
            "", str(value),
            prompt=(f"เส้นตรงสองเส้นขนานกันถูกตัดด้วยเส้นตัดขวาง "
                    f"ถ้ามุมหนึ่งมีขนาด {a} องศา แล้ว{kind}กับมุมนั้นมีขนาดกี่องศา"),
            distractors=[str(180 - value), str(90 - value if value < 90 else value - 90),
                         str(360 - value)])
