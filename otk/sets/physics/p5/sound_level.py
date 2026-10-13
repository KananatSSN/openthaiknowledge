"""การวัดระดับเสียงด้วยเครื่องมือวัดระดับเสียง

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.5/4

Sets moved here from: science_wave_d25.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d24 import FIFTH

PROVENANCE = Provenance("original")


SOUND_LEVEL_TOPIC = "การวัดระดับเสียงด้วยเครื่องมือวัดระดับเสียง"


LEVEL_FACTS = (
    ("ระดับเสียงมีหน่วยเป็นอะไร และวัดด้วยเครื่องมือใด", "หน่วยเดซิเบล (dB) วัดด้วยเครื่องวัดระดับเสียง",
     ("หน่วยเฮิรตซ์ (Hz) วัดด้วยเครื่องวัดความถี่", "หน่วยนิวตัน (N) วัดด้วยเครื่องชั่งสปริง", "หน่วยองศาเซลเซียส (°C) วัดด้วยเทอร์มอมิเตอร์",
      "หน่วยเมตร วัดด้วยไม้บรรทัด", "หน่วยกิโลกรัม วัดด้วยตาชั่ง")),
    ("ค่าเดซิเบลที่มากขึ้นหมายความว่าอย่างไร", "เสียงดังขึ้น", ("เสียงสูงขึ้น", "เสียงค่อยลง", "เสียงต่ำลง", "เสียงเดินทางเร็วขึ้น", "เสียงหายไป")),
    ("ระดับเสียงที่ดังเกินเท่าใดหากฟังต่อเนื่องนานอาจเป็นอันตรายต่อการได้ยิน", "เกิน 85 เดซิเบล",
     ("เกิน 20 เดซิเบล", "เกิน 40 เดซิเบล", "เกิน 5 เดซิเบล", "เกิน 1,000 เดซิเบล", "ไม่มีระดับใดเป็นอันตราย")),
)


LEVEL_FACTS += (
    ('เสียงกระซิบเบา ๆ กับเสียงเครื่องบินขึ้นในระยะใกล้ เสียงใดมีระดับเสียงสูงกว่า', 'เสียงเครื่องบินขึ้น',
     ('เสียงกระซิบ', 'ทั้งสองมีระดับเสียงเท่ากัน', 'เปรียบเทียบไม่ได้เพราะเป็นเสียงคนละชนิด', 'เสียงกระซิบ เพราะอยู่ใกล้หู', 'ทั้งสองไม่มีระดับเสียง')),
    ('วิธีใดช่วยป้องกันอันตรายต่อการได้ยินเมื่อต้องทำงานในที่ที่มีเสียงดังมาก', 'สวมที่อุดหูหรือที่ครอบหูลดเสียง',
     ('เปิดเพลงในหูฟังให้ดังกว่าเสียงรอบข้าง', 'ยืนให้ใกล้แหล่งกำเนิดเสียงมากขึ้น', 'ตะโกนแข่งกับเสียงรอบข้าง', 'ปิดตาขณะทำงาน', 'ดื่มน้ำเย็นบ่อย ๆ')),
    ('เมื่อเดินห่างออกจากลำโพงที่เปิดเพลงอยู่ ระดับเสียงที่ได้ยินจะเป็นอย่างไร', 'ลดลง',
     ('เพิ่มขึ้น', 'เท่าเดิม', 'เปลี่ยนเป็นเสียงสูงขึ้น', 'หายไปทันที', 'เพิ่มขึ้นแล้วจึงลดลง')),
    ('มลพิษทางเสียงหมายถึงอะไร', 'เสียงที่ดังเกินไปหรือรบกวนจนเป็นอันตรายต่อสุขภาพและการได้ยิน',
     ('เสียงทุกเสียงที่มนุษย์ได้ยิน', 'เสียงเพลงที่ไพเราะ', 'เสียงที่เบามากจนไม่ได้ยิน', 'เสียงที่เดินทางในน้ำ', 'เสียงที่เกิดจากธรรมชาติเท่านั้น')),
)


class SoundPlace(NamedTuple):
    name: str
    level: int


SOUND_PLACES = (
    SoundPlace("ห้องสมุดที่เงียบสงบ", 40),
    SoundPlace("การสนทนาพูดคุยกันตามปกติ", 60),
    SoundPlace("ถนนที่มีรถพลุกพล่าน", 85),
    SoundPlace("เวทีคอนเสิร์ตขณะเปิดเพลง", 110),
)


MORE_PLACES = (
    SoundPlace("เสียงใบไม้ไหว", 20), SoundPlace("เสียงกระซิบ", 30), SoundPlace("ห้องเรียนขณะครูสอน", 55),
    SoundPlace("เครื่องดูดฝุ่น", 70), SoundPlace("เครื่องตัดหญ้า", 90), SoundPlace("เครื่องบินขณะขึ้น", 130),
    SoundPlace("ตลาดสดที่คึกคัก", 75), SoundPlace("สว่านเจาะถนน", 100),
)


SOUND_LEVEL_SCENARIOS = (
    ("เหตุใดผู้ที่ทำงานใกล้เครื่องบินไอพ่นขณะขึ้นบินจึงต้องสวมที่ครอบหูป้องกันเสียงเสมอ",
     "เสียงเครื่องบินไอพ่นมีระดับเสียงสูงมาก การฟังโดยไม่ป้องกันเป็นเวลานานอาจทำอันตรายต่อการได้ยิน",
     ("เสียงเครื่องบินไอพ่นมีระดับเสียงต่ำแต่มีความถี่สูงมาก", "ที่ครอบหูใช้ป้องกันฝุ่นเพียงอย่างเดียว ไม่เกี่ยวกับระดับเสียง", "ระดับเสียงของเครื่องบินไอพ่นเท่ากับเสียงกระซิบทั่วไป")),
    ("นักเรียนวัดระดับเสียงในห้องเรียนได้ 55 เดซิเบล และวัดระดับเสียงข้างถนนได้ 85 เดซิเบล ข้อใดสรุปได้ถูกต้อง",
     "ระดับเสียงข้างถนนดังกว่าในห้องเรียนมาก เพราะค่าเดซิเบลที่วัดได้สูงกว่า",
     ("ระดับเสียงทั้งสองที่ดังเท่ากัน เพราะต่างวัดด้วยหน่วยเดซิเบลเหมือนกัน", "ระดับเสียงในห้องเรียนดังกว่าข้างถนน", "ค่าเดซิเบลที่วัดได้ไม่สามารถใช้เปรียบเทียบความดังของเสียงได้")),
    ("โรงงานแห่งหนึ่งติดป้ายเตือนว่าบริเวณที่มีระดับเสียงเกิน 85 เดซิเบลต้องสวมอุปกรณ์ป้องกันหู เหตุใดจึงกำหนดเช่นนี้",
     "เสียงที่ระดับสูงเป็นเวลานานอาจทำอันตรายต่อการได้ยิน จึงต้องป้องกันเมื่อระดับเสียงเกินเกณฑ์ที่กำหนด",
     ("ระดับเสียง 85 เดซิเบลเป็นระดับที่เงียบมากจนไม่มีอันตราย", "การกำหนดเกณฑ์ระดับเสียงไม่เกี่ยวกับสุขภาพของผู้ปฏิบัติงาน", "อุปกรณ์ป้องกันหูใช้ป้องกันฝุ่นละอองในโรงงานเท่านั้น")),
)


@question_type(
    "phys.sound_level_foundation",
    display_name={"th": "บอกหน่วยและเครื่องมือที่ใช้วัดระดับเสียง"},
    level=FIFTH, subject=SUBJECT, topic=SOUND_LEVEL_TOPIC,
)
class SoundLevelFoundation(QuestionType):
    """Decibels, the meter, what a bigger number means, the 85 dB line."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(LEVEL_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs),
                         hint="เดซิเบล (dB) เป็นหน่วยของระดับเสียง ยิ่งมากยิ่งดัง และเกิน 85 dB ต่อเนื่องนานเป็นอันตราย", topic=SOUND_LEVEL_TOPIC)


@question_type(
    "phys.sound_level_fluency",
    display_name={"th": "เรียงลำดับระดับเสียงจากค่าที่วัดได้"},
    level=FIFTH, subject=SUBJECT, topic=SOUND_LEVEL_TOPIC,
)
class SoundLevelFluency(QuestionType):
    """Meter readings at four places; sort them quiet to loud."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pool = SOUND_PLACES + MORE_PLACES
        shown = rng.sample(pool, 4)
        record = " / ".join(f"{p.name}: {p.level} เดซิเบล" for p in shown)
        ascending = sorted(shown, key=lambda p: p.level)
        rotate1 = ascending[1:] + ascending[:1]
        rotate2 = ascending[2:] + ascending[:2]
        return _labelled(
            stem=(f"เครื่องวัดระดับเสียงอ่านค่าได้ดังนี้ — {record} จากข้อมูลนี้ ข้อใดเรียงลำดับสถานที่จากเสียงเบาที่สุดไปดังที่สุดได้ถูกต้อง"),
            correct=" → ".join(p.name for p in ascending),
            wrongs=(" → ".join(p.name for p in reversed(ascending)),
                    " → ".join(p.name for p in rotate1),
                    " → ".join(p.name for p in rotate2)),
            hint="เรียงจากค่าเดซิเบลน้อยที่สุดไปมากที่สุด",
            topic=SOUND_LEVEL_TOPIC,
        )


@question_type(
    "phys.sound_level_application",
    display_name={"th": "ใช้ค่าระดับเสียงเปรียบเทียบและประเมินความเสี่ยง"},
    level=FIFTH, subject=SUBJECT, topic=SOUND_LEVEL_TOPIC,
)
class SoundLevelApplication(QuestionType):
    """Authored cases, the gap between two readings, and whether ear protection is needed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.25:
            return _retopic(scenario_question(rng, SOUND_LEVEL_SCENARIOS,
                                              hint="ค่าเดซิเบลที่สูงกว่าหมายถึงเสียงที่ดังกว่า และเสียงดังต่อเนื่องเป็นอันตรายต่อการได้ยิน"), SOUND_LEVEL_TOPIC)
        a, b = rng.sample(SOUND_PLACES + MORE_PLACES, 2)
        if roll < 0.6:
            louder, quieter = (a, b) if a.level > b.level else (b, a)
            return numeric(stem=f"เครื่องวัดระดับเสียงอ่านค่า{louder.name}ได้ {louder.level} เดซิเบล และ{quieter.name}ได้ {quieter.level} เดซิเบล "
                                f"สองค่านี้ต่างกันกี่เดซิเบล", answer=louder.level - quieter.level,
                           wrongs=[louder.level + quieter.level, louder.level, louder.level - quieter.level + 10], unit="เดซิเบล",
                           topic=SOUND_LEVEL_TOPIC, hint="ผลต่าง = ค่าที่มากกว่า − ค่าที่น้อยกว่า")
        place = rng.choice(SOUND_PLACES + MORE_PLACES)
        while place.level == 85:
            place = rng.choice(SOUND_PLACES + MORE_PLACES)
        need = place.level > 85
        right = "ควรสวมอุปกรณ์ป้องกันหู เพราะระดับเสียงเกิน 85 เดซิเบล" if need else "ไม่จำเป็นต้องสวม เพราะระดับเสียงไม่เกิน 85 เดซิเบล"
        other = "ไม่จำเป็นต้องสวม เพราะระดับเสียงไม่เกิน 85 เดซิเบล" if need else "ควรสวมอุปกรณ์ป้องกันหู เพราะระดับเสียงเกิน 85 เดซิเบล"
        return _labelled(stem=f"คนที่ต้องอยู่ใกล้{place.name}ซึ่งวัดระดับเสียงได้ {place.level} เดซิเบลเป็นเวลานานทุกวัน ควรทำอย่างไร (เกณฑ์ 85 เดซิเบล)",
                         correct=right, wrongs=(other, "ควรเพิ่มเสียงเพลงกลบเสียงให้ดังกว่า", "ควรเข้าไปใกล้แหล่งเสียงมากขึ้นเพื่อให้ชิน"),
                         hint="เทียบค่าที่วัดได้กับเกณฑ์ 85 เดซิเบล", topic=SOUND_LEVEL_TOPIC)
