"""การแลกเปลี่ยนแก๊สและการคายน้ำ

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/5

Sets moved here from: science_wave_f55.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f55 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_TRANS = "การแลกเปลี่ยนแก๊สและการคายน้ำ"


TRANS_FACTS = (
    ("เซลล์คุมทำให้ปากใบเปิดได้อย่างไร", "ไอออน K⁺ เข้าสู่เซลล์คุม น้ำออสโมซิสเข้า เซลล์คุมเต่งและโค้งออก",
     ("น้ำออกจากเซลล์คุมจนเหี่ยว", "เซลล์คุมหดตัวด้วยเส้นใยกล้ามเนื้อ", "ปากใบถูกดันเปิดด้วยแก๊ส O₂", "ไอออน K⁺ ออกจากเซลล์คุม")),
    ("ฮอร์โมนใดทำให้ปากใบปิดเมื่อพืชขาดน้ำ", "กรดแอบไซซิก", ("ออกซิน", "จิบเบอเรลลิน", "ไซโทไคนิน", "เอทิลีน")),
    ("พืชคายน้ำทางใดมากที่สุด", "ปากใบ", ("ผิวใบที่มีคิวทิน", "เลนทิเซลที่ลำต้น", "ขนราก", "ไฮดาโทด")),
    ("การที่หยดน้ำออกมาตามขอบใบในตอนเช้ามืด (กัตเตชัน) เกิดจากอะไร", "แรงดันรากดันน้ำออกทางไฮดาโทด",
     ("น้ำค้างเกาะที่ผิวใบในเวลากลางคืน", "การคายน้ำทางปากใบ", "การลำเลียงอาหารทางโฟลเอ็ม", "เซลล์ใบแตกเพราะอากาศเย็นจัด")),
    ("การคายน้ำมีประโยชน์ต่อพืชอย่างไร", "ช่วยดึงน้ำและธาตุอาหารขึ้นสู่ยอด และช่วยลดอุณหภูมิของใบ",
     ("ทำให้พืชได้แก๊ส O₂ เพิ่มสำหรับการหายใจของรากทุกเซลล์", "ช่วยสร้างกลูโคสได้โดยตรงจากน้ำที่คายออก", "ทำให้รากดูดแร่ธาตุไม่ได้ จึงต้องคายน้ำออกเพื่อพักราก", "ไม่มีประโยชน์ใดเลย")),
    ("เมื่อเซลล์คุมสูญเสียน้ำจนเหี่ยว จะเกิดอะไรขึ้น", "ปากใบปิด การคายน้ำลดลง",
     ("ปากใบเปิดกว้างขึ้น", "เซลล์คุมแบ่งเซลล์", "ใบคายน้ำมากขึ้น", "คลอโรพลาสต์หายไป")),
    ("โดยทั่วไปปากใบของพืชส่วนใหญ่เปิดเมื่อใด", "เวลากลางวันที่มีแสงและพืชมีน้ำเพียงพอ",
     ("เวลากลางคืนเท่านั้นที่ไม่มีแสง", "เมื่อพืชขาดน้ำรุนแรงในเวลากลางวัน", "เมื่อมีกรดแอบไซซิกสะสมมาก", "เมื่อ CO₂ ในใบสูงมากในเวลากลางคืน")),
    ("แก๊ส CO₂ เข้าสู่ใบเพื่อใช้สังเคราะห์ด้วยแสงทางใด", "ปากใบ", ("เส้นใบ", "คิวทิน", "ขนราก", "โฟลเอ็ม")),
)


FACTORS = (("ความเข้มแสงเพิ่มขึ้น", 1), ("ความเข้มแสงลดลง", -1), ("อุณหภูมิอากาศสูงขึ้น", 1), ("อุณหภูมิอากาศลดลง", -1),
           ("ความชื้นในอากาศสูงขึ้น", -1), ("ความชื้นในอากาศลดลง", 1), ("ลมพัดแรงขึ้น", 1), ("อากาศนิ่งไม่มีลม", -1),
           ("ดินขาดน้ำจนปากใบปิด", -1), ("รดน้ำให้ดินชุ่มหลังจากขาดน้ำ", 1))


TRANS_HINT = ("การคายน้ำเพิ่มเมื่อแสงมาก อุณหภูมิสูง อากาศแห้ง และมีลม ลดลงเมื่ออากาศชื้น ไม่มีลม หรือพืชขาดน้ำจนปากใบปิด "
              "เซลล์คุมเต่งเมื่อ K⁺ และน้ำเข้า ปากใบจึงเปิด")


@question_type(
    "biology.transpiration_foundation",
    display_name={"th": "การปิดเปิดปากใบและการคายน้ำ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TRANS,
)
class TranspirationFoundation(QuestionType):
    """Guard cells, ABA, and where the water leaves."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(TRANS_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_TRANS, hint=TRANS_HINT)


@question_type(
    "biology.transpiration_fluency",
    display_name={"th": "ปัจจัยที่มีผลต่ออัตราการคายน้ำ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TRANS,
)
class TranspirationFluency(QuestionType):
    """Light, heat, dry air and wind speed it up; humid still air and drought slow it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        plant = rng.choice(("ต้นมะเขือเทศ", "ต้นทานตะวัน", "ต้นถั่วเขียว", "ต้นพริก", "ต้นชบา", "ต้นผักบุ้ง"))
        if rng.random() < 0.6:
            change, sign = rng.choice(FACTORS)
            answer = "อัตราการคายน้ำเพิ่มขึ้น" if sign > 0 else "อัตราการคายน้ำลดลง"
            return _labelled(stem=f"ถ้าปัจจัยอื่นคงที่ แต่{change} {plant}จะเป็นอย่างไร", correct=answer,
                             wrongs=("อัตราการคายน้ำลดลง" if sign > 0 else "อัตราการคายน้ำเพิ่มขึ้น", "อัตราการคายน้ำไม่เปลี่ยนแปลง",
                                     "หยุดคายน้ำทันทีอย่างถาวร"), topic=TOPIC_TRANS, hint=TRANS_HINT)
        up = rng.random() < 0.5
        right = rng.choice([c for c, s in FACTORS if (s > 0) == up])
        wrongs = rng.sample([c for c, s in FACTORS if (s > 0) != up], 3)
        return _labelled(stem=f"ข้อใดทำให้{plant}คายน้ำ{'มากขึ้น' if up else 'น้อยลง'} เมื่อปัจจัยอื่นคงที่", correct=right,
                         wrongs=tuple(wrongs), topic=TOPIC_TRANS, hint=TRANS_HINT)


@question_type(
    "biology.transpiration_application",
    display_name={"th": "คำนวณอัตราการคายน้ำจากโพโตมิเตอร์และน้ำหนักที่หายไป"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TRANS,
)
class TranspirationApplication(QuestionType):
    """Bubble travel × tube cross-section, or mass lost, over time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            section = rng.choice((Fraction(1, 2), 1, Fraction(3, 2), 2, Fraction(5, 2)))
            minutes = rng.choice((2, 4, 5, 10, 20))
            rate = rng.randrange(2, 41, 2)
            travel = Fraction(rate * minutes, 1) / section
            if (travel * 100).denominator != 1:
                section, travel = 1, Fraction(rate * minutes)
            volume = travel * section
            ask_volume = rng.random() < 0.4
            return numeric(stem=f"โพโตมิเตอร์มีหลอดแคปิลลารีพื้นที่หน้าตัด {show(section)} mm² ฟองอากาศเคลื่อนที่ได้ {show(travel)} mm "
                                f"ในเวลา {minutes} นาที "
                                + ("ต้นพืชดูดน้ำไปกี่ mm³" if ask_volume else "อัตราการดูดน้ำเป็นกี่ mm³ ต่อนาที"),
                           answer=volume if ask_volume else volume / minutes,
                           wrongs=[travel, travel / minutes, volume * minutes] if ask_volume else [travel / minutes, volume, rate * 2],
                           unit="mm³" if ask_volume else "mm³ ต่อนาที", topic=TOPIC_TRANS,
                           hint="ปริมาตรน้ำ = ระยะที่ฟองอากาศเคลื่อน × พื้นที่หน้าตัดของหลอด อัตรา = ปริมาตร ÷ เวลา")
        hours = rng.choice((2, 4, 5, 6, 8, 10, 12))
        rate = Fraction(rng.randrange(5, 101, 5), 10)
        loss = rate * hours
        start = rng.randrange(400, 1501, 10)
        leaf = rng.choice((100, 200, 250, 400, 500))
        if rng.random() < 0.5:
            return numeric(stem=f"กระถางต้นไม้ที่หุ้มดินด้วยพลาสติกหนัก {start} g วางไว้ {hours} ชั่วโมง เหลือหนัก {show(start - loss)} g "
                                f"อัตราการคายน้ำเป็นกี่กรัมต่อชั่วโมง", answer=rate,
                           wrongs=[loss, Fraction(start - loss, hours), rate * 2], unit="g ต่อชั่วโมง", topic=TOPIC_TRANS,
                           hint="หุ้มดินไว้ น้ำหนักที่หายไปจึงเป็นน้ำที่คายออกทางใบ อัตรา = น้ำหนักที่หายไป ÷ เวลา")
        per_area = loss * 1000 / leaf
        return numeric(stem=f"ต้นไม้ในกระถางที่หุ้มดินไว้คายน้ำหายไป {show(loss)} g ใน {hours} ชั่วโมง ใบทั้งต้นมีพื้นที่ {leaf} cm² "
                            f"คายน้ำเฉลี่ยกี่มิลลิกรัมต่อตารางเซนติเมตรตลอดช่วงเวลานี้", answer=per_area,
                       wrongs=[loss / leaf, per_area / hours, loss * 1000], unit="mg/cm²", topic=TOPIC_TRANS,
                       hint="แปลง g เป็น mg (× 1,000) แล้วหารด้วยพื้นที่ใบ")
