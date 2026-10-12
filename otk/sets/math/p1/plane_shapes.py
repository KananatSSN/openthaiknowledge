"""เรขาคณิต 2 มิติ

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.1/*

Sets moved here from: math, math_diagrams, math_geometry.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import SHAPES_2D, _img, _text_q
from otk.sets._support.math_geometry import _POLYGONS

PROVENANCE = Provenance("original")


@question_type("math.shape_2d_picture_p1", display_name={"th": "บอกชื่อรูปเรขาคณิตสองมิติจากรูป"},
               level={"th": "ป.1"}, topic="เรขาคณิต 2 มิติ")
class Shape2DPictureP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SHAPES_2D)
        # Near neighbours first: square/rectangle, circle/ellipse.
        near = {"square": "รูปสี่เหลี่ยมผืนผ้า", "rectangle": "รูปสี่เหลี่ยมจัตุรัส",
                "circle": "รูปวงรี", "ellipse": "รูปวงกลม", "pentagon": "รูปหกเหลี่ยม",
                "hexagon": "รูปห้าเหลี่ยม", "triangle": "รูปสี่เหลี่ยมจัตุรัส"}[s.name]
        others = [x.thai for x in SHAPES_2D if x.thai not in (s.thai, near)]
        rng.shuffle(others)
        return _text_q([text("รูปนี้คือรูปใด"), _img(s.asset_id, "รูปเรขาคณิตสองมิติหนึ่งรูป")],
                       s.thai, [near] + others, self.topic)


@question_type("math.classify_2d_shape",
               display_name={"th": "จำแนกรูปเรขาคณิต 2 มิติ"}, level={"th": "ป.1"},
               topic="เรขาคณิต 2 มิติ")
class Classify2DShape(ConceptBankType):
    _OTHER = ("สามเหลี่ยม", "สี่เหลี่ยม", "วงกลม", "วงรี")

    ITEMS = [
        Concept("รูปใดมี 3 ด้าน?", "สามเหลี่ยม",
                ("สี่เหลี่ยม", "วงกลม", "วงรี")),
        Concept("รูปใดมี 4 ด้าน?", "สี่เหลี่ยม",
                ("สามเหลี่ยม", "วงกลม", "วงรี")),
        Concept("รูปใดมี 3 มุม?", "สามเหลี่ยม",
                ("สี่เหลี่ยม", "วงกลม", "วงรี")),
        Concept("รูปใดมี 4 มุม?", "สี่เหลี่ยม",
                ("สามเหลี่ยม", "วงกลม", "วงรี")),
        Concept("รูปใดกลม มีขอบโค้งห่างจากจุดศูนย์กลางเท่ากันทุกด้าน?", "วงกลม",
                ("สามเหลี่ยม", "สี่เหลี่ยม", "วงรี")),
        Concept("รูปใดมีลักษณะรีคล้ายไข่?", "วงรี",
                ("สามเหลี่ยม", "สี่เหลี่ยม", "วงกลม")),
        Concept("เหรียญบาทมีขอบเป็นรูปใด?", "วงกลม",
                ("สามเหลี่ยม", "สี่เหลี่ยม", "วงรี")),
        Concept("ประตูห้องเรียนเป็นรูปใด?", "สี่เหลี่ยม",
                ("สามเหลี่ยม", "วงกลม", "วงรี")),
        Concept("ขนมปังแผ่นสี่เหลี่ยมจัตุรัสตัดตามแนวทแยงมุม ได้ชิ้นขนมปังเป็นรูปใด?", "สามเหลี่ยม",
                ("สี่เหลี่ยม", "วงกลม", "วงรี")),
        Concept("จานใส่ปลาที่ยาวรีเป็นรูปใด?", "วงรี",
                ("วงกลม", "สี่เหลี่ยม", "สามเหลี่ยม")),
        Concept("หน้าจอโทรทัศน์เป็นรูปใด?", "สี่เหลี่ยม",
                ("สามเหลี่ยม", "วงกลม", "วงรี")),
        Concept("ถาดพิซซ่าก่อนตัดเป็นรูปใด?", "วงกลม",
                ("วงรี", "สี่เหลี่ยม", "สามเหลี่ยม")),
        Concept("ไม้ฉากสามเหลี่ยมที่ครูใช้เขียนกระดานมีกี่ด้าน?", "3 ด้าน",
                ("4 ด้าน", "2 ด้าน", "5 ด้าน")),
        Concept("รูปใดมีด้านมากที่สุด?", "สี่เหลี่ยม",
                ("สามเหลี่ยม", "วงกลม", "วงรี")),
    ]


@question_type("math.polygon_sides", display_name={"th": "จำนวนด้านของรูปหลายเหลี่ยม"},
               level={"th": "ป.1"}, topic="เรขาคณิต 2 มิติ")
class PolygonSides(WordProblem):
    def expr(self, rng: Random, sides_lo: int = 3, sides_hi: int = 10):
        name, n = rng.choice([p for p in _POLYGONS if sides_lo <= p[1] <= sides_hi])
        # Sides and corners come in equal numbers, which is the point of asking both.
        ask = rng.choice(("มีด้านกี่ด้าน", "มีมุมกี่มุม", "มีจุดมุมกี่จุด"))
        return MathDraw("", str(n), prompt=f"{name}{ask}",
                        distractors=[str(n - 1), str(n + 1), str(2 * n)])
