"""รูปเรขาคณิต

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.2/*

Sets moved here from: math_chapters, math_pictures_extra.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_chapters import P2
from otk.sets._support.math_diagrams import SHAPES_2D, _math_q
from otk.sets._support.math_p2 import _texts
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_extra import POLYGON_PICS

PROVENANCE = Provenance("original")


_SHAPE_TOPIC = "รูปเรขาคณิต"


_POLY = (("รูปสามเหลี่ยม", 3), ("รูปสี่เหลี่ยม", 4), ("รูปห้าเหลี่ยม", 5), ("รูปหกเหลี่ยม", 6))


_SOLIDS = {
    "ทรงสี่เหลี่ยมมุมฉาก": (("กล่องนม", "ก้อนอิฐ", "ตู้เย็น", "กล่องดินสอ"),
                            "มีหน้าเรียบเป็นรูปสี่เหลี่ยม 6 หน้า และกลิ้งไม่ได้", "รูปสี่เหลี่ยม"),
    "ทรงกลม": (("ลูกฟุตบอล", "ลูกแก้ว", "ลูกส้ม"), "ไม่มีหน้าเรียบ และกลิ้งได้ทุกทิศทาง", ""),
    "ทรงกระบอก": (("กระป๋องนม", "ท่อนไม้", "ถ่านไฟฉาย"),
                  "มีหน้าเรียบเป็นวงกลม 2 หน้า และกลิ้งได้", "วงกลม"),
    "กรวย": (("กรวยจราจร", "หมวกงานวันเกิด"), "มีหน้าเรียบเป็นวงกลม 1 หน้า และมียอดแหลม", "วงกลม"),
}


_POLYGON_SIDES = {"triangle": 3, "square": 4, "rectangle": 4, "pentagon": 5, "hexagon": 6}


_POLYGONS = tuple(s for s in SHAPES_2D if s.name in _POLYGON_SIDES)


@question_type("math.shape_properties_p2", display_name={"th": "ด้านและมุมของรูปหลายเหลี่ยมและวงกลม"},
               level=P2, topic=_SHAPE_TOPIC)
class ShapePropertiesP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        name, k = rng.choice(_POLY)
        others = [n for n, _ in _POLY if n != name]
        kind = rng.randrange(3)
        if kind == 0:
            wrongs = rng.sample(others + ["วงกลม"], 3)
            return _texts([text(f"รูปที่มี {k} ด้าน และ {k} มุม คือรูปใด")], name, wrongs, self.topic)
        if kind == 1:
            right = rng.choice(("วงกลม", "วงรี"))
            return _texts([text("รูปใดไม่มีด้านและไม่มีมุม")], right,
                          rng.sample([n for n, _ in _POLY], 3), self.topic)
        part = rng.choice(("ด้าน", "มุม"))
        wrongs = [f"{x} {part}" for x in (k + 1, k - 1, k + 2)]
        return _texts([text(f"{name}มีกี่{part}")], f"{k} {part}", wrongs, self.topic)


@question_type("math.shape_sides_picture_p2", display_name={"th": "นับด้านและมุมของรูปจากภาพ"},
               level={"th": "ป.2"}, topic="รูปเรขาคณิต")
class ShapeSidesPictureP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.25:
            s = rng.choice(_POLYGONS)
            n = _POLYGON_SIDES[s.name]
            asset = s.asset_id
        else:
            p = rng.choice(POLYGON_PICS)
            n, asset = p.sides, p.asset_id
        what = rng.choice(("ด้าน", "มุม"))
        img = image(asset, alt="รูปเรขาคณิตสองมิติหนึ่งรูป")
        return _math_q([text(f"รูปนี้มี{what}กี่{what}"), img], str(n),
                       _near(n, n + 1, n - 1, 2 * n, lo=1), self.topic)


@question_type("math.solid_shapes_p2", display_name={"th": "ทรงสี่เหลี่ยมมุมฉาก ทรงกลม ทรงกระบอก และกรวย"},
               level=P2, topic=_SHAPE_TOPIC)
class SolidShapesP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 2:
            solid = rng.choice([s for s, v in _SOLIDS.items() if v[2]])
            objects, _, trace = _SOLIDS[solid]
            flat = ["รูปสามเหลี่ยม", "รูปสี่เหลี่ยม", "วงกลม", "วงรี", "รูปห้าเหลี่ยม"]
            wrongs = rng.sample([f for f in flat if f != trace], 3)
            return _texts([text(f"นำ{rng.choice(objects)}วางบนกระดาษ ให้หน้าที่เรียบแนบกับกระดาษ "
                                f"แล้วลากเส้นตามขอบของหน้านั้น จะได้รูปใด")], trace, wrongs, self.topic)
        solid = rng.choice(sorted(_SOLIDS))
        objects, described, _ = _SOLIDS[solid]
        wrongs = [s for s in _SOLIDS if s != solid]
        if kind == 0:
            stem = f"{rng.choice(objects)}มีลักษณะเป็นรูปเรขาคณิตสามมิติแบบใด"
        else:
            stem = f"รูปเรขาคณิตสามมิติที่{described} คือรูปใด"
        return _texts([text(stem)], solid, wrongs, self.topic)


@question_type("math.shape_count_p2", display_name={"th": "โจทย์ปัญหาจำนวนด้านและมุมของรูปหลายเหลี่ยม"},
               level=P2, topic=_SHAPE_TOPIC)
class ShapeCountP2(WordProblem):
    def expr(self, rng: Random):
        (n1, k1), (n2, k2) = rng.sample(_POLY, 2)
        if rng.random() < 0.6:
            a, b = rng.randint(2, 6), rng.randint(2, 6)
            part = rng.choice(("ด้าน", "มุม"))
            ans = a * k1 + b * k2
            return MathDraw("", str(ans),
                            prompt=f"มี{n1} {a} รูป และ{n2} {b} รูป มี{part}รวมกันกี่{part}",
                            # The shapes counted, the sides swapped between them.
                            distractors=_story.keep(a + b, a * k2 + b * k1, a * k1 + b * k1,
                                                    ans + k1, answer=ans, lo=1))
        n = rng.randint(2, 9)
        ans = n * k1
        return MathDraw("", str(ans),
                        prompt=(f"ใช้ไม้จิ้มฟันต่อเป็น{n1} {n} รูป โดยแต่ละรูปไม่ใช้ไม้จิ้มฟันร่วมกัน "
                                f"ต้องใช้ไม้จิ้มฟันทั้งหมดกี่อัน"),
                        distractors=_story.keep(n + k1, (n + 1) * k1, n * k2, ans - 1,
                                                answer=ans, lo=1))
