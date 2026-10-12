"""แนวการเคลื่อนที่ของแสงและการมองเห็นวัตถุ

ฟิสิกส์ · ป.2 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.2/1

Sets moved here from: science_wave_d22.
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
from otk.sets._support.science_wave_d22 import SECOND, _facts

PROVENANCE = Provenance("original")


LIGHT_SEEING_TOPIC = "แนวการเคลื่อนที่ของแสงและการมองเห็นวัตถุ"


LUMINOUS = ("ดวงอาทิตย์", "หลอดไฟที่เปิดอยู่", "เทียนที่จุดอยู่", "หิ่งห้อย", "ไฟฉายที่เปิดอยู่", "จอโทรศัพท์ที่เปิดอยู่", "กองไฟ")


NON_LUMINOUS = ("ดวงจันทร์", "กระจกเงา", "โต๊ะ", "หนังสือ", "ช้อน", "ดินสอ", "ลูกบอล", "ต้นไม้")


LIGHT_FACTS = (
    ("แสงจากแหล่งกำเนิดแสงเคลื่อนที่ในแนวใด", "เคลื่อนที่เป็นเส้นตรงออกจากแหล่งกำเนิดแสงไปทุกทิศทาง",
     ("เคลื่อนที่เป็นเส้นโค้งออกจากแหล่งกำเนิดแสงเสมอ", "เคลื่อนที่เฉพาะเมื่อมีอากาศเท่านั้น ในสุญญากาศแสงเคลื่อนที่ไม่ได้",
      "หยุดนิ่งอยู่ที่แหล่งกำเนิดแสง ไม่เคลื่อนที่ออกไป", "เคลื่อนที่ไปทางเดียวเท่านั้น", "เคลื่อนที่วนเป็นวงกลม")),
    ("เหตุใดเราจึงมองไม่เห็นสิ่งของในห้องที่มืดสนิท", "ไม่มีแสงไปกระทบสิ่งของแล้วสะท้อนเข้าตา",
     ("ดวงตาของเราหยุดทำงานเมื่ออยู่ในที่มืด", "สิ่งของหายไปเมื่อไม่มีแสง", "อากาศในห้องมืดบังสิ่งของไว้ไม่ให้มองเห็น", "สิ่งของเปลี่ยนเป็นสีดำทั้งหมด", "ห้องมืดไม่มีอากาศ")),
    ("ดวงจันทร์สว่างในเวลากลางคืนได้อย่างไร", "ดวงจันทร์สะท้อนแสงจากดวงอาทิตย์",
     ("ดวงจันทร์ผลิตแสงได้เอง", "ดวงจันทร์สะท้อนแสงไฟจากเมือง", "ดวงจันทร์มีไฟอยู่ข้างใน", "ดวงจันทร์เก็บแสงไว้ตอนกลางวัน", "ดาวดวงอื่นส่องแสงให้ดวงจันทร์")),
)


LIGHT_HINT = "แสงเคลื่อนที่เป็นเส้นตรงออกจากแหล่งกำเนิดแสง เรามองเห็นวัตถุเมื่อแสงจากวัตถุ หรือแสงที่สะท้อนจากวัตถุ เข้าสู่ตา"


LIGHT_SEEING_SCENARIOS = (
    ("นักเรียนฉายเลเซอร์ผ่านห้องที่มีฝุ่นละอองฟุ้งกระจาย เห็นลำแสงเป็นเส้นตรงพาดผ่านห้อง ข้อใดอธิบายได้ถูกต้อง",
     "แสงเดินทางเป็นเส้นตรง ฝุ่นละอองที่กระทบลำแสงจึงสะท้อนแสงเข้าตาเป็นแนวเส้นตรงเดียวกับลำแสง",
     ("แสงเดินทางเป็นเส้นโค้งตามรูปร่างของฝุ่นละออง แต่ฝุ่นเรียงตัวเป็นแนวตรงพอดี", "ฝุ่นละอองเปล่งแสงออกมาเอง ไม่เกี่ยวกับแสงเลเซอร์ที่ส่องผ่าน จึงเห็นเป็นแนวเส้นตรง", "แสงเลเซอร์ไม่เคลื่อนที่ ฝุ่นละอองเคลื่อนที่เข้าหาแสงแทน")),
    ("เหตุใดเราจึงมองเห็นดวงจันทร์สว่างในเวลากลางคืนทั้งที่ดวงจันทร์ไม่มีแสงในตัวเอง",
     "ดวงจันทร์สะท้อนแสงจากดวงอาทิตย์ แสงที่สะท้อนนั้นเดินทางมาเข้าตาเราจึงมองเห็น",
     ("ดวงจันทร์เปล่งแสงได้เองในเวลากลางคืน เช่นเดียวกับดวงอาทิตย์ในเวลากลางวัน", "ดวงตาของเราเปล่งแสงออกไปกระทบดวงจันทร์ แล้วสะท้อนกลับเข้าตาเรา", "อากาศในเวลากลางคืนทำให้ดวงจันทร์สว่างขึ้นเอง")),
    ("กล่องทึบแสงปิดสนิทไม่มีรูรั่วและไม่มีแหล่งกำเนิดแสงภายใน นักเรียนมองผ่านรูเล็ก ๆ ที่เจาะใหม่ จะเห็นสิ่งใดภายในกล่องก่อนเปิดฝา",
     "มองไม่เห็นสิ่งใดเลย เพราะไม่มีแสงในกล่องที่จะสะท้อนวัตถุภายในเข้าตา",
     ("มองเห็นวัตถุภายในได้ปกติ เพราะดวงตาสามารถมองเห็นในที่มืดได้เอง", "มองเห็นเป็นเงาสีเทาจาง ๆ เสมอ เพราะวัตถุมีแสงในตัวเองเล็กน้อย", "มองเห็นได้เฉพาะวัตถุสีขาว เพราะสีขาวสว่างในตัวเองแม้ไม่มีแสง")),
)


CARD_LABELS = ("แผ่นที่ 1", "แผ่นที่ 2", "แผ่นที่ 3", "แผ่นที่ 4")


@question_type(
    "phys.light_travel_foundation",
    display_name={"th": "บรรยายแนวการเคลื่อนที่ของแสงจากแหล่งกำเนิดแสง"},
    level=SECOND, subject=SUBJECT, topic=LIGHT_SEEING_TOPIC,
)
class LightTravelFoundation(QuestionType):
    """Straight lines from the source; sources against things that only reflect."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            return _labelled(stem="ข้อใดเป็นแหล่งกำเนิดแสง (ผลิตแสงได้เอง)", correct=rng.choice(LUMINOUS), wrongs=tuple(NON_LUMINOUS),
                             hint="แหล่งกำเนิดแสงผลิตแสงได้เอง ส่วนวัตถุอื่นเพียงสะท้อนแสง", topic=LIGHT_SEEING_TOPIC)
        if roll < 0.6:
            return _labelled(stem="ข้อใดไม่ใช่แหล่งกำเนิดแสง แต่เรามองเห็นได้เพราะสะท้อนแสง", correct=rng.choice(NON_LUMINOUS),
                             wrongs=tuple(LUMINOUS), hint="แหล่งกำเนิดแสงผลิตแสงได้เอง ส่วนวัตถุอื่นเพียงสะท้อนแสง",
                             topic=LIGHT_SEEING_TOPIC)
        return _facts(rng, LIGHT_FACTS, hint=LIGHT_HINT, topic=LIGHT_SEEING_TOPIC)


@question_type(
    "phys.light_travel_fluency",
    display_name={"th": "อธิบายการมองเห็นวัตถุจากหลักฐานเชิงประจักษ์"},
    level=SECOND, subject=SUBJECT, topic=LIGHT_SEEING_TOPIC,
)
class LightTravelFluency(QuestionType):
    """How we see a lit object, and how we see a light source."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.2:
            return _labelled(
                stem=("ในห้องที่มืดสนิทไม่มีแสงเลย นักเรียนมองไม่เห็นสมุดที่วางอยู่บนโต๊ะ แต่ทันทีที่เปิดไฟ นักเรียนมองเห็นสมุดได้ "
                      "จากหลักฐานนี้ เหตุใดจึงมองเห็นวัตถุได้"),
                correct="เพราะมีแสงจากไฟตกกระทบสมุดแล้วสะท้อนเข้าตา ในที่มืดไม่มีแสงสะท้อนเข้าตาจึงมองไม่เห็น",
                wrongs=("เพราะดวงตาเปล่งแสงออกไปกระทบสมุดเองเมื่อเปิดไฟ ในที่มืดดวงตาจึงเปล่งแสงไม่ได้",
                        "เพราะสมุดเปล่งแสงได้เองตลอดเวลา เพียงแต่แสงจากไฟช่วยให้เปล่งแสงแรงขึ้น",
                        "เพราะอากาศในห้องเปลี่ยนแปลงไปเมื่อเปิดไฟ ทำให้มองเห็นได้แม้ไม่มีแสงสะท้อนเข้าตา"),
                hint=LIGHT_HINT, topic=LIGHT_SEEING_TOPIC,
            )
        own = rng.random() < 0.4
        if own:
            thing = rng.choice(LUMINOUS)
            right = f"แสงจาก{thing}เคลื่อนที่เป็นเส้นตรงเข้าสู่ตาโดยตรง"
            wrongs = (f"ตาของเราส่งแสงออกไปกระทบ{thing}ก่อนจึงมองเห็น", f"{thing}สะท้อนแสงที่ออกจากตาของเรากลับมา",
                      f"อากาศรอบ{thing}ส่องสว่างขึ้นจนมองเห็นได้")
            stem = f"เรามองเห็น{thing}ได้อย่างไร"
        else:
            thing = rng.choice(NON_LUMINOUS)
            source = rng.choice(("ดวงอาทิตย์", "หลอดไฟ", "ไฟฉาย", "เทียน"))
            right = f"แสงจาก{source}ตกกระทบ{thing} แล้วสะท้อนเข้าสู่ตา"
            wrongs = (f"{thing}ผลิตแสงได้เอง โดยไม่ต้องอาศัยแสงจาก{source}", f"ดวงตาส่งแสงออกไปกระทบ{thing} โดยไม่ต้องมีแสงจาก{source}", f"แสงจาก{source}เคลื่อนที่เป็นเส้นโค้งอ้อม{thing}เข้าตา")
            stem = f"เมื่อมีแสงจาก{source} เรามองเห็น{thing}ได้อย่างไร"
        return _labelled(stem=stem, correct=right, wrongs=wrongs, hint=LIGHT_HINT, topic=LIGHT_SEEING_TOPIC)


@question_type(
    "phys.light_travel_application",
    display_name={"th": "ใช้ความรู้เรื่องแนวแสงและการมองเห็นอธิบายสถานการณ์"},
    level=SECOND, subject=SUBJECT, topic=LIGHT_SEEING_TOPIC,
)
class LightTravelApplication(QuestionType):
    """Authored cases, and the cards-with-holes test of straight-line light."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _retopic(scenario_question(rng, LIGHT_SEEING_SCENARIOS, hint=LIGHT_HINT), LIGHT_SEEING_TOPIC)
        if rng.random() < 0.35:
            tube = rng.choice(("หลอดดูดน้ำ", "ท่อพลาสติก", "ท่อกระดาษ"))
            target = rng.choice(("เปลวเทียน", "หลอดไฟ", "ไฟฉายที่เปิดอยู่"))
            straight = rng.random() < 0.5
            right = (f"มองเห็น{target} เพราะแสงเคลื่อนที่เป็นเส้นตรง ผ่าน{tube}ที่ตรงได้ตลอดแนว" if straight
                     else f"มองไม่เห็น{target} เพราะแสงเคลื่อนที่เป็นเส้นตรง เลี้ยวตาม{tube}ที่งอไม่ได้")
            other = (f"มองไม่เห็น{target} เพราะแสงเคลื่อนที่เป็นเส้นตรง เลี้ยวตาม{tube}ที่งอไม่ได้" if straight
                     else f"มองเห็น{target} เพราะแสงเคลื่อนที่เป็นเส้นตรง ผ่าน{tube}ที่ตรงได้ตลอดแนว")
            return _labelled(stem=f"นักเรียนมอง{target}ผ่าน{tube}ที่{'ตรง' if straight else 'งอตรงกลาง'} จะมองเห็น{target}หรือไม่ เพราะเหตุใด",
                             correct=right, wrongs=(other, f"มองเห็น{target} เพราะแสงเคลื่อนที่โค้งไปตามผนังด้านในของ{tube}ได้",
                                                    f"มองไม่เห็น{target} เพราะผนังด้านในของ{tube}ดูดกลืนแสงที่ผ่านเข้าไป"),
                             hint=LIGHT_HINT, topic=LIGHT_SEEING_TOPIC)
        cards = rng.randint(3, 4)
        source = rng.choice(("เทียนที่จุดอยู่", "หลอดไฟ", "ไฟฉาย"))
        aligned = rng.random() < 0.5
        moved = None if aligned else rng.randrange(cards)
        setup = (f"วางกระดาษแข็งเจาะรู {cards} แผ่นเรียงกันระหว่างตาของนักเรียนกับ{source} "
                 + ("โดยรูทุกแผ่นอยู่ในแนวเส้นตรงเดียวกัน" if aligned else f"แล้วเลื่อน{CARD_LABELS[moved]}ออกไปด้านข้างเล็กน้อย"))
        right = (f"มองเห็นแสงจาก{source} เพราะแสงเคลื่อนที่เป็นเส้นตรง ผ่านรูที่อยู่ในแนวเดียวกันทุกแผ่นได้" if aligned
                 else f"มองไม่เห็นแสงจาก{source} เพราะแสงเคลื่อนที่เป็นเส้นตรง ผ่านรูที่ไม่อยู่ในแนวเดียวกันไม่ได้")
        other = (f"มองไม่เห็นแสงจาก{source} เพราะแสงเคลื่อนที่เป็นเส้นตรง ผ่านรูที่ไม่อยู่ในแนวเดียวกันไม่ได้" if aligned
                 else f"มองเห็นแสงจาก{source} เพราะแสงเคลื่อนที่เป็นเส้นตรง ผ่านรูที่อยู่ในแนวเดียวกันทุกแผ่นได้")
        return _labelled(stem=f"{setup} นักเรียนจะมองเห็นแสงหรือไม่ เพราะเหตุใด", correct=right,
                         wrongs=(other, f"มองเห็นแสงจาก{source} เพราะแสงเลี้ยวอ้อมขอบกระดาษแข็งแต่ละแผ่นแล้วมาถึงตาได้",
                                 f"มองไม่เห็นแสงจาก{source} เพราะแสงผ่านรูเล็ก ๆ บนกระดาษแข็งไม่ได้ แม้รูจะเรียงตรงกัน"),
                         hint=LIGHT_HINT, topic=LIGHT_SEEING_TOPIC)
