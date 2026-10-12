"""หมู่ฟังก์ชันและประเภทของสารประกอบอินทรีย์

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/3

Sets moved here from: science_wave_f26.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f26 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_GROUP = "หมู่ฟังก์ชันและประเภทของสารประกอบอินทรีย์"


# class: (group as written, group name, examples)
CLASSES = {
    "แอลเคน": ("C–C (พันธะเดี่ยวทั้งหมด)", "ไม่มีหมู่ฟังก์ชัน", ("CH₃CH₂CH₃", "CH₃(CH₂)₄CH₃", "CH₃CH(CH₃)CH₃")),
    "แอลคีน": ("C=C", "พันธะคู่ระหว่างคาร์บอน", ("CH₂=CHCH₃", "CH₃CH=CHCH₃", "CH₂=CHCH₂CH₃")),
    "แอลไคน์": ("C≡C", "พันธะสามระหว่างคาร์บอน", ("HC≡CCH₃", "CH₃C≡CCH₃", "HC≡CCH₂CH₃")),
    "แอลกอฮอล์": ("–OH", "ไฮดรอกซิล", ("CH₃OH", "CH₃CH₂OH", "CH₃CH(OH)CH₃", "CH₃CH₂CH₂CH₂OH")),
    "อีเทอร์": ("–O–", "แอลคอกซี", ("CH₃OCH₃", "CH₃CH₂OCH₂CH₃", "CH₃OCH₂CH₃")),
    "แอลดีไฮด์": ("–CHO", "ฟอร์มิล", ("HCHO", "CH₃CHO", "CH₃CH₂CHO")),
    "คีโตน": ("–CO– (C=O ระหว่างคาร์บอนสองอะตอม)", "คาร์บอนิล", ("CH₃COCH₃", "CH₃COCH₂CH₃", "CH₃CH₂COCH₂CH₃")),
    "กรดคาร์บอกซิลิก": ("–COOH", "คาร์บอกซิล", ("HCOOH", "CH₃COOH", "CH₃CH₂COOH")),
    "เอสเทอร์": ("–COO–", "แอลคอกซีคาร์บอนิล", ("HCOOCH₃", "CH₃COOCH₃", "CH₃COOCH₂CH₃", "CH₃CH₂COOCH₃")),
    "เอมีน": ("–NH₂", "อะมิโน", ("CH₃NH₂", "CH₃CH₂NH₂", "CH₃CH₂CH₂NH₂")),
    "เอไมด์": ("–CONH₂", "เอไมด์", ("HCONH₂", "CH₃CONH₂", "CH₃CH₂CONH₂")),
}


# Classes a student most often confuses, tried first as distractors.
CONFUSED = {"แอลกอฮอล์": "อีเทอร์", "อีเทอร์": "แอลกอฮอล์", "แอลดีไฮด์": "คีโตน", "คีโตน": "แอลดีไฮด์",
            "กรดคาร์บอกซิลิก": "เอสเทอร์", "เอสเทอร์": "กรดคาร์บอกซิลิก", "เอมีน": "เอไมด์", "เอไมด์": "เอมีน",
            "แอลเคน": "แอลคีน", "แอลคีน": "แอลไคน์", "แอลไคน์": "แอลคีน"}


EXAMPLES = tuple((f, c) for c, (_, _, fs) in CLASSES.items() for f in fs)


def _class_wrongs(rng: Random, right: str) -> tuple[str, ...]:
    rest = [c for c in CLASSES if c not in (right, CONFUSED[right])]
    return (CONFUSED[right], *rng.sample(rest, 2))


@question_type(
    "chem.functional_group_foundation",
    display_name={"th": "หมู่ฟังก์ชันและชื่อหมู่"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GROUP,
)
class FunctionalGroupFoundation(QuestionType):
    """Group ↔ class ↔ group name."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cls = rng.choice([c for c in CLASSES if c != "แอลเคน"])
        group, group_name, _ = CLASSES[cls]
        hint = "–OH ไฮดรอกซิล (แอลกอฮอล์) –O– (อีเทอร์) –CHO (แอลดีไฮด์) –CO– (คีโตน) –COOH (กรด) –COO– (เอสเทอร์) –NH₂ (เอมีน) –CONH₂ (เอไมด์)"
        # Only the heteroatom groups have names; C=C and C≡C are just bonds.
        ask = rng.randrange(3) if cls not in ("แอลคีน", "แอลไคน์") else rng.randrange(2)
        if ask == 0:
            return _labelled(stem=f"สารประกอบอินทรีย์ที่มีหมู่ฟังก์ชัน {group} จัดเป็นสารประเภทใด", correct=cls,
                             wrongs=_class_wrongs(rng, cls), topic=TOPIC_GROUP, hint=hint)
        if ask == 1:
            others = [CLASSES[c][0] for c in _class_wrongs(rng, cls)]
            return _labelled(stem=f"สารประเภท{cls}มีหมู่ฟังก์ชันใด", correct=group, wrongs=tuple(others),
                             topic=TOPIC_GROUP, hint=hint)
        named = [CLASSES[c][1] for c in CLASSES if c not in ("แอลเคน", "แอลคีน", "แอลไคน์", cls)]
        names = rng.sample(named, 3)
        return _labelled(stem=f"หมู่ฟังก์ชันของ{cls} ({group}) มีชื่อว่าหมู่อะไร", correct=group_name,
                         wrongs=tuple(names), topic=TOPIC_GROUP, hint=hint)


@question_type(
    "chem.functional_group_fluency",
    display_name={"th": "ระบุประเภทสารประกอบอินทรีย์จากสูตรโครงสร้าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GROUP,
)
class FunctionalGroupFluency(QuestionType):
    """Find the group in a condensed formula and name the class."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        formula, cls = rng.choice(EXAMPLES)
        return _labelled(stem=f"สาร {formula} จัดเป็นสารประกอบอินทรีย์ประเภทใด", correct=cls,
                         wrongs=_class_wrongs(rng, cls), topic=TOPIC_GROUP,
                         hint="แยกให้ออก: -COOH (กรด) กับ -COO- ที่มี C ต่อท้าย (เอสเทอร์), -CHO ที่ปลาย (แอลดีไฮด์) "
                              "กับ -CO- กลางสาย (คีโตน), -OH (แอลกอฮอล์) กับ -O- กลางสาย (อีเทอร์)")


@question_type(
    "chem.functional_group_application",
    display_name={"th": "เลือกสารตามประเภทและเปรียบเทียบหมู่ฟังก์ชัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GROUP,
)
class FunctionalGroupApplication(QuestionType):
    """Pick the one compound of a class, or the one sharing a class with a given compound."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cls = rng.choice(sorted(CLASSES))
        right = rng.choice(CLASSES[cls][2])
        confused = [f for f in CLASSES[CONFUSED[cls]][2]]
        rest = [f for f, c in EXAMPLES if c not in (cls, CONFUSED[cls])]
        wrongs = (rng.choice(confused), *rng.sample(rest, 2))
        hint = "หาหมู่ฟังก์ชันในแต่ละสูตรก่อน แล้วจึงจัดประเภท"
        if rng.random() < 0.5:
            return _labelled(stem=f"สารในข้อใดจัดเป็น{cls}", correct=right, wrongs=wrongs, topic=TOPIC_GROUP, hint=hint)
        given = rng.choice([f for f in CLASSES[cls][2] if f != right])
        return _labelled(stem=f"สารในข้อใดเป็นสารประเภทเดียวกับ {given}", correct=right, wrongs=wrongs,
                         topic=TOPIC_GROUP, hint=hint)
