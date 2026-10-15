"""สิ่งแวดล้อมรอบตัว

ภูมิศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ส 5.1 ป.1/1, ส 5.2 ป.1/1
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.geography import P1, SUBJECT, choices, scenario, stage

PROVENANCE = Provenance("original")


TOPIC = "สิ่งแวดล้อมรอบตัว"

NATURAL = "สิ่งแวดล้อมที่เกิดขึ้นเองตามธรรมชาติ"
MADE = "สิ่งแวดล้อมที่มนุษย์สร้างขึ้น"


@question_type(
    "geog.natural_or_made_p1",
    display_name={"th": "จำแนกสิ่งแวดล้อมตามธรรมชาติกับที่มนุษย์สร้างขึ้น"},
    level=P1, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class NaturalOrMade(ClassifyType):
    ASKS = ("pick",)           # two groups: a classify question would offer two choices
    PICK_STEM = "ข้อใดเป็น{category}"
    CATEGORIES = [
        Category(NATURAL, ("ภูเขา", "แม่น้ำ", "ทะเล", "ก้อนเมฆ", "น้ำตก", "ป่าไม้",
                           "หาดทราย", "ดวงอาทิตย์", "ถ้ำ", "เกาะ")),
        Category(MADE, ("บ้าน", "ถนน", "สะพาน", "โรงเรียน", "เขื่อน", "ตลาด",
                        "สนามเด็กเล่น", "เสาไฟฟ้า", "รถยนต์", "วัด")),
    ]


# What each natural surrounding gives the people who live near it. Each benefit
# belongs to one thing only, so the other things' benefits are wrong choices.
BENEFITS = (
    ("แม่น้ำ", "มีน้ำให้คนใช้ดื่ม ใช้อาบ และใช้รดพืช"),
    ("ต้นไม้", "ให้ร่มเงาและผลไม้เป็นอาหาร"),
    ("ดิน", "เป็นที่ปลูกข้าวและผักให้เติบโต"),
    ("ทะเล", "เป็นแหล่งปลา กุ้ง และหอยให้คนจับมาเป็นอาหาร"),
    ("แสงแดด", "ให้แสงสว่างตอนกลางวันและช่วยให้ผ้าที่ตากแห้ง"),
    ("ลม", "ช่วยพัดให้อากาศถ่ายเทและทำให้รู้สึกเย็นสบาย"),
)


@question_type(
    "geog.nature_benefit_p1",
    display_name={"th": "บอกประโยชน์ของสิ่งแวดล้อมทางธรรมชาติต่อความเป็นอยู่ของคน"},
    level=P1, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class NatureBenefit(QuestionType):
    def build(self, rng: Random, **params):
        thing, benefit = rng.choice(BENEFITS)
        others = [b for t, b in BENEFITS if t != thing]
        if rng.random() < 0.5:
            return choices(stem=f"{thing}มีประโยชน์ต่อความเป็นอยู่ของคนอย่างไร",
                           correct=benefit, wrongs=rng.sample(others, 3),
                           hint="นึกถึงว่าคนที่อยู่ใกล้สิ่งนั้นได้ใช้อะไรจากมันในชีวิตประจำวัน",
                           topic=TOPIC)
        things = [t for t, b in BENEFITS if t != thing]
        return choices(stem=f"สิ่งแวดล้อมทางธรรมชาติข้อใด{benefit}",
                       correct=thing, wrongs=rng.sample(things, 3),
                       hint="นึกถึงว่าคนที่อยู่ใกล้สิ่งนั้นได้ใช้อะไรจากมันในชีวิตประจำวัน",
                       topic=TOPIC)


# A place and how the people there live from what nature gives them.
LIVING = (
    ("หมู่บ้านของแก้วอยู่ติดแม่น้ำใหญ่", "คนในหมู่บ้านใช้น้ำจากแม่น้ำและพายเรือข้ามฝั่ง", ()),
    ("บ้านของต้นอยู่ใกล้ทะเล", "คนในชุมชนออกเรือหาปลาทะเลและตากปลาเค็มขาย", ()),
    ("ภูอาศัยอยู่บนภูเขาที่อากาศเย็น", "คนในหมู่บ้านใส่เสื้อหนาวและปลูกผักเมืองหนาว", ()),
    ("หมู่บ้านของดาวมีป่าไม้ล้อมรอบ", "คนในหมู่บ้านเก็บเห็ดและหน่อไม้จากป่ามาเป็นอาหาร", ()),
    ("หมู่บ้านของฟ้าอยู่กลางทุ่งหญ้ากว้าง", "คนในหมู่บ้านเลี้ยงวัวควายโดยปล่อยให้กินหญ้า", ()),
    ("หมู่บ้านของบอลอยู่ใกล้บึงที่มีบัวขึ้นเต็ม", "คนในหมู่บ้านเก็บสายบัวและฝักบัวมาทำอาหาร", ()),
)


@question_type(
    "geog.nature_and_living_p1",
    display_name={"th": "บอกว่าสิ่งแวดล้อมทางธรรมชาติรอบบ้านส่งผลต่อความเป็นอยู่อย่างไร"},
    level=P1, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class NatureAndLiving(QuestionType):
    def build(self, rng: Random, **params):
        return scenario(rng, LIVING, ask="คนที่อยู่ที่นั่นน่าจะใช้ชีวิตอย่างไร",
                        hint="ดูว่ารอบบ้านมีอะไรตามธรรมชาติ แล้วนึกว่าคนจะใช้สิ่งนั้นอย่างไร",
                        topic=TOPIC)

# More rows and items: these tables held five or six, so a learner met them
# all in a few tries. Each added situation is one no other row answers.
LIVING += (
    ('หมู่บ้านของมดอยู่ริมคลองที่น้ำท่วมทุกปี',
     'คนในหมู่บ้านสร้างบ้านใต้ถุนสูงและมีเรือไว้ใช้', ()),
    ('บ้านของเอกอยู่ในเมืองใหญ่ที่มีรถมาก',
     'คนในเมืองเดินทางด้วยรถโดยสารและรถไฟฟ้า', ()),
    ('หมู่บ้านของนกอยู่ใกล้สวนผลไม้กว้างใหญ่',
     'คนในหมู่บ้านเก็บผลไม้ไปขายที่ตลาด', ()),
    ('หมู่บ้านของเมฆอยู่ในที่แห้งแล้งซึ่งฝนตกน้อย',
     'คนในหมู่บ้านเก็บน้ำฝนไว้ในโอ่งใช้ตลอดหน้าแล้ง', ()),
    ('บ้านของน้ำอยู่ติดนาข้าวกว้างใหญ่',
     'คนในหมู่บ้านปลูกข้าวไว้กินและขาย', ()),
    ('หมู่บ้านของฝนอยู่ใกล้ถ้ำและน้ำตกที่สวยงาม',
     'คนในหมู่บ้านพานักท่องเที่ยวชมถ้ำและน้ำตก', ()),
)
