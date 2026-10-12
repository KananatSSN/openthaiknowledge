"""โครงสร้างภายในของราก

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/2

Sets moved here from: science_wave_f54.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f54 import SECTIONS, SUBJECT, UPPER_FIVE, slide

PROVENANCE = Provenance("original")


TOPIC_ROOT = "โครงสร้างภายในของราก"


ROOT_PARTS = (
    ("เอพิเดอร์มิส", "มีเซลล์บางเซลล์ยื่นออกไปเป็นขนราก ช่วยดูดน้ำ"),
    ("คอร์เทกซ์", "เป็นชั้นพาเรงคิมาหนาที่สะสมอาหาร"),
    ("เอนโดเดอร์มิส", "มีแถบแคสแพเรียนควบคุมการผ่านของน้ำและสารเข้าสู่ท่อลำเลียง"),
    ("เพริไซเคิล", "เป็นแหล่งกำเนิดของรากแขนง"),
    ("ไซเลมของราก", "ลำเลียงน้ำและธาตุอาหารขึ้นสู่ลำต้น"),
    ("พิธของรากพืชใบเลี้ยงเดี่ยว", "อยู่ตรงกลางราก เป็นพาเรงคิมาสะสมอาหาร"),
)


ROOT_COMPARE = {
    "รากพืชใบเลี้ยงคู่": ("ไซเลมเรียงเป็นแฉก 2-6 แฉกอยู่ตรงกลาง", "ส่วนใหญ่ไม่มีพิธ หรือมีขนาดเล็กมาก",
                          "มีวาสคิวลาร์แคมเบียมทำให้เกิดการเติบโตขั้นที่สอง", "จำนวนแฉกของไซเลมมักไม่เกิน 6 แฉก",
                          "รากแก้วของไม้ยืนต้นขยายขนาดขึ้นได้ทุกปี"),
    "รากพืชใบเลี้ยงเดี่ยว": ("ไซเลมเรียงเป็นวงรอบพิธ มีจำนวนแฉกมาก", "มีพิธขนาดใหญ่อยู่ตรงกลาง",
                             "ไม่มีวาสคิวลาร์แคมเบียม จึงไม่มีการเติบโตขั้นที่สอง", "จำนวนกลุ่มไซเลมมักมากกว่า 6 กลุ่ม",
                             "รากฝอยมีขนาดใกล้เคียงกันตลอดอายุ"),
}


ROOT_HINT = ("ภาคตัดขวางรากจากนอกเข้าใน: เอพิเดอร์มิส คอร์เทกซ์ เอนโดเดอร์มิส เพริไซเคิล และท่อลำเลียง "
             "ใบเลี้ยงคู่ไซเลมเป็นแฉกน้อยไม่มีพิธ ใบเลี้ยงเดี่ยวไซเลมเป็นวงหลายกลุ่มมีพิธ")


DICOT_ROOT_PLANTS = ("ถั่วเขียว", "พริก", "มะเขือ", "ทานตะวัน")


MONOCOT_PLANTS = ("ข้าวโพด", "หญ้า", "ข้าว", "พุทธรักษา")


@question_type(
    "biology.root_structure_foundation",
    display_name={"th": "ส่วนประกอบภายในของรากและหน้าที่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ROOT,
)
class RootStructureFoundation(QuestionType):
    """Each layer of the root and its job, and their order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            order = ["เอพิเดอร์มิส", "คอร์เทกซ์", "เอนโดเดอร์มิส", "เพริไซเคิล", "ไซเลม"]
            wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
            while len(wrongs) < 3:
                o = order[:]
                rng.shuffle(o)
                if o != order:
                    wrongs[" → ".join(o)] = None
            return _labelled(stem="น้ำจากดินเคลื่อนที่ผ่านชั้นต่าง ๆ ของรากตามลำดับใดก่อนเข้าสู่ไซเลม", correct=" → ".join(order),
                             wrongs=tuple(wrongs), topic=TOPIC_ROOT, hint=ROOT_HINT)
        name, role = rng.choice(ROOT_PARTS)
        others = rng.sample([p for p in ROOT_PARTS if p[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}มีลักษณะหรือหน้าที่ใด", correct=role, wrongs=tuple(p[1] for p in others), topic=TOPIC_ROOT,
                             hint=ROOT_HINT)
        return _labelled(stem=f"ส่วนใดของราก{role}", correct=name, wrongs=tuple(p[0] for p in others), topic=TOPIC_ROOT, hint=ROOT_HINT)


@question_type(
    "biology.root_structure_fluency",
    display_name={"th": "เปรียบเทียบรากพืชใบเลี้ยงเดี่ยวและใบเลี้ยงคู่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ROOT,
)
class RootStructureFluency(QuestionType):
    """What sets the two kinds of root apart."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(ROOT_COMPARE))
        other = next(k for k in ROOT_COMPARE if k != kind)
        if rng.random() < 0.6:
            return _labelled(stem=f"ข้อใดเป็นลักษณะของ{kind}", correct=rng.choice(ROOT_COMPARE[kind]),
                             wrongs=tuple(ROOT_COMPARE[other]), topic=TOPIC_ROOT, hint=ROOT_HINT)
        feature = rng.choice(ROOT_COMPARE[kind])
        return _labelled(stem=f"ภาคตัดขวางรากที่ \"{feature}\" เป็นรากของพืชกลุ่มใด", correct=kind,
                         wrongs=(other, "ลำต้นพืชใบเลี้ยงคู่", "ลำต้นพืชใบเลี้ยงเดี่ยว"), topic=TOPIC_ROOT, hint=ROOT_HINT)


@question_type(
    "biology.root_structure_application",
    display_name={"th": "ระบุชนิดของภาคตัดขวางรากและลำต้นจากสิ่งที่เห็น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ROOT,
)
class RootStructureApplication(QuestionType):
    """A described slide of a root, identified among roots and stems."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(SECTIONS[:2])
        if rng.random() < 0.3:
            plant = rng.choice(DICOT_ROOT_PLANTS if kind == "รากพืชใบเลี้ยงคู่" else MONOCOT_PLANTS)
            feature = "ไซเลมเรียงเป็นแฉกจำนวนน้อยและไม่มีพิธ" if kind == "รากพืชใบเลี้ยงคู่" else "ไซเลมเรียงเป็นวงหลายกลุ่มรอบพิธ"
            wrongs = ("ไซเลมเรียงเป็นวงหลายกลุ่มรอบพิธ" if kind == "รากพืชใบเลี้ยงคู่" else "ไซเลมเรียงเป็นแฉกจำนวนน้อยและไม่มีพิธ",
                      "มัดท่อลำเลียงกระจายทั่วไปไม่เป็นระเบียบ", "มัดท่อลำเลียงเรียงเป็นวงเดียวและมีแคมเบียม")
            return _labelled(stem=f"ภาคตัดขวางรากของ{plant}น่าจะมีลักษณะใด", correct=feature, wrongs=wrongs, topic=TOPIC_ROOT,
                             hint=ROOT_HINT)
        return _labelled(stem=f"ภาคตัดขวางที่ส่องด้วยกล้องจุลทรรศน์ {slide(rng, kind)} เป็นภาคตัดขวางของส่วนใด", correct=kind,
                         wrongs=tuple(k for k in SECTIONS if k != kind), topic=TOPIC_ROOT, hint=ROOT_HINT)
