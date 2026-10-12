"""แนวปะทะอากาศ

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/9

Sets moved here from: science_wave_f80.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f80 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_FRONT = "แนวปะทะอากาศ"


FRONTS = (
    ("แนวปะทะอากาศเย็น", "มวลอากาศเย็นเคลื่อนที่เข้าดันมวลอากาศอุ่นให้ยกตัวขึ้นอย่างรวดเร็ว", "เส้นสีน้ำเงินมีรูปสามเหลี่ยม",
     "เมฆคิวมูโลนิมบัส ฝนตกหนักและพายุฝนฟ้าคะนองในช่วงสั้น ๆ", "อุณหภูมิลดลงและความกดอากาศสูงขึ้น"),
    ("แนวปะทะอากาศอุ่น", "มวลอากาศอุ่นเคลื่อนที่ขึ้นไปตามลาดของมวลอากาศเย็นอย่างช้า ๆ", "เส้นสีแดงมีรูปครึ่งวงกลม",
     "เมฆแผ่นเป็นชั้นจากเซอร์รัสไปจนถึงนิมโบสเตรตัส ฝนตกเบาถึงปานกลางเป็นเวลานาน", "อุณหภูมิสูงขึ้นและอากาศชื้นขึ้น"),
    ("แนวปะทะอากาศคงที่", "มวลอากาศเย็นและอุ่นมาพบกันแต่แทบไม่เคลื่อนที่", "เส้นสลับสีแดงครึ่งวงกลมกับสีน้ำเงินสามเหลี่ยมหันไปคนละด้าน",
     "เมฆและฝนตกต่อเนื่องหลายวันในบริเวณเดิม", "สภาพอากาศแทบไม่เปลี่ยนเพราะแนวปะทะไม่เคลื่อนผ่านไป"),
    ("แนวปะทะอากาศรวม", "แนวปะทะอากาศเย็นเคลื่อนที่ไล่ทันแนวปะทะอากาศอุ่น", "เส้นสีม่วงมีทั้งสามเหลี่ยมและครึ่งวงกลมด้านเดียวกัน",
     "มีเมฆหลายชนิดและฝนตกเป็นบริเวณกว้าง", "อุณหภูมิเปลี่ยนเล็กน้อยเพราะมวลอากาศอุ่นถูกยกขึ้นพ้นผิวพื้น"),
)


FRONT_HINT = ("แนวปะทะอากาศเย็น: อากาศเย็นดันอากาศอุ่นขึ้นเร็ว เมฆคิวมูโลนิมบัส ฝนหนักช่วงสั้น ผ่านไปแล้วเย็นลง "
              "แนวปะทะอากาศอุ่น: อากาศอุ่นไต่ลาดอากาศเย็นช้า ๆ เมฆแผ่นเป็นชั้น ฝนเบาเป็นเวลานาน "
              "สัญลักษณ์ เย็น=สามเหลี่ยมสีน้ำเงิน อุ่น=ครึ่งวงกลมสีแดง คงที่=สลับสองแบบ รวม=สีม่วง")


FRONT_PARTS = ("การเกิด", "สัญลักษณ์บนแผนที่อากาศ", "ลักษณะเมฆและฝน", "สภาพอากาศหลังแนวปะทะผ่าน")


@question_type(
    "geo.weather_front_foundation",
    display_name={"th": "การเกิดแนวปะทะอากาศแต่ละแบบ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FRONT,
)
class WeatherFrontFoundation(QuestionType):
    """How each front forms, and air masses."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            facts = (("แนวปะทะอากาศคืออะไร", "แนวที่มวลอากาศสองมวลซึ่งมีอุณหภูมิและความชื้นต่างกันมาพบกัน",
                      ("แนวที่ลมบกพบลมทะเล", "แนวเส้นศูนย์สูตร", "แนวเทือกเขาที่กั้นลม", "แนวชายฝั่งที่มีคลื่นแรง")),
                     ("มวลอากาศที่เกิดเหนือพื้นทวีปในเขตละติจูดสูงมีลักษณะอย่างไร", "เย็นและแห้ง",
                      ("ร้อนและชื้น", "เย็นและชื้นมาก", "ร้อนและแห้งจัด", "อุณหภูมิเท่ากับเขตร้อน")),
                     ("มวลอากาศที่เกิดเหนือมหาสมุทรในเขตร้อนมีลักษณะอย่างไร", "ร้อนและชื้น",
                      ("เย็นและแห้ง", "เย็นจัดและชื้น", "ร้อนและแห้งจัด", "ไม่มีไอน้ำเลย")),
                     ("ในฤดูหนาว ภาคเหนือและภาคอีสานของไทยมีอากาศเย็นลงอย่างรวดเร็วหลังมีฝนเล็กน้อย เกิดจากอะไร",
                      "มวลอากาศเย็นจากจีนแผ่ลงมาเป็นแนวปะทะอากาศเย็น",
                      ("มวลอากาศร้อนชื้นจากทะเลอันดามัน", "แนวปะทะอากาศอุ่นจากมหาสมุทรอินเดีย", "พายุไต้ฝุ่นจากทะเลจีนใต้", "ลมบกลมทะเล")),
                     ("มวลอากาศที่เกิดเหนือมหาสมุทรในเขตละติจูดสูงมีลักษณะอย่างไร", "เย็นและชื้น",
                      ("ร้อนและแห้ง", "ร้อนและชื้นมาก", "ร้อนจัดและไม่มีไอน้ำ", "อุณหภูมิเท่ากับเขตร้อน")),
                     ("เหตุใดผิวแนวปะทะอากาศเย็นจึงชันกว่าผิวแนวปะทะอากาศอุ่น", "อากาศเย็นหนาแน่นกว่า จึงมุดดันใต้อากาศอุ่นให้ยกตัวอย่างรวดเร็ว",
                      ("อากาศเย็นเบากว่าจึงลอยขึ้นเหนืออากาศอุ่น", "อากาศอุ่นหนาแน่นกว่าจึงจมลงใต้อากาศเย็น", "แรงคอริออลิสยกอากาศเย็นขึ้น",
                       "ทั้งสองแบบชันเท่ากันเสมอ")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_FRONT, hint=FRONT_HINT)
        front = rng.choice(FRONTS)
        others = [f for f in FRONTS if f is not front]
        if rng.random() < 0.5:
            return _labelled(stem=f"{front[0]}เกิดขึ้นอย่างไร", correct=front[1], wrongs=tuple(f[1] for f in others), topic=TOPIC_FRONT, hint=FRONT_HINT)
        return _labelled(stem=f"แนวปะทะอากาศที่{front[1]}คือแนวปะทะอากาศแบบใด", correct=front[0], wrongs=tuple(f[0] for f in others),
                         topic=TOPIC_FRONT, hint=FRONT_HINT)


@question_type(
    "geo.weather_front_fluency",
    display_name={"th": "สัญลักษณ์และลักษณะลมฟ้าอากาศของแนวปะทะอากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FRONT,
)
class WeatherFrontFluency(QuestionType):
    """Symbol, clouds and rain, and what follows, for each front."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            order = ("เซอร์รัส", "ซีร์โรสเตรตัส", "อัลโตสเตรตัส", "นิมโบสเตรตัส")
            perms = [p for p in permutations(order) if p != order]
            return _labelled(stem="เมื่อแนวปะทะอากาศอุ่นเคลื่อนเข้าใกล้ ผู้สังเกตบนพื้นจะเห็นเมฆเรียงตามลำดับใด",
                             correct=" → ".join(order), wrongs=tuple(" → ".join(p) for p in rng.sample(perms, 3)),
                             topic=TOPIC_FRONT, hint=FRONT_HINT + " เมฆที่อยู่สูงบนผิวแนวปะทะด้านหน้าจะมาถึงก่อน แล้วเมฆต่ำลงและหนาขึ้นจนมีฝน")
        part = rng.randrange(3)
        # Only a moving front has weather "after it passes".
        front = rng.choice(FRONTS[:2] if part == 2 else FRONTS)
        others = [f for f in FRONTS if f is not front]
        label = FRONT_PARTS[part + 1]
        if rng.random() < 0.5:
            return _labelled(stem=f"{label}ของ{front[0]}เป็นอย่างไร", correct=front[part + 2], wrongs=tuple(f[part + 2] for f in others),
                             topic=TOPIC_FRONT, hint=FRONT_HINT)
        what = {0: f"มีสัญลักษณ์บนแผนที่อากาศเป็น{front[2]}", 1: f"ทำให้เกิด{front[3]}", 2: f"เมื่อผ่านไปแล้ว{front[4]}"}[part]
        return _labelled(stem=f"แนวปะทะอากาศที่{what}คือแนวปะทะอากาศแบบใด", correct=front[0], wrongs=tuple(f[0] for f in others),
                         topic=TOPIC_FRONT, hint=FRONT_HINT)


@question_type(
    "geo.weather_front_application",
    display_name={"th": "คำนวณความสูงของผิวแนวปะทะและเวลาที่แนวปะทะมาถึง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FRONT,
)
class WeatherFrontApplication(QuestionType):
    """Height of the frontal surface from its slope; arrival time; station records."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            cold = rng.random() < 0.5
            slope = 100 if cold else 200
            distance = rng.randrange(50, 1001, 50)
            name = "แนวปะทะอากาศเย็น" if cold else "แนวปะทะอากาศอุ่น"
            return numeric(stem=f"{name}มีความลาดชันประมาณ 1 : {slope} ที่ตำแหน่งห่างจากแนวปะทะบนผิวพื้นไปในด้านอากาศเย็น {distance} km "
                                f"ผิวแนวปะทะอยู่สูงจากพื้นกี่ km",
                           answer=Fraction(distance, slope), wrongs=[Fraction(distance, 300 - slope), distance * slope // 1000, Fraction(distance, slope) * 10],
                           unit="km", topic=TOPIC_FRONT, hint="ความสูง = ระยะทางแนวราบ × ความลาดชัน")
        if roll < 0.7:
            speed = rng.choice((10, 15, 20, 25, 30, 40, 50))
            hours = rng.randint(3, 36)
            name = rng.choice(("แนวปะทะอากาศเย็น", "แนวปะทะอากาศอุ่น"))
            city = rng.choice(("เชียงราย", "ขอนแก่น", "นครพนม", "อุดรธานี", "น่าน"))
            return numeric(stem=f"{name}อยู่ห่างจากจังหวัด{city} {show(speed * hours)} km และเคลื่อนที่เข้าหาด้วยอัตราเร็ว {speed} km/h "
                                f"อีกกี่ชั่วโมงแนวปะทะจะมาถึง",
                           answer=hours, wrongs=[hours * 2, hours + 6, Fraction(hours, 2) if hours % 2 == 0 else hours + 3], unit="ชั่วโมง",
                           topic=TOPIC_FRONT, hint="เวลา = ระยะทาง ÷ อัตราเร็ว")
        records = (("อุณหภูมิลดลงจาก {a} °C เป็น {b} °C ภายในไม่กี่ชั่วโมง ความกดอากาศสูงขึ้น มีฝนฟ้าคะนองช่วงสั้น ๆ แล้วท้องฟ้าแจ่มใส", "แนวปะทะอากาศเย็น"),
                   ("เมฆเซอร์รัสปรากฏก่อน ตามด้วยเมฆเป็นชั้นหนาขึ้น ฝนตกปรอย ๆ นานนับวัน แล้วอุณหภูมิสูงขึ้นจาก {b} °C เป็น {a} °C", "แนวปะทะอากาศอุ่น"),
                   ("ฝนตกต่อเนื่องหลายวันในบริเวณเดิม อุณหภูมิอยู่ระหว่าง {b} ถึง {a} °C ทุกวันและลมแทบไม่เปลี่ยนทิศ", "แนวปะทะอากาศคงที่"))
        text, right = rng.choice(records)
        a = rng.randint(24, 32)
        b = a - rng.randint(4, 12)
        return _labelled(stem=f"สถานีตรวจอากาศบันทึกว่า {text.format(a=a, b=b)} ข้อมูลนี้แสดงว่ามีแนวปะทะอากาศแบบใดผ่าน",
                         correct=right, wrongs=tuple(f[0] for f in FRONTS if f[0] != right), topic=TOPIC_FRONT, hint=FRONT_HINT)
