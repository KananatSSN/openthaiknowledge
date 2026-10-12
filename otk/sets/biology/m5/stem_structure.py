"""โครงสร้างภายในของลำต้น

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/3

Sets moved here from: science_wave_f54.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f54 import SECTIONS, SUBJECT, UPPER_FIVE, slide

PROVENANCE = Provenance("original")


TOPIC_STEM = "โครงสร้างภายในของลำต้น"


STEM_PARTS = (
    ("เอพิเดอร์มิสของลำต้น", "เป็นชั้นนอกสุด มีคิวทินเคลือบลดการสูญเสียน้ำ"),
    ("คอร์เทกซ์ของลำต้น", "อยู่ถัดจากเอพิเดอร์มิส ส่วนใหญ่เป็นพาเรงคิมาและคอลเลงคิมา"),
    ("มัดท่อลำเลียง", "ประกอบด้วยไซเลมและโฟลเอ็มอยู่ในกลุ่มเดียวกัน"),
    ("วาสคิวลาร์แคมเบียม", "อยู่ระหว่างไซเลมและโฟลเอ็ม แบ่งเซลล์ทำให้ลำต้นขยายขนาด"),
    ("พิธของลำต้น", "อยู่ตรงกลางลำต้นพืชใบเลี้ยงคู่ เป็นพาเรงคิมาสะสมอาหาร"),
    ("บันเดิลชีท", "เป็นกลุ่มเซลล์ที่ล้อมรอบมัดท่อลำเลียงของพืชใบเลี้ยงเดี่ยว"),
)


STEM_COMPARE = {
    "ลำต้นพืชใบเลี้ยงคู่": ("มัดท่อลำเลียงเรียงเป็นวงเดียว", "มีวาสคิวลาร์แคมเบียมจึงเติบโตขั้นที่สองได้",
                            "แยกชั้นคอร์เทกซ์และพิธได้ชัดเจน", "ไม้ยืนต้นมีวงปีให้เห็น"),
    "ลำต้นพืชใบเลี้ยงเดี่ยว": ("มัดท่อลำเลียงกระจายทั่วลำต้น", "ส่วนใหญ่ไม่มีวาสคิวลาร์แคมเบียม",
                               "แยกชั้นคอร์เทกซ์และพิธได้ไม่ชัดเจน", "มัดท่อลำเลียงมีบันเดิลชีทล้อมรอบ"),
}


STEM_HINT = ("ลำต้นใบเลี้ยงคู่มีมัดท่อลำเลียงเป็นวงและมีแคมเบียม ลำต้นใบเลี้ยงเดี่ยวมีมัดท่อลำเลียงกระจายและไม่มีแคมเบียม "
             "วงปีเกิดจากไซเลมที่แคมเบียมสร้างในแต่ละปี")


@question_type(
    "biology.stem_structure_foundation",
    display_name={"th": "ส่วนประกอบภายในของลำต้นและหน้าที่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STEM,
)
class StemStructureFoundation(QuestionType):
    """Each part of the stem and its job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, role = rng.choice(STEM_PARTS)
        others = rng.sample([p for p in STEM_PARTS if p[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}มีลักษณะหรือหน้าที่ใด", correct=role, wrongs=tuple(p[1] for p in others), topic=TOPIC_STEM,
                             hint=STEM_HINT)
        return _labelled(stem=f"ส่วนใดของลำต้น{role}", correct=name, wrongs=tuple(p[0] for p in others), topic=TOPIC_STEM,
                         hint=STEM_HINT)


@question_type(
    "biology.stem_structure_fluency",
    display_name={"th": "เปรียบเทียบลำต้นพืชใบเลี้ยงเดี่ยวและใบเลี้ยงคู่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STEM,
)
class StemStructureFluency(QuestionType):
    """Ring against scattered bundles, cambium against none, and slides of each."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(STEM_COMPARE))
        other = next(k for k in STEM_COMPARE if k != kind)
        roll = rng.random()
        if roll < 0.45:
            return _labelled(stem=f"ข้อใดเป็นลักษณะของ{kind}", correct=rng.choice(STEM_COMPARE[kind]),
                             wrongs=tuple(STEM_COMPARE[other]), topic=TOPIC_STEM, hint=STEM_HINT)
        if roll < 0.7:
            return _labelled(stem=f"ลำต้นที่ \"{rng.choice(STEM_COMPARE[kind])}\" เป็นลำต้นของพืชกลุ่มใด", correct=kind,
                             wrongs=(other, "รากพืชใบเลี้ยงคู่", "รากพืชใบเลี้ยงเดี่ยว"), topic=TOPIC_STEM, hint=STEM_HINT)
        return _labelled(stem=f"ภาคตัดขวางที่ส่องด้วยกล้องจุลทรรศน์ {slide(rng, kind)} เป็นภาคตัดขวางของส่วนใด", correct=kind,
                         wrongs=tuple(k for k in SECTIONS if k != kind), topic=TOPIC_STEM, hint=STEM_HINT)


@question_type(
    "biology.stem_structure_application",
    display_name={"th": "วงปีและการเติบโตขั้นที่สองของลำต้น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STEM,
)
class StemStructureApplication(QuestionType):
    """One ring of xylem a year: count or measure rings for age and growth."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "แคมเบียมสร้างไซเลมเพิ่มปีละ 1 วงปี (เนื้อไม้สีอ่อนช่วงฝนและสีเข้มช่วงแล้ง) อายุ = จำนวนวงปี"
        roll = rng.random()
        if roll < 0.4:
            width = Fraction(rng.choice((2, 3, 4, 5, 6, 8, 10, 12, 15)), rng.choice((1, 2)))
            years = rng.randint(8, 80)
            radius = width * years
            return numeric(stem=f"ตัดลำต้นไม้ยืนต้นพบว่าเนื้อไม้มีรัศมี {show(radius)} mm (ไม่รวมพิธและเปลือก) ถ้าวงปีแต่ละวงกว้างเฉลี่ย "
                                f"{show(width)} mm ต้นไม้นี้มีอายุประมาณกี่ปี", answer=years,
                           wrongs=[years * 2, radius, years + 1], unit="ปี", topic=TOPIC_STEM, hint=hint)
        if roll < 0.7:
            planted = rng.randint(1990, 2015)
            cut = rng.randint(planted + 8, 2026)
            return numeric(stem=f"ต้นสักปลูกจากต้นกล้าอายุไม่ถึงปีเมื่อ พ.ศ. {planted + 543} และถูกตัดเมื่อ พ.ศ. {cut + 543} "
                                f"คาดว่าจะนับวงปีได้ประมาณกี่วง", answer=cut - planted,
                           wrongs=[(cut - planted) * 2, cut - planted + 1, cut - planted - 1], unit="วง", topic=TOPIC_STEM, hint=hint)
        facts = (("ข้อใดทำให้เกิดวงปีในลำต้นไม้ยืนต้น", "ไซเลมที่แคมเบียมสร้างในฤดูต่าง ๆ มีขนาดเซลล์และสีต่างกัน",
                  ("โฟลเอ็มที่สะสมพอกหนาขึ้นทุกวัน", "เปลือกไม้ที่ลอกออกทุกปี", "พิธที่ขยายตัวทุกฤดู", "เอพิเดอร์มิสที่หนาขึ้น")),
                 ("เหตุใดลำต้นข้าวโพดจึงไม่มีวงปี", "ไม่มีวาสคิวลาร์แคมเบียม จึงไม่มีการเติบโตขั้นที่สอง",
                  ("ไม่มีไซเลม", "มีวาสคิวลาร์แคมเบียมมากเกินไป", "มีมัดท่อลำเลียงเรียงเป็นวงเดียว", "เติบโตเฉพาะในฤดูฝน")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_STEM, hint=hint)
