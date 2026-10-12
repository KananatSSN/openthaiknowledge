"""คาร์โบไฮเดรต

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/4

Sets moved here from: science_wave_f44.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f44 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_CARB = "คาร์โบไฮเดรต"


# (carbohydrate, group, made of, where it is found or its role, Benedict positive)
CARBS = (
    ("กลูโคส", "มอนอแซ็กคาไรด์", "—", "น้ำตาลในเลือด แหล่งพลังงานหลักของเซลล์", True),
    ("ฟรักโทส", "มอนอแซ็กคาไรด์", "—", "น้ำตาลในผลไม้และน้ำผึ้ง", True),
    ("กาแล็กโทส", "มอนอแซ็กคาไรด์", "—", "ส่วนประกอบของน้ำตาลในนม", True),
    ("ซูโครส", "ไดแซ็กคาไรด์", "กลูโคส + ฟรักโทส", "น้ำตาลทราย", False),
    ("แล็กโทส", "ไดแซ็กคาไรด์", "กลูโคส + กาแล็กโทส", "น้ำตาลในนม", True),
    ("มอลโทส", "ไดแซ็กคาไรด์", "กลูโคส + กลูโคส", "น้ำตาลจากการย่อยแป้ง", True),
    ("แป้ง", "พอลิแซ็กคาไรด์", "กลูโคสจำนวนมาก", "อาหารสะสมในพืช", False),
    ("ไกลโคเจน", "พอลิแซ็กคาไรด์", "กลูโคสจำนวนมาก", "อาหารสะสมในตับและกล้ามเนื้อของสัตว์", False),
    ("เซลลูโลส", "พอลิแซ็กคาไรด์", "กลูโคสจำนวนมาก", "ผนังเซลล์พืช", False),
    ("ไคทิน", "พอลิแซ็กคาไรด์", "อนุพันธ์ของกลูโคสจำนวนมาก", "เปลือกแข็งของแมลงและผนังเซลล์ของรา", False),
)


GROUPS = ("มอนอแซ็กคาไรด์", "ไดแซ็กคาไรด์", "พอลิแซ็กคาไรด์", "ลิพิด")


@question_type(
    "biology.carbohydrate_foundation",
    display_name={"th": "กลุ่มของคาร์โบไฮเดรต"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CARB,
)
class CarbohydrateFoundation(QuestionType):
    """Single sugars, pairs, and long chains."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, group, _, role, _ = rng.choice(CARBS)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name} จัดเป็นคาร์โบไฮเดรตกลุ่มใด", correct=group,
                             wrongs=tuple(g for g in GROUPS if g != group), topic=TOPIC_CARB,
                             hint="มอนอแซ็กคาไรด์เป็นน้ำตาลโมเลกุลเดี่ยว ไดแซ็กคาไรด์มีสองหน่วย พอลิแซ็กคาไรด์มีหลายหน่วย")
        others = [c for c in CARBS if c[0] != name]
        return _labelled(stem=f"\"{role}\" คือคาร์โบไฮเดรตชนิดใด", correct=name,
                         wrongs=tuple(c[0] for c in rng.sample(others, 3)), topic=TOPIC_CARB,
                         hint="นึกถึงแหล่งที่พบและหน้าที่ของคาร์โบไฮเดรตแต่ละชนิด")


@question_type(
    "biology.carbohydrate_fluency",
    display_name={"th": "หน่วยย่อยของไดแซ็กคาไรด์และพอลิแซ็กคาไรด์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CARB,
)
class CarbohydrateFluency(QuestionType):
    """What each larger sugar breaks down to, and the water that joins them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            name, _, parts, _, _ = rng.choice([c for c in CARBS if c[1] == "ไดแซ็กคาไรด์"])
            options = sorted(({c[2] for c in CARBS if c[1] == "ไดแซ็กคาไรด์"} | {"ฟรักโทส + กาแล็กโทส"}) - {parts})
            return _labelled(stem=f"เมื่อย่อย {name} จะได้มอนอแซ็กคาไรด์ใด", correct=parts, wrongs=tuple(options[:3]),
                             topic=TOPIC_CARB, hint="ซูโครส = กลูโคส + ฟรักโทส แล็กโทส = กลูโคส + กาแล็กโทส มอลโทส = กลูโคส + กลูโคส")
        n = rng.randint(3, 500)
        return numeric(stem=f"กลูโคส {n} โมเลกุลเชื่อมกันเป็นสายตรงด้วยพันธะไกลโคซิดิก จะเกิดพันธะไกลโคซิดิกและปล่อยน้ำออกมากี่โมเลกุล",
                       answer=n - 1, wrongs=[n, n + 1, n * 2], unit="โมเลกุล", topic=TOPIC_CARB,
                       hint="การเชื่อมหน่วยย่อยแต่ละครั้งเสียน้ำ 1 โมเลกุล สาย n หน่วยมีพันธะ n − 1 พันธะ")


@question_type(
    "biology.carbohydrate_application",
    display_name={"th": "ทดสอบคาร์โบไฮเดรตและเปรียบเทียบบทบาท"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CARB,
)
class CarbohydrateApplication(QuestionType):
    """Benedict's solution finds reducing sugars; iodine finds starch."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, group, _, _, reducing = rng.choice(CARBS)
        if rng.random() < 0.35:
            want_reducing = rng.random() < 0.5
            match = [c[0] for c in CARBS if c[4] == want_reducing]
            other = [c[0] for c in CARBS if c[4] != want_reducing]
            ask = "ให้ตะกอนสีแดงอิฐเมื่อต้มกับสารละลายเบเนดิกต์" if want_reducing else "ไม่ให้ตะกอนสีแดงอิฐเมื่อต้มกับสารละลายเบเนดิกต์"
            return _labelled(stem=f"คาร์โบไฮเดรตใด{ask}", correct=rng.choice(match), wrongs=tuple(other),
                             topic=TOPIC_CARB, hint="มอนอแซ็กคาไรด์ แล็กโทส และมอลโทสเป็นน้ำตาลรีดิวซ์ ซูโครสและพอลิแซ็กคาไรด์ไม่ใช่")
        if rng.random() < 0.6:
            if name == "แป้ง":
                right = "สารละลายไอโอดีนเปลี่ยนเป็นสีน้ำเงินเข้ม"
            elif reducing:
                right = "เมื่อต้มกับสารละลายเบเนดิกต์ได้ตะกอนสีแดงอิฐ"
            else:
                right = "ไม่เกิดตะกอนสีแดงอิฐกับสารละลายเบเนดิกต์ และไม่ให้สีน้ำเงินเข้มกับไอโอดีน"
            options = ("เมื่อต้มกับสารละลายเบเนดิกต์ได้ตะกอนสีแดงอิฐ", "สารละลายไอโอดีนเปลี่ยนเป็นสีน้ำเงินเข้ม",
                       "ไม่เกิดตะกอนสีแดงอิฐกับสารละลายเบเนดิกต์ และไม่ให้สีน้ำเงินเข้มกับไอโอดีน",
                       "สารละลายไบยูเร็ตเปลี่ยนเป็นสีม่วง")
            return _labelled(stem=f"ทดสอบ{name}จะได้ผลตามข้อใด", correct=right, wrongs=tuple(o for o in options if o != right),
                             topic=TOPIC_CARB, hint="น้ำตาลรีดิวซ์ (มอนอแซ็กคาไรด์ แล็กโทส มอลโทส) ให้ตะกอนแดงอิฐ ซูโครสไม่ให้ แป้งให้สีน้ำเงินเข้มกับไอโอดีน")
        facts = (
            ("แป้ง ไกลโคเจน และเซลลูโลสต่างก็ประกอบด้วยกลูโคส แต่มีสมบัติต่างกันเพราะเหตุใด", "รูปแบบการเชื่อมต่อและการแตกกิ่งของสายกลูโคสต่างกัน",
             ("มีจำนวนคาร์บอนในกลูโคสต่างกัน", "มีธาตุไนโตรเจนต่างกัน", "เป็นมอนอแซ็กคาไรด์ต่างชนิดกัน")),
            ("คนย่อยเซลลูโลสไม่ได้ แต่วัวย่อยได้เพราะเหตุใด", "ในกระเพาะของวัวมีจุลินทรีย์ที่สร้างเอนไซม์ย่อยเซลลูโลส",
             ("วัวมีฟันที่บดเซลลูโลสให้เป็นกลูโคส", "เซลลูโลสในหญ้าต่างจากในผัก", "วัวมีกรดในกระเพาะมากกว่าคน")),
            ("ร่างกายสะสมคาร์โบไฮเดรตส่วนเกินไว้ในรูปใด", "ไกลโคเจนในตับและกล้ามเนื้อ",
             ("แป้งในลำไส้", "เซลลูโลสในเลือด", "ซูโครสในไต")),
        )
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_CARB,
                         hint="พอลิแซ็กคาไรด์จากกลูโคสต่างกันที่รูปแบบพันธะและการแตกกิ่ง")
