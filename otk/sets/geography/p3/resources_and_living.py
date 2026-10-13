"""ทรัพยากรกับการดำเนินชีวิต

ภูมิศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ส 5.2 ป.3/2, ส 5.2 ป.3/5
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.geography import P3, SUBJECT, scenario, stage

PROVENANCE = Provenance("original")


TOPIC = "ทรัพยากรกับการดำเนินชีวิต"


@question_type(
    "geog.basic_needs_p3",
    display_name={"th": "บอกว่าทรัพยากรธรรมชาติตอบสนองปัจจัยสี่ข้อใด"},
    level=P3, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class BasicNeeds(ClassifyType):
    CLASSIFY_STEM = "การนำทรัพยากรมาใช้ “{member}” ตอบสนองปัจจัยสี่ข้อใด"
    PICK_STEM = "การใช้ทรัพยากรข้อใดตอบสนองปัจจัยสี่ด้าน{category}"
    CATEGORIES = [
        Category("อาหาร", ("ปลูกข้าวในนาไว้หุงกิน", "จับปลาในแม่น้ำมาทำกับข้าว", "เก็บผักบุ้งริมคลองมาผัด")),
        Category("เครื่องนุ่งห่ม", ("ปลูกฝ้ายมาปั่นเป็นด้ายทอผ้า", "เลี้ยงไหมเพื่อนำเส้นไหมมาทอผ้า",
                                    "ใช้ครามย้อมผ้าให้เป็นสีน้ำเงิน")),
        Category("ที่อยู่อาศัย", ("ตัดไม้มาสร้างบ้าน", "ใช้หญ้าคามามุงหลังคา", "ใช้ไม้ไผ่ทำฝาบ้าน")),
        Category("ยารักษาโรค", ("ใช้ฟ้าทะลายโจรบรรเทาอาการเจ็บคอ", "ใช้ว่านหางจระเข้ทาแผลไฟไหม้",
                                "ใช้ขมิ้นชันบรรเทาอาการท้องอืด")),
    ]


@question_type(
    "geog.land_occupation_p3",
    display_name={"th": "บอกอาชีพที่เหมาะกับลักษณะทางกายภาพของชุมชน"},
    level=P3, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class LandOccupation(ClassifyType):
    ASKS = ("pick",)           # three groups: a classify question would offer three choices
    PICK_STEM = "ชุมชนที่ตั้งอยู่บน{category} คนส่วนใหญ่น่าจะประกอบอาชีพใด"
    CATEGORIES = [
        Category("ที่ราบลุ่มริมแม่น้ำ", ("ทำนาปลูกข้าว", "ปลูกผักริมตลิ่ง", "เลี้ยงปลาในกระชังริมแม่น้ำ")),
        Category("ชายฝั่งทะเล", ("ออกเรือหาปลาในทะเล", "ทำนาเกลือ", "เลี้ยงหอยแครงในทะเลตม")),
        Category("ภูเขาและที่สูง", ("ปลูกชาและกาแฟบนเนินเขา", "ทำนาขั้นบันได", "ปลูกผักเมืองหนาว")),
    ]


PRODUCTS = (
    ("ชุมชนหนึ่งมีป่าไผ่ขึ้นอยู่มาก",
     "สานตะกร้าและเครื่องจักสานจากไม้ไผ่ไปขาย", ()),
    ("ชุมชนหนึ่งมีดินเหนียวคุณภาพดีอยู่ริมแม่น้ำ",
     "ปั้นโอ่งและเครื่องปั้นดินเผาไปขาย", ()),
    ("ชุมชนหนึ่งอยู่บนดอยที่อากาศเย็นเกือบทั้งปี",
     "ปลูกผักและผลไม้เมืองหนาวส่งไปขาย", ()),
    ("ชุมชนหนึ่งอยู่ริมทะเลที่มีหาดทรายสวยงาม",
     "เปิดที่พักและบริการให้นักท่องเที่ยว", ()),
    ("ชุมชนหนึ่งปลูกต้นหม่อนได้งอกงาม",
     "เลี้ยงไหมแล้วทอผ้าไหมไปขาย", ()),
    ("ชุมชนหนึ่งมีต้นมะพร้าวขึ้นอยู่มาก",
     "ทำน้ำตาลมะพร้าวและกะทิไปขาย", ()),
)


@question_type(
    "geog.local_product_p3",
    display_name={"th": "เสนอวิธีใช้ทรัพยากรในชุมชนสร้างอาชีพ"},
    level=P3, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class LocalProduct(QuestionType):
    def build(self, rng: Random, **params):
        return scenario(rng, PRODUCTS, ask="คนในชุมชนควรใช้ทรัพยากรนี้สร้างรายได้อย่างไร",
                        hint="ดูว่าชุมชนมีทรัพยากรอะไรมาก แล้วเลือกอาชีพที่ใช้ทรัพยากรนั้นโดยตรง",
                        topic=TOPIC)
