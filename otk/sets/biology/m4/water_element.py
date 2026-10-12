"""น้ำและธาตุที่สำคัญต่อสิ่งมีชีวิต

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/3

Sets moved here from: science_wave_f44.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f44 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_WATER = "น้ำและธาตุที่สำคัญต่อสิ่งมีชีวิต"


WATER = (
    ("โมเลกุลของน้ำมีขั้วและเกิดพันธะไฮโดรเจนระหว่างโมเลกุล", "น้ำเป็นตัวทำละลายที่ดีของสารมีขั้วและไอออน"),
    ("น้ำมีความจุความร้อนจำเพาะสูง", "ช่วยรักษาอุณหภูมิของร่างกายและแหล่งน้ำไม่ให้เปลี่ยนเร็ว"),
    ("น้ำใช้ความร้อนมากในการระเหย", "เหงื่อที่ระเหยช่วยระบายความร้อนออกจากร่างกาย"),
    ("โมเลกุลน้ำยึดเกาะกันเองและยึดเกาะผนังท่อ (โคฮีชันและแอดฮีชัน)", "น้ำเคลื่อนที่ขึ้นไปตามท่อไซเล็มของพืชได้"),
    ("น้ำแข็งมีความหนาแน่นน้อยกว่าน้ำ", "น้ำแข็งลอยปกคลุมผิวน้ำ สิ่งมีชีวิตใต้น้ำจึงอยู่รอดในฤดูหนาว"),
    ("น้ำเป็นตัวกลางของปฏิกิริยาเคมี", "ปฏิกิริยาในเซลล์ส่วนใหญ่เกิดในสารละลายที่มีน้ำ"),
)


# (element, role in the body, deficiency)
ELEMENTS = (
    ("เหล็ก (Fe)", "เป็นองค์ประกอบของฮีโมโกลบินที่ลำเลียงออกซิเจน", "โลหิตจาง"),
    ("ไอโอดีน (I)", "เป็นองค์ประกอบของฮอร์โมนไทรอกซิน", "คอพอก"),
    ("แคลเซียม (Ca)", "เป็นองค์ประกอบของกระดูกและฟัน และช่วยการแข็งตัวของเลือด", "กระดูกเปราะ"),
    ("แมกนีเซียม (Mg)", "เป็นองค์ประกอบของคลอโรฟิลล์ในพืช", "ใบพืชเหลือง"),
    ("ฟอสฟอรัส (P)", "เป็นองค์ประกอบของ ATP กรดนิวคลีอิก และฟอสโฟลิพิด", "กระดูกและฟันไม่แข็งแรง"),
    ("ไนโตรเจน (N)", "เป็นองค์ประกอบของโปรตีนและกรดนิวคลีอิก", "พืชแคระแกร็น ใบเหลือง"),
    ("ฟลูออรีน (F)", "ช่วยให้เคลือบฟันแข็งแรง", "ฟันผุง่าย"),
    ("โพแทสเซียม (K)", "ช่วยการทำงานของเซลล์ประสาทและกล้ามเนื้อ", "กล้ามเนื้ออ่อนแรง"),
)


@question_type(
    "biology.water_element_foundation",
    display_name={"th": "สมบัติของน้ำและความสำคัญต่อสิ่งมีชีวิต"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterElementFoundation(QuestionType):
    """Each property of water explains something living things rely on."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        prop, importance = rng.choice(WATER)
        others = [w for w in WATER if w[0] != prop]
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{prop}\" มีความสำคัญต่อสิ่งมีชีวิตอย่างไร", correct=importance,
                             wrongs=tuple(w[1] for w in rng.sample(others, 3)), topic=TOPIC_WATER,
                             hint="น้ำมีขั้ว เกิดพันธะไฮโดรเจน จุความร้อนสูง และยึดเกาะกันได้ดี")
        return _labelled(stem=f"\"{importance}\" เป็นผลจากสมบัติใดของน้ำ", correct=prop,
                         wrongs=tuple(w[0] for w in rng.sample(others, 3)), topic=TOPIC_WATER,
                         hint="น้ำมีขั้ว เกิดพันธะไฮโดรเจน จุความร้อนสูง และยึดเกาะกันได้ดี")


@question_type(
    "biology.water_element_fluency",
    display_name={"th": "ธาตุที่สำคัญต่อร่างกายสิ่งมีชีวิต"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterElementFluency(QuestionType):
    """What each element builds, and what happens without it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        element, role, lack = rng.choice(ELEMENTS)
        others = [e for e in ELEMENTS if e[0] != element]
        kind = rng.randrange(3)
        if kind == 0:
            return _labelled(stem=f"{element} มีบทบาทใดในร่างกายสิ่งมีชีวิต", correct=role,
                             wrongs=tuple(e[1] for e in rng.sample(others, 3)), topic=TOPIC_WATER,
                             hint="นึกถึงสารสำคัญที่มีธาตุนั้นเป็นองค์ประกอบ")
        if kind == 1:
            return _labelled(stem=f"การขาด{element}ทำให้เกิดอาการใด", correct=lack,
                             wrongs=tuple(e[2] for e in rng.sample(others, 3)), topic=TOPIC_WATER,
                             hint="ขาดธาตุใด สารที่ต้องใช้ธาตุนั้นก็สร้างไม่ได้")
        return _labelled(stem=f"ผู้ที่มีอาการ{lack}อาจขาดธาตุใด", correct=element,
                         wrongs=tuple(e[0] for e in rng.sample(others, 3)), topic=TOPIC_WATER,
                         hint="ขาดธาตุใด สารที่ต้องใช้ธาตุนั้นก็สร้างไม่ได้")


@question_type(
    "biology.water_element_application",
    display_name={"th": "สัดส่วนน้ำและธาตุในร่างกาย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterElementApplication(QuestionType):
    """About 60-70% of the body is water; C, H, O and N make up about 96% of its mass."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            mass = rng.randrange(40, 91)
            percent = rng.choice((60, 65, 70))
            return numeric(stem=f"ถ้าร่างกายมีน้ำร้อยละ {percent} ของมวลร่างกาย คนที่หนัก {mass} kg มีน้ำในร่างกายกี่กิโลกรัม",
                           answer=Fraction(mass * percent, 100),
                           wrongs=[Fraction(mass * (100 - percent), 100), mass, percent], unit="kg", topic=TOPIC_WATER,
                           hint="มวลน้ำ = มวลร่างกาย × ร้อยละ ÷ 100")
        facts = (
            ("ธาตุ 4 ชนิดใดรวมกันเป็นมวลส่วนใหญ่ประมาณร้อยละ 96 ของร่างกาย", "C H O และ N",
             ("Fe Ca Na และ K", "C Ca Fe และ I", "O Na Cl และ S")),
            ("ธาตุใดจัดเป็นธาตุที่ร่างกายต้องการในปริมาณน้อย (ธาตุรอง)", "เหล็กและไอโอดีน",
             ("คาร์บอนและออกซิเจน", "ไฮโดรเจนและไนโตรเจน", "คาร์บอนและไฮโดรเจน")),
            ("เพราะเหตุใดร่างกายจึงต้องได้รับน้ำทุกวัน", "น้ำสูญเสียออกทางเหงื่อ ลมหายใจ และปัสสาวะตลอดเวลา",
             ("ร่างกายสร้างน้ำเองไม่ได้เลย", "น้ำให้พลังงานแก่ร่างกาย", "น้ำเป็นแหล่งโปรตีน")),
        )
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_WATER,
                         hint="ธาตุหลักคือ C H O N ธาตุรองต้องการน้อยแต่ขาดไม่ได้")
