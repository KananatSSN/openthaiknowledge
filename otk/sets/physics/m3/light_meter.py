"""การวัดความสว่างของแสงด้วยอุปกรณ์วัดความสว่าง

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/20

Sets moved here from: science_wave_d34.
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
from otk.sets._support.science_wave_d32 import THIRD_SECONDARY

PROVENANCE = Provenance("original")


LIGHT_METER_TOPIC = "การวัดความสว่างของแสงด้วยอุปกรณ์วัดความสว่าง"


LIGHT_METER_READINGS = ((500, 50), (300, 30), (800, 100), (600, 40), (400, 50), (900, 90), (1000, 200), (700, 70),
                        (450, 50), (360, 40), (750, 150), (640, 80), (480, 60), (540, 90), (720, 120), (1200, 300),
                        (350, 70), (560, 70), (250, 50), (420, 60), (900, 300), (630, 90), (880, 110), (1000, 125),
                        (1500, 300), (320, 80), (660, 110), (840, 120))


LIGHT_METER_HINT = "เครื่องวัดความสว่างวัดความสว่างที่ตกบนพื้นผิวเป็นลักซ์ ค่ายิ่งมากยิ่งสว่าง"


LIGHT_METER_FACTS = (
    ("ขณะวัดความสว่างบนโต๊ะเรียน ควรวางตัวรับแสงของเครื่องวัดไว้อย่างไร", "วางบนพื้นผิวที่ทำงาน หันรับแสงโดยไม่มีสิ่งใดบัง",
     ("ใช้มือปิดตัวรับแสงไว้", "หันตัวรับแสงลงพื้นโต๊ะ", "ถือไว้ใต้โต๊ะ", "วางในลิ้นชัก", "หันเข้าหาตัวผู้วัด")),
    ("เครื่องวัดความสว่างอ่านค่าได้มากขึ้น แสดงว่าอย่างไร", "บริเวณนั้นสว่างมากขึ้น",
     ("บริเวณนั้นมืดลง", "หลอดไฟร้อนขึ้น", "เครื่องวัดเสีย", "ใช้ไฟฟ้าน้อยลง", "แสงมีความถี่ต่ำลง")),
    ("ถ้าต้องการรู้ว่าห้องสว่างสม่ำเสมอหรือไม่ ควรวัดความสว่างอย่างไร", "วัดหลายจุดทั่วห้องแล้วเปรียบเทียบค่า",
     ("วัดจุดเดียวกลางห้อง", "วัดที่หลอดไฟโดยตรงจุดเดียว", "วัดนอกห้อง", "ไม่ต้องวัด ดูด้วยตาก็พอ", "วัดเฉพาะตอนปิดไฟ")),
    ("หน่วยลักซ์ (lux) ใช้บอกปริมาณใด", "ความสว่างที่ตกกระทบพื้นผิว",
     ("ความดังของเสียง", "อุณหภูมิ", "กำลังไฟฟ้าของหลอด", "ความยาวคลื่นของแสง", "ความเร็วของแสง")),
    ("ถ้านำเครื่องวัดความสว่างเข้าใกล้หลอดไฟมากขึ้น ค่าที่อ่านได้มักเป็นอย่างไร", "มากขึ้น",
     ("น้อยลง", "เท่าเดิม", "เป็นศูนย์", "ติดลบ", "แกว่งขึ้นลงตลอด")),
)


LUX_PLACES = ("ห้องเรียน", "ห้องสมุด", "ทางเดิน", "ห้องครัว", "ห้องทำงาน", "ห้องนอน", "ลานจอดรถ", "ห้องปฏิบัติการ")


LIGHT_METER_SCENARIOS = (
    ("ห้องผ่าตัดต้องการความสว่างสูงกว่าห้องนอนมาก เหตุใดจึงต้องกำหนดค่าความสว่างที่เหมาะสมกับแต่ละพื้นที่ด้วยเครื่องวัดความสว่าง",
     "แต่ละกิจกรรมต้องการความสว่างต่างกัน การวัดค่าจริงช่วยให้ปรับแสงให้เหมาะสมกับความละเอียดของงานที่ทำ",
     ("ทุกพื้นที่ควรมีความสว่างเท่ากันเสมอไม่ว่าจะทำกิจกรรมใด", "การวัดความสว่างไม่มีผลต่อความเหมาะสมในการทำกิจกรรม", "ห้องนอนควรมีความสว่างมากกว่าห้องผ่าตัดเสมอ")),
    ("นักเรียนวัดความสว่างบนโต๊ะอ่านหนังสือได้เพียง 50 ลักซ์ ซึ่งต่ำกว่าค่าที่แนะนำสำหรับการอ่านหนังสือมาก ควรทำอย่างไร",
     "เพิ่มแหล่งกำเนิดแสงหรือย้ายไปอ่านในบริเวณที่มีความสว่างเพียงพอตามค่าที่วัดได้",
     ("ไม่ต้องทำอะไรเพราะ 50 ลักซ์เพียงพอสำหรับการอ่านหนังสือเสมอ", "ควรลดความสว่างลงอีกเพื่อถนอมดวงตา", "ค่าที่วัดได้จากเครื่องวัดความสว่างไม่น่าเชื่อถือ")),
    ("โรงงานแห่งหนึ่งใช้เครื่องวัดความสว่างตรวจสอบพื้นที่ทำงานเป็นประจำ เหตุใดจึงต้องตรวจสอบซ้ำเป็นระยะแทนที่จะวัดเพียงครั้งเดียว",
     "ความสว่างอาจเปลี่ยนแปลงได้ตามเวลาและการเสื่อมสภาพของหลอดไฟ การตรวจสอบซ้ำช่วยให้มั่นใจว่าแสงยังเหมาะสมอยู่",
     ("ความสว่างของหลอดไฟไม่เปลี่ยนแปลงตามเวลาเลย", "การวัดครั้งแรกเพียงพอตลอดอายุการใช้งานของหลอดไฟ", "การตรวจสอบซ้ำไม่มีประโยชน์ต่อความปลอดภัยในการทำงาน")),
)


@question_type(
    "phys.light_meter_foundation",
    display_name={"th": "บอกปริมาณและหน่วยที่อุปกรณ์วัดความสว่างของแสงวัดได้"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=LIGHT_METER_TOPIC,
)
class LightMeterFoundation(QuestionType):
    """What a lux meter measures, how to use it, and which of two readings is brighter."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            stem, right, wrongs = rng.choice(LIGHT_METER_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=LIGHT_METER_HINT,
                             topic=LIGHT_METER_TOPIC)
        if roll < 0.8:
            a, b = rng.sample(LUX_PLACES, 2)
            la, lb = rng.sample(range(50, 1001, 25), 2)
            bright = a if la > lb else b
            dim = b if la > lb else a
            return _labelled(
                stem=f"เครื่องวัดความสว่างอ่านค่าใน{a}ได้ {la} ลักซ์ และใน{b}ได้ {lb} ลักซ์ ข้อใดสรุปได้ถูกต้อง",
                correct=f"{bright}สว่างกว่า{dim}",
                wrongs=(f"{dim}สว่างกว่า{bright}", "สว่างเท่ากัน เพราะวัดด้วยเครื่องเดียวกัน", "เปรียบเทียบไม่ได้ เพราะอยู่คนละห้อง"),
                hint=LIGHT_METER_HINT, topic=LIGHT_METER_TOPIC,
            )
        return _labelled(
            stem="อุปกรณ์วัดความสว่างของแสง (lux meter) วัดปริมาณใด และมีหน่วยเป็นอะไร",
            correct="วัดความสว่าง (ความเข้มของแสงที่ตกกระทบพื้นผิว) มีหน่วยเป็นลักซ์ (lux)",
            wrongs=("วัดความถี่ของแสง มีหน่วยเป็นเฮิรตซ์ (Hz)",
                    "วัดพลังงานไฟฟ้าที่ใช้ในการให้แสงสว่าง มีหน่วยเป็นจูล",
                    "วัดอุณหภูมิของหลอดไฟ มีหน่วยเป็นองศาเซลเซียส"),
            hint="ลักซ์ (lux) เป็นหน่วยเฉพาะของความสว่างที่ตกกระทบพื้นผิว ไม่ใช่ความถี่ พลังงาน หรืออุณหภูมิ",
            topic=LIGHT_METER_TOPIC,
        )


@question_type(
    "phys.light_meter_fluency",
    display_name={"th": "เปรียบเทียบค่าความสว่างที่วัดได้จากอุปกรณ์วัดความสว่าง"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=LIGHT_METER_TOPIC,
)
class LightMeterFluency(QuestionType):
    """Two lux readings from the same room at different times; the ratio between them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        day, evening = rng.choice(LIGHT_METER_READINGS)
        ratio = day // evening
        return _labelled(
            stem=(f"เครื่องวัดความสว่างอ่านค่าได้ {day} ลักซ์ในห้องเรียนช่วงกลางวัน และ {evening} ลักซ์ในห้องเดียวกัน "
                  "เมื่อปิดไฟหลักช่วงเย็น ข้อใดแปลความหมายข้อมูลนี้ได้ถูกต้อง"),
            correct=f"ห้องเรียนช่วงกลางวันมีความสว่างมากกว่าช่วงเย็นถึง {ratio} เท่า",
            wrongs=(f"ห้องเรียนช่วงเย็นมีความสว่างมากกว่าช่วงกลางวันถึง {ratio} เท่า",
                    "ห้องเรียนทั้งสองช่วงเวลามีความสว่างเท่ากันเพราะวัดในห้องเดียวกัน",
                    f"ความสว่างช่วงกลางวันต่างจากช่วงเย็น {day - evening} ลักซ์ จึงถือว่าใกล้เคียงกัน",
                    # The wrong way round and the wrong factor.
                    f"ห้องเรียนช่วงเย็นมีความสว่างมากกว่าช่วงกลางวันถึง {ratio + 1} เท่า",
                    f"ห้องเรียนช่วงเย็นมีความสว่างมากกว่าช่วงกลางวันถึง {ratio * 2} เท่า"),
            hint="เทียบอัตราส่วนของค่าที่วัดได้สองค่า ไม่ใช่แค่ผลต่าง",
            topic=LIGHT_METER_TOPIC,
        )


@question_type(
    "phys.light_meter_application",
    display_name={"th": "ใช้ค่าความสว่างที่วัดได้ประเมินความเหมาะสมของพื้นที่ทำงาน"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=LIGHT_METER_TOPIC,
)
class LightMeterApplication(QuestionType):
    """Authored cases, and a reading checked against a stated recommendation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            activity, rec = rng.choice((("อ่านหนังสือ", 400), ("เขียนแบบหรือวาดภาพละเอียด", 750), ("เดินในทางเดิน", 100),
                                        ("ทำอาหารในครัว", 300), ("เรียนในห้องเรียน", 300), ("ตรวจชิ้นงานในโรงงาน", 1000)))
            reading = rng.choice((rng.randrange(max(25, rec // 5), rec, 25), rng.randrange(rec, rec * 2 + 1, 25)))
            enough = reading >= rec
            return _labelled(
                stem=(f"ค่าความสว่างที่แนะนำสำหรับ{activity}คืออย่างน้อย {rec} ลักซ์ นักเรียนวัดได้ {reading} ลักซ์ "
                      "ข้อใดสรุปและเสนอแนะได้เหมาะสม"),
                correct=("เพียงพอสำหรับกิจกรรมนี้ ไม่จำเป็นต้องเพิ่มแสง" if enough
                         else f"ไม่เพียงพอ ขาดอยู่ {rec - reading} ลักซ์ ควรเพิ่มแสงหรือย้ายไปบริเวณที่สว่างกว่า"),
                wrongs=((f"ไม่เพียงพอ ขาดอยู่ {reading - rec + 50} ลักซ์ ควรเพิ่มแสงหรือย้ายไปบริเวณที่สว่างกว่า" if enough
                         else "เพียงพอสำหรับกิจกรรมนี้ ไม่จำเป็นต้องเพิ่มแสง"),
                        "ควรลดแสงลง เพราะค่ายิ่งน้อยยิ่งถนอมสายตา",
                        "สรุปไม่ได้ เพราะเครื่องวัดความสว่างใช้วัดได้เฉพาะกลางแจ้ง"),
                hint="เทียบค่าที่วัดได้กับค่าที่แนะนำ ถ้าต่ำกว่าต้องเพิ่มแสง",
                topic=LIGHT_METER_TOPIC,
            )
        return _retopic(scenario_question(
            rng, LIGHT_METER_SCENARIOS,
            hint="ความสว่างที่เหมาะสมขึ้นกับชนิดของกิจกรรม การวัดค่าจริงช่วยตรวจสอบและปรับให้เหมาะสม",
        ), LIGHT_METER_TOPIC)
