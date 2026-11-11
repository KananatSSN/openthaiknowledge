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


# ── More plane shapes (2026-11): corners, sides of two shapes together, the odd one out, a shape from its
# description, things shaped like a given shape, folding and cutting, and which has more sides ──

from otk.kit import story as _story  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p1 import LEVEL  # noqa: E402

_POLY_SIDES_P1 = {"รูปสามเหลี่ยม": 3, "รูปสี่เหลี่ยม": 4, "รูปห้าเหลี่ยม": 5, "รูปหกเหลี่ยม": 6}
_SHAPE_OBJECTS = {
    "รูปวงกลม": ("เหรียญ", "นาฬิกาแขวนผนัง", "จานข้าว", "ล้อจักรยาน"),
    "รูปสามเหลี่ยม": ("ธงสามเหลี่ยม", "ชิ้นพิซซ่า", "ไม้แขวนเสื้อ"),
    "รูปสี่เหลี่ยม": ("ประตู", "หน้าต่าง", "กระดานดำ", "ธนบัตร"),
}


@question_type("math.shape_corners_p1", display_name={"th": "จำนวนมุมของรูปเรขาคณิต"},
               level=LEVEL, topic="เรขาคณิต 2 มิติ")
class ShapeCornersP1(WordProblem):
    def expr(self, rng: Random):
        name = rng.choice((*_POLY_SIDES_P1, "รูปวงกลม"))
        right = _POLY_SIDES_P1.get(name, 0)
        # One more or one fewer; the next shape's count.
        return MathDraw("", str(right), prompt=f"{name}มีมุมกี่มุม",
                        distractors=_story.keep(right + 1, right - 1, right + 2, 1, answer=right, lo=0))


@question_type("math.shape_total_sides_p1", display_name={"th": "นับด้านของรูปสองรูปรวมกัน"},
               level=LEVEL, topic="เรขาคณิต 2 มิติ")
class ShapeTotalSidesP1(WordProblem):
    def expr(self, rng: Random):
        x, y = rng.sample(tuple(_POLY_SIDES_P1), 2)
        a, b = _POLY_SIDES_P1[x], _POLY_SIDES_P1[y]
        right = a + b
        # The difference; one shape only; one off.
        return MathDraw("", str(right), prompt=f"{x} 1 รูป และ{y} 1 รูป มีด้านรวมกันกี่ด้าน",
                        distractors=_story.keep(abs(a - b), max(a, b), right + 1, right - 1, answer=right, lo=1))


@question_type("math.shape_odd_one_p1", display_name={"th": "สิ่งของใดมีรูปร่างต่างจากพวก"},
               level=LEVEL, topic="เรขาคณิต 2 มิติ")
class ShapeOddOneP1(ChoiceType):
    def compose(self, rng: Random):
        same, odd = rng.sample(tuple(_SHAPE_OBJECTS), 2)
        group = rng.sample(_SHAPE_OBJECTS[same], 3)
        return "สิ่งของใดมีรูปร่างต่างจากสิ่งของอื่น", rng.choice(_SHAPE_OBJECTS[odd]), group


@question_type("math.shape_description_p1", display_name={"th": "ระบุรูปเรขาคณิตจากคำบรรยาย"},
               level=LEVEL, topic="เรขาคณิต 2 มิติ")
class ShapeDescriptionP1(ConceptBankType):
    ITEMS = [
        Concept("รูปที่มีด้าน 3 ด้าน และมุม 3 มุม คือรูปใด", "รูปสามเหลี่ยม", ("รูปสี่เหลี่ยม", "รูปวงกลม", "รูปห้าเหลี่ยม")),
        Concept("รูปที่ไม่มีมุมและไม่มีด้านตรงเลย คือรูปใด", "รูปวงกลม", ("รูปสามเหลี่ยม", "รูปสี่เหลี่ยม", "รูปห้าเหลี่ยม")),
        Concept("รูปที่มีด้าน 4 ด้านยาวเท่ากันทุกด้าน และมุมเป็นมุมฉาก คือรูปใด", "รูปสี่เหลี่ยมจัตุรัส",
                ("รูปสี่เหลี่ยมผืนผ้า", "รูปสามเหลี่ยม", "รูปวงกลม")),
        Concept("รูปที่มีด้าน 4 ด้าน ด้านตรงข้ามยาวเท่ากัน แต่ด้านยาวกับด้านกว้างไม่เท่ากัน คือรูปใด",
                "รูปสี่เหลี่ยมผืนผ้า", ("รูปสี่เหลี่ยมจัตุรัส", "รูปสามเหลี่ยม", "รูปห้าเหลี่ยม")),
        Concept("รูปที่มีด้าน 5 ด้าน คือรูปใด", "รูปห้าเหลี่ยม", ("รูปสี่เหลี่ยม", "รูปหกเหลี่ยม", "รูปสามเหลี่ยม")),
        Concept("รูปที่มีด้าน 6 ด้าน คือรูปใด", "รูปหกเหลี่ยม", ("รูปห้าเหลี่ยม", "รูปสี่เหลี่ยม", "รูปแปดเหลี่ยม")),
    ]


@question_type("math.shape_objects_p1", display_name={"th": "สิ่งของใดมีรูปร่างตามที่กำหนด"},
               level=LEVEL, topic="เรขาคณิต 2 มิติ")
class ShapeObjectsP1(ChoiceType):
    def compose(self, rng: Random):
        shapes = list(_SHAPE_OBJECTS)
        shape = rng.choice(shapes)
        right = rng.choice(_SHAPE_OBJECTS[shape])
        wrongs = [rng.choice(_SHAPE_OBJECTS[s]) for s in shapes if s != shape]
        wrongs.append(rng.choice([o for o in _SHAPE_OBJECTS[rng.choice([s for s in shapes if s != shape])]
                                  if o not in wrongs]))
        return f"สิ่งของใดมีรูปร่างเป็น{shape}", right, wrongs


@question_type("math.fold_cut_shape_p1", display_name={"th": "พับและตัดกระดาษได้รูปใด"},
               level=LEVEL, topic="เรขาคณิต 2 มิติ")
class FoldCutShapeP1(ConceptBankType):
    ITEMS = [
        Concept("พับกระดาษรูปสี่เหลี่ยมจัตุรัสครึ่งหนึ่งตามแนวเส้นทแยงมุม จะได้รูปใด", "รูปสามเหลี่ยม",
                ("รูปสี่เหลี่ยมจัตุรัส", "รูปวงกลม", "รูปห้าเหลี่ยม")),
        Concept("ตัดกระดาษรูปสี่เหลี่ยมจัตุรัสออกเป็นสองส่วนเท่ากันตามแนวเส้นทแยงมุม แต่ละส่วนเป็นรูปใด",
                "รูปสามเหลี่ยม", ("รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมจัตุรัส", "รูปวงกลม")),
        Concept("ตัดกระดาษรูปสี่เหลี่ยมจัตุรัสออกเป็นสองส่วนเท่ากันโดยตัดขนานกับด้าน แต่ละส่วนเป็นรูปใด",
                "รูปสี่เหลี่ยมผืนผ้า", ("รูปสามเหลี่ยม", "รูปสี่เหลี่ยมจัตุรัส", "รูปวงกลม")),
        Concept("นำรูปสามเหลี่ยมที่เหมือนกันสองรูปมาต่อกันตามด้านที่ยาวที่สุด อาจได้รูปใด", "รูปสี่เหลี่ยม",
                ("รูปวงกลม", "รูปห้าเหลี่ยม", "รูปหกเหลี่ยม")),
        Concept("นำรูปสี่เหลี่ยมจัตุรัสที่เท่ากันสองรูปมาวางต่อกันด้านต่อด้าน จะได้รูปใด", "รูปสี่เหลี่ยมผืนผ้า",
                ("รูปสามเหลี่ยม", "รูปวงกลม", "รูปห้าเหลี่ยม")),
    ]


@question_type("math.shape_sides_compare_p1", display_name={"th": "รูปใดมีด้านมากกว่ากี่ด้าน"},
               level=LEVEL, topic="เรขาคณิต 2 มิติ")
class ShapeSidesCompareP1(WordProblem):
    def expr(self, rng: Random):
        x, y = rng.sample(tuple(_POLY_SIDES_P1), 2)
        if _POLY_SIDES_P1[x] < _POLY_SIDES_P1[y]:
            x, y = y, x
        a, b = _POLY_SIDES_P1[x], _POLY_SIDES_P1[y]
        right = a - b
        # Added instead; the larger count; one off.
        return MathDraw("", str(right), prompt=f"{x}มีด้านมากกว่า{y}กี่ด้าน",
                        distractors=_story.keep(a + b, a, b, right + 1, answer=right, lo=1))
