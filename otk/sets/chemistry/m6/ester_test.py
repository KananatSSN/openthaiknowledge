"""การทดสอบปฏิกิริยาเอสเทอริฟิเคชัน ไฮโดรลิซิส และสะปอนนิฟิเคชัน

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/9

Sets moved here from: science_wave_i1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_i1 import CHEMISTRY, UPPER_SIX, _others

PROVENANCE = Provenance("original")


TOPIC_ESTER = "การทดสอบปฏิกิริยาเอสเทอริฟิเคชัน ไฮโดรลิซิส และสะปอนนิฟิเคชัน"


ESTERIFICATION, HYDROLYSIS, SAPONIFICATION = "เอสเทอริฟิเคชัน", "ไฮโดรลิซิสของเอสเทอร์", "สะปอนนิฟิเคชัน"


REACTION_SETUPS = {
    ESTERIFICATION: "ผสมกรดคาร์บอกซิลิกกับแอลกอฮอล์ เติมกรดซัลฟิวริกเข้มข้นเล็กน้อย แล้วอุ่นในอ่างน้ำร้อน",
    HYDROLYSIS: "ต้มเอสเทอร์กับน้ำโดยมีกรดเป็นตัวเร่งปฏิกิริยา",
    SAPONIFICATION: "ต้มน้ำมันพืชกับสารละลายโซเดียมไฮดรอกไซด์",
}


REACTION_PRODUCTS = {
    ESTERIFICATION: "เอสเทอร์และน้ำ",
    HYDROLYSIS: "กรดคาร์บอกซิลิกและแอลกอฮอล์",
    SAPONIFICATION: "สบู่ (เกลือของกรดไขมัน) และกลีเซอรอล",
}


REACTION_SIGNS = {
    ESTERIFICATION: "เมื่อเทลงในน้ำเย็น ได้ของเหลวกลิ่นหอมที่ไม่ละลายน้ำ ลอยเป็นชั้นอยู่บนผิวน้ำ",
    HYDROLYSIS: "กลิ่นหอมของเอสเทอร์จางหายไป",
    SAPONIFICATION: "ได้ของผสมข้น เมื่อเขย่ากับน้ำเกิดฟอง",
}


NOT_THESE = ("การเติมไฮโดรเจน", "การสะเทิน", "การเผาไหม้")


FALSE_SIGNS = ("สีม่วงของสารละลายจางหายไปทันที", "เกิดตะกอนสีเหลืองของกำมะถัน", "เกิดแก๊สที่ทำให้น้ำปูนใสขุ่น")


# (role question, right, wrongs)
ESTER_ROLES = (
    ("ในการเตรียมเอสเทอร์ เติมกรดซัลฟิวริกเข้มข้นเพื่ออะไร",
     "เป็นตัวเร่งปฏิกิริยา และช่วยดึงน้ำที่เกิดขึ้นออก",
     ("เป็นสารตั้งต้นที่กลายเป็นเอสเทอร์", "ทำให้เอสเทอร์มีสี", "ทำให้แอลกอฮอล์ระเหยหมด")),
    ("ในการเตรียมเอสเทอร์ ใช้การอุ่นในอ่างน้ำร้อนแทนการตั้งบนเปลวไฟโดยตรงเพราะเหตุใด",
     "แอลกอฮอล์และเอสเทอร์ติดไฟง่าย", ("ปฏิกิริยานี้ดูดความร้อนจากน้ำ", "เปลวไฟทำให้กรดเป็นกลาง",
                                       "น้ำร้อนเป็นสารตั้งต้นของปฏิกิริยา")),
    ("ในการทำสบู่ เติมเกลือแกง (NaCl) ลงในของผสมหลังต้มเพื่ออะไร",
     "ทำให้สบู่แยกตัวออกมาเป็นของแข็ง", ("เพิ่มฟองให้สบู่", "ทำให้น้ำมันเหลือมากขึ้น",
                                          "เป็นตัวเร่งปฏิกิริยาสะปอนนิฟิเคชัน")),
)


# (acid, alcohol, ester, smell) — the textbook's classroom esters
ESTER_SMELLS = (
    ("กรดเอทาโนอิก", "เพนทานอล", "เพนทิลเอทาโนเอต", "กล้วยหอม"),
    ("กรดเอทาโนอิก", "ออกทานอล", "ออกทิลเอทาโนเอต", "ส้ม"),
    ("กรดบิวทาโนอิก", "เอทานอล", "เอทิลบิวทาโนเอต", "สับปะรด"),
    ("กรดซาลิไซลิก", "เมทานอล", "เมทิลซาลิไซเลต", "น้ำมันระกำ"),
)


@question_type(
    "chem.ester_test_foundation",
    display_name={"th": "ระบุปฏิกิริยาจากวิธีทดลองและผลิตภัณฑ์"},
    level=UPPER_SIX, subject=CHEMISTRY, topic=TOPIC_ESTER,
)
class EsterTestFoundation(QuestionType):
    """From the method to the reaction, and from the reaction to its products."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reaction = rng.choice(sorted(REACTION_SETUPS))
        hint = "เอสเทอริฟิเคชัน: กรด + แอลกอฮอล์ → เอสเทอร์ + น้ำ; ไฮโดรลิซิสย้อนกลับ; สะปอนนิฟิเคชัน: ไขมัน + เบส → สบู่ + กลีเซอรอล"
        if rng.random() < 0.5:
            return _labelled(stem=f"การทดลอง: {REACTION_SETUPS[reaction]} เป็นการทดสอบปฏิกิริยาใด",
                             correct=reaction, wrongs=tuple(r for r in REACTION_SETUPS if r != reaction) + NOT_THESE,
                             topic=TOPIC_ESTER, hint=hint)
        return _labelled(stem=f"ปฏิกิริยา{reaction}ให้ผลิตภัณฑ์ใด", correct=REACTION_PRODUCTS[reaction],
                         wrongs=_others(REACTION_PRODUCTS, reaction) + ("แก๊สคาร์บอนไดออกไซด์และน้ำ",),
                         topic=TOPIC_ESTER, hint=hint)


@question_type(
    "chem.ester_test_fluency",
    display_name={"th": "ผลการสังเกตและหน้าที่ของสารในการทดสอบ"},
    level=UPPER_SIX, subject=CHEMISTRY, topic=TOPIC_ESTER,
)
class EsterTestFluency(QuestionType):
    """What each test shows, and what each added substance is for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            reaction = rng.choice(sorted(REACTION_SIGNS))
            return _labelled(stem=f"ผลการสังเกตใดแสดงว่าเกิดปฏิกิริยา{reaction}",
                             correct=REACTION_SIGNS[reaction],
                             wrongs=_others(REACTION_SIGNS, reaction) + FALSE_SIGNS, topic=TOPIC_ESTER,
                             hint="เอสเทอร์มีกลิ่นหอมและไม่ละลายน้ำ สบู่ทำให้เกิดฟอง เมื่อเอสเทอร์ถูกไฮโดรไลส์ กลิ่นหอมจะหายไป")
        stem, right, wrongs = rng.choice(ESTER_ROLES)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_ESTER,
                         hint="ตัวเร่งปฏิกิริยาไม่ได้กลายเป็นผลิตภัณฑ์ สารไวไฟต้องไม่ถูกเปลวไฟโดยตรง")


@question_type(
    "chem.ester_test_application",
    display_name={"th": "กลิ่นของเอสเทอร์และการระบุสารจากผลการทดลอง"},
    level=UPPER_SIX, subject=CHEMISTRY, topic=TOPIC_ESTER,
)
class EsterTestApplication(QuestionType):
    """Which acid and alcohol give a smell; which tube held which reaction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        acid, alcohol, ester, smell = rng.choice(ESTER_SMELLS)
        others = [e for e in ESTER_SMELLS if e[2] != ester]
        hint = "ชื่อเอสเทอร์ขึ้นต้นด้วยส่วนของแอลกอฮอล์ (-อิล) แล้วตามด้วยส่วนของกรด (-โอเอต)"
        if kind == 0:
            return _labelled(stem=f"ต้องการเตรียมเอสเทอร์ที่มีกลิ่น{smell} ต้องใช้สารคู่ใดทำปฏิกิริยากัน",
                             correct=f"{acid} กับ{alcohol}",
                             wrongs=tuple(f"{e[0]} กับ{e[1]}" for e in others)
                             + (f"{acid} กับน้ำ",), topic=TOPIC_ESTER, hint=hint)
        if kind == 1:
            return _labelled(stem=f"อุ่น{acid}กับ{alcohol}โดยมีกรดซัลฟิวริกเข้มข้นเป็นตัวเร่ง จะได้เอสเทอร์ชื่อใด "
                                  "และมีกลิ่นคล้ายอะไร",
                             correct=f"{ester} กลิ่นคล้าย{smell}",
                             wrongs=tuple(f"{e[2]} กลิ่นคล้าย{e[3]}" for e in others)
                             + (f"{ester} ไม่มีกลิ่น",), topic=TOPIC_ESTER, hint=hint)
        reactions = list(REACTION_SIGNS)
        rng.shuffle(reactions)
        tubes = dict(zip("ABC", reactions))
        tube = rng.choice("ABC")
        listing = " ".join(f"หลอด {name}: {REACTION_SIGNS[r]}" for name, r in tubes.items())
        return _labelled(stem=f"ผลการทดลองสามหลอด {listing} หลอด {tube} เกิดปฏิกิริยาใด",
                         correct=tubes[tube], wrongs=tuple(r for r in reactions if r != tubes[tube]) + NOT_THESE,
                         topic=TOPIC_ESTER,
                         hint="กลิ่นหอมและชั้นบนผิวน้ำคือเอสเทอร์เกิดขึ้น กลิ่นหายคือเอสเทอร์ถูกไฮโดรไลส์ ฟองคือสบู่")
