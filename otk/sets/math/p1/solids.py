"""เรขาคณิต 3 มิติ

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.1/*

Sets moved here from: math, math_apply_stage, math_diagrams, math_thin_topics.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_diagrams import SOLIDS, _img, _text_q
from otk.sets._support.math_gaps_shape_data import _choices
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_p2 import _texts

PROVENANCE = Provenance("original")


_OBJECTS = (("ลูกฟุตบอล", "ทรงกลม"), ("ส้มโอ", "ทรงกลม"), ("กระป๋องนม", "ทรงกระบอก"),
            ("แก้วน้ำทรงตรง", "ทรงกระบอก"), ("กล่องนม", "ทรงสี่เหลี่ยมมุมฉาก"),
            ("ตู้เย็น", "ทรงสี่เหลี่ยมมุมฉาก"), ("กรวยจราจร", "กรวย"), ("หมวกวันเกิดทรงแหลม", "กรวย"),
            ("ลูกเต๋า", "ทรงสี่เหลี่ยมมุมฉาก"), ("ท่อน้ำ", "ทรงกระบอก"))


_SOLIDS = ("ทรงกลม", "ทรงกระบอก", "ทรงสี่เหลี่ยมมุมฉาก", "กรวย")


P1 = {"th": "ป.1"}


_OBJECTS_math_thin_topics = (
    ("กล่องนม", "ทรงสี่เหลี่ยมมุมฉาก"), ("ก้อนอิฐ", "ทรงสี่เหลี่ยมมุมฉาก"), ("กล่องดินสอ", "ทรงสี่เหลี่ยมมุมฉาก"),
    ("ลูกบอล", "ทรงกลม"), ("ลูกส้ม", "ทรงกลม"), ("ลูกแก้ว", "ทรงกลม"),
    ("กระป๋องนม", "ทรงกระบอก"), ("ท่อนไม้", "ทรงกระบอก"), ("ถ่านไฟฉาย", "ทรงกระบอก"),
    ("กรวยจราจร", "กรวย"), ("หมวกวันเกิด", "กรวย"), ("กรวยไอศกรีม", "กรวย"),
)


_SHAPES = ("ทรงสี่เหลี่ยมมุมฉาก", "ทรงกลม", "ทรงกระบอก", "กรวย")


@question_type("math.classify_3d_solid",
               display_name={"th": "จำแนกรูปทรง 3 มิติ"}, level={"th": "ป.1"},
               topic="เรขาคณิต 3 มิติ")
class Classify3DSolid(ConceptBankType):
    ITEMS = [
        Concept("ทรงใดกลิ้งได้ทุกทิศทางและมีผิวโค้งทั้งหมด?", "ทรงกลม",
                ("ทรงสี่เหลี่ยมมุมฉาก", "พีระมิด", "กรวย")),
        Concept("ทรงใดมียอดแหลมและฐานเป็นวงกลม?", "กรวย",
                ("ทรงกลม", "ทรงกระบอก", "พีระมิด")),
        Concept("ทรงใดมียอดแหลมและฐานเป็นรูปหลายเหลี่ยม?", "พีระมิด",
                ("ทรงกลม", "กรวย", "ทรงกระบอก")),
        Concept("ทรงใดมีหน้าเรียบทุกหน้าและทุกหน้าเป็นรูปสี่เหลี่ยม?",
                "ทรงสี่เหลี่ยมมุมฉาก",
                ("ทรงกลม", "กรวย", "พีระมิด")),
        Concept("ลูกบอลมีรูปทรงแบบใด?", "ทรงกลม",
                ("ทรงกระบอก", "กรวย", "ทรงสี่เหลี่ยมมุมฉาก")),
        Concept("กระป๋องน้ำอัดลมมีรูปทรงแบบใด?", "ทรงกระบอก",
                ("ทรงกลม", "กรวย", "พีระมิด")),
        Concept("หมวกปาร์ตี้ทรงแหลมมีรูปทรงแบบใด?", "กรวย",
                ("ทรงกลม", "ทรงกระบอก", "ทรงสี่เหลี่ยมมุมฉาก")),
        Concept("กล่องของขวัญมีรูปทรงแบบใด?", "ทรงสี่เหลี่ยมมุมฉาก",
                ("ทรงกลม", "กรวย", "ทรงกระบอก")),
    ]


@question_type("math.solid_count_p1", display_name={"th": "นับสิ่งของตามรูปทรง"},
               level=P1, topic="เรขาคณิต 3 มิติ")
class SolidCountP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.6:
            things = rng.sample(_OBJECTS_math_thin_topics, 6)
            shape = rng.choice(sorted({s for _, s in things}))
            n = sum(s == shape for _, s in things)
            other = next(s for s in _SHAPES if s != shape)
            names = " ".join(o for o, _ in things)
            return _num_maths([text(f"มีสิ่งของดังนี้ {names} สิ่งของที่มีรูปทรงเป็น{shape}มีกี่ชิ้น")],
                              str(n), [str(n + 1), str(6 - n), str(sum(s == other for _, s in things) or n + 2)],
                              self.topic)
        shape = rng.choice(_SHAPES)
        same = [o for o, s in _OBJECTS_math_thin_topics if s == shape]
        odd = rng.choice([o for o, s in _OBJECTS_math_thin_topics if s != shape])
        return _texts([text("สิ่งของใดมีรูปทรงต่างจากสิ่งของอื่น")], odd, same, self.topic)


@question_type("math.solid_objects_p1", display_name={"th": "รูปเรขาคณิตสามมิติของสิ่งของรอบตัว"},
               level={"th": "ป.1"}, topic="เรขาคณิต 3 มิติ")
class SolidObjectsP1(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            thing, solid = rng.choice(_OBJECTS)
            return _choices([text(f"{thing}มีรูปร่างคล้ายรูปเรขาคณิตสามมิติชนิดใด")], solid,
                            [s for s in _SOLIDS if s != solid], self.topic)
        if kind == 1:
            solid = rng.choice(_SOLIDS)
            right = rng.choice([t for t, s in _OBJECTS if s == solid])
            others = [rng.choice([t for t, s in _OBJECTS if s == o]) for o in _SOLIDS if o != solid]
            return _choices([text(f"สิ่งของใดมีรูปร่างคล้าย{solid}")], right, others, self.topic)
        picked = rng.sample(_OBJECTS, 5)
        solid = rng.choice([s for _, s in picked])
        count = sum(s == solid for _, s in picked)
        listed = " ".join(t for t, _ in picked)
        return maths([text(f"มีสิ่งของดังนี้: {listed} สิ่งของที่มีรูปร่างคล้าย{solid}มีกี่ชิ้น")], str(count),
                     _nums(count, count + 1, count - 1, 5 - count, lo=0), self.topic)


@question_type("math.solid_picture_p1", display_name={"th": "บอกชื่อรูปเรขาคณิตสามมิติจากรูป"},
               level={"th": "ป.1"}, topic="เรขาคณิต 3 มิติ")
class SolidPictureP1(QuestionType):
    _NEAR = {"cube": "ทรงสี่เหลี่ยมมุมฉาก", "cuboid": "ทรงลูกบาศก์", "cylinder": "กรวย",
             "cone": "พีระมิดฐานสี่เหลี่ยม", "sphere": "ทรงกระบอก", "sq_pyramid": "กรวย",
             "tri_pyramid": "พีระมิดฐานสี่เหลี่ยม", "tri_prism": "พีระมิดฐานสามเหลี่ยม",
             "pent_prism": "ปริซึมสามเหลี่ยม"}

    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SOLIDS)
        others = [x.thai for x in SOLIDS if x.thai not in (s.thai, self._NEAR[s.name])]
        rng.shuffle(others)
        return _text_q([text("รูปนี้คือรูปเรขาคณิตสามมิติชนิดใด"),
                        _img(s.asset_id, "รูปเรขาคณิตสามมิติหนึ่งรูป")],
                       s.thai, [self._NEAR[s.name]] + others, self.topic)


# ── More solids (2026-11): rolling and stacking, the shapes of the faces, tracing a base, counting solids,
# the odd one out, and which object has a given shape ──

from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem  # noqa: E402
from otk.sets._support.math_p1 import LEVEL  # noqa: E402

_SOLID_OBJECTS = {
    "ทรงกลม": ("ลูกฟุตบอล", "ส้ม", "ลูกแก้ว", "ลูกปิงปอง"),
    "ทรงกระบอก": ("กระป๋องนม", "แก้วน้ำ", "ท่อน้ำ", "ถ่านไฟฉาย"),
    "ทรงสี่เหลี่ยมมุมฉาก": ("กล่องนม", "หนังสือ", "ตู้เย็น", "กล่องดินสอ"),
    "กรวย": ("กรวยจราจร", "หมวกวันเกิด", "โคนไอศกรีม"),
}


@question_type("math.solid_roll_stack_p1", display_name={"th": "รูปทรงใดกลิ้งได้ รูปทรงใดวางซ้อนได้"},
               level=LEVEL, topic="เรขาคณิต 3 มิติ")
class SolidRollStackP1(ConceptBankType):
    ITEMS = [
        Concept("รูปทรงใดกลิ้งได้ทุกทิศทาง", "ทรงกลม", ("ทรงสี่เหลี่ยมมุมฉาก", "กรวย", "ทรงกระบอก")),
        Concept("รูปทรงใดวางซ้อนกันได้มั่นคงที่สุด", "ทรงสี่เหลี่ยมมุมฉาก", ("ทรงกลม", "กรวย", "ทรงกระบอกที่วางนอน")),
        Concept("รูปทรงใดกลิ้งไม่ได้เลย", "ทรงสี่เหลี่ยมมุมฉาก", ("ทรงกลม", "ทรงกระบอก", "กรวย")),
        Concept("รูปทรงใดทั้งกลิ้งได้เมื่อวางนอน และวางตั้งซ้อนกันได้", "ทรงกระบอก", ("ทรงกลม", "กรวย", "ทรงสี่เหลี่ยมมุมฉาก")),
        Concept("รูปทรงใดกลิ้งได้เป็นวงรอบปลายแหลมของมัน", "กรวย", ("ทรงกลม", "ทรงกระบอก", "ทรงสี่เหลี่ยมมุมฉาก")),
    ]


@question_type("math.solid_face_shape_p1", display_name={"th": "หน้าของรูปทรงเป็นรูปใด"},
               level=LEVEL, topic="เรขาคณิต 3 มิติ")
class SolidFaceShapeP1(ConceptBankType):
    ITEMS = [
        Concept("หน้าของทรงสี่เหลี่ยมมุมฉากเป็นรูปใด", "รูปสี่เหลี่ยม", ("รูปวงกลม", "รูปสามเหลี่ยม", "รูปวงรี")),
        Concept("ฐานของทรงกระบอกเป็นรูปใด", "รูปวงกลม", ("รูปสี่เหลี่ยม", "รูปสามเหลี่ยม", "รูปห้าเหลี่ยม")),
        Concept("ฐานของกรวยเป็นรูปใด", "รูปวงกลม", ("รูปสามเหลี่ยม", "รูปสี่เหลี่ยม", "รูปห้าเหลี่ยม")),
        Concept("ทรงกลมมีหน้าที่เป็นรูปแบนราบกี่หน้า", "ไม่มีเลย", ("1 หน้า", "2 หน้า", "6 หน้า")),
        Concept("ทรงกระบอกมีหน้าที่เป็นรูปวงกลมกี่หน้า", "2 หน้า", ("1 หน้า", "ไม่มีเลย", "6 หน้า")),
        Concept("ลูกเต๋ามีหน้าทั้งหมดกี่หน้า", "6 หน้า", ("4 หน้า", "5 หน้า", "8 หน้า")),
    ]


@question_type("math.solid_trace_p1", display_name={"th": "วาดรอยรอบฐานของรูปทรงได้รูปใด"},
               level=LEVEL, topic="เรขาคณิต 3 มิติ")
class SolidTraceP1(ConceptBankType):
    ITEMS = [
        Concept("วางกระป๋องนมตั้งบนกระดาษแล้ววาดรอบฐาน จะได้รูปใด", "รูปวงกลม",
                ("รูปวงรี", "รูปดาว", "รูปสามเหลี่ยม")),
        Concept("วางกล่องนมบนกระดาษแล้ววาดรอบด้านที่วางลง จะได้รูปใด", "รูปสี่เหลี่ยม",
                ("รูปวงกลม", "รูปสามเหลี่ยม", "รูปวงรี")),
        Concept("วางกรวยจราจรตั้งบนกระดาษแล้ววาดรอบฐาน จะได้รูปใด", "รูปวงกลม",
                ("รูปดาว", "รูปหัวใจ", "รูปสามเหลี่ยม")),
        Concept("วางลูกเต๋าบนกระดาษแล้ววาดรอบด้านที่วางลง จะได้รูปใด", "รูปสี่เหลี่ยมจัตุรัส",
                ("รูปวงกลม", "รูปสามเหลี่ยม", "รูปห้าเหลี่ยม")),
        Concept("วางแก้วน้ำทรงกระบอกตั้งบนกระดาษแล้ววาดรอบฐาน จะได้รูปใด", "รูปวงกลม",
                ("รูปวงรี", "รูปหัวใจ", "รูปสี่เหลี่ยม")),
    ]


@question_type("math.solid_sum_p1", display_name={"th": "นับและรวมสิ่งของตามรูปทรง"},
               level=LEVEL, topic="เรขาคณิต 3 มิติ")
class SolidSumP1(WordProblem):
    def expr(self, rng: Random):
        s1, s2 = rng.sample(tuple(_SOLID_OBJECTS), 2)
        o1, o2 = rng.choice(_SOLID_OBJECTS[s1]), rng.choice(_SOLID_OBJECTS[s2])
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        c = rng.randint(1, 9)
        o3 = rng.choice([o for o in _SOLID_OBJECTS[s1] if o != o1])
        right = a + c
        prompt = (f"ในห้องมี{o1} {a} ชิ้น {o2} {b} ชิ้น และ{o3} {c} ชิ้น "
                  f"มีสิ่งของที่เป็น{s1}ทั้งหมดกี่ชิ้น")
        # Everything counted; the wrong pair counted; only the first kind.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a + b + c, a + b, b + c, a, answer=right, lo=1))


@question_type("math.solid_odd_one_p1", display_name={"th": "สิ่งของใดมีรูปทรงต่างจากพวก"},
               level=LEVEL, topic="เรขาคณิต 3 มิติ")
class SolidOddOneP1(ChoiceType):
    def compose(self, rng: Random):
        same, odd = rng.sample(tuple(_SOLID_OBJECTS), 2)
        group = rng.sample(_SOLID_OBJECTS[same], 3)
        right = rng.choice(_SOLID_OBJECTS[odd])
        return "สิ่งของใดมีรูปทรงต่างจากสิ่งของอื่น", right, group


@question_type("math.solid_which_object_p1", display_name={"th": "สิ่งของใดมีรูปทรงตามที่กำหนด"},
               level=LEVEL, topic="เรขาคณิต 3 มิติ")
class SolidWhichObjectP1(ChoiceType):
    def compose(self, rng: Random):
        shapes = list(_SOLID_OBJECTS)
        shape = rng.choice(shapes)
        right = rng.choice(_SOLID_OBJECTS[shape])
        wrongs = [rng.choice(_SOLID_OBJECTS[s]) for s in shapes if s != shape]
        return f"สิ่งของใดมีรูปทรงเป็น{shape}", right, wrongs
