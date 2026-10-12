"""การจำแนกวัตถุเป็นตัวกลางโปร่งใส ตัวกลางโปร่งแสง และวัตถุทึบแสง

ฟิสิกส์ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.4/1

Sets moved here from: science_wave_d24.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT

PROVENANCE = Provenance("original")


FOURTH = {"th": "ป.4"}


LIGHT_MEDIUM_TOPIC = "การจำแนกวัตถุเป็นตัวกลางโปร่งใส ตัวกลางโปร่งแสง และวัตถุทึบแสง"


CATEGORY_DESCRIPTIONS = {
    "ตัวกลางโปร่งใส": "มองเห็นสิ่งต่าง ๆ ด้านหลังได้ชัดเจน",
    "ตัวกลางโปร่งแสง": "มองเห็นสิ่งต่าง ๆ ด้านหลังได้ราง ๆ ไม่ชัดเจน",
    "วัตถุทึบแสง": "มองไม่เห็นสิ่งต่าง ๆ ด้านหลังเลย",
}


LIGHT_THROUGH = {
    "ตัวกลางโปร่งใส": "แสงผ่านไปได้เกือบทั้งหมด ฉากด้านหลังสว่างมาก",
    "ตัวกลางโปร่งแสง": "แสงผ่านไปได้บางส่วน ฉากด้านหลังสว่างเล็กน้อย",
    "วัตถุทึบแสง": "แสงผ่านไปไม่ได้เลย ฉากด้านหลังมืดเป็นเงา",
}


MEDIUM_HINT = "โปร่งใสมองเห็นชัดและแสงผ่านเกือบหมด โปร่งแสงมองเห็นราง ๆ และแสงผ่านบางส่วน ทึบแสงมองไม่เห็นและแสงผ่านไม่ได้"


class Medium(NamedTuple):
    name: str
    seen: str
    category: str


MEDIA = (
    Medium("กระจกใส", "มองเห็นสิ่งต่าง ๆ ด้านหลังได้ชัดเจน", "ตัวกลางโปร่งใส"),
    Medium("แผ่นพลาสติกใส", "มองเห็นสิ่งต่าง ๆ ด้านหลังได้ชัดเจน", "ตัวกลางโปร่งใส"),
    Medium("แก้วน้ำใส", "มองเห็นสิ่งต่าง ๆ ด้านหลังได้ชัดเจน", "ตัวกลางโปร่งใส"),
    Medium("ถุงพลาสติกใส", "มองเห็นสิ่งต่าง ๆ ด้านหลังได้ชัดเจน", "ตัวกลางโปร่งใส"),
    Medium("แผ่นอะคริลิกใส", "มองเห็นสิ่งต่าง ๆ ด้านหลังได้ชัดเจน", "ตัวกลางโปร่งใส"),
    Medium("กระดาษไข", "มองเห็นเพียงเงาราง ๆ ไม่ชัดเจน", "ตัวกลางโปร่งแสง"),
    Medium("กระจกฝ้า", "มองเห็นเพียงเงาราง ๆ ไม่ชัดเจน", "ตัวกลางโปร่งแสง"),
    Medium("ผ้าขาวบาง", "มองเห็นเพียงเงาราง ๆ ไม่ชัดเจน", "ตัวกลางโปร่งแสง"),
    Medium("ถุงพลาสติกขุ่น", "มองเห็นเพียงเงาราง ๆ ไม่ชัดเจน", "ตัวกลางโปร่งแสง"),
    Medium("กระดาษทาน้ำมัน", "มองเห็นเพียงเงาราง ๆ ไม่ชัดเจน", "ตัวกลางโปร่งแสง"),
    Medium("แผ่นไม้อัด", "มองไม่เห็นสิ่งใดด้านหลังเลย", "วัตถุทึบแสง"),
    Medium("แผ่นเหล็ก", "มองไม่เห็นสิ่งใดด้านหลังเลย", "วัตถุทึบแสง"),
    Medium("กระดาษแข็ง", "มองไม่เห็นสิ่งใดด้านหลังเลย", "วัตถุทึบแสง"),
    Medium("หนังสือ", "มองไม่เห็นสิ่งใดด้านหลังเลย", "วัตถุทึบแสง"),
    Medium("แผ่นอะลูมิเนียมฟอยล์", "มองไม่เห็นสิ่งใดด้านหลังเลย", "วัตถุทึบแสง"),
)


LIGHT_MEDIUM_SCENARIOS = (
    ("หน้าต่างห้องน้ำมักใช้กระจกฝ้าแทนกระจกใส เพราะเหตุใด",
     "กระจกฝ้าเป็นตัวกลางโปร่งแสง ให้แสงผ่านเข้ามาได้แต่มองเห็นภาพด้านในไม่ชัดเจน จึงรักษาความเป็นส่วนตัวได้",
     ("กระจกฝ้าเป็นวัตถุทึบแสง ไม่ให้แสงผ่านเข้ามาเลย", "กระจกฝ้าเป็นตัวกลางโปร่งใสเช่นเดียวกับกระจกใส", "กระจกฝ้าทำให้ห้องมืดกว่ากระจกใสเสมอ")),
    ("เหตุใดจึงมองไม่เห็นสิ่งของในกล่องกระดาษที่ปิดฝาสนิท",
     "กระดาษเป็นวัตถุทึบแสง แสงจึงผ่านไม่ได้เลย มองไม่เห็นสิ่งของด้านใน",
     ("กระดาษเป็นตัวกลางโปร่งแสง แสงผ่านได้บางส่วน", "กระดาษเป็นตัวกลางโปร่งใส แต่กล่องปิดสนิทเกินไป", "แสงผ่านกระดาษได้ปกติ เพียงแต่สิ่งของอยู่ไกลเกินไป")),
    ("เหตุใดจึงมองเห็นปลาในตู้ปลาแก้วได้ชัดเจนจากภายนอก",
     "กระจกใสเป็นตัวกลางโปร่งใส แสงผ่านได้เกือบทั้งหมด จึงมองเห็นภาพด้านในได้ชัดเจน",
     ("กระจกใสเป็นวัตถุทึบแสงแต่บางมาก", "กระจกใสเป็นตัวกลางโปร่งแสงเช่นเดียวกับกระดาษไข", "น้ำในตู้ปลาเป็นตัวที่ทำให้มองเห็นปลาได้ ไม่เกี่ยวกับกระจก")),
)


PURPOSES = (
    ("หน้าต่างห้องเรียนที่ต้องการมองเห็นวิวภายนอกได้ชัด", "ตัวกลางโปร่งใส"), ("กล่องใส่ขนมที่ต้องการให้ลูกค้ามองเห็นขนมข้างใน", "ตัวกลางโปร่งใส"),
    ("โป๊ะโคมไฟที่ต้องการให้แสงนุ่มนวลไม่แยงตา", "ตัวกลางโปร่งแสง"), ("ประตูห้องน้ำที่ต้องการแสงสว่างแต่ไม่ให้มองเห็นข้างใน", "ตัวกลางโปร่งแสง"),
    ("ผ้าม่านห้องนอนที่ต้องการให้ห้องมืดสนิทตอนกลางวัน", "วัตถุทึบแสง"), ("กล่องเก็บฟิล์มถ่ายรูปที่ห้ามโดนแสง", "วัตถุทึบแสง"),
    ("ที่บังแดดหน้ารถยนต์ที่ต้องการกันแสงแดดทั้งหมด", "วัตถุทึบแสง"), ("ฝาครอบนาฬิกาที่ต้องการมองเห็นเข็มชัดเจน", "ตัวกลางโปร่งใส"),
)


@question_type(
    "phys.light_medium_foundation",
    display_name={"th": "บอกลักษณะการมองเห็นของตัวกลางแต่ละชนิด"},
    level=FOURTH, subject=SUBJECT, topic=LIGHT_MEDIUM_TOPIC,
)
class LightMediumFoundation(QuestionType):
    """What each kind of medium lets through, and which objects belong to it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        category = rng.choice(tuple(CATEGORY_DESCRIPTIONS))
        roll = rng.random()
        if roll < 0.3:
            others = [v for k, v in CATEGORY_DESCRIPTIONS.items() if k != category]
            return _labelled(stem=f"{category}มีลักษณะการมองเห็นสิ่งต่าง ๆ ด้านหลังอย่างไร", correct=CATEGORY_DESCRIPTIONS[category],
                             wrongs=tuple(others) + ("สะท้อนแสงทั้งหมดกลับไปโดยไม่มีแสงผ่านเข้าไปเลย",), hint=MEDIUM_HINT, topic=LIGHT_MEDIUM_TOPIC)
        right = rng.choice([m.name for m in MEDIA if m.category == category])
        pool = [m.name for m in MEDIA if m.category != category]
        return _labelled(stem=f"วัตถุใดเป็น{category}", correct=right, wrongs=tuple(pool), hint=MEDIUM_HINT, topic=LIGHT_MEDIUM_TOPIC)


@question_type(
    "phys.light_medium_fluency",
    display_name={"th": "จำแนกตัวกลางจากลักษณะการมองเห็นซึ่งเป็นหลักฐานเชิงประจักษ์"},
    level=FOURTH, subject=SUBJECT, topic=LIGHT_MEDIUM_TOPIC,
)
class LightMediumFluency(QuestionType):
    """What is seen through an object, or how much torchlight it lets onto a screen."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(MEDIA)
        others = [c for c in CATEGORY_DESCRIPTIONS if c != item.category]
        if rng.random() < 0.5:
            stem = (f"นักเรียนถือ{item.name}บังตาแล้วมองไปด้านหลัง พบว่า{item.seen} "
                    f"จากหลักฐานนี้ {item.name}จัดเป็นตัวกลางชนิดใด")
        else:
            stem = (f"นักเรียนส่องไฟฉายผ่าน{item.name}ไปยังฉาก พบว่า{LIGHT_THROUGH[item.category]} "
                    f"จากหลักฐานนี้ {item.name}จัดเป็นตัวกลางชนิดใด")
        return _labelled(stem=stem, correct=item.category, wrongs=tuple(others) + ("ไม่สามารถจำแนกได้จากหลักฐานนี้",),
                         hint="ดูว่ามองเห็นด้านหลังชัดเจน ราง ๆ หรือมองไม่เห็นเลย และแสงผ่านได้มากน้อยเพียงใด", topic=LIGHT_MEDIUM_TOPIC)


@question_type(
    "phys.light_medium_application",
    display_name={"th": "ใช้ความรู้เรื่องตัวกลางแสงอธิบายการเลือกใช้วัสดุ"},
    level=FOURTH, subject=SUBJECT, topic=LIGHT_MEDIUM_TOPIC,
)
class LightMediumApplication(QuestionType):
    """Authored cases, and a material chosen for a purpose."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _retopic(scenario_question(rng, LIGHT_MEDIUM_SCENARIOS, hint=MEDIUM_HINT), LIGHT_MEDIUM_TOPIC)
        purpose, category = rng.choice(PURPOSES)
        right = rng.choice([m.name for m in MEDIA if m.category == category])
        pool = [m.name for m in MEDIA if m.category != category]
        return _labelled(stem=f"ต้องการทำ{purpose} ควรเลือกใช้วัสดุใดเหมาะสมที่สุด", correct=right, wrongs=tuple(pool),
                         hint=MEDIUM_HINT, topic=LIGHT_MEDIUM_TOPIC)
