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
