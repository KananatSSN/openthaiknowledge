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


# ── More shapes (2026-11): curved and straight edges, kinds of lines, the faces of solids, corners of
# several shapes, a circle beside an ellipse, and counting shapes in a list ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import WordProblem  # noqa: E402
from otk.sets._support.math_p2 import LEVEL  # noqa: E402

_P2_POLY = {"รูปสามเหลี่ยม": 3, "รูปสี่เหลี่ยม": 4, "รูปห้าเหลี่ยม": 5, "รูปหกเหลี่ยม": 6}
_P2_SOLID_FACES = {"ทรงสี่เหลี่ยมมุมฉาก": 6, "ลูกบาศก์": 6, "ทรงกระบอก": 2, "กรวย": 1, "ทรงกลม": 0}


@question_type("math.curved_straight_p2", display_name={"th": "รูปที่มีขอบโค้งหรือขอบตรง"},
               level=LEVEL, topic="รูปเรขาคณิต")
class CurvedStraightP2(ConceptBankType):
    ITEMS = [
        Concept("รูปใดมีขอบเป็นเส้นโค้งทั้งหมด", "รูปวงกลม", ("รูปสามเหลี่ยม", "รูปสี่เหลี่ยม", "รูปห้าเหลี่ยม")),
        Concept("รูปใดมีขอบเป็นเส้นตรงทั้งหมด", "รูปสี่เหลี่ยม", ("รูปวงกลม", "รูปวงรี", "รูปครึ่งวงกลม")),
        Concept("รูปใดมีขอบเป็นเส้นตรงและเส้นโค้ง", "รูปครึ่งวงกลม", ("รูปวงกลม", "รูปสามเหลี่ยม", "รูปสี่เหลี่ยม")),
        Concept("รูปใดไม่มีมุมเลย", "รูปวงรี", ("รูปสามเหลี่ยม", "รูปสี่เหลี่ยม", "รูปครึ่งวงกลม")),
        Concept("รูปใดมีขอบเป็นเส้นตรง 3 เส้น", "รูปสามเหลี่ยม", ("รูปสี่เหลี่ยม", "รูปวงกลม", "รูปห้าเหลี่ยม")),
    ]


@question_type("math.line_kinds_p2", display_name={"th": "เส้นตรง เส้นโค้ง และส่วนของเส้นตรง"},
               level=LEVEL, topic="รูปเรขาคณิต")
class LineKindsP2(ConceptBankType):
    ITEMS = [
        Concept("ขอบของไม้บรรทัดเป็นเส้นแบบใด", "เส้นตรง", ("เส้นโค้ง", "เส้นซิกแซก", "จุด")),
        Concept("ขอบของจานข้าวกลม ๆ เป็นเส้นแบบใด", "เส้นโค้ง", ("เส้นตรง", "เส้นซิกแซก", "จุด")),
        Concept("ด้านของรูปสามเหลี่ยมเป็นเส้นแบบใด", "เส้นตรง", ("เส้นโค้ง", "เส้นวงกลม", "จุด")),
        Concept("ใช้เครื่องมือใดช่วยลากเส้นตรง", "ไม้บรรทัด", ("ยางลบ", "กรรไกร", "กาว")),
        Concept("จุดที่ด้านสองด้านของรูปสามเหลี่ยมมาพบกันเรียกว่าอะไร", "จุดยอดมุม", ("ด้าน", "เส้นโค้ง", "ขอบโค้ง")),
    ]


@question_type("math.solid_faces_count_p2", display_name={"th": "จำนวนหน้าเรียบของรูปเรขาคณิตสามมิติ"},
               level=LEVEL, topic="รูปเรขาคณิต")
class SolidFacesCountP2(WordProblem):
    def expr(self, rng: Random):
        name = rng.choice(tuple(_P2_SOLID_FACES))
        right = _P2_SOLID_FACES[name]
        # The other solids' counts and one off.
        return MathDraw("", str(right), prompt=f"{name}มีหน้าที่เป็นรูปแบนเรียบกี่หน้า",
                        distractors=_story.keep(*[v for v in (6, 2, 1, 0, 4) if v != right], right + 1,
                                                answer=right, lo=0))


@question_type("math.total_corners_p2", display_name={"th": "จำนวนมุมของรูปหลายรูปรวมกัน"},
               level=LEVEL, topic="รูปเรขาคณิต")
class TotalCornersP2(WordProblem):
    def expr(self, rng: Random):
        x, y = rng.sample(tuple(_P2_POLY), 2)
        a, b = rng.randint(2, 4), rng.randint(1, 3)
        right = a * _P2_POLY[x] + b * _P2_POLY[y]
        prompt = f"{x} {a} รูป และ{y} {b} รูป มีมุมรวมกันกี่มุม"
        # Shapes counted instead of corners; one shape of each; the counts swapped.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a + b, _P2_POLY[x] + _P2_POLY[y], b * _P2_POLY[x] + a * _P2_POLY[y],
                                                right + 1, answer=right, lo=1))


@question_type("math.circle_ellipse_p2", display_name={"th": "รูปวงกลมและรูปวงรี"},
               level=LEVEL, topic="รูปเรขาคณิต")
class CircleEllipseP2(ConceptBankType):
    ITEMS = [
        Concept("รูปใดกว้างและยาวเท่ากันทุกทาง", "รูปวงกลม", ("รูปวงรี", "รูปสี่เหลี่ยมผืนผ้า", "รูปสามเหลี่ยม")),
        Concept("ไข่ไก่เมื่อมองจากด้านข้างมีรูปร่างคล้ายรูปใด", "รูปวงรี", ("รูปวงกลม", "รูปสี่เหลี่ยม", "รูปสามเหลี่ยม")),
        Concept("เหรียญบาทมีรูปร่างเป็นรูปใด", "รูปวงกลม", ("รูปวงรี", "รูปสี่เหลี่ยม", "รูปหกเหลี่ยม")),
        Concept("รูปวงกลมกับรูปวงรีเหมือนกันอย่างไร", "ไม่มีมุมทั้งสองรูป",
                ("มีมุมเท่ากัน", "มีด้านตรงเท่ากัน", "กว้างและยาวเท่ากัน")),
        Concept("รูปวงรีต่างจากรูปวงกลมอย่างไร", "รูปวงรียาวด้านหนึ่งมากกว่าอีกด้าน",
                ("รูปวงรีมีมุม", "รูปวงรีมีด้านตรง", "รูปวงรีมีขนาดเล็กกว่าเสมอ")),
    ]


@question_type("math.count_shapes_list_p2", display_name={"th": "นับรูปเรขาคณิตแต่ละชนิด"},
               level=LEVEL, topic="รูปเรขาคณิต")
class CountShapesListP2(WordProblem):
    _SYMBOLS = {"△": "รูปสามเหลี่ยม", "□": "รูปสี่เหลี่ยม", "○": "รูปวงกลม"}

    def expr(self, rng: Random):
        row = [rng.choice(tuple(self._SYMBOLS)) for _ in range(rng.randint(8, 14))]
        sym = rng.choice(tuple(self._SYMBOLS))
        right = row.count(sym)
        if right == 0:
            row[rng.randrange(len(row))] = sym
            right = 1
        prompt = f"{'  '.join(row)}  มี{self._SYMBOLS[sym]}กี่รูป"
        # Another shape's count; all of them; one off.
        others = [row.count(s) for s in self._SYMBOLS if s != sym]
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(*others, len(row), right + 1, right - 1, answer=right, lo=0))
