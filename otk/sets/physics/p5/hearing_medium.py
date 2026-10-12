"""การได้ยินเสียงผ่านตัวกลาง

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.5/1

Sets moved here from: science_wave_d24.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d24 import FIFTH

PROVENANCE = Provenance("original")


HEARING_MEDIUM_TOPIC = "การได้ยินเสียงผ่านตัวกลาง"


KIDS = ("ต้น", "ฝน", "มะลิ", "ภูมิ", "ข้าวหอม", "ปลา", "บอส", "น้ำใส")


HEARING_FACTS = (
    ("เสียงสามารถเดินทางผ่านตัวกลางใดได้บ้าง", "ของแข็ง ของเหลว และแก๊ส",
     ("ของแข็งเท่านั้น", "แก๊สเท่านั้น", "สุญญากาศที่ไม่มีอนุภาคใดเลย", "ของเหลวเท่านั้น", "ของแข็งและสุญญากาศ")),
    ("เหตุใดเสียงจึงเดินทางผ่านสุญญากาศไม่ได้", "สุญญากาศไม่มีอนุภาคของตัวกลางที่จะส่งต่อการสั่น",
     ("สุญญากาศมืดเกินไป", "สุญญากาศเย็นเกินไป", "สุญญากาศมีแรงโน้มถ่วงมากจนดึงเสียงไว้ไม่ให้ออกไป", "เสียงเดินทางผ่านสุญญากาศได้ดีที่สุด", "สุญญากาศมีอากาศหนาแน่นเกินไปจนเสียงผ่านไม่ได้")),
    ("โดยทั่วไปเสียงเดินทางผ่านตัวกลางใดได้เร็วที่สุด", "ของแข็ง", ("แก๊ส", "ของเหลว", "สุญญากาศ", "เร็วเท่ากันทุกตัวกลาง", "อากาศร้อน")),
)


NO_MEDIUM = ("อวกาศระหว่างดาวเคราะห์", "โหลแก้วที่สูบอากาศออก", "ห้องสุญญากาศในห้องแล็บ")


WITH_MEDIUM = ("อากาศในห้องเรียน", "น้ำในสระว่ายน้ำ", "โต๊ะไม้ในห้องเรียน", "รางรถไฟที่ทำจากเหล็ก", "ผนังคอนกรีตของอาคาร",
               "น้ำทะเลที่ชายหาด", "เส้นเชือกที่ขึงตึง")


SOLIDS = ("เหล็ก", "ไม้", "คอนกรีต", "อะลูมิเนียม")


LIQUIDS = ("น้ำ", "น้ำทะเล", "น้ำมันพืช")


GASES = ("อากาศ", "แก๊สในลูกโป่ง")


HEARING_RECORDS = (
    ("เคาะโต๊ะเบา ๆ แล้วแนบหูลงบนโต๊ะ ได้ยินเสียงเคาะชัดกว่ายืนฟังในอากาศห่าง ๆ", "ของแข็ง (โต๊ะ)"),
    ("ดำน้ำอยู่ในสระแล้วเพื่อนเคาะขอบสระใต้น้ำ ยังได้ยินเสียงเคาะได้ชัดเจน", "ของเหลว (น้ำ)"),
    ("เพื่อนพูดคุยกับนักเรียนตามปกติในห้องเรียนที่มีอากาศ และนักเรียนได้ยินเสียงพูดนั้น", "แก๊ส (อากาศ)"),
)


HEARING_EXTRA = (
    ("พูดใส่ถ้วยกระดาษที่ต่อเชือกขึงตึงไปยังถ้วยของเพื่อน เพื่อนได้ยินเสียงผ่านเชือก", "ของแข็ง (เชือก)"),
    ("แนบหูกับผนังห้อง ได้ยินเสียงคนเคาะผนังจากอีกห้องหนึ่ง", "ของแข็ง (ผนัง)"),
    ("ปลาในตู้ว่ายหนีเมื่อมีคนเคาะน้ำในตู้เบา ๆ ด้วยไม้", "ของเหลว (น้ำในตู้)"),
    ("ได้ยินเสียงนกร้องจากต้นไม้หน้าบ้าน", "แก๊ส (อากาศ)"),
    ("ได้ยินเสียงฟ้าร้องจากเมฆที่อยู่ไกล", "แก๊ส (อากาศ)"),
    ("นักดำน้ำได้ยินเสียงเครื่องยนต์เรือที่แล่นผ่านขณะอยู่ใต้ทะเล", "ของเหลว (น้ำทะเล)"),
)


HEARING_SCENARIOS = (
    ("เหตุใดนักบินอวกาศที่อยู่นอกยานในอวกาศจึงต้องสื่อสารกันด้วยวิทยุแทนการพูดคุยกันตรง ๆ",
     "อวกาศเป็นสุญญากาศ ไม่มีตัวกลางให้เสียงเดินทางผ่าน จึงไม่ได้ยินเสียงพูดกันโดยตรง",
     ("อวกาศมีอากาศเบาบางเกินไปแต่ยังพอได้ยินเสียงพูดอยู่บ้าง", "เสียงเดินทางในสุญญากาศได้เร็วกว่าในอากาศมาก", "นักบินอวกาศใส่หมวกจึงไม่ได้ยินเสียงเท่านั้น")),
    ("เหตุใดคนโบราณจึงแนบหูลงกับรางรถไฟเพื่อฟังว่ามีรถไฟกำลังมาหรือไม่ ทั้งที่ยังมองไม่เห็นรถไฟ",
     "เสียงเดินทางผ่านของแข็งอย่างรางเหล็กได้เร็วและชัดกว่าผ่านอากาศ จึงได้ยินเสียงรถไฟจากระยะไกลได้ก่อน",
     ("รางรถไฟไม่ใช่ตัวกลางของเสียง แค่ช่วยขยายเสียงเท่านั้น", "เสียงผ่านอากาศได้ชัดกว่าผ่านรางเหล็กเสมอ", "การแนบหูกับรางช่วยกรองเสียงรบกวนอื่นออกไปเท่านั้น")),
    ("เหตุใดวาฬจึงสามารถส่งเสียงร้องสื่อสารกับวาฬตัวอื่นที่อยู่ไกลออกไปหลายกิโลเมตรใต้ทะเลได้",
     "น้ำทะเลเป็นตัวกลางที่ส่งผ่านเสียงได้ดีและไกล เสียงจึงเดินทางไปถึงวาฬตัวอื่นได้",
     ("เสียงเดินทางในน้ำไม่ได้เลย วาฬใช้วิธีอื่นในการสื่อสาร", "น้ำทะเลลดทอนเสียงจนไม่สามารถเดินทางไกลได้", "วาฬสื่อสารกันด้วยการสั่นของน้ำโดยไม่มีเสียงเกี่ยวข้อง")),
)


BELL_JAR = (
    ("กริ่งไฟฟ้าดังอยู่ในโหลแก้วที่มีอากาศเต็ม", "ได้ยินเสียงกริ่งชัดเจน"),
    ("สูบอากาศออกจากโหลแก้วไปครึ่งหนึ่งขณะกริ่งยังดัง", "ได้ยินเสียงกริ่งเบาลง"),
    ("สูบอากาศออกจากโหลแก้วจนเกือบหมดขณะกริ่งยังดัง", "แทบไม่ได้ยินเสียงกริ่ง ทั้งที่ยังเห็นกริ่งสั่น"),
    ("ปล่อยอากาศกลับเข้าโหลแก้วขณะกริ่งยังดัง", "กลับมาได้ยินเสียงกริ่งชัดขึ้น"),
)


@question_type(
    "phys.hearing_medium_foundation",
    display_name={"th": "บอกตัวกลางที่เสียงเดินทางผ่านได้"},
    level=FIFTH, subject=SUBJECT, topic=HEARING_MEDIUM_TOPIC,
)
class HearingMediumFoundation(QuestionType):
    """Sound needs a medium: solid, liquid, or gas, but not a vacuum."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            stem, right, wrongs = rng.choice(HEARING_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs),
                             hint="เสียงต้องอาศัยอนุภาคของตัวกลางในการส่งผ่านการสั่น จึงเดินทางผ่านสุญญากาศไม่ได้", topic=HEARING_MEDIUM_TOPIC)
        return _labelled(stem="เสียงเดินทางผ่านบริเวณใดไม่ได้", correct=rng.choice(NO_MEDIUM), wrongs=tuple(WITH_MEDIUM),
                         hint="เสียงต้องอาศัยตัวกลาง บริเวณที่ไม่มีอนุภาคของตัวกลางเสียงจึงผ่านไม่ได้", topic=HEARING_MEDIUM_TOPIC)


@question_type(
    "phys.hearing_medium_fluency",
    display_name={"th": "อธิบายการได้ยินเสียงผ่านตัวกลางจากหลักฐานเชิงประจักษ์"},
    level=FIFTH, subject=SUBJECT, topic=HEARING_MEDIUM_TOPIC,
)
class HearingMediumFluency(QuestionType):
    """A hearing observation and its medium, or which of three media carries sound fastest."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.2:
            index = rng.randrange(len(HEARING_RECORDS))
            record, medium = HEARING_RECORDS[index]
            others = [m for i, (_, m) in enumerate(HEARING_RECORDS) if i != index]
            return _labelled(stem=f"{record} จากหลักฐานนี้ เสียงเดินทางผ่านตัวกลางชนิดใด", correct=medium,
                             wrongs=tuple(others) + ("ไม่มีตัวกลางใดเลย เสียงเดินทางในสุญญากาศได้เช่นกัน",),
                             hint="ตัวกลางคือสิ่งที่อยู่ระหว่างแหล่งกำเนิดเสียงกับหูผู้ฟังในสถานการณ์นั้น", topic=HEARING_MEDIUM_TOPIC)
        if roll < 0.55:
            record, medium = rng.choice(HEARING_EXTRA)
            kind = medium.split(" ")[0]
            return _labelled(stem=f"{record} ในเหตุการณ์นี้ เสียงเดินทางมาถึงหูผ่านตัวกลางประเภทใดเป็นหลัก", correct=kind,
                             wrongs=tuple(k for k in ("ของแข็ง", "ของเหลว", "แก๊ส", "สุญญากาศ") if k != kind),
                             hint="ตัวกลางคือสิ่งที่อยู่ระหว่างแหล่งกำเนิดเสียงกับหูผู้ฟังในสถานการณ์นั้น", topic=HEARING_MEDIUM_TOPIC)
        solid, liquid, gas = rng.choice(SOLIDS), rng.choice(LIQUIDS), rng.choice(GASES)
        fastest = rng.random() < 0.5
        right = solid if fastest else gas
        return _labelled(stem=f"ถ้าเคาะให้เกิดเสียงแล้วส่งผ่าน{solid} {liquid} และ{gas}ที่ยาวเท่ากัน เสียงเดินทางผ่านตัวกลางใด{'เร็ว' if fastest else 'ช้า'}ที่สุด",
                         correct=right, wrongs=(liquid, gas if fastest else solid, "เร็วเท่ากันทุกตัวกลาง"),
                         hint="โดยทั่วไปเสียงเดินทางผ่านของแข็งเร็วที่สุด รองลงมาคือของเหลว และแก๊สช้าที่สุด", topic=HEARING_MEDIUM_TOPIC)


@question_type(
    "phys.hearing_medium_application",
    display_name={"th": "ใช้ความรู้เรื่องตัวกลางของเสียงอธิบายสถานการณ์"},
    level=FIFTH, subject=SUBJECT, topic=HEARING_MEDIUM_TOPIC,
)
class HearingMediumApplication(QuestionType):
    """Authored cases, and the bell in a jar as air is pumped out and let back in."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, HEARING_SCENARIOS, hint="ไม่มีตัวกลางก็ไม่มีเสียงเดินทางถึงผู้ฟัง สุญญากาศจึงไม่มีเสียง"),
                            HEARING_MEDIUM_TOPIC)
        step, right = rng.choice(BELL_JAR)
        kid = rng.choice(KIDS)
        return _labelled(stem=f"{kid}ทดลองโดย{step} {kid}จะได้ยินเสียงอย่างไร", correct=right,
                         wrongs=tuple(r for _, r in BELL_JAR if r != right)[:3],
                         hint="ยิ่งมีอากาศเป็นตัวกลางน้อย เสียงยิ่งเดินทางมาถึงหูได้น้อย", topic=HEARING_MEDIUM_TOPIC)
