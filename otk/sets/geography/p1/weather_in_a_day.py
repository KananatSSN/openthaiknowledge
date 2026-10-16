"""สภาพอากาศในรอบวัน

ภูมิศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ส 5.1 ป.1/4
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.sets._support.geography import P1, SUBJECT, choices, scenario, stage

PROVENANCE = Provenance("original")


TOPIC = "สภาพอากาศในรอบวัน"


@question_type(
    "geog.weather_in_a_day_p1",
    display_name={"th": "บอกการเปลี่ยนแปลงของสภาพอากาศในรอบวัน"},
    level=P1, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class WeatherInADay(ConceptBankType):
    ITEMS = [
        Concept("ช่วงเวลาใดของวันที่อากาศมักร้อนที่สุด", "ช่วงบ่าย",
                ("ช่วงเช้ามืด", "ช่วงหัวค่ำ", "ช่วงเที่ยงคืน")),
        Concept("ช่วงเวลาใดของวันที่อากาศมักเย็นที่สุด", "ช่วงเช้ามืด",
                ("ช่วงเที่ยงวัน", "ช่วงบ่าย", "ช่วงหัวค่ำ")),
        Concept("ตอนเช้าตรู่มีหยดน้ำเล็ก ๆ เกาะอยู่ตามใบหญ้า หยดน้ำนั้นเรียกว่าอะไร", "น้ำค้าง",
                ("ลูกเห็บ", "หิมะ", "ฝุ่นละออง")),
        Concept("ถ้าท้องฟ้ามีเมฆดำครึ้มและลมพัดแรง ควรเตรียมตัวอย่างไร", "เตรียมร่มเพราะฝนอาจตก",
                ("ทาครีมกันแดดเพราะแดดจะจัด", "นำผ้าออกไปตากกลางแจ้ง", "ออกไปเล่นว่าวกลางทุ่ง")),
        Concept("ตอนเที่ยงแดดจัด ควรทำอย่างไรเมื่อต้องออกไปนอกอาคาร", "สวมหมวกและดื่มน้ำให้เพียงพอ",
                ("สวมเสื้อกันหนาวตัวหนา", "สวมเสื้อกันฝนตลอดเวลา", "วิ่งเล่นกลางแดดนาน ๆ")),
    ]


HOURS = range(7, 18)


def _clear(rng: Random, pick) -> tuple[list[int], int]:
    """Four whole hours where the one ``pick`` chooses by distance from noon
    stands at least two hours clear of the next, so the sun's true noon
    (shortly after 12.00 in Thailand) cannot change the answer."""
    while True:
        hours = rng.sample(HOURS, 4)
        gaps = sorted(abs(h - 12) for h in hours)
        edge = gaps[0] if pick is min else gaps[-1]
        nearest = gaps[1] if pick is min else gaps[-2]
        if abs(edge - nearest) >= 2:
            return hours, pick(hours, key=lambda h: abs(h - 12))


@question_type(
    "geog.shadow_length_p1",
    display_name={"th": "บอกเวลาที่เงายาวหรือสั้นที่สุดในรอบวัน"},
    level=P1, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class ShadowLength(QuestionType):
    def build(self, rng: Random, **params):
        short = rng.random() < 0.5
        hours, answer = _clear(rng, min if short else max)
        word = "สั้น" if short else "ยาว"
        return choices(
            stem=f"วันที่ท้องฟ้าแจ่มใส เงาของเสาธงหน้าโรงเรียนจะ{word}ที่สุดในเวลาใด",
            correct=f"{answer:02d}.00 น.",
            wrongs=[f"{h:02d}.00 น." for h in hours if h != answer],
            hint="ตอนเที่ยงดวงอาทิตย์อยู่สูงเกือบเหนือศีรษะ เงาจึงสั้น ตอนเช้าและตอนเย็นดวงอาทิตย์อยู่ต่ำ เงาจึงยาว",
            topic=TOPIC)


PREPARE = (
    ("ตอนเช้าท้องฟ้าแจ่มใส แต่ตอนบ่ายมีเมฆดำตั้งเค้า ถ้าจะออกไปข้างนอกตอนบ่าย",
     "ควรพกร่มหรือเสื้อกันฝนไปด้วย", ()),
    ("ตอนเที่ยงแดดร้อนจัด ถ้าต้องเล่นกีฬากลางสนาม",
     "ควรสวมหมวก ทาครีมกันแดด และพกน้ำดื่ม", ()),
    ("ไปเที่ยวบนดอยในฤดูหนาว ตอนเช้ามืดอากาศเย็นจัด", "ควรสวมเสื้อกันหนาวก่อนออกจากที่พัก", ()),
    ("ตอนเช้ามีหมอกหนาจนมองเห็นได้ไม่ไกล ถ้าต้องเดินไปโรงเรียนริมถนน",
     "ควรเดินชิดขอบทางและสวมเสื้อสีสว่าง", ()),
    ("ลมพัดแรงขึ้นเรื่อย ๆ ก่อนพายุฝนจะมา", "ควรเก็บของที่ปลิวได้เข้าไว้ในบ้าน", ()),
    ("ฝนตกหนักและฟ้าร้องฟ้าผ่าขณะเล่นอยู่กลางสนาม", "ควรรีบเข้าหลบในอาคาร ไม่ยืนใต้ต้นไม้ใหญ่", ()),
)


@question_type(
    "geog.weather_prepare_p1",
    display_name={"th": "เตรียมตัวให้เหมาะกับสภาพอากาศที่เปลี่ยนไปในรอบวัน"},
    level=P1, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class WeatherPrepare(QuestionType):
    def build(self, rng: Random, **params):
        return scenario(rng, PREPARE, ask="ควรทำอย่างไรจึงเหมาะสมที่สุด",
                        hint="ดูว่าอากาศกำลังจะเป็นอย่างไร แล้วเลือกสิ่งที่ช่วยให้ปลอดภัยในอากาศแบบนั้น",
                        topic=TOPIC)

# More rows and items: these tables held five or six, so a learner met them
# all in a few tries. Each added situation is one no other row answers.
PREPARE += (
    ('แดดจัดตอนกลางวัน และต้องการตากผ้าให้แห้งเร็ว',
     'ควรนำผ้าไปตากกลางแดดช่วงสายถึงบ่าย', ()),
    ('ตอนกลางคืนมียุงมากหลังฝนหยุดตก',
     'ควรนอนในมุ้งหรือทายากันยุง', ()),
    ('ตอนบ่ายอากาศร้อนอบอ้าว และห้องเรียนไม่มีพัดลม',
     'ควรเปิดหน้าต่างให้ลมผ่านและดื่มน้ำบ่อย ๆ', ()),
    ('ฝนเพิ่งหยุดตก พื้นทางเดินยังเปียกลื่น',
     'ควรเดินช้า ๆ และระวังลื่นล้ม', ()),
    ('ตอนเช้าอากาศเย็นสบายและแดดอ่อน',
     'ควรออกไปวิ่งเล่นหรือออกกำลังกายกลางแจ้ง', ()),
    ('อากาศร้อนจัดหลายวันติดกัน น้ำในตุ่มเหลือน้อย',
     'ควรใช้น้ำอย่างประหยัดเท่าที่จำเป็น', ()),
)

WeatherInADay.ITEMS = [*WeatherInADay.ITEMS,
    Concept('ตอนเช้าตรู่บนดอย เห็นเหมือนเมฆลอยอยู่ใกล้พื้นจนมองไม่ไกล สิ่งนั้นเรียกว่าอะไร',
            'หมอก',
            ('ลูกเห็บ', 'รุ้งกินน้ำ', 'ฟ้าแลบ', 'ฝุ่นทราย')),
    Concept('หลังฝนหยุดตกและมีแดดออก บางครั้งเห็นแถบสีโค้งบนท้องฟ้า เรียกว่าอะไร',
            'รุ้งกินน้ำ',
            ('หมอก', 'น้ำค้าง', 'ฟ้าร้อง', 'ลูกเห็บ')),
    Concept('เงาของเราตอนเที่ยงวันเป็นอย่างไรเมื่อเทียบกับตอนเช้า',
            'สั้นกว่าตอนเช้า',
            ('ยาวกว่าตอนเช้า', 'ยาวเท่ากับตอนเช้า', 'หายไปทั้งวัน', 'ยาวที่สุดในวัน')),
    Concept('ถ้าท้องฟ้าไม่มีเมฆเลยตอนกลางวัน อากาศมักเป็นอย่างไร',
            'แดดจัดและร้อน',
            ('ฝนตกหนัก', 'หนาวจัด', 'มีหิมะตก', 'มืดครึ้มทั้งวัน')),
]
