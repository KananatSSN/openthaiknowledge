"""การลำเลียงน้ำและธาตุอาหาร

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/6

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


TOPIC_WATER = "การลำเลียงน้ำและธาตุอาหาร"


MECHANISMS = (
    ("แรงดึงจากการคายน้ำ", "เมื่อน้ำระเหยออกทางปากใบ โมเลกุลน้ำในไซเลมถูกดึงต่อกันขึ้นมาแทนที่"),
    ("แรงโคฮีชัน", "โมเลกุลน้ำยึดเหนี่ยวกันเองด้วยพันธะไฮโดรเจน ทำให้สายน้ำในไซเลมไม่ขาด"),
    ("แรงแอดฮีชัน", "โมเลกุลน้ำยึดเกาะกับผนังของเวสเซลและเทรคีด"),
    ("แรงดันราก", "รากลำเลียงไอออนเข้าไซเลม น้ำออสโมซิสตามเข้าไปจนดันน้ำขึ้นไป เห็นได้จากกัตเตชัน"),
    ("การลำเลียงแบบแอกทีฟทรานสปอร์ต", "เซลล์รากใช้พลังงานจาก ATP ดูดไอออนจากดินที่มีความเข้มข้นต่ำกว่าในเซลล์"),
)


WATER_FACTS = (
    ("น้ำเคลื่อนที่ไปตามผนังเซลล์และช่องว่างระหว่างเซลล์เรียกว่าเส้นทางใด", "อโพพลาสต์",
     ("ซิมพลาสต์", "โฟลเอ็ม", "บันเดิลชีท", "ทรานส์เมมเบรน")),
    ("น้ำเคลื่อนที่ผ่านไซโทพลาซึมจากเซลล์หนึ่งไปอีกเซลล์หนึ่งทางพลาสโมเดสมาตาเรียกว่าเส้นทางใด", "ซิมพลาสต์",
     ("อโพพลาสต์", "ไซเลม", "คิวทิน", "ปากใบ", "โฟลเอ็ม")),
    ("เมื่อน้ำไปถึงชั้นเอนโดเดอร์มิส เหตุใดจึงต้องผ่านเข้าไปในเซลล์", "แถบแคสแพเรียนมีซูเบอรินกั้นเส้นทางอโพพลาสต์ไว้",
     ("เอนโดเดอร์มิสไม่มีผนังเซลล์ จึงกั้นน้ำไว้", "ไซเลมอยู่ภายในเซลล์เอนโดเดอร์มิส", "น้ำเคลื่อนที่ผ่านผนังเซลล์ไม่ได้ในทุกชั้น",
      "เอนโดเดอร์มิสไม่มีเยื่อหุ้มเซลล์ น้ำจึงผ่านไม่ได้")),
    ("ขนรากช่วยให้รากดูดน้ำได้ดีขึ้นอย่างไร", "เพิ่มพื้นที่ผิวในการสัมผัสกับน้ำในดิน",
     ("สร้างน้ำขึ้นเองได้", "ปิดกั้นไม่ให้น้ำออกจากรากสู่ดินที่แห้ง", "สังเคราะห์ด้วยแสงให้พลังงานแก่ราก", "เป็นทางลำเลียงอาหารลงสู่ดิน")),
    ("น้ำและธาตุอาหารถูกลำเลียงจากรากขึ้นสู่ใบผ่านเนื้อเยื่อใด", "ไซเลม",
     ("โฟลเอ็ม", "คอร์เทกซ์", "พิธ", "เอพิเดอร์มิส")),
    ("น้ำส่วนใหญ่ที่รากดูดเข้าไปถูกนำไปใช้อย่างไร", "คายออกทางปากใบเป็นส่วนใหญ่ ใช้สังเคราะห์ด้วยแสงเพียงส่วนน้อย",
     ("ใช้สังเคราะห์ด้วยแสงเกือบทั้งหมด คายออกทางปากใบเพียงส่วนน้อย", "เก็บไว้ในรากทั้งหมด", "เปลี่ยนเป็นแป้งทั้งหมดแล้วเก็บไว้ในลำต้น", "ขับออกทางรากกลับสู่ดินเป็นส่วนใหญ่ในเวลากลางคืน")),
)


WATER_HINT = ("น้ำเข้าสู่รากทางอโพพลาสต์และซิมพลาสต์ แต่ต้องผ่านเซลล์ที่เอนโดเดอร์มิส ขึ้นสู่ยอดด้วยแรงดึงจากการคายน้ำ "
              "โคฮีชัน แอดฮีชัน และแรงดันราก ไอออนเข้ารากด้วยแอกทีฟทรานสปอร์ต")


@question_type(
    "biology.water_transport_foundation",
    display_name={"th": "เส้นทางการเคลื่อนที่ของน้ำเข้าสู่ราก"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterTransportFoundation(QuestionType):
    """Apoplast, symplast and the Casparian strip."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(WATER_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_WATER, hint=WATER_HINT)


@question_type(
    "biology.water_transport_fluency",
    display_name={"th": "แรงที่ทำให้น้ำและธาตุอาหารเคลื่อนที่ในพืช"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterTransportFluency(QuestionType):
    """Name the force from what it does, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, how = rng.choice(MECHANISMS)
        others = rng.sample([m for m in MECHANISMS if m[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{how}\" เป็นกลไกใด", correct=name, wrongs=tuple(m[0] for m in others), topic=TOPIC_WATER,
                             hint=WATER_HINT)
        return _labelled(stem=f"ข้อใดอธิบาย{name}ได้ถูกต้อง", correct=how, wrongs=tuple(m[1] for m in others), topic=TOPIC_WATER,
                         hint=WATER_HINT)


@question_type(
    "biology.water_transport_application",
    display_name={"th": "คำนวณการลำเลียงน้ำขึ้นสู่ยอด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterTransportApplication(QuestionType):
    """Height ÷ speed gives time; the share kept is what is not transpired."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            speed = rng.choice((2, 4, 5, 8, 10, 20))
            hours = Fraction(rng.randrange(1, 21), rng.choice((1, 2, 4)))
            height = speed * hours
            tree = rng.choice(("ต้นยางนา", "ต้นสัก", "ต้นมะพร้าว", "ต้นยูคาลิปตัส"))
            if rng.random() < 0.6:
                return numeric(stem=f"น้ำในไซเลมของ{tree}เคลื่อนที่ขึ้นด้วยอัตรา {speed} เมตรต่อชั่วโมง จากโคนถึงยอดสูง {show(height)} เมตร "
                                    f"ใช้เวลากี่ชั่วโมง", answer=hours, wrongs=[height * speed, height, hours * 2], unit="ชั่วโมง",
                               topic=TOPIC_WATER, hint="เวลา = ระยะทาง ÷ อัตราเร็ว")
            return numeric(stem=f"สีย้อมในน้ำเคลื่อนที่ขึ้นในไซเลมของ{tree}ได้ {show(height)} เมตรใน {show(hours)} ชั่วโมง "
                                f"อัตราเร็วเป็นกี่เมตรต่อชั่วโมง", answer=speed, wrongs=[height * hours, hours, speed * 2],
                           unit="เมตรต่อชั่วโมง", topic=TOPIC_WATER, hint="อัตราเร็ว = ระยะทาง ÷ เวลา")
        absorbed = rng.randrange(100, 2001, 50)
        lost = rng.choice((90, 95, 97, 98, 99))
        kept = Fraction(absorbed * (100 - lost), 100)
        return numeric(stem=f"พืชต้นหนึ่งดูดน้ำ {absorbed} g ในหนึ่งวัน และคายน้ำออกไปร้อยละ {lost} ของน้ำที่ดูด "
                            f"เหลือน้ำที่ใช้ในการสังเคราะห์ด้วยแสงและกิจกรรมอื่นกี่กรัม", answer=kept,
                       wrongs=[Fraction(absorbed * lost, 100), 100 - lost, kept * 10], unit="g", topic=TOPIC_WATER,
                       hint="น้ำที่เหลือใช้ = น้ำที่ดูด × (100 − ร้อยละที่คายออก) ÷ 100")
